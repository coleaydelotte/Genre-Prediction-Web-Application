class LowLevelHandler():
    def __init__(self, model, *, lower_params, class_ratio=0.20, random_state=None):
        self.model = model
        self.lower_params = lower_params
        self.class_ratio = class_ratio
        self.random_state = None
        self.classes = []
        self.predictors = {}

    def create_predictors(self, y):
        self.get_classes(y)
        if self.lower_params:
            for i in self.classes:
                self.predictors[i] = ClassPredictor(self.model, param_grid=self.lower_params)
        else:
            for i in self.classes:
                self.predictors[i] = ClassPredictor(self.model)
        return self.predictors

    def get_predictors(self):
        return self.predictors

    def get_classes(self, y):
        self.classes = pd.Series(y).value_counts().index.tolist()
    
    def split_data(self, X, y, class_ratio, random_state=None):
        data = {}
        rng = np.random.default_rng(random_state)

        for i in self.classes:
            class_samples = X[y == i]
            non_class_samples = X[y != i]
            num_non_class_samples = int(len(class_samples) * (1 - class_ratio) / class_ratio)
            if len(non_class_samples) > num_non_class_samples:
                non_class_samples = non_class_samples[rng.choice(
                    len(non_class_samples), size=num_non_class_samples, replace=False
                )]
            data[i] = class_samples
            data["not_" + str(i)] = non_class_samples
        
        return data


    def fit(self, X, y):
        data = self.split_data(X, y, self.class_ratio)
        
        for i in self.classes:
            class_samples = data[i]
            non_class_samples = data["not_" + str(i)]
            
            combined_X = np.vstack((class_samples, non_class_samples))
            combined_y = np.hstack((np.ones(len(class_samples)), np.zeros(len(non_class_samples))))
            
            self.predictors[i].fit(combined_X, combined_y)

    def fit_predictor(self, X, y):
        for i in self.classes:
            self.predictors[i].fit(X, y==i)

    def get_predictor_results(self, class_name, X):
        return self.predictors[class_name].predict(X)

    def get_predictor_proba(self, class_name, X):
        return self.predictors[class_name].predict_proba(X)