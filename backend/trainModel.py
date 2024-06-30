import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import classification_report
from joblib import dump
import os

# Load data
data = pd.read_csv('malwarebenignfeatures.csv')
feature_df = pd.read_csv('dataset-features-categories.csv')
data["class"] = data["class"].map({"B": 0, "S": 1})

# Replace '?' with NaN and impute missing values
data.replace('?', pd.NA, inplace=True)
data.fillna(data.median(), inplace=True)

# Check the number of rows and columns after preprocessing
print(f"Number of rows after preprocessing: {data.shape[0]}")
print(f"Number of columns after preprocessing: {data.shape[1]}")

X = data.drop("class", axis=1)
y = data["class"]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify=y)

# Hyperparameter tuning for RandomForestClassifier
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

cv = StratifiedKFold(n_splits=5)
grid_search_rf = GridSearchCV(estimator=RandomForestClassifier(random_state=42), param_grid=param_grid, cv=cv, n_jobs=-1, verbose=2)
grid_search_rf.fit(X_train, y_train)
best_rf = grid_search_rf.best_estimator_

# Train a GradientBoostingClassifier
gbc = GradientBoostingClassifier(random_state=42)
gbc.fit(X_train, y_train)

# Ensemble model with VotingClassifier
voting_clf = VotingClassifier(estimators=[('rf', best_rf), ('gbc', gbc)], voting='soft')
voting_clf.fit(X_train, y_train)

# Evaluate the model
y_pred = voting_clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the trained model
dump(voting_clf, 'malware_detector.joblib')