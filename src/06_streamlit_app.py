import os

import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Sleep Quality Predictor", page_icon="😴", layout="centered")

@st.cache_resource
def load_artifacts():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    
    model = joblib.load(os.path.join(MODEL_DIR, "sleep_quality_model.pkl"))
    target_encoder = joblib.load(os.path.join(MODEL_DIR, "target_label_encoder.pkl"))
    columns = joblib.load(os.path.join(MODEL_DIR, "feature_columns.pkl"))
    return model, target_encoder, columns

model, target_encoder, columns = load_artifacts()

st.title("😴 Sleep Quality Predictor")
st.write(
    "ทำนายคุณภาพการนอน (Good / Bad) จากพฤติกรรมการใช้มือถือและข้อมูลส่วนตัว "
    "โมเดลนี้เทรนจากข้อมูลแบบสำรวจภาษาไทยและชุดข้อมูล Kaggle ที่รวมกันแล้ว"
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("อายุ (Age)", min_value=10, max_value=80, value=10, step=1)
    sleep_hours = st.number_input("ชั่วโมงนอนเฉลี่ยต่อวัน (Sleep Hours)", min_value=0.0, max_value=24.0, value=0.0, step=0.5)
    screen_time = st.number_input("เวลาหน้าจอต่อวัน (Screen Time, ชม.)", min_value=0.0, max_value=24.0, value=0.0, step=0.5)
    stress_level = st.number_input("ระดับความเครียด (1-10)", min_value=0, max_value=10, value=0, step=1)

with col2:
    morning_freshness = st.radio("ตื่นมาสดชื่นไหม?", ["yes", "no"], horizontal=True, index=None)
    use_phone_before_sleep = st.radio("ใช้มือถือก่อนนอนไหม?", ["yes", "no"], horizontal=True,index=None)
    phone_anxiety = st.radio("หงุดหงิด/วิตกกังวลเมื่อไม่ได้ใช้มือถือ?", ["yes", "no"], horizontal=True, index=None)
    health_app_use = st.radio("ใช้แอปสุขภาพไหม?", ["yes", "no"], horizontal=True, index=None)
    phone_affects_sleep = st.selectbox("คิดว่ามือถือส่งผลต่อการนอนไหม?", ["yes", "no", "not sure"], index=None)

st.divider()

if st.button("🔮 Predict Sleep Quality", type="primary", use_container_width=True):
    input_df = pd.DataFrame([{
        "age": age,
        "sleep_hours": sleep_hours,
        "screen_time": screen_time,
        "stress_level": stress_level,
        "morning_freshness": morning_freshness,
        "use_phone_before_sleep": use_phone_before_sleep,
        "phone_anxiety": phone_anxiety,
        "health_app_use": health_app_use,
        "phone_affects_sleep": phone_affects_sleep,
    }])

    pred = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]
    label = target_encoder.inverse_transform([pred])[0]

    proba_dict = dict(zip(target_encoder.classes_, proba))

    if label == "good":
        st.success(f"### ผลทำนาย: คุณภาพการนอน = **ดี (Good)** 🎉")
    else:
        st.error(f"### ผลทำนาย: คุณภาพการนอน = **ไม่ดี (Bad)** 😴")

    st.write("ความน่าจะเป็นของแต่ละ class:")
    proba_df = pd.DataFrame({
        "Sleep Quality": list(proba_dict.keys()),
        "Probability": list(proba_dict.values())
    })
    st.bar_chart(proba_df.set_index("Sleep Quality"))

st.divider()
st.caption("Model: RandomForestClassifier | Test Accuracy ≈ 80.5% | Trained on merged Thai + English survey data")
