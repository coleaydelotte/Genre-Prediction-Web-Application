class ClassPredictor():
    def __init__(self, model=XGBClassifier(), *, param_grid=None):
        self.model = model
        self.param_grid = param_grid
    
    def fit(self, X, y):
        if self.param_grid:
            grid_model = GridSearchCV(self.model, self.param_grid, n_jobs=-1)
            try:
                grid_model.fit(X, y)
                self.model = grid_model.best_estimator_
                return True
            except Exception as e:
                print(e, "Error in fitting the model, passed param_grid could be the issue, make sure it is in the correct format.")
                return False
        try:
            self.model.fit(X, y)
            return True
        except Exception as e:
            print(e, "Error in fitting the model")
            return False

    def predict(self, X):
        try:
            if X.ndim == 1:
                X = X.reshape(1, -1)
            return self.model.predict(X)
        except Exception as e:
            print(e, "Error in predicting the model")
        
    def predict_proba(self, X):
        try:
            if X.ndim == 1:
                X = X.reshape(1, -1)
            return self.model.predict_proba(X)
        except Exception as e:
            print(e, "Error in predicting the model")