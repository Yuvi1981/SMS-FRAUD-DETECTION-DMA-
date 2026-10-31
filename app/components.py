import os
import re
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

from app.theme import (
    NAVY, TEAL, SPAM_RED, HAM_GREEN, AMBER,
    CARD_BG, CARD_BORDER, TEXT_PRIMARY, TEXT_MUTED
)

# ---------------------------------------------------------
# CACHED ARTIFACT LOADERS WITH GRACEFUL ERROR HANDLING
# ---------------------------------------------------------

@st.cache_resource(show_spinner="Loading machine learning models...")
def load_model(filepath: str):
    """Loads a serialized joblib model or bundle. Never crashes with a traceback."""
    if not os.path.exists(filepath):
        return None
    try:
        return joblib.load(filepath)
    except Exception as e:
        st.warning(f"⚠️ Error reading model artifact `{filepath}`: {e}")
        return None

@st.cache_data(show_spinner="Loading project dataset...")
def load_csv_data(filepath: str):
    """Loads a CSV dataset or table. Never crashes with a traceback."""
    if not os.path.exists(filepath):
        return None
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        st.warning(f"⚠️ Error reading table artifact `{filepath}`: {e}")
        return None

def check_file_exists(filepath: str, label: str = "Artifact") -> bool:
    """Verifies artifact presence and displays a friendly warning if missing."""
    if not os.path.exists(filepath):
        st.warning(f"⚠️ Missing expected {label}: `{filepath}`. Please ensure pipeline artifacts are generated.")
        return False
    return True

# ---------------------------------------------------------
# TEXT PREPROCESSING PIPELINE (REPRODUCIBLE FOR LIVE DEMO)
# ---------------------------------------------------------
stemmer = PorterStemmer()
try:
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    STOP_WORDS = {"i", "me", "my", "myself", "we", "our", "ours", "you", "your", "he", "him", "she", "it", "they", "the", "a", "an", "and", "or", "to", "in", "is", "of", "for", "on", "that", "this"}

