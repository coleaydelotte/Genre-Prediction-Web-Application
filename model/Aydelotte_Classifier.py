from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
import numpy as np
from model.High_Level_Handler import HighLevelHandler

class AydelotteClassifier():
    def __init__(self, margin=0.05, include_status=False, model=XGBClassifier(), lower_params=None, class_ratio=0.20, hidden_layer_sizes=(100,), activation='relu', *, 
                 solver='adam', alpha=0.0001, batch_size='auto', learning_rate='constant', learning_rate_init=0.001, power_t=0.5, max_iter=200, shuffle=True, 
                 random_state=None, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, 
                 beta_1=0.9, beta_2=0.999, epsilon=1e-08, n_iter_no_change=10, max_fun=15000):
        
        self.margin = margin
        self.include_status = include_status
        self.model = model
        self.lower_params = lower_params
        self.class_ratio = class_ratio
        self.hidden_layer_sizes = hidden_layer_sizes
        self.activation = activation
        self.solver = solver
        self.alpha = alpha
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.learning_rate_init = learning_rate_init
        self.power_t = power_t
        self.max_iter = max_iter
        self.shuffle = shuffle
        self.random_state = random_state
        self.tol = tol
        self.verbose = verbose
        self.warm_start = warm_start
        self.momentum = momentum
        self.nesterovs_momentum = nesterovs_momentum
        self.early_stopping = early_stopping
        self.validation_fraction = validation_fraction
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon
        self.n_iter_no_change = n_iter_no_change
        self.max_fun = max_fun
        
        self.high_level_handler = HighLevelHandler(
            margin=self.margin, 
            include_status=self.include_status, 
            model=self.model,
            lower_params=self.lower_params,
            hidden_layer_sizes=self.hidden_layer_sizes,
            activation=self.activation,
            solver=self.solver,
            alpha=self.alpha,
            batch_size=self.batch_size,
            learning_rate=self.learning_rate,
            learning_rate_init=self.learning_rate_init,
            power_t=self.power_t,
            max_iter=self.max_iter,
            shuffle=self.shuffle,
            random_state=self.random_state,
            tol=self.tol,
            verbose=self.verbose,
            warm_start=self.warm_start,
            momentum=self.momentum,
            nesterovs_momentum=self.nesterovs_momentum,
            early_stopping=self.early_stopping,
            validation_fraction=self.validation_fraction,
            beta_1=self.beta_1,
            beta_2=self.beta_2,
            epsilon=self.epsilon,
            n_iter_no_change=self.n_iter_no_change,
            max_fun=self.max_fun
        )

    def fit(self, X, y):
        self.high_level_handler.fit(X, y)
        self.high_level_handler.low_level_handler.fit(X, y)

    def predict(self, X):
        return self.high_level_handler.predict(X)

    def predict_proba(self, X):
        low_level_predictions = []
        for i in self.high_level_handler.low_level_handler.classes:
            low_level_predictions.append(self.high_level_handler.low_level_handler.get_predictor_results(i, X))
        
        low_level_predictions = np.column_stack(low_level_predictions)
        
        high_level_predictions = self.high_level_handler.high_level_model.predict_proba(low_level_predictions)
        
        return high_level_predictions

    def score(self, X, y):
        y_pred = self.predict(X)
        return np.mean(y_pred == y)
    
    def get_params(self, deep=True):
        return {
            'margin': self.margin,
            'include_status': self.include_status,
            'model': self.model,
            'lower_params': self.lower_params,
            'class_ratio': self.class_ratio,
            'hidden_layer_sizes': self.hidden_layer_sizes,
            'activation': self.activation,
            'solver': self.solver,
            'alpha': self.alpha,
            'batch_size': self.batch_size,
            'learning_rate': self.learning_rate,
            'learning_rate_init': self.learning_rate_init,
            'power_t': self.power_t,
            'max_iter': self.max_iter,
            'shuffle': self.shuffle,
            'random_state': self.random_state,
            'tol': self.tol,
            'verbose': self.verbose,
            'warm_start': self.warm_start,
            'momentum': self.momentum,
            'nesterovs_momentum': self.nesterovs_momentum,
            'early_stopping': self.early_stopping,
            'validation_fraction': self.validation_fraction,
            'beta_1': self.beta_1,
            'beta_2': self.beta_2,
            'epsilon': self.epsilon,
            'n_iter_no_change': self.n_iter_no_change,
            'max_fun': self.max_fun
        }

    def set_params(self, **params):
        for key, value in params.items():
            setattr(self, key, value)
        return self