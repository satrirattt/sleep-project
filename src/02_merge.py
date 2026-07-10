"""
Step 2: Merge
- รวมข้อมูลไทย (cleaned_thai_data.xlsx) + อังกฤษ (cleaned_english_data.csv)
  ให้เป็น schema เดียวกัน (แปลค่าภาษาไทย -> อังกฤษ)
Output: merged_cleaned_data.csv
"""

import pandas as pd

df_th = pd.read_excel("cleaned_thai_data.xlsx")
df_en = pd.read_csv("cleaned_english_data.csv")

# ==========================================
# Map English columns -> common schema (ตั้งชื่อคอลัมน์ให้ตรงกับฝั่งไทย)
# ==========================================
df_en_std = df_en.rename(columns={
    "feel_rested": "morning_freshness",
    "daily_screen_time": "screen_time",
    "use_before_sleep": "use_phone_before_sleep",
    "anxiety/low_mood": "phone_anxiety",
    "wellness_apps": "health_app_use",
    "screen_time_affects_sleep?": "phone_affects_sleep",
})

# ==========================================
# Standardize Thai categorical values -> English labels
# ==========================================
th_map = {
    "morning_freshness": {"ไม่สดชื่น": "no", "สดชื่น": "yes"},
    "use_phone_before_sleep": {"ใช่": "yes", "ไม่ใช่": "no"},
    "phone_anxiety": {"ไม่หงุดหงิด/ไม่วิตกกังวล": "no", "หงุดหงิด/วิตกกังวล": "yes"},
    "health_app_use": {"ไม่ใช่": "no", "ใช่": "yes"},
    "sleep_quality": {"ไม่ดี": "bad", "ดี": "good"},
    "phone_affects_sleep": {"ไม่แน่ใจ": "not sure", "ใช่": "yes", "ไม่ใช่": "no"},
}

df_th_std = df_th.copy()
for col, mapping in th_map.items():
    df_th_std[col] = df_th_std[col].map(mapping)

df_th_std = df_th_std.drop(columns=["timestamp"])

common_cols = ["age", "sleep_hours", "morning_freshness", "screen_time",
               "use_phone_before_sleep", "stress_level", "phone_anxiety",
               "health_app_use", "sleep_quality", "phone_affects_sleep"]

df_merged = pd.concat([df_th_std[common_cols], df_en_std[common_cols]], ignore_index=True)

print("Merged shape:", df_merged.shape)
print("\nMissing values:")
print(df_merged.isnull().sum())

df_merged.to_csv("merged_cleaned_data.csv", index=False)
print("\nSaved -> merged_cleaned_data.csv")
print(df_merged.head())
