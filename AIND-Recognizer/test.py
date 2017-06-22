import numpy as np
import pandas as pd
from asl_data import AslDb
from sklearn.model_selection import KFold
asl = AslDb() # initializes the database
asl.df['grnd-ry'] = asl.df['right-y'] - asl.df['nose-y']
asl.df['grnd-rx'] = asl.df['right-x'] - asl.df['nose-x']
asl.df['grnd-ly'] = asl.df['left-y'] - asl.df['nose-y']
asl.df['grnd-lx'] = asl.df['left-x'] - asl.df['nose-x']
features_ground = ['grnd-rx','grnd-ry','grnd-lx','grnd-ly']
training = asl.build_training(features_ground)
df_means = asl.df.groupby('speaker').mean()
asl.df['left-x-mean']= asl.df['speaker'].map(df_means['left-x'])
df_std = asl.df.groupby('speaker').std()
asl.df['left-y-mean']= asl.df['speaker'].map(df_means['left-y'])
asl.df['right-x-mean']= asl.df['speaker'].map(df_means['right-x'])
asl.df['right-y-mean']= asl.df['speaker'].map(df_means['right-y'])

asl.df['left-x-std']= asl.df['speaker'].map(df_std['left-x'])
asl.df['left-y-std']= asl.df['speaker'].map(df_std['left-y'])
asl.df['right-x-std']= asl.df['speaker'].map(df_std['right-x'])
asl.df['right-y-std']= asl.df['speaker'].map(df_std['right-y'])

asl.df['norm-rx'] = (asl.df['right-x'] - asl.df['right-x-mean']) / asl.df['right-x-std']
asl.df['norm-ry'] = (asl.df['right-y'] - asl.df['right-y-mean']) / asl.df['right-y-std']
asl.df['norm-lx'] = (asl.df['left-x'] - asl.df['left-x-mean']) / asl.df['left-x-std']
asl.df['norm-ly'] = (asl.df['left-y'] - asl.df['left-y-mean']) / asl.df['left-y-std']

features_norm = ['norm-rx', 'norm-ry', 'norm-lx','norm-ly']
asl.df['polar-rr'] = (asl.df['grnd-rx']**2 + asl.df['grnd-ry']**2)**0.5
asl.df['polar-lr'] = (asl.df['grnd-lx']**2 + asl.df['grnd-ly']**2)**0.5
asl.df['polar-rtheta'] = np.arctan2(asl.df['grnd-rx'], asl.df['grnd-ry'])
asl.df['polar-ltheta'] = np.arctan2(asl.df['grnd-lx'], asl.df['grnd-ly'])

features_polar = ['polar-rr', 'polar-rtheta', 'polar-lr', 'polar-ltheta']

asl.df['delta-rx'] = asl.df['right-x'].diff()
asl.df['delta-ry'] = asl.df['right-y'].diff()
asl.df['delta-lx'] = asl.df['left-x'].diff()
asl.df['delta-ly'] = asl.df['left-y'].diff()
asl.df.head()
features_delta = ['delta-rx', 'delta-ry', 'delta-lx', 'delta-ly']
asl.df = asl.df.fillna(0)

df_means = asl.df.groupby('speaker').mean()
df_std = asl.df.groupby('speaker').std()
asl.df['polar-rr-mean']= asl.df['speaker'].map(df_means['polar-rr'])
asl.df['polar-rr-std']= asl.df['speaker'].map(df_std['polar-rr'])
asl.df['polar-lr-mean']= asl.df['speaker'].map(df_means['polar-lr'])
asl.df['polar-lr-std']= asl.df['speaker'].map(df_std['polar-lr'])

asl.df['polar-nrr'] = (asl.df['polar-rr'] - asl.df['polar-rr-mean']) / asl.df['polar-rr-std']
asl.df['polar-nlr'] = (asl.df['polar-lr'] - asl.df['polar-lr-mean']) / asl.df['polar-lr-std']
# TODO define a list named 'features_custom' for building the training set
features_npolar = ['polar-nrr', 'polar-rtheta', 'polar-nlr', 'polar-ltheta']
words_to_train = ['FISH', 'BOOK', 'VEGETABLE', 'FUTURE', 'JOHN']
import timeit

# TODO: Implement SelectorDIC in module my_model_selectors.py
# from my_model_selectors import SelectorDIC
#
# training = asl.build_training(features_norm)  # Experiment here with different feature sets defined in part 1
# sequences = training.get_all_sequences()
# Xlengths = training.get_all_Xlengths()
# for word in words_to_train:
#     start = timeit.default_timer()
#     model = SelectorDIC(sequences, Xlengths, word,
#                     min_n_components=2, max_n_components=15, random_state = 14).select()
#     end = timeit.default_timer()-start
#     if model is not None:
#         print("Training complete for {} with {} states with time {} seconds".format(word, model.n_components, end))
#     else:
#         print("Training failed for {}".format(word))

test_set = asl.build_test(features_ground)
from my_recognizer import recognize
from asl_utils import show_errors
from my_model_selectors import SelectorConstant
from my_model_selectors import SelectorCV
from my_model_selectors import SelectorBIC
from my_model_selectors import SelectorDIC
def train_all_words(features, model_selector):
    training = asl.build_training(features)  # Experiment here with different feature sets defined in part 1
    sequences = training.get_all_sequences()
    Xlengths = training.get_all_Xlengths()
    model_dict = {}
    for word in training.words:
        model = model_selector(sequences, Xlengths, word,
                        n_constant=3).select()
        model_dict[word]=model
    return model_dict

features = features_polar # change as needed
model_selector = SelectorCV # change as needed

# TODO Recognize the test set and display the result with the show_errors method
models = train_all_words(features, model_selector)
test_set = asl.build_test(features)
probabilities, guesses = recognize(models, test_set)
show_errors(guesses, test_set)