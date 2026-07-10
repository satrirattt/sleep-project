# 😴 Sleep Quality Prediction Pipeline

โปรเจกต์วิเคราะห์และทำนาย **คุณภาพการนอน (Sleep Quality)** จากพฤติกรรมการใช้มือถือ
โดยรวมข้อมูลจาก 2 แหล่ง: แบบสำรวจภาษาไทย และชุดข้อมูล Kaggle (ภาษาอังกฤษ)
ผ่านกระบวนการ Data Cleaning → Merge → EDA → Transform → Machine Learning Pipeline → Deploy (Streamlit)

---

## 📂 โครงสร้างไฟล์

```
sleep-project/
├── survey_data.xlsx              ← ข้อมูลดิบ (แบบสำรวจไทย) ต้องเตรียมเอง
├── kgdataset.csv                 ← ข้อมูลดิบ (Kaggle อังกฤษ) ต้องเตรียมเอง
│
├── 01_cleaning.py                ← Step 1: ทำความสะอาดข้อมูล
├── 02_merge.py                   ← Step 2: รวมข้อมูลไทย+อังกฤษเป็นชุดเดียว
├── 03_eda.py                     ← Step 3: วิเคราะห์ข้อมูล (EDA)
├── 04_transform.py               ← Step 4: Feature engineering / encode / scale
├── 05_pipeline_training.py       ← Step 5: เทรนโมเดล ML
├── 06_streamlit_app.py           ← Step 6: เว็บแอปทำนายผล
│
├── sleep_quality_model.pkl       ← โมเดลที่เทรนไว้แล้ว (พร้อมใช้)
├── target_label_encoder.pkl      ← ตัวแปลงผลลัพธ์ (good/bad)
├── feature_columns.pkl           ← รายชื่อฟีเจอร์ที่โมเดลใช้
│
├── requirements.txt              ← รายการไลบรารีที่ต้องติดตั้ง
├── README_deploy.md              ← คู่มือ deploy ขึ้น Streamlit Cloud โดยละเอียด
└── README.md                     ← ไฟล์นี้
```

---

## 🚀 วิธีใช้งาน (Quick Start)

```bash
# 1) ติดตั้งไลบรารีที่จำเป็น
pip install -r requirements.txt

# 2) วางไฟล์ survey_data.xlsx และ kgdataset.csv ไว้โฟลเดอร์เดียวกับสคริปต์

# 3) รันทีละขั้นตอน (ต้องรันตามลำดับ เพราะแต่ละไฟล์ใช้ output จากไฟล์ก่อนหน้า)
python 01_cleaning.py
python 02_merge.py
python 03_eda.py
python 04_transform.py
python 05_pipeline_training.py

# 4) เปิดเว็บแอปทำนายผล (มีโมเดล .pkl แนบมาให้แล้ว รันได้ทันทีโดยไม่ต้องเทรนใหม่)
py -m streamlit run 06_streamlit_app.py 
```

> ทุกสคริปต์อ่าน/เขียนไฟล์แบบ relative path จึงต้องรัน `python` จากภายในโฟลเดอร์นี้เท่านั้น

---

## 🔍 รายละเอียดแต่ละขั้นตอน

### 1. Cleaning (`01_cleaning.py`)
- ตั้งชื่อคอลัมน์ใหม่ให้อ่านง่าย, แปลงค่าตัวเลขที่เป็น range (เช่น "6-7 ชม.") ให้เป็นค่าเฉลี่ย
- ตัดค่าผิดปกติ (outlier) เช่น อายุ, ชั่วโมงนอน, เวลาหน้าจอ ที่เกินขอบเขตที่สมเหตุสมผล
- Output: `cleaned_thai_data.xlsx`, `cleaned_english_data.csv`

### 2. Merge (`02_merge.py`)
- แปลงค่าคำภาษาไทย (เช่น "ใช่/ไม่ใช่", "ดี/ไม่ดี") ให้เป็นภาษาอังกฤษ (yes/no/good/bad) เพื่อให้ schema ตรงกัน
- รวมข้อมูลทั้งสองแหล่งเป็นไฟล์เดียว **ไม่มีการแยกแหล่งที่มาอีกต่อไป**
- Output: `merged_cleaned_data.csv` (1,178 แถว)

### 3. EDA (`03_eda.py`)
- สรุปสถิติเชิงพรรณนา, histogram, boxplot, correlation heatmap, scatter plot
- Output: โฟลเดอร์ `eda_plots/` (กราฟ .png ทั้งหมด 16 ไฟล์)

### 4. Transform (`04_transform.py`)
- สร้างฟีเจอร์ใหม่: `screen_sleep_ratio`, `age_group`, `sleep_category`
- Encode categorical (LabelEncoder) และ Scale ตัวเลข (MinMaxScaler)
- Output: `transformed_merged_data.csv`

### 5. Pipeline & Training (`05_pipeline_training.py`)
- สร้าง sklearn `Pipeline` (ColumnTransformer: StandardScaler + OneHotEncoder) ต่อด้วย `RandomForestClassifier`
- ทำนาย **sleep_quality (good/bad)**
- **Test Accuracy ≈ 81%**
- Output: `sleep_quality_model.pkl`, `target_label_encoder.pkl`, `feature_columns.pkl`

### 6. Deploy (`06_streamlit_app.py`)
- เว็บแอปให้กรอก อายุ, ชั่วโมงนอน, เวลาหน้าจอ, ความเครียด และพฤติกรรมการใช้มือถือ
- ช่องตัวเลือกทั้งหมดเป็น dropdown/selectbox (ไม่มีค่า default ให้ผู้ใช้ต้องเลือกเอง)
- ทำนายผลพร้อมกราฟความน่าจะเป็นของแต่ละ class
- ดูวิธี deploy ขึ้น Streamlit Community Cloud ได้ใน `README_deploy.md`

---

## 🧠 Model Info

| รายการ | ค่า |
|---|---|
| Algorithm | RandomForestClassifier (n_estimators=300, max_depth=8) |
| Target | sleep_quality (good / bad) |
| Test Accuracy | ~81% |
| Features | age, sleep_hours, screen_time, stress_level, morning_freshness, use_phone_before_sleep, phone_anxiety, health_app_use, phone_affects_sleep |
| Feature สำคัญสุด | sleep_hours, screen_time, stress_level, phone_affects_sleep |

---

## 📦 Dependencies

ดูรายการทั้งหมดใน `requirements.txt`:
- pandas, scikit-learn, joblib
- streamlit (สำหรับ deploy)

## 🔄 Retrain โมเดลใหม่

ถ้ามีข้อมูลใหม่ ให้แทนที่ `survey_data.xlsx` / `kgdataset.csv` แล้วรันสคริปต์ตั้งแต่ `01_cleaning.py` ถึง `05_pipeline_training.py` ใหม่ทั้งหมด ไฟล์ `.pkl` จะถูกเขียนทับด้วยโมเดลเวอร์ชันล่าสุดโดยอัตโนมัติ
