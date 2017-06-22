import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    for test_key, test_value in test_set.get_all_Xlengths().items():
        prob_dict = dict()
        guess_word = None
        max_logL = float("-inf")
        for model_key, model_value in models.items():
            try:
                logL = model_value.score(test_value[0], test_value[1])
            except (ValueError, AttributeError):
                logL = float("-inf")
            prob_dict[model_key] = logL
            if logL > max_logL:
                guess_word = model_key
                max_logL = logL
        probabilities.append(prob_dict)
        guesses.append(guess_word)
    return probabilities, guesses

    # return probabilities, guesses
    raise NotImplementedError
