"""
Multi-Disease Prediction System — Main Dashboard & Entry Point
"""
import streamlit as st
import os
import sys
import json
import pandas as pd

# Add project root to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.utils.constants import APP_TITLE, APP_SUBTITLE, DISEASE_METADATA, MEDICAL_DISCLAIMER
from src.utils.ui_components import inject_custom_css, render_disclaimer

st.set_page_config(
    page_title=f"{APP_TITLE} | Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_custom_css()

# Sidebar
with st.sidebar:
    st.markdown("### 🩺 Multi-Disease System")
    st.markdown("**Major Project — CSE Department**")
    st.caption("R R Institute of Technology")
    st.caption("AICTE Approved, VTU Affiliated")
    st.divider()
    st.markdown("#### 🎯 Quick Navigation")
    st.page_link("app.py", label="Home Dashboard", icon="🏠")
    st.page_link("pages/1_Heart_Disease.py", label="Heart Disease", icon="❤️")
    st.page_link("pages/2_Kidney_Disease.py", label="Kidney Disease", icon="🫘")
    st.page_link("pages/3_Liver_Disease.py", label="Liver Disease", icon="🫀")
    st.page_link("pages/4_Lung_Disease.py", label="Lung Disease", icon="🫁")
    st.page_link("pages/5_Breast_Cancer.py", label="Breast Cancer", icon="🎗️")
    st.divider()
    st.markdown("#### 👨‍🔬 Project Guide & Team")
    st.caption("**Guide:** Dr. Manjunath R, Professor & HOD")
    st.caption("**Team (Group 17):**")
    st.caption("• M Kushala (1RI23CS078)\n• Prajwal Aravind D M (1RI23CS108)\n• Sameeksha M G (1RI23CS128)\n• Shiva Prakash T R (1RI23CS134)")

# Hero Section
st.markdown(
    f"""
    <div class="hero-container">
        <div class="hero-title">
            <span>🩺</span> {APP_TITLE}
        </div>
        <div class="hero-subtitle">
            An end-to-end intelligent clinical decision-support framework powered by Classical Machine Learning. 
            Assess risk profiles across five major chronic pathologies through structured diagnostic parameters.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Load metadata for all 5 diseases to display live stats
model_stats = {}
for d_key in DISEASE_METADATA.keys():
    meta_path = os.path.join(BASE_DIR, "models", d_key, "metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            model_stats[d_key] = json.load(f)
    else:
        model_stats[d_key] = {
            "model_name": "Trained Model",
            "accuracy": 0.0,
            "f1_score": 0.0,
            "dataset_rows": 0
        }

# Five Disease Cards
st.markdown("### 🫀 Diagnostic Screening Modules")
st.caption("Select a disease category to launch the interactive risk assessment form:")

col1, col2, col3 = st.columns(3)

with col1:
    meta_h = model_stats.get("heart", {})
    st.markdown(
        f"""
        <div class="disease-card">
            <div>
                <div class="disease-card-header">
                    <div class="disease-icon-box">❤️</div>
                    <div>
                        <h4 class="disease-title">Heart Disease</h4>
                        <span class="badge-pill">{meta_h.get('model_name', 'Random Forest')}</span>
                        <span class="badge-pill">Acc: {meta_h.get('accuracy', 0)*100:.1f}%</span>
                    </div>
                </div>
                <div class="disease-desc">
                    {DISEASE_METADATA['heart']['short_desc']}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link("pages/1_Heart_Disease.py", label="Launch Heart Assessment →", icon="❤️")

with col2:
    meta_k = model_stats.get("kidney", {})
    st.markdown(
        f"""
        <div class="disease-card">
            <div>
                <div class="disease-card-header">
                    <div class="disease-icon-box">🫘</div>
                    <div>
                        <h4 class="disease-title">Kidney Disease</h4>
                        <span class="badge-pill">{meta_k.get('model_name', 'Random Forest')}</span>
                        <span class="badge-pill">Acc: {meta_k.get('accuracy', 0)*100:.1f}%</span>
                    </div>
                </div>
                <div class="disease-desc">
                    {DISEASE_METADATA['kidney']['short_desc']}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link("pages/2_Kidney_Disease.py", label="Launch Kidney Assessment →", icon="🫘")

with col3:
    meta_l = model_stats.get("liver", {})
    st.markdown(
        f"""
        <div class="disease-card">
            <div>
                <div class="disease-card-header">
                    <div class="disease-icon-box">🫀</div>
                    <div>
                        <h4 class="disease-title">Liver Disease</h4>
                        <span class="badge-pill">{meta_l.get('model_name', 'Logistic Reg.')}</span>
                        <span class="badge-pill">Acc: {meta_l.get('accuracy', 0)*100:.1f}%</span>
                    </div>
                </div>
                <div class="disease-desc">
                    {DISEASE_METADATA['liver']['short_desc']}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link("pages/3_Liver_Disease.py", label="Launch Liver Assessment →", icon="🫀")

col4, col5 = st.columns(2)

with col4:
    meta_lu = model_stats.get("lung", {})
    st.markdown(
        f"""
        <div class="disease-card">
            <div>
                <div class="disease-card-header">
                    <div class="disease-icon-box">🫁</div>
                    <div>
                        <h4 class="disease-title">Lung Disease</h4>
                        <span class="badge-pill">{meta_lu.get('model_name', 'KNN')}</span>
                        <span class="badge-pill">Acc: {meta_lu.get('accuracy', 0)*100:.1f}%</span>
                    </div>
                </div>
                <div class="disease-desc">
                    {DISEASE_METADATA['lung']['short_desc']}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link("pages/4_Lung_Disease.py", label="Launch Lung Assessment →", icon="🫁")

with col5:
    meta_b = model_stats.get("breast_cancer", {})
    st.markdown(
        f"""
        <div class="disease-card">
            <div>
                <div class="disease-card-header">
                    <div class="disease-icon-box">🎗️</div>
                    <div>
                        <h4 class="disease-title">Breast Cancer</h4>
                        <span class="badge-pill">{meta_b.get('model_name', 'SVM')}</span>
                        <span class="badge-pill">Acc: {meta_b.get('accuracy', 0)*100:.1f}%</span>
                    </div>
                </div>
                <div class="disease-desc">
                    {DISEASE_METADATA['breast_cancer']['short_desc']}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link("pages/5_Breast_Cancer.py", label="Launch Breast Cancer Assessment →", icon="🎗️")

st.divider()

# How It Works Workflow
st.markdown("### ⚙️ System Workflow")
st.markdown(
    """
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-top: 12px; margin-bottom: 24px;">
        <div class="stat-card">
            <div style="font-size: 1.8rem;">📝</div>
            <div style="font-weight: 700; color: #0f172a; margin-top: 6px;">1. Clinical Data Entry</div>
            <div style="font-size: 0.85rem; color: #64748b;">Patient inputs vitals, laboratory values & symptoms with real-time validation.</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 1.8rem;">🔄</div>
            <div style="font-weight: 700; color: #0f172a; margin-top: 6px;">2. Feature Pipeline</div>
            <div style="font-size: 0.85rem; color: #64748b;">Categorical encoding, imputation & standard scaling via fitted transformers.</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 1.8rem;">🤖</div>
            <div style="font-weight: 700; color: #0f172a; margin-top: 6px;">3. ML Inference</div>
            <div style="font-size: 0.85rem; color: #64748b;">High-performance serialized algorithm generates binary classification & probabilities.</div>
        </div>
        <div class="stat-card">
            <div style="font-size: 1.8rem;">📊</div>
            <div style="font-weight: 700; color: #0f172a; margin-top: 6px;">4. Risk Stratification</div>
            <div style="font-size: 0.85rem; color: #64748b;">Instant risk categorization, confidence score & clinical guidance displayed.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Model Performance Summary Table
st.markdown("### 📈 Live Machine Learning Model Metrics")
metrics_rows = []
for d_key, info in DISEASE_METADATA.items():
    st_data = model_stats.get(d_key, {})
    metrics_rows.append({
        "Disease Module": f"{info['icon']} {info['name']}",
        "Selected Algorithm": st_data.get("model_name", "N/A"),
        "Accuracy": f"{st_data.get('accuracy', 0)*100:.2f}%",
        "Precision": f"{st_data.get('precision', 0)*100:.2f}%",
        "Recall": f"{st_data.get('recall', 0)*100:.2f}%",
        "F1-Score": f"{st_data.get('f1_score', 0)*100:.2f}%",
        "ROC-AUC": f"{st_data.get('roc_auc', 0)*100:.2f}%",
        "Dataset Samples": f"{st_data.get('dataset_rows', 0):,}"
    })

st.dataframe(pd.DataFrame(metrics_rows), use_container_width=True, hide_index=True)

# Tech Stack & Architecture Badges
st.markdown("### 💻 Technology Stack")
st.markdown(
    """
    <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;">
        <span class="badge-pill">🐍 Python 3.11</span>
        <span class="badge-pill">⚡ Streamlit</span>
        <span class="badge-pill">🔬 Scikit-Learn</span>
        <span class="badge-pill">🐼 Pandas</span>
        <span class="badge-pill">🔢 NumPy</span>
        <span class="badge-pill">💾 Joblib</span>
    </div>
    """,
    unsafe_allow_html=True
)

render_disclaimer()
