# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 13:00:27 2025

@author: shris
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Step 2: Load Dataset
# Using seaborn's built-in Titanic dataset (cleaned version)
df = sns.load_dataset('titanic')
print("Dataset loaded. Shape:", df.shape)
print(df.head())

# Step 3: Data Cleaning & Feature Selection
# Select relevant features
features = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked']
target = 'survived'

X = df[features]
y = df[target]

# Handle missing values and categorical encoding
num_features = ['age', 'fare']
cat_features = ['pclass', 'sex', 'sibsp', 'parch', 'embarked']

# Preprocessing pipeline
num_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median'))
])

cat_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop='first', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_transformer, num_features),
        ('cat', cat_transformer, cat_features)
    ])

# Step 4: Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Step 5: Build Model Pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(max_iter=1000, random_state=42))
])

# Train the model
model.fit(X_train, y_train)
print("\nModel training completed.")

# Step 6: Predictions & Evaluation
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")

# Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Died', 'Survived']))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Died', 'Survived'], 
            yticklabels=['Died', 'Survived'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Step 7: Feature Importance (Coefficients)
# Get feature names after one-hot encoding
feature_names = (num_features + 
                 list(model.named_steps['preprocessor']
                      .named_transformers_['cat']['onehot']
                      .get_feature_names_out(cat_features)))

coef = model.named_steps['classifier'].coef_[0]
importance = pd.DataFrame({'Feature': feature_names, 'Coefficient': coef})
importance['Abs_Coefficient'] = np.abs(importance['Coefficient'])
importance = importance.sort_values('Abs_Coefficient', ascending=False)

print("\nTop 5 Most Important Features:")
print(importance.head(5)[['Feature', 'Coefficient']])

# Step 8: Interpretation & Insights
print("\n" + "="*60)
print("INTERPRETATION & INSIGHTS")
print("="*60)
print(f"• Model Accuracy: {accuracy:.1%} — predicts survival correctly in {int(accuracy*len(X_test))} out of {len(X_test)} test cases.")
