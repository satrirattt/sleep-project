"""
Step 4: Transform
- Feature engineering, encode categorical, scale numeric บนข้อมูลรวม (merged)
Output: transformed_merged_data.csv
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

df = pd.read_csv("merged_cleaned_data.csv")

# ==========================================
# 1) FEATURE ENGINEERING
# ==========================================
df["screen_sleep_ratio"] = df["screen_time"] / df["sleep_hours"].replace(0, np.nan)

df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 18, 25, 35, 50, 100],
    labels=["<=18", "19-25", "26-35", "36-50", "50+"]
)

df["sleep_category"] = pd.cut(
    df["sleep_hours"],
    bins=[0, 5, 7, 9, 24],
    labels=["very_low", "low", "adequate", "high"]
)

# ==========================================
# 2) ENCODE CATEGORICAL COLUMNS
# ==========================================
categorical_cols = df.select_dtypes(include="object").columns.tolist()

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    df[col + "_encoded"] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le
    print(f"{col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")

# ==========================================
# 3) SCALE NUMERIC COLUMNS
# ==========================================
numeric_cols = ["age", "sleep_hours", "screen_time", "stress_level", "screen_sleep_ratio"]
numeric_cols = [c for c in numeric_cols if c in df.columns]

scaler = MinMaxScaler()
scaled_values = scaler.fit_transform(df[numeric_cols])
scaled_df = pd.DataFrame(
    scaled_values,
    columns=[c + "_scaled" for c in numeric_cols],
    index=df.index
)
df = pd.concat([df, scaled_df], axis=1)

# ==========================================
# 4) SAVE
# ==========================================
df.to_csv("transformed_merged_data.csv", index=False)
print(f"\nTransform สำเร็จ -> transformed_merged_data.csv, shape={df.shape}")
print(df.head())
