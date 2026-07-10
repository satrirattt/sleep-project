# Sleep Quality Predictor — Streamlit Deployment

## ไฟล์ในโฟลเดอร์นี้
- `streamlit_app.py` — โค้ดแอป Streamlit
- `sleep_quality_model.pkl` — โมเดล RandomForest ที่เทรนแล้ว (sklearn Pipeline)
- `target_label_encoder.pkl` — LabelEncoder สำหรับ target (good/bad)
- `feature_columns.pkl` — รายชื่อคอลัมน์ฟีเจอร์ที่โมเดลใช้
- `requirements.txt` — dependency สำหรับรันแอป

## วิธีรันบนเครื่องตัวเอง (Local)
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```
แอปจะเปิดที่ http://localhost:8501

## วิธี Deploy ขึ้น Streamlit Community Cloud (ฟรี)
1. สร้าง GitHub repo แล้วอัปโหลดไฟล์ทั้งหมดในโฟลเดอร์นี้ (streamlit_app.py, *.pkl, requirements.txt)
2. เข้า https://share.streamlit.io แล้ว login ด้วย GitHub
3. กด "New app" → เลือก repo/branch → ตั้ง Main file path เป็น `streamlit_app.py`
4. กด Deploy รอสักครู่ก็จะได้ลิงก์แอปสาธารณะ

## Retrain โมเดลใหม่
ถ้าอยากเทรนใหม่ด้วยข้อมูลอัปเดต ให้รันสคริปต์ `train_pipeline.py` (อยู่นอกโฟลเดอร์ deploy)
แล้ว copy ไฟล์ .pkl ทั้ง 3 ไฟล์มาไว้ในโฟลเดอร์นี้อีกครั้ง
