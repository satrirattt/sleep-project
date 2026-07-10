"""
Step 5: Pipeline & Training
- สร้าง sklearn Pipeline (ColumnTransformer + RandomForestClassifier)
  เพื่อทำนาย sleep_quality (good/bad) จากข้อมูลรวม
Output: sleep_quality_model.pkl, target_label_encoder.pkl, feature_columns.pkl
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

df = pd.read_csv("merged_cleaned_data.csv")

TARGET = "sleep_quality"

feature_cols_num = ["age", "sleep_hours", "screen_time", "stress_level"]
feature_cols_cat = ["morning_freshness", "use_phone_before_sleep",
                     "phone_anxiety", "health_app_use", "phone_affects_sleep"]

X = df[feature_cols_num + feature_cols_cat]
y = df[TARGET]

le_target = LabelEncoder()
y_enc = le_target.fit_transform(y)
print("Target classes:", dict(zip(le_target.classes_, le_target.transform(le_target.classes_))))

X_train, X_test, y_train, y_test = train_test_split(
    X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
)

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), feature_cols_num),
    ("cat", OneHotEncoder(handle_unknown="ignore"), feature_cols_cat),
])

model = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=300, max_depth=8, random_state=42))
])

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nTest Accuracy: {acc:.3f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=le_target.classes_))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

importances = model.named_steps["classifier"].feature_importances_
feature_names = model.named_steps["preprocess"].get_feature_names_out()
fi = pd.Series(importances, index=feature_names).sort_values(ascending=False)
print("\nTop 10 Feature Importances:")
print(fi.head(10))

joblib.dump(model, "sleep_quality_model.pkl")
joblib.dump(le_target, "target_label_encoder.pkl")
joblib.dump({"num": feature_cols_num, "cat": feature_cols_cat}, "feature_columns.pkl")

print("\nSaved: sleep_quality_model.pkl, target_label_encoder.pkl, feature_columns.pkl")
