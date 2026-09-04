"""
Shared UI helper components and custom CSS design system for Streamlit app.
"""
import streamlit as st
import json
import os
from typing import Dict, Any, Optional

def inject_custom_css():
    """
    Injects a cohesive, modern healthcare design system with sleek typography,
    custom cards, gradients, and responsive elements.
    """
    custom_css = """
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        color: #0f172a;
    }

    /* Main Container Padding */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 40%, #0369a1 100%);
        border-radius: 16px;
        padding: 32px 36px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 10px 25px -5px rgba(14, 165, 233, 0.25), 0 8px 10px -6px rgba(14, 165, 233, 0.2);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #e0f2fe;
        line-height: 1.5;
        max-width: 800px;
    }

    /* Disease Card */
    .disease-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.25s ease-in-out;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .disease-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px -6px rgba(15, 23, 42, 0.08);
        border-color: #38bdf8;
    }
    .disease-card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .disease-icon-box {
        font-size: 2rem;
        background: #f0f9ff;
        border-radius: 12px;
        width: 52px;
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #bae6fd;
    }
    .disease-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0;
    }
    .disease-desc {
        font-size: 0.92rem;
        color: #64748b;
        line-height: 1.5;
        margin-bottom: 16px;
    }
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        background: #e0f2fe;
        color: #0369a1;
        margin-right: 6px;
    }

    /* Result Cards */
    .result-card-positive {
        background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%);
        border: 2px solid #f43f5e;
        border-radius: 16px;
        padding: 24px;
        margin-top: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 20px -5px rgba(244, 63, 94, 0.2);
    }
    .result-card-negative {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #22c55e;
        border-radius: 16px;
        padding: 24px;
        margin-top: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 20px -5px rgba(34, 197, 94, 0.2);
    }
    .result-title-positive {
        color: #be123c !important;
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .result-title-negative {
        color: #15803d !important;
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .result-recommendation {
        font-size: 1rem;
        color: #334155;
        line-height: 1.6;
        margin-top: 12px;
    }

    /* Disclaimer Box */
    .disclaimer-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 14px 18px;
        font-size: 0.85rem;
        color: #64748b;
        line-height: 1.5;
        margin-top: 24px;
        margin-bottom: 24px;
    }

    /* Section Cards */
    .section-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .section-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0369a1;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Model Stat Badge */
    .stat-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
    }
    .stat-val {
        font-size: 1.5rem;
        font-weight: 800;
        color: #0284c7;
    }
    .stat-lbl {
        font-size: 0.78rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Form buttons styling */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.6rem 1.8rem;
        border: none;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
        transition: all 0.2s ease;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        box-shadow: 0 6px 16px rgba(14, 165, 233, 0.4);
        transform: translateY(-1px);
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_disclaimer():
    """Renders the standard medical disclaimer banner."""
    st.markdown(
        """
        <div class="disclaimer-box">
            <strong>⚠️ Medical Disclaimer:</strong> This system is an academic machine-learning screening prototype developed for educational and research demonstration. It is <strong>NOT</strong> a certified medical device and its predictions are <strong>NOT</strong> a substitute for professional clinical diagnosis or consultation. Always consult a licensed healthcare practitioner.
        </div>
        """,
        unsafe_allow_html=True
    )

def render_model_info_expander(disease: str):
    """
    Renders an expandable section with live metrics loaded from metadata.json.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    meta_path = os.path.join(base_dir, "models", disease, "metadata.json")

    if not os.path.exists(meta_path):
        st.info("Model metrics metadata not available.")
        return

    with open(meta_path, "r") as f:
        meta = json.load(f)

    with st.expander(f"📊 Model Information & Evaluation Metrics ({meta.get('model_name', 'Model')})", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Selected Algorithm", meta.get("model_name", "N/A"))
        c2.metric("Accuracy", f"{meta.get('accuracy', 0)*100:.2f}%")
        c3.metric("F1 Score", f"{meta.get('f1_score', 0)*100:.2f}%")
        c4.metric("ROC-AUC", f"{meta.get('roc_auc', 0)*100:.2f}%")

        st.caption(f"Dataset Records: **{meta.get('dataset_rows', 0)}** (Training split: {meta.get('train_rows', 0)}, Test split: {meta.get('test_rows', 0)}) | Last Trained: {meta.get('last_trained', 'N/A')}")

        if "candidate_comparison" in meta:
            st.markdown("##### 🔬 Candidate Algorithms Comparison Table")
            comp = meta["candidate_comparison"]
            rows = []
            for alg, scores in comp.items():
                rows.append({
                    "Algorithm": alg,
                    "Accuracy": f"{scores['accuracy']*100:.2f}%",
                    "Precision": f"{scores['precision']*100:.2f}%",
                    "Recall": f"{scores['recall']*100:.2f}%",
                    "F1 Score": f"{scores['f1_score']*100:.2f}%",
                    "ROC-AUC": f"{scores['roc_auc']*100:.2f}%"
                })
            st.dataframe(rows, use_container_width=True, hide_index=True)

def render_prediction_result(res: Dict[str, Any]):
    """
    Renders the rich prediction card with confidence and risk stratification.
    """
    if res["status"] != "success":
        st.error(f"Prediction Error: {res.get('message', 'Unknown failure')}")
        if "errors" in res:
            for err in res["errors"]:
                st.warning(f"• {err}")
        return

    is_pos = res["is_positive"]
    card_class = "result-card-positive" if is_pos else "result-card-negative"
    title_class = "result-title-positive" if is_pos else "result-title-negative"
    icon = "⚠️" if is_pos else "✅"

    st.markdown(
        f"""
        <div class="{card_class}">
            <div style="font-size: 0.85rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; color: {'#be123c' if is_pos else '#15803d'};">
                {res['risk_level'].upper()} ASSESSMENT
            </div>
            <div class="{title_class}">
                {icon} {res['result_label']}
            </div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #334155; margin-bottom: 8px;">
                Model Prediction Confidence: <strong>{res['confidence']:.2f}%</strong>
            </div>
            <div class="result-recommendation">
                {res['recommendation']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Progress bar and probabilities
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("**Confidence Level:**")
        st.progress(res["confidence"] / 100.0)
    with c2:
        st.caption(f"Risk Probability: **{res['probability_positive']}%** | Normal Probability: **{res['probability_negative']}%**")