def preprocess_live_sms(s: str) -> dict:
    """Applies exact project preprocessing pipeline to live SMS input."""
    raw = str(s)
    # Feature signals
    has_url = int(bool(re.search(r"https?://|www\.", raw, re.I)))
    has_phone = int(bool(re.search(r"\b\d{7,}\b", raw)))
    has_money = int(bool(re.search(r"[\$£€]|prize|claim|cash|won", raw, re.I)))
    n_chars = len(raw)
    n_words = len(raw.split())

    # Text cleaning
    clean = raw.lower()
    clean = re.sub(r"(https?://\S+|www\.\S+)", " urltoken ", clean)
    clean = re.sub(r"\b\d{7,}\b", " phonetoken ", clean)
    clean = re.sub(r"[\$£€]\s?\d*", " moneytoken ", clean)
    clean = re.sub(r"\d+", " numtoken ", clean)
    clean = re.sub(r"[^a-z\s]", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()

    # Stemmed tokens
    tokens = [stemmer.stem(w) for w in clean.split() if w not in STOP_WORDS and len(w) > 1]
    tokens_str = " ".join(tokens) if tokens else "texttoken"

    return {
        "raw": raw,
        "clean": clean,
        "tokens": tokens_str,
        "token_list": tokens,
        "has_url": has_url,
        "has_phone": has_phone,
        "has_money": has_money,
        "n_chars": n_chars,
        "n_words": n_words
    }

# ---------------------------------------------------------
# UI PRESENTATION COMPONENTS
# ---------------------------------------------------------

def render_header(title: str, subtitle: str, badge: str = "DMA Mini Project"):
    """Renders the top header bar with title, subtitle, and project badge."""
    st.markdown(f"""
    <div class="header-bar">
        <div class="header-title-box">
            <h1>{title}</h1>
            <div class="header-subtitle">{subtitle}</div>
        </div>
        <div class="header-badge">{badge}</div>
    </div>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, subtitle: str = None, icon: str = None):
    """Renders a styled KPI metric card with elevation hover."""
    icon_html = f"<span style='font-size:20px;margin-right:6px;'>{icon}</span>" if icon else ""
    sub_html = f"<div class='metric-subtitle'>{subtitle}</div>" if subtitle else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{icon_html}{title}</div>
        <div class="metric-value">{value}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def render_pipeline_strip():
    """Renders the 5 connected pipeline cards across the bottom of the overview."""
    st.markdown("""
    <div style="margin-top: 32px; margin-bottom: 12px;">
        <h4 style="color:#1F2A44; font-weight:700; margin-bottom:4px;">End-to-End Machine Learning Pipeline</h4>
        <div style="color:#64748B; font-size:13px; margin-bottom:16px;">Systematic architecture from raw SMS strings to classification and time-series volume forecasting.</div>
    </div>
    <div class="pipeline-container">
        <div class="pipeline-step">
            <div class="pipeline-step-num">Step 01</div>
            <div class="pipeline-step-name">Preprocess</div>
            <div class="pipeline-step-desc">Regex tokenization, entity replacement, stopword removal & Porter stemming.</div>
        </div>
        <div class="pipeline-step">
            <div class="pipeline-step-num">Step 02</div>
            <div class="pipeline-step-name">Features</div>
            <div class="pipeline-step-desc">TF-IDF n-grams (1,2), Chi-square selection (top 500) & handcrafted signals.</div>
        </div>
        <div class="pipeline-step">
            <div class="pipeline-step-num">Step 03</div>
            <div class="pipeline-step-name">Models</div>
            <div class="pipeline-step-desc">Naive Bayes, Cosine k-NN, Bayesian Network DAG, and L2 Logistic Regression.</div>
        </div>
        <div class="pipeline-step">
            <div class="pipeline-step-num">Step 04</div>
            <div class="pipeline-step-name">Evaluate</div>
            <div class="pipeline-step-desc">Stratified 5-fold CV, holdout ROC/PR curves, odds-ratio interpretability.</div>
        </div>
        <div class="pipeline-step">
            <div class="pipeline-step-num">Step 05</div>
            <div class="pipeline-step-name">Forecast</div>
            <div class="pipeline-step-desc">365-day simulated time series, 7-day smoothing & 30-day ARIMA projection.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_verdict_badge(is_spam: bool, confidence: float, spam_prob: float):
    """Renders the large visual verdict badge and probability bar."""
    if is_spam:
        badge_html = f"""
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px; margin-bottom:16px;">
            <div class="badge-spam">
                <span>🚨</span> SPAM MESSAGE
            </div>
            <div style="text-align:right;">
                <div style="font-size:13px; color:#64748B; font-weight:600; text-transform:uppercase;">Model Confidence</div>
                <div style="font-size:26px; font-weight:800; color:{SPAM_RED};">{confidence*100:.1f}%</div>
            </div>
        </div>
        """
    else:
        badge_html = f"""
        <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px; margin-bottom:16px;">
            <div class="badge-ham">
                <span>✅</span> HAM (LEGITIMATE)
            </div>
            <div style="text-align:right;">
                <div style="font-size:13px; color:#64748B; font-weight:600; text-transform:uppercase;">Model Confidence</div>
                <div style="font-size:26px; font-weight:800; color:{HAM_GREEN};">{(1.0 - spam_prob)*100:.1f}%</div>
            </div>
        </div>
        """
    st.markdown(badge_html, unsafe_allow_html=True)
    
    # Probability bar with Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=["Probability"],
        x=[spam_prob * 100],
        orientation="h",
        name="Spam Risk",
        marker=dict(color=SPAM_RED),
        text=f"Spam: {spam_prob*100:.1f}%",
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(color="white", size=13, family="Inter")
    ))
    fig.add_trace(go.Bar(
        y=["Probability"],
        x=[(1.0 - spam_prob) * 100],
        orientation="h",
        name="Ham Likelihood",
        marker=dict(color=HAM_GREEN),
        text=f"Ham: {(1.0-spam_prob)*100:.1f}%",
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(color="white", size=13, family="Inter")
    ))
    fig.update_layout(
        barmode="stack",
        height=70,
        margin=dict(l=0, r=0, t=10, b=10),
        xaxis=dict(range=[0, 100], showgrid=False, showticklabels=False),
        yaxis=dict(showticklabels=False),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def render_why_chips(token_list: list, odds_lookup: dict):
    """Renders colour-coded chips with odds ratios showing why the model decided spam vs ham."""
    if not token_list:
        st.info("No significant predictive keywords identified in message.")
        return

    chips_html = ["<div style='margin-top:10px; margin-bottom:16px; display:flex; flex-wrap:wrap;'>"]
    matched_count = 0
    
    for token in token_list:
        if token in odds_lookup:
            matched_count += 1
            info = odds_lookup[token]
            odds_val = info.get("odds_ratio", 1.0)
            if odds_val > 1.2:
                chips_html.append(
                    f"<div class='word-chip word-chip-spam'><strong>{token}</strong> (OR: {odds_val:.2f}x 🚨)</div>"
                )
            elif odds_val < 0.8:
                chips_html.append(
                    f"<div class='word-chip word-chip-ham'><strong>{token}</strong> (OR: {odds_val:.2f}x ✅)</div>"
                )
            else:
                chips_html.append(
                    f"<div class='word-chip word-chip-neutral'>{token} (OR: {odds_val:.2f}x)</div>"
                )
        else:
            chips_html.append(f"<div class='word-chip word-chip-neutral'>{token}</div>")

    chips_html.append("</div>")
    st.markdown("".join(chips_html), unsafe_allow_html=True)
    
    if matched_count > 0:
        st.caption("ℹ️ **Interpretation Guide**: Odds Ratio (OR) > 1.0 indicates that presence of this term increases the odds of the SMS being Spam. OR < 1.0 indicates the term shifts the odds toward legitimate Ham.")

def render_simulated_banner():
    """Renders prominent amber warning indicating dates are simulated."""
    st.markdown("""
    <div class="simulated-banner">
        <span style="font-size:20px;">⚠️</span>
        <div>
            <strong>Notice on Timestamps</strong>: The UCI SMS Spam Collection does not contain native timestamps.
            Daily volumes and series dates are <strong>SIMULATED</strong> with mild annual trend, weekly seasonality, and realistic noise for time-series and forecasting demonstrations.
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Renders the standard footer across all pages."""
    st.markdown("""
    <div class="app-footer">
        <strong>Data Mining & Analytics (DMA) Mini Project</strong> • Built with Streamlit & Scikit-Learn<br>
        Dataset: <em>SMS Spam Collection</em> (Almeida, Gómez Hidalgo & Yamakami, UCI Machine Learning Repository)<br>
        <span style="color:#B45309; font-weight:600;">Note: Daily time-series timestamps are SIMULATED for demonstration purposes.</span>
    </div>
    """, unsafe_allow_html=True)
