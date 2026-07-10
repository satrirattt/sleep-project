"""
Step 1: Cleaning
- ทำความสะอาดข้อมูลแบบสำรวจภาษาไทย (survey_data.xlsx)
- ทำความสะอาดข้อมูล Kaggle ภาษาอังกฤษ (kgdataset.csv)
Output: cleaned_thai_data.xlsx, cleaned_english_data.csv
"""

import pandas as pd
import numpy as np
import re

# ==========================================
# 1) THAI SURVEY DATA
# ==========================================
df = pd.read_excel("survey_data.xlsx")

df.columns = [
    "timestamp",
    "age",
    "sleep_hours",
    "morning_freshness",
    "screen_time",
    "use_phone_before_sleep",
    "stress_level",
    "phone_anxiety",
    "health_app_use",
    "sleep_quality",
    "phone_affects_sleep"
]


def clean_numeric(value):
    if pd.isna(value):
        return np.nan
    value = str(value).strip()
    if "ล้านปีแสง" in value:
        return np.nan
    range_match = re.search(r'(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)', value)
    if range_match:
        low = float(range_match.group(1))
        high = float(range_match.group(2))
        return (low + high) / 2
    single_match = re.search(r'(\d+\.?\d*)', value)
    if single_match:
        return float(single_match.group(1))
    return np.nan


numeric_cols = ["age", "sleep_hours", "screen_time", "stress_level"]
for col in numeric_cols:
    df[col] = df[col].apply(clean_numeric)

df["age"] = df["age"].where(df["age"].between(10, 80))
df["sleep_hours"] = df["sleep_hours"].where(df["sleep_hours"].between(1, 24))
df["screen_time"] = df["screen_time"].where(df["screen_time"].between(0, 24))
df["stress_level"] = df["stress_level"].where(df["stress_level"].between(1, 10))

df = df.dropna(subset=["age", "sleep_hours", "screen_time"])

df.to_excel("cleaned_thai_data.xlsx", index=False)
print(f"[Thai] Cleaned successfully -> cleaned_thai_data.xlsx, shape={df.shape}")


# ==========================================
# 2) ENGLISH (KAGGLE) DATA
# ==========================================
df_en = pd.read_csv("kgdataset.csv")

df_en = df_en.drop_duplicates()
df_en.columns = df_en.columns.str.strip().str.lower().str.replace(" ", "_")

for col in df_en.select_dtypes(include='object').columns:
    df_en[col] = df_en[col].str.strip().str.lower()

print("\n[English] Missing values per column:")
print(df_en.isnull().sum())

if "age" in df_en.columns:
    df_en = df_en[(df_en["age"] >= 10) & (df_en["age"] <= 100)]

df_en.to_csv("cleaned_english_data.csv", index=False)
print(f"\n[English] Cleaned successfully -> cleaned_english_data.csv, shape={df_en.shape}")
