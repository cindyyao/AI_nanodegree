import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        lowest_bic = float("inf")
        best_model = None
        N, num_features = self.X.shape
        for num_hidden_states in range(self.min_n_components, self.max_n_components + 1):
            # model = GaussianHMM(n_components=num_hidden_states, n_iter=1000).fit(self.X, self.lengths)
            # num_params = num_hidden_states * (num_hidden_states - 1) + 2 * num_hidden_states * num_features
            try:
                model = GaussianHMM(n_components=num_hidden_states, n_iter=1000).fit(self.X, self.lengths)
                num_params = num_hidden_states ** 2 + 2 * num_hidden_states * num_features - 1
                bic = -2 * model.score(self.X, self.lengths) + num_params * math.log(N)
                if bic < lowest_bic:
                    best_model = model
                    lowest_bic = bic
            except ValueError:
                continue
        return best_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        highest_dic = float("-inf")
        best_model = None
        M = len(self.words)
        for num_hidden_states in range(self.min_n_components, self.max_n_components + 1):
            # model = GaussianHMM(n_components=num_hidden_states, n_iter=1000).fit(self.X, self.lengths)
            try:
                model = GaussianHMM(n_components=num_hidden_states, n_iter=1000).fit(self.X, self.lengths)
                dic = model.score(self.X, self.lengths) - self.get_sum_against(model)
                if dic > highest_dic:
                    best_model = model
                    highest_dic = dic
            except ValueError:
                continue
        return best_model

    def get_sum_against(self, model):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        num_features = len(self.sequences[0][0])
        sum = 0
        M = 0
        for key in self.words:
            if key != self.this_word:
                try:
                    sum += model.score(self.hwords[key])
                    M += 1
                except ValueError:
                    continue
        return sum / (M - 1)





class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection using CV
        split_method = KFold()
        sequences = self.sequences
        best_log = float("-inf")
        best_model = None
        for num_hidden_states in range(self.min_n_components, self.max_n_components + 1):
            try:
                logL = []
                for train_idx, test_idx in split_method.split(sequences):
                    train_X, train_lengths = combine_sequences(train_idx, sequences)
                    test_X, test_lengths = combine_sequences(test_idx, sequences)
                    model = GaussianHMM(n_components=num_hidden_states, n_iter=1000).fit(train_X, train_lengths)
                    logL.append(model.score(test_X, test_lengths))
                if np.mean(logL) > best_log:
                    best_model = model
                    best_log = np.mean(logL)
            except ValueError:
                # model = GaussianHMM(n_components=num_hidden_states, n_iter=1000).fit(self.X, self.lengths)
                try:
                    model = GaussianHMM(n_components=num_hidden_states, n_iter=1000).fit(self.X, self.lengths)
                    if model.score(self.X, self.lengths) > best_log:
                        best_model = model
                        best_log = model.score(self.X, self.lengths)
                except ValueError:
                    continue
        return best_model