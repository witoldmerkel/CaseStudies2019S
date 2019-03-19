#:# libraries
from sklearn.preprocessing import Imputer, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from matplotlib import pyplot as plt
from platform import python_version

import openml
import pandas as pd
import numpy as np
import hashlib
import pkg_resources
import datetime
import json

#:# config

np.random.seed(42)

#:# data

datasetId = 1070

dataset = openml.datasets.get_dataset(datasetId)
(X, y, categorical, names) = dataset.get_data(
    target=dataset.default_target_attribute,
    return_categorical_indicator=True,
    return_attribute_names=True,
    include_ignore_attributes=True
)

vals = {}
for i, name in enumerate(names):
    vals[name] = X[:, i]
vals[dataset.default_target_attribute] = y
df = pd.DataFrame(vals)

X = df.drop('NUMDEFECTS', axis=1)
y = df.loc[:, 'NUMDEFECTS']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

#:# preprocessing

transform_pipeline = Pipeline([
    ('scaler', StandardScaler())
])

X_train = pd.DataFrame(transform_pipeline.fit_transform(X_train), columns=X_train.columns)

#:# model


regressor = MLPRegressor(hidden_layer_sizes=[100, 75, 50, 20], random_state=42, max_iter=300, alpha=0.0015)
regressor.fit(X_train, y_train)

#:# hash
#:# c2624181e167ddd143c1200a733786f3
md5 = hashlib.md5(str(regressor).encode('utf-8')).hexdigest()
print(f'md5: {md5}')

#:# audit
y_pred = regressor.predict(transform_pipeline.transform(X_test))

print(f'MSE: {mean_squared_error(y_test, y_pred)}')
print(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred))}')
print(f'MAE: {mean_absolute_error(y_test, y_pred)}')
print(f'R2: {r2_score(y_test, y_pred)}')

#:# session info

# Dodaj wersję pythona w session info

sessionInfo = {
    "python_version": python_version(),
    "library_versions":[str(d) for d in pkg_resources.working_set]
}
with open('sessionInfo.txt', 'w') as f:
    json.dump(sessionInfo, f, indent=4)
