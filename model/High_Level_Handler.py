class HighLevelHandler():
    def __init__(self, margin=0.05, include_status=False, model=XGBClassifier(), lower_params=None, class_ratio=0.20, hidden_layer_sizes=(100,), 
    activation='relu', *, solver='adam',alpha=0.0001, batch_size='auto', learning_rate='constant', learning_rate_init=0.001, power_t=0.5, max_iter=200, 
    shuffle=True, random_state=None, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, 
    beta_1=0.9, beta_2=0.999, epsilon=1e-08, n_iter_no_change=10, max_fun=15000):
        
        self.low_level_handler = LowLevelHandler(model=model, lower_params=lower_params, class_ratio=class_ratio, random_state=random_state)
        self.margin = margin
        self.include_status = include_status
        self.high_level_model = MLPClassifier(
            hidden_layer_sizes=hidden_layer_sizes, 
            activation=activation, 
            solver=solver, 
            alpha=alpha, 
            batch_size=batch_size, 
            learning_rate=learning_rate, 
            learning_rate_init=learning_rate_init, 
            power_t=power_t, 
            max_iter=max_iter, 
            shuffle=shuffle, 
            random_state=random_state, 
            tol=tol, 
            verbose=verbose, 
            warm_start=warm_start, 
            momentum=momentum, 
            nesterovs_momentum=nesterovs_momentum, 
            early_stopping=early_stopping, 
            validation_fraction=validation_fraction, 
            beta_1=beta_1, 
            beta_2=beta_2, 
            epsilon=epsilon, 
            n_iter_no_change=n_iter_no_change, 
            max_fun=max_fun
        )

    def fit(self, X, y):
        self.low_level_handler.create_predictors(y)
        self.low_level_handler.fit(X, y)
        
        low_level_predictions = []
        for i in self.low_level_handler.classes:
            low_level_predictions.append(self.low_level_handler.get_predictor_results(i, X))
        
        low_level_predictions = np.column_stack(low_level_predictions)
        self.high_level_model.fit(low_level_predictions, y)

    def predict(self, X):
        low_level_predictions = []
        for i in self.low_level_handler.classes:
            low_level_predictions.append(self.low_level_handler.get_predictor_results(i, X))
        
        low_level_predictions = np.column_stack(low_level_predictions)
        
        high_level_predictions = self.high_level_model.predict_proba(low_level_predictions)
        
        final_predictions = []
        
        for idx, prob_distribution in enumerate(high_level_predictions):
            sorted_classes = sorted(
                enumerate(prob_distribution), key=lambda x: x[1], reverse=True
            )
            
            primary_class, primary_confidence = sorted_classes[0]
            
            primary_result = self.low_level_handler.get_predictor_results(self.high_level_model.classes_[primary_class], X[idx])

            if primary_result:
                final_predictions.append((primary_class, False) if self.include_status else primary_class)
                continue

            is_dirty = True
            for alt_class, alt_confidence in sorted_classes[1:]:
                alt_result = self.low_level_handler.get_predictor_results(alt_class, X[idx])
                
                if alt_result and abs(primary_confidence - alt_confidence) <= self.margin:
                    final_predictions.append((alt_class, False) if self.include_status else alt_class)
                    is_dirty = False
                    break

            if is_dirty:
                final_predictions.append(
                    (primary_class, True) if self.include_status else primary_class
                )
        
        return final_predictions

    def predict_proba(self, X):
        low_level_predictions = []
        for i in self.low_level_handler.classes:
            low_level_predictions.append(self.low_level_handler.get_predictor_proba(i, X))

        reshaped_predictions = np.column_stack([pred[:, 1] for pred in low_level_predictions])

        high_level_predictions = self.high_level_model.predict_proba(reshaped_predictions)

        return high_level_predictions

    def fit_predictor(self, X, y):
        self.low_level_handler.fit_predictor(X, y)