"""
Heart Disease Prediction Page — Multi-Disease Prediction System
"""
import streamlit as st
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.utils.constants import HEART_FIELDS, DISEASE_METADATA
from src.utils.ui_components import inject_custom_css, render_disclaimer, render_model_info_expander, render_prediction_result
from src.prediction.predict import predict_disease

st.set_page_config(
    page_title="Heart Disease Prediction | MDPS",
    page_icon="❤️",
    layout="wide"
)

inject_custom_css()

# Header
st.markdown("## ❤️ Heart Disease Risk Assessment")
st.markdown(
    "Predict cardiovascular risk using patient demographics, resting vitals, electrocardiogram (ECG) metrics, and exercise stress parameters."
)

render_disclaimer()

# Presets for quick demo evaluation
st.markdown("##### ⚡ Quick Demonstration Presets")
c_preset1, c_preset2, c_preset3 = st.columns([1.5, 1.5, 3])

if "heart_data" not in st.session_state:
    st.session_state.heart_data = {k: v["default"] for k, v in HEART_FIELDS.items()}

with c_preset1:
    if st.button("🟢 Load Normal / Low Risk Sample"):
        st.session_state.heart_data = {
            "age": 35, "sex": "Female", "cp": "Typical Angina", "trestbps": 118, "chol": 182,
            "fbs": "No", "restecg": "Normal", "thalach": 172, "exang": "No", "oldpeak": 0.0,
            "slope": "Upsloping", "ca": 0, "thal": "Normal"
        }
        st.rerun()

with c_preset2:
    if st.button("🔴 Load Elevated / High Risk Sample"):
        st.session_state.heart_data = {
            "age": 62, "sex": "Male", "cp": "Asymptomatic", "trestbps": 160, "chol": 290,
            "fbs": "Yes", "restecg": "Left Ventricular Hypertrophy", "thalach": 108, "exang": "Yes", "oldpeak": 3.2,
            "slope": "Downsloping", "ca": 2, "thal": "Reversible Defect"
        }
        st.rerun()

with c_preset3:
    if st.button("🔄 Reset Defaults"):
        st.session_state.heart_data = {k: v["default"] for k, v in HEART_FIELDS.items()}
        st.rerun()

st.markdown("---")

# Main Form
with st.form("heart_form"):
    st.markdown("#### 📋 Clinical Input Parameters")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**1. Demographics & Vitals**")
        age = st.number_input("Age (years)", min_value=18, max_value=100, value=int(st.session_state.heart_data.get("age", 54)), help="Patient age in years")
        sex = st.selectbox("Biological Sex", options=["Male", "Female"], index=["Male", "Female"].index(st.session_state.heart_data.get("sex", "Male")))
        trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=80, max_value=200, value=int(st.session_state.heart_data.get("trestbps", 130)), help="Resting BP upon admission")
        chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=100, max_value=600, value=int(st.session_state.heart_data.get("chol", 240)), help="Total serum cholesterol")

    with c2:
        st.markdown("**2. Symptoms & Metabolic**")
        cp = st.selectbox("Chest Pain Type (CP)", options=["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"], index=["Typical Angina", "Atypical Angina", "Non-anginal Pain", "Asymptomatic"].index(st.session_state.heart_data.get("cp", "Typical Angina")))
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.heart_data.get("fbs", "No")))
        restecg = st.selectbox("Resting ECG Result", options=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"], index=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"].index(st.session_state.heart_data.get("restecg", "Normal")))
        thalach = st.number_input("Max Heart Rate Achieved (bpm)", min_value=60, max_value=220, value=int(st.session_state.heart_data.get("thalach", 150)))

    with c3:
        st.markdown("**3. Stress Test & Diagnostics**")
        exang = st.selectbox("Exercise-Induced Angina", options=["No", "Yes"], index=["No", "Yes"].index(st.session_state.heart_data.get("exang", "No")))
        oldpeak = st.number_input("ST Depression (Oldpeak)", min_value=0.0, max_value=6.5, value=float(st.session_state.heart_data.get("oldpeak", 1.0)), step=0.1)
        slope = st.selectbox("Slope of Peak Exercise ST", options=["Upsloping", "Flat", "Downsloping"], index=["Upsloping", "Flat", "Downsloping"].index(st.session_state.heart_data.get("slope", "Flat")))
        ca = st.number_input("Major Vessels Colored by Fluoroscopy (0-4)", min_value=0, max_value=4, value=int(st.session_state.heart_data.get("ca", 0)))
        thal = st.selectbox("Thalassemia Status", options=["Normal", "Fixed Defect", "Reversible Defect"], index=["Normal", "Fixed Defect", "Reversible Defect"].index(st.session_state.heart_data.get("thal", "Normal")))

    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.form_submit_button("🩺 Run Heart Disease Prediction", use_container_width=True)

if submit_btn:
    user_payload = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal
    }

    with st.spinner("Analyzing cardiovascular biomarker indicators..."):
        prediction_res = predict_disease("heart", user_payload)
        render_prediction_result(prediction_res)

st.markdown("---")
render_model_info_expander("heart")
