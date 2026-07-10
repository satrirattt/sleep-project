"""
Step 3: EDA (Exploratory Data Analysis)
- วิเคราะห์ข้อมูลรวม (merged_cleaned_data.csv) เป็นชุดเดียวกัน (ไม่แยกไทย/อังกฤษ)
Output: eda_plots/*.png, สรุปสถิติทาง stdout
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

os.makedirs("eda_plots", exist_ok=True)

df = pd.read_csv("merged_cleaned_data.csv")

print("========== DATASET SUMMARY ==========")
summary = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.values,
    "Missing": df.isnull().sum().values,
    "Unique": df.nunique().values
})
print(summary)

num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
cat_cols = df.select_dtypes(include="object").columns.tolist()

print("\n========== NUMERIC SUMMARY ==========")
print(df[num_cols].describe())

# --- Histograms (numeric) ---
for col in num_cols:
    plt.figure(figsize=(7, 4))
    plt.hist(df[col].dropna(), bins=15, color="#4C72B0", edgecolor="white")
    plt.title(f"Distribution - {col}")
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(f"eda_plots/hist_{col}.png", dpi=120)
    plt.close()

# --- Boxplot (numeric) ---
for col in num_cols:
    plt.figure(figsize=(6, 4))
    plt.boxplot(df[col].dropna())
    plt.title(f"Boxplot - {col}")
    plt.ylabel(col)
    plt.tight_layout()
    plt.savefig(f"eda_plots/box_{col}.png", dpi=120)
    plt.close()

# --- Category bar charts ---
for col in cat_cols:
    plt.figure(figsize=(7, 4))
    df[col].value_counts().plot(kind="bar", color="#DD8452")
    plt.title(f"Distribution - {col}")
    plt.xlabel(col)
    plt.ylabel("Count")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(f"eda_plots/bar_{col}.png", dpi=120)
    plt.close()

# --- Correlation heatmap ---
corr = df[num_cols].corr()
print("\n========== CORRELATION MATRIX ==========")
print(corr)

plt.figure(figsize=(6, 5))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("eda_plots/correlation_heatmap.png", dpi=120)
plt.close()

# --- Scatter: screen_time vs sleep_hours ---
plt.figure(figsize=(7, 5))
plt.scatter(df["screen_time"], df["sleep_hours"], alpha=0.5, color="#4C72B0")
plt.xlabel("Screen Time (hours)")
plt.ylabel("Sleep Hours")
plt.title("Screen Time vs Sleep Hours")
plt.tight_layout()
plt.savefig("eda_plots/scatter_screen_vs_sleep.png", dpi=120)
plt.close()

corr_screen_sleep = df["screen_time"].corr(df["sleep_hours"])

print("\n========== INSIGHT (ข้อมูลรวมทั้งหมด) ==========")
print(f"- จำนวนข้อมูลทั้งหมด: {len(df)} แถว")
print(f"- Average age: {df['age'].mean():.1f}")
print(f"- Average sleep: {df['sleep_hours'].mean():.1f} hours")
print(f"- Average screen time: {df['screen_time'].mean():.1f} hours")
print(f"- Average stress level: {df['stress_level'].mean():.1f}")
print(f"- Correlation screen_time vs sleep_hours: {corr_screen_sleep:.2f}")

print("\nกราฟทั้งหมดถูกบันทึกไว้ในโฟลเดอร์ eda_plots/")
