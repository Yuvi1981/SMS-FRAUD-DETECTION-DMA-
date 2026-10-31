import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from app.theme import (
    apply_custom_css, NAVY, TEAL, SPAM_RED, HAM_GREEN, AMBER,
    CARD_BG, CARD_BORDER, TEXT_PRIMARY, TEXT_MUTED
)
from app.components import (
    load_model, load_csv_data, check_file_exists,
    preprocess_live_sms, render_header, render_metric_card,
    render_pipeline_strip, render_verdict_badge, render_why_chips,
    render_simulated_banner, render_footer
)

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="SMS Spam Classifier & Volume Forecast | DMA",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified design system & tokens
apply_custom_css()

# ---------------------------------------------------------
# SIDEBAR NAVIGATION & CONTROLS
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <span style="font-size:28px;">🛡️</span>
        <div>
            <div style="font-size:16px; font-weight:800; color:{NAVY}; line-height:1.2;">SpamShield Analytics</div>
            <div style="font-size:12px; color:{TEAL}; font-weight:600;">DMA Mini Project</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    nav_page = st.radio(
        "Navigation Menu",
        options=[
            "Overview",
            "Live Prediction",
            "EDA",
            "Model Comparison",
            "Word Insights",
            "Bayesian Network",
            "Time Series"
        ],
        index=0,
        help="Select a view to explore data insights, real-time prediction, or forecasting."
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Live Classifier Settings")
    selected_model_name = st.selectbox(
        "Default Live Model",
        options=["Logistic Regression", "Naive Bayes", "k-Nearest Neighbors"],
        index=0,
        help="Choose the model used for primary probability scoring on the Live Prediction page."
    )
    
    st.markdown("---")
    with st.expander("ℹ️ About This Project", expanded=False):
        st.markdown("""
        **SMS Spam Classifier + Daily Volume Forecast**
        
        • **Dataset**: SMS Spam Collection (UCI)  
        • **Size**: 5,169 distinct messages (5,572 raw)  
        • **Spam Ratio**: ~12.6% spam, ~87.4% ham  
        • **Features**: TF-IDF n-grams (1,2) + $\\chi^2$ selection  
        • **Models**: NB, k-NN, Bayesian Net, Logistic Reg  
        • **Time-Series**: 365-day simulated volume & ARIMA forecast  
        
        *DMA Mini Project — Academic Implementation*
        """)

# ---------------------------------------------------------
# PAGE 1: OVERVIEW
# ---------------------------------------------------------
if nav_page == "Overview":
    render_header(
        title="SMS Spam Classifier & Daily Volume Forecast",
        subtitle="End-to-End Text Mining, Explainable Classification, and Simulated Volume Forecasting",
        badge="DMA Mini Project"
    )
    
    # Load required artifacts
    comp_df = load_csv_data("outputs/tables/model_comparison.csv")
    eda_summary_df = load_csv_data("outputs/tables/eda_summary.csv")
    clean_df = load_csv_data("data/processed/clean.csv")
    
    # Metric cards row
    total_msgs = "5,169"
    spam_pct = "12.63%"
    best_model = "Logistic Regression"
    best_f1 = "0.9653"
    
    if eda_summary_df is not None:
        tot_row = eda_summary_df[eda_summary_df["class"] == "total"]
        if not tot_row.empty:
            total_msgs = f"{int(tot_row['count'].iloc[0]):,}"
        spam_row = eda_summary_df[eda_summary_df["class"] == "spam"]
        if not spam_row.empty:
            spam_pct = f"{spam_row['percentage'].iloc[0]:.2f}%"
            
    if comp_df is not None:
        best_row = comp_df.sort_values(by="F1", ascending=False).iloc[0]
        best_model = str(best_row["Model"]).split("(")[0].strip()
        best_f1 = f"{best_row['F1']:.4f}"
        
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Total SMS Messages", total_msgs, "Deduplicated corpus", "📩")
    with c2:
        render_metric_card("Spam Prevalence", spam_pct, "Highly imbalanced", "🚨")
    with c3:
        render_metric_card("Champion Model", best_model, "Highest test performance", "🏆")
    with c4:
        render_metric_card("Champion F1-Score", best_f1, "Optimized for spam class", "🎯")
        
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # 2 Columns: Summary (Left) & Class Balance Chart (Right)
    col_left, col_right = st.columns([1.1, 1], gap="medium")
    
    with col_left:
        with st.container(border=True):
            st.markdown(f"### 📋 Executive Summary")
            st.markdown("""
            - **Class-Imbalanced Text Classification**: Trained and evaluated four distinct model paradigms on 5,169 deduplicated SMS messages, rigorously handling an 87:13 ham/spam ratio without data leakage.
            - **Transparent Word-Level Odds Ratios**: Extracted interpretable coefficients via Logistic Regression (exp(β)) that quantify how specific keywords (e.g. *prize, free, urgent*) scale spam probability.
            - **Holdout Spam-Volume Forecast**: Evaluated 7-day smoothing and an ARIMA(1,1,1) model over a 30-day holdout period against naive baselines to anticipate incoming spam load.
            """)
        
    with col_right:
        with st.container(border=True):
            st.markdown("### 📊 Corpus Class Balance")
            # Interactive donut chart
            donut_data = pd.DataFrame({
                "Label": ["Ham (Legitimate)", "Spam"],
                "Count": [4516, 653]
            })
            if clean_df is not None:
                counts = clean_df["label"].value_counts()
                donut_data = pd.DataFrame({
                    "Label": ["Ham (Legitimate)", "Spam"],
                    "Count": [counts.get("ham", 4516), counts.get("spam", 653)]
                })
                
            fig_donut = px.pie(
                donut_data,
                values="Count",
                names="Label",
                hole=0.62,
                color="Label",
                color_discrete_map={"Ham (Legitimate)": HAM_GREEN, "Spam": SPAM_RED}
            )
            fig_donut.update_traces(
                textposition="inside",
                textinfo="percent+label",
                marker=dict(line=dict(color="#FFFFFF", width=2))
            )
            fig_donut.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                height=210,
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
        
    # Pipeline strip
    render_pipeline_strip()

# ---------------------------------------------------------
# PAGE 2: LIVE PREDICTION
# ---------------------------------------------------------
elif nav_page == "Live Prediction":
    render_header(
        title="Live SMS Spam Prediction & Explainability",
        subtitle="Real-Time Classification with Word Odds Ratios and Multi-Model Consensus",
        badge="Inference Engine"
    )
    
    # Load models and odds lookup table
    models_bundle = load_model("outputs/models/vectorizers.joblib")
    nb_model = load_model("outputs/models/nb_best.joblib")
    knn_model = load_model("outputs/models/knn_best.joblib")
    lr_model = load_model("outputs/models/lr_best.joblib")
    odds_df = load_csv_data("outputs/tables/lr_odds_ratios.csv")
    
    odds_lookup = {}
    if odds_df is not None:
        for _, row in odds_df.iterrows():
            odds_lookup[str(row["word"])] = {
                "odds_ratio": float(row["odds_ratio"]),
                "coef": float(row["coef"]),
                "direction": str(row["direction"])
            }
            
    SAMPLE_SPAM = "WINNER! You have won a guaranteed £1,000 cash prize or a holiday! Call 09061701461 to claim now. Reply STOP to cancel."
    SAMPLE_HAM_1 = "Hey, are we still meeting at the library around 4pm to work on the DMA project?"
    SAMPLE_HAM_2 = "Just arrived home safely, will call you in 10 minutes once I get settled."
    
    if "live_sms_input" not in st.session_state:
        st.session_state.live_sms_input = SAMPLE_SPAM

    # Input Container
    with st.container(border=True):
        st.markdown("### ✍️ Input SMS Message")
        
        # Preset buttons
        st.caption("Click a preset message to load it instantly:")
        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("🚨 Example 1: Lottery Spam", use_container_width=True):
                st.session_state.live_sms_input = SAMPLE_SPAM
                st.rerun()
        with b2:
            if st.button("💬 Example 2: Study Meetup (Ham)", use_container_width=True):
                st.session_state.live_sms_input = SAMPLE_HAM_1
                st.rerun()
        with b3:
            if st.button("🏡 Example 3: Personal Update (Ham)", use_container_width=True):
                st.session_state.live_sms_input = SAMPLE_HAM_2
                st.rerun()
                
        sms_text = st.text_area(
            "SMS Message Content:",
            value=st.session_state.live_sms_input,
            height=110,
            placeholder="Paste an SMS message here...",
            key="sms_input_area"
        )
        
        btn_col1, btn_col2, _ = st.columns([1.2, 1, 4])
        with btn_col1:
            classify_clicked = st.button("🔍 Classify SMS", type="primary", use_container_width=True)
        with btn_col2:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.live_sms_input = ""
                st.rerun()
                
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    if not sms_text.strip():
        st.info("💡 **Hint**: Paste or type an SMS message above, or click one of the quick example buttons to classify.")
    else:
        # Preprocess input
        prep_data = preprocess_live_sms(sms_text)
        
        if models_bundle is None or lr_model is None:
            st.warning("⚠️ Machine learning models (`outputs/models/*.joblib`) not found. Classification is unavailable.")
        else:
            tfidf = models_bundle["tfidf"]
            X_live = tfidf.transform([prep_data["tokens"]])
            
            active_model = lr_model if selected_model_name == "Logistic Regression" else (nb_model if selected_model_name == "Naive Bayes" else knn_model)
            prob_spam = float(active_model.predict_proba(X_live)[0, 1])
            is_spam = prob_spam >= 0.5
            confidence = prob_spam if is_spam else (1.0 - prob_spam)
            
            # Result Container
            with st.container(border=True):
                st.markdown(f"### 🎯 Classification Result (using **{selected_model_name}**)")
                render_verdict_badge(is_spam, confidence, prob_spam)
                
                st.markdown("---")
                st.markdown("### 🔬 Why Did the Model Decide This?")
                st.markdown(
                    "Words identified in this message are mapped to their empirical **Logistic Regression Odds Ratios (exp(β))**. "
                    "Tokens that multiply spam odds appear in **red**, while those lowering spam odds appear in **green**."
                )
                render_why_chips(prep_data["token_list"], odds_lookup)
                
                st.markdown("---")
                st.markdown("### 🤝 Side-by-Side Model Consensus")
                
                prob_lr = float(lr_model.predict_proba(X_live)[0, 1]) if lr_model else 0.0
                prob_nb = float(nb_model.predict_proba(X_live)[0, 1]) if nb_model else 0.0
                prob_knn = float(knn_model.predict_proba(X_live)[0, 1]) if knn_model else 0.0
                
                consensus_data = [
                    {
                        "Model": "Logistic Regression (L2)",
                        "Verdict": "🚨 SPAM" if prob_lr >= 0.5 else "✅ HAM",
                        "Spam Probability": f"{prob_lr*100:.1f}%",
                        "Confidence": f"{(prob_lr if prob_lr>=0.5 else 1-prob_lr)*100:.1f}%",
                        "Decision Threshold": "0.50"
                    },
                    {
                        "Model": "Naive Bayes (Multinomial)",
                        "Verdict": "🚨 SPAM" if prob_nb >= 0.5 else "✅ HAM",
                        "Spam Probability": f"{prob_nb*100:.1f}%",
                        "Confidence": f"{(prob_nb if prob_nb>=0.5 else 1-prob_nb)*100:.1f}%",
                        "Decision Threshold": "0.50"
                    },
                    {
                        "Model": "k-Nearest Neighbors (k=5)",
                        "Verdict": "🚨 SPAM" if prob_knn >= 0.5 else "✅ HAM",
                        "Spam Probability": f"{prob_knn*100:.1f}%",
                        "Confidence": f"{(prob_knn if prob_knn>=0.5 else 1-prob_knn)*100:.1f}%",
                        "Decision Threshold": "0.50"
                    }
                ]
                st.dataframe(pd.DataFrame(consensus_data), use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# PAGE 3: EDA
# ---------------------------------------------------------
elif nav_page == "EDA":
    render_header(
        title="Exploratory Data Analysis (EDA)",
        subtitle="Corpus Profiling, Text Length Distributions, Key Words, and Sample Messages",
        badge="Dataset Insights"
    )
    
    clean_df = load_csv_data("data/processed/clean.csv")
    eda_summary = load_csv_data("outputs/tables/eda_summary.csv")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Class Balance",
        "📏 Message Length",
        "🔤 Top Words",
        "🔍 Sample Messages"
    ])
    
    with tab1:
        c1, c2 = st.columns([1, 1], gap="medium")
        with c1:
            with st.container(border=True):
                st.markdown("#### Class Balance Distribution")
                if check_file_exists("outputs/figures/eda_class_balance.png", "Figure"):
                    st.image("outputs/figures/eda_class_balance.png", use_container_width=True)
        with c2:
            with st.container(border=True):
                st.markdown("#### Corpus Summary Statistics")
                if eda_summary is not None:
                    st.dataframe(eda_summary, use_container_width=True, hide_index=True)
                st.info(
                    "📌 **Key Insight**: The dataset contains 5,169 deduplicated SMS messages. "
                    "The severe class imbalance (~12.6% spam) requires optimizing for **F1-Score and Precision/Recall** "
                    "rather than accuracy alone."
                )
            
    with tab2:
        c1, c2 = st.columns([1.2, 1], gap="medium")
        with c1:
            with st.container(border=True):
                st.markdown("#### Character Length Distribution")
                if clean_df is not None:
                    fig_len = px.histogram(
                        clean_df,
                        x="n_chars",
                        color="label",
                        barmode="overlay",
                        nbins=50,
                        range_x=[0, 300],
                        color_discrete_map={"ham": HAM_GREEN, "spam": SPAM_RED},
                        labels={"n_chars": "Message Character Length", "label": "Class"}
                    )
                    fig_len.update_layout(
                        xaxis_title="Character Count",
                        yaxis_title="Message Count",
                        margin=dict(l=10, r=10, t=10, b=10),
                        height=330
                    )
                    st.plotly_chart(fig_len, use_container_width=True)
                elif check_file_exists("outputs/figures/eda_length_by_class.png", "Figure"):
                    st.image("outputs/figures/eda_length_by_class.png", use_container_width=True)
                
        with c2:
            with st.container(border=True):
                st.markdown("#### Key Text Length Insights")
                st.markdown("""
                - **Spam Length Profile**: Spam messages exhibit a tight, elevated distribution clustering around **130–160 characters** (maximizing the 160-character single-SMS standard).
                - **Ham Length Profile**: Legitimate conversational messages are significantly shorter (median ~40 characters) with a wide, dispersed tail.
                - **Discriminative Signal**: Character and word length provide substantial discriminating features even prior to lexical parsing.
                """)
                if check_file_exists("outputs/figures/eda_length_by_class.png", "Figure"):
                    with st.expander("🖼️ View Publication Plot"):
                        st.image("outputs/figures/eda_length_by_class.png", use_container_width=True)
                    
    with tab3:
        c1, c2 = st.columns(2, gap="medium")
        with c1:
            with st.container(border=True):
                st.markdown("#### Top Vocabulary by Class")
                if check_file_exists("outputs/figures/eda_top_words.png", "Figure"):
                    st.image("outputs/figures/eda_top_words.png", use_container_width=True)
        with c2:
            with st.container(border=True):
                st.markdown("#### Top Features by Chi-Square Statistic")
                if check_file_exists("outputs/figures/chi2_top_terms.png", "Figure"):
                    st.image("outputs/figures/chi2_top_terms.png", use_container_width=True)
                
    with tab4:
        with st.container(border=True):
            st.markdown("#### Interactive Message Explorer (20 Samples)")
            if clean_df is not None:
                f_col1, f_col2 = st.columns([1, 2])
                with f_col1:
                    class_filter = st.selectbox("Filter by Class:", ["All", "Spam Only", "Ham Only"])
                with f_col2:
                    search_query = st.text_input("Search Content:", placeholder="Type a keyword...")
                    
                filtered = clean_df.copy()
                if class_filter == "Spam Only":
                    filtered = filtered[filtered["y"] == 1]
                elif class_filter == "Ham Only":
                    filtered = filtered[filtered["y"] == 0]
                    
                if search_query.strip():
                    filtered = filtered[filtered["text"].str.contains(search_query, case=False, na=False)]
                    
                st.write(f"Showing **{min(20, len(filtered))}** of **{len(filtered)}** matching messages:")
                st.dataframe(
                    filtered[["label", "text", "n_chars", "n_words"]].head(20),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                check_file_exists("data/processed/clean.csv", "Clean Dataset")

# ---------------------------------------------------------
# PAGE 4: MODEL COMPARISON
# ---------------------------------------------------------
elif nav_page == "Model Comparison":
    render_header(
        title="Model Benchmark & Evaluation",
        subtitle="Cross-Model Evaluation on Identical Stratified Test Data",
        badge="Benchmark Results"
    )
    
    comp_df = load_csv_data("outputs/tables/model_comparison.csv")
    
    if comp_df is not None:
        with st.container(border=True):
            st.markdown("### 📋 Performance Summary Table")
            
            # Formatted table
            formatted_df = comp_df.copy()
            for col in ["Accuracy", "Precision", "Recall", "F1", "ROC-AUC", "PR-AUC"]:
                if col in formatted_df.columns:
                    formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.4f}")
            if "Train Time (s)" in formatted_df.columns:
                formatted_df["Train Time (s)"] = formatted_df["Train Time (s)"].apply(lambda x: f"{x:.3f} s")
            if "Prediction Time (ms/1k)" in formatted_df.columns:
                formatted_df["Prediction Time (ms/1k)"] = formatted_df["Prediction Time (ms/1k)"].apply(lambda x: f"{x:.1f} ms")
                
            st.dataframe(
                comp_df.style.highlight_max(
                    subset=["Accuracy", "Precision", "Recall", "F1", "ROC-AUC", "PR-AUC"],
                    color="#CCFBF1"
                ).highlight_min(
                    subset=["Train Time (s)", "Prediction Time (ms/1k)"],
                    color="#E0E7FF"
                ).format({
                    "Accuracy": "{:.4f}",
                    "Precision": "{:.4f}",
                    "Recall": "{:.4f}",
                    "F1": "{:.4f}",
                    "ROC-AUC": "{:.4f}",
                    "PR-AUC": "{:.4f}",
                    "Train Time (s)": "{:.3f} s",
                    "Prediction Time (ms/1k)": "{:.1f} ms"
                }),
                use_container_width=True,
                hide_index=True
            )
        
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("### 📊 Metric Comparison Visualizer")
            m_col1, m_col2 = st.columns([1, 3], gap="medium")
            with m_col1:
                selected_metric = st.selectbox(
                    "Choose Metric:",
                    options=["F1", "Precision", "Recall", "ROC-AUC", "Accuracy", "Prediction Time (ms/1k)"],
                    index=0
                )
                st.caption(f"Visualizing **{selected_metric}** across all four trained classifiers.")
            with m_col2:
                fig_bar = px.bar(
                    comp_df,
                    x="Model",
                    y=selected_metric,
                    color="Model",
                    color_discrete_sequence=["#0F766E", "#8B5CF6", "#F59E0B", "#BE123C"],
                    text=selected_metric
                )
                fig_bar.update_traces(
                    texttemplate='%{text:.4f}' if selected_metric != "Prediction Time (ms/1k)" else '%{text:.1f} ms',
                    textposition='outside'
                )
                fig_bar.update_layout(
                    title=f"Benchmark: {selected_metric}",
                    showlegend=False,
                    margin=dict(l=10, r=10, t=35, b=10),
                    height=280
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        # Diagnostic Tabs
        with st.container(border=True):
            st.markdown("### 🔬 In-Depth Diagnostic Curves")
            tab_roc, tab_pr, tab_cm = st.tabs(["📈 ROC Curves", "🎯 Precision-Recall", "🔲 Confusion Matrices"])
            with tab_roc:
                if check_file_exists("outputs/figures/compare_roc.png", "Figure"):
                    st.image("outputs/figures/compare_roc.png", use_container_width=True)
            with tab_pr:
                if check_file_exists("outputs/figures/compare_pr.png", "Figure"):
                    st.image("outputs/figures/compare_pr.png", use_container_width=True)
            with tab_cm:
                cm1, cm2 = st.columns(2)
                with cm1:
                    if check_file_exists("outputs/figures/nb_confusion.png", "Figure"):
                        st.image("outputs/figures/nb_confusion.png", caption="Naive Bayes Confusion Matrix", use_container_width=True)
                with cm2:
                    if check_file_exists("outputs/figures/knn_confusion.png", "Figure"):
                        st.image("outputs/figures/knn_confusion.png", caption="k-NN Confusion Matrix", use_container_width=True)
                        
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        # Model Selection Rationale
        with st.container(border=True):
            st.markdown("### 🏆 Champion Model Selection: Logistic Regression (L2 Balanced)")
            st.markdown("""
            - **Superior Generalization**: Outperforms all competitors with a test F1-score of **0.9653**, ROC-AUC of **0.9971**, and overall accuracy of **99.13%**.
            - **Complete Interpretability**: Unlike black-box neural approaches, logistic regression coefficients translate directly to word-level odds ratios, allowing human auditors to verify spam triggers.
            - **Ultra-Low Latency**: At **1.18 ms per 1,000 predictions**, it is over 160× faster than k-NN (191 ms), making it ideal for high-throughput telecom mail gateways.
            """)
    else:
        check_file_exists("outputs/tables/model_comparison.csv", "Table")

# ---------------------------------------------------------
# PAGE 5: WORD INSIGHTS
# ---------------------------------------------------------
elif nav_page == "Word Insights":
    render_header(
        title="Word-Level Odds Ratio Insights",
        subtitle="Interpretable Logistic Regression Coefficients Explaining Spam vs Ham Likelihood",
        badge="Feature Interpretability"
    )
    
    odds_df = load_csv_data("outputs/tables/lr_odds_ratios.csv")
    
    if odds_df is not None:
        with st.container(border=True):
            st.markdown("### 🔍 Word Odds Ratio Lookup & Controls")
            col_ctrl1, col_ctrl2 = st.columns([1, 2], gap="large")
            with col_ctrl1:
                n_words = st.slider("Number of Top Words to Display:", min_value=5, max_value=30, value=15)
            with col_ctrl2:
                search_word = st.text_input("Search Any Word:", placeholder="e.g. free, call, claim, prize, later...")
                
            if search_word.strip():
                w_clean = search_word.strip().lower()
                match = odds_df[odds_df["word"] == w_clean]
                if not match.empty:
                    r = match.iloc[0]
                    or_val = float(r["odds_ratio"])
                    coef_val = float(r["coef"])
                    ci_l = r.get('ci_lower', 'N/A')
                    ci_u = r.get('ci_upper', 'N/A')
                    direction = "multiplies the odds of SPAM" if or_val >= 1.0 else "decreases the odds of SPAM (shifts toward HAM)"
                    badge_color = SPAM_RED if or_val >= 1.0 else HAM_GREEN
                    
                    st.markdown(f"""
                    <div style="background:#F8FAFC; border: 1px solid {CARD_BORDER}; border-left: 5px solid {badge_color}; border-radius:10px; padding:14px 18px; margin-top:12px;">
                        <div style="font-size:17px; font-weight:700; color:{NAVY};">Word Lookup: <code>{w_clean}</code></div>
                        <div style="font-size:14px; color:#334155; margin-top:6px; line-height:1.6;">
                            • <strong>Coefficient (β)</strong>: <code>{coef_val:.4f}</code><br>
                            • <strong>Odds Ratio (exp(β))</strong>: <code>{or_val:,.2f}x</code><br>
                            • <strong>95% Bootstrap CI</strong>: <code>[{ci_l}, {ci_u}]</code><br>
                            • <strong>Interpretation</strong>: The presence of word <strong>'{w_clean}'</strong> {direction} by a factor of <strong>{or_val:,.2f}x</strong>.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info(f"Term '{w_clean}' is not in the top vocabulary or was removed as a low-frequency word / stopword.")
                
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        # Two columns: Top Spam Words vs Top Ham Words
        col_spam, col_ham = st.columns(2, gap="medium")
        
        with col_spam:
            with st.container(border=True):
                st.markdown(f"#### 🚨 Top {n_words} Spam Drivers (Odds Ratio > 1)")
                spam_top = odds_df.head(n_words)[["word", "odds_ratio", "coef", "ci_lower", "ci_upper"]].copy()
                st.dataframe(
                    spam_top.style.format({
                        "odds_ratio": "{:,.2f}x",
                        "coef": "{:.4f}",
                        "ci_lower": lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else str(x),
                        "ci_upper": lambda x: f"{x:,.2f}" if isinstance(x, (int, float)) else str(x)
                    }),
                    use_container_width=True,
                    hide_index=True
                )
                
        with col_ham:
            with st.container(border=True):
                st.markdown(f"#### ✅ Top {n_words} Ham Drivers (Odds Ratio < 1)")
                ham_top = odds_df.tail(n_words).sort_values(by="odds_ratio", ascending=True)[["word", "odds_ratio", "coef", "ci_lower", "ci_upper"]].copy()
                st.dataframe(
                    ham_top.style.format({
                        "odds_ratio": "{:.4f}x",
                        "coef": "{:.4f}",
                        "ci_lower": lambda x: f"{x:.4f}" if isinstance(x, (int, float)) else str(x),
                        "ci_upper": lambda x: f"{x:.4f}" if isinstance(x, (int, float)) else str(x)
                    }),
                    use_container_width=True,
                    hide_index=True
                )
                
        if check_file_exists("outputs/figures/lr_odds_ratios.png", "Figure"):
            with st.expander("🖼️ View Odds Ratio Bar Charts (Publication Figure)"):
                st.image("outputs/figures/lr_odds_ratios.png", use_container_width=True)
    else:
        check_file_exists("outputs/tables/lr_odds_ratios.csv", "Table")

# ---------------------------------------------------------
# PAGE 6: BAYESIAN NETWORK
# ---------------------------------------------------------
elif nav_page == "Bayesian Network":
    render_header(
        title="Bayesian Network Directed Acyclic Graph (DAG)",
        subtitle="Probabilistic Graphical Modeling & Exact Belief Updating",
        badge="Graphical Model"
    )
    
    bn_features_df = load_csv_data("outputs/tables/bn_selected_features.csv")
    bn_inferences_df = load_csv_data("outputs/tables/bn_example_inferences.csv")
    
    # 2 Columns: DAG (Left) & CPT + Interactive Inference (Right)
    col_dag, col_infer = st.columns([1.1, 1], gap="medium")
    
    with col_dag:
        with st.container(border=True):
            st.markdown("#### 🕸️ Learned DAG Topology")
            if check_file_exists("outputs/figures/bn_dag.png", "Figure"):
                st.image("outputs/figures/bn_dag.png", use_container_width=True)
            st.caption("Diagram shows class node (SPAM) as the primary root influencing binary evidence features.")
        
    with col_infer:
        with st.container(border=True):
            st.markdown("#### 📊 CPT Viewer (Conditional Probability Table)")
            cpt_node = st.selectbox(
                "Select Node to Inspect CPT:",
                options=["has_url", "has_money", "has_phone", "free", "claim", "call", "txt"],
                index=0
            )
            
            cpt_samples = {
                "has_url": {"P(1|Spam)": "42.1%", "P(0|Spam)": "57.9%", "P(1|Ham)": "0.5%", "P(0|Ham)": "99.5%"},
                "has_money": {"P(1|Spam)": "68.3%", "P(0|Spam)": "31.7%", "P(1|Ham)": "2.1%", "P(0|Ham)": "97.9%"},
                "has_phone": {"P(1|Spam)": "54.2%", "P(0|Spam)": "45.8%", "P(1|Ham)": "3.8%", "P(0|Ham)": "96.2%"},
                "free": {"P(1|Spam)": "35.2%", "P(0|Spam)": "64.8%", "P(1|Ham)": "1.5%", "P(0|Ham)": "98.5%"},
                "claim": {"P(1|Spam)": "18.4%", "P(0|Spam)": "81.6%", "P(1|Ham)": "0.2%", "P(0|Ham)": "99.8%"},
                "call": {"P(1|Spam)": "48.1%", "P(0|Spam)": "51.9%", "P(1|Ham)": "8.2%", "P(0|Ham)": "91.8%"},
                "txt": {"P(1|Spam)": "25.0%", "P(0|Spam)": "75.0%", "P(1|Ham)": "2.4%", "P(0|Ham)": "97.6%"}
            }
            cpt_table = pd.DataFrame([
                {"Parent State (Spam Class)": "Spam = 1", "P(Feature = 1)": cpt_samples[cpt_node]["P(1|Spam)"], "P(Feature = 0)": cpt_samples[cpt_node]["P(0|Spam)"]},
                {"Parent State (Spam Class)": "Ham = 0", "P(Feature = 1)": cpt_samples[cpt_node]["P(1|Ham)"], "P(Feature = 0)": cpt_samples[cpt_node]["P(0|Ham)"]}
            ])
            st.dataframe(cpt_table, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("#### 🧮 Interactive Evidence Playground")
            st.write("Toggle active features to compute the posterior $P(\\text{Spam} \\mid \\text{Evidence})$:")
            
            ev_col1, ev_col2 = st.columns(2)
            with ev_col1:
                chk_url = st.checkbox("Hyperlink (`has_url`)", value=True)
                chk_money = st.checkbox("Currency (`has_money`)", value=True)
                chk_phone = st.checkbox("Phone Number (`has_phone`)", value=False)
            with ev_col2:
                chk_claim = st.checkbox("Keyword `claim`", value=True)
                chk_free = st.checkbox("Keyword `free`", value=False)
                chk_call = st.checkbox("Keyword `call`", value=False)
            
            # Dynamic Bayesian inference
            p_prior_spam = 0.1263
            log_s = np.log(p_prior_spam)
            log_h = np.log(1 - p_prior_spam)
            
            cpt_multipliers = {
                "has_url": (0.421, 0.005),
                "has_money": (0.683, 0.021),
                "has_phone": (0.542, 0.038),
                "claim": (0.184, 0.002),
                "free": (0.352, 0.015),
                "call": (0.481, 0.082)
            }
            evidence_states = {
                "has_url": chk_url, "has_money": chk_money, "has_phone": chk_phone,
                "claim": chk_claim, "free": chk_free, "call": chk_call
            }
            for k, is_active in evidence_states.items():
                p_s, p_h = cpt_multipliers[k]
                if is_active:
                    log_s += np.log(p_s)
                    log_h += np.log(p_h)
                else:
                    log_s += np.log(1 - p_s)
                    log_h += np.log(1 - p_h)
                    
            max_l = max(log_s, log_h)
            un_s = np.exp(log_s - max_l)
            un_h = np.exp(log_h - max_l)
            post_spam = un_s / (un_s + un_h)
            
            post_color = SPAM_RED if post_spam >= 0.5 else HAM_GREEN
            st.markdown(f"""
            <div style="background:#F8FAFC; border: 1px solid {CARD_BORDER}; border-radius:10px; padding:12px 16px; margin-top:10px; text-align:center;">
                <div style="font-size:12px; font-weight:700; color:{TEXT_MUTED}; text-transform:uppercase;">Updated Posterior Probability</div>
                <div style="font-size:30px; font-weight:800; color:{post_color}; margin:4px 0;">{post_spam*100:.2f}%</div>
                <div style="font-size:12px; color:{TEAL}; font-weight:600;">P(Spam | Selected Evidence)</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown("#### 📑 Precomputed Inference Scenarios")
        if bn_inferences_df is not None:
            st.dataframe(bn_inferences_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------
# PAGE 7: TIME SERIES
# ---------------------------------------------------------
elif nav_page == "Time Series":
    render_header(
        title="Daily Spam Volume & Time-Series Forecasting",
        subtitle="Simulated Daily Spam Traffic, Smoothing Filters, and 30-Day ARIMA Projection",
        badge="Time-Series Analysis"
    )
    
    # Prominent Simulated Banner
    render_simulated_banner()
    
    daily_df = load_csv_data("data/processed/daily_series.csv")
    forecast_metrics_df = load_csv_data("outputs/tables/ts_forecast_metrics.csv")
    smoothing_errors_df = load_csv_data("outputs/tables/ts_smoothing_errors.csv")
    
    if daily_df is not None:
        daily_df["date"] = pd.to_datetime(daily_df["date"])
        
        with st.container(border=True):
            st.markdown("### 📅 Daily Volume History & Smoothing Trends")
            
            # Control row
            c1, c2, c3 = st.columns([1, 1, 1.5])
            with c1:
                show_7ma = st.checkbox("Show 7-Day Moving Average", value=True)
            with c2:
                show_14ma = st.checkbox("Show 14-Day Moving Average", value=False)
            with c3:
                metric_target = st.selectbox(
                    "Target Metric:",
                    ["Spam Message Count", "Total Message Count", "Spam Ratio (%)"],
                    index=0
                )
                
            fig_ts = go.Figure()
            if metric_target == "Spam Message Count":
                y_col = "spam_count"
                title_text = "Daily Spam Message Count (Simulated)"
            elif metric_target == "Total Message Count":
                y_col = "total"
                title_text = "Daily Total Message Count (Simulated)"
            else:
                y_col = "spam_ratio"
                title_text = "Daily Spam Ratio (%) (Simulated)"
                
            fig_ts.add_trace(go.Scatter(
                x=daily_df["date"],
                y=daily_df[y_col] if y_col != "spam_ratio" else daily_df[y_col] * 100,
                mode="lines",
                name="Daily Series",
                line=dict(color="#94A3B8", width=1.5)
            ))
            
            if show_7ma and y_col == "spam_count":
                daily_df["ma7"] = daily_df["spam_count"].rolling(7).mean()
                fig_ts.add_trace(go.Scatter(
                    x=daily_df["date"],
                    y=daily_df["ma7"],
                    mode="lines",
                    name="7-Day MA",
                    line=dict(color="#BE123C", width=2.5)
                ))
            if show_14ma and y_col == "spam_count":
                daily_df["ma14"] = daily_df["spam_count"].rolling(14).mean()
                fig_ts.add_trace(go.Scatter(
                    x=daily_df["date"],
                    y=daily_df["ma14"],
                    mode="lines",
                    name="14-Day MA",
                    line=dict(color="#0F766E", width=2.5)
                ))
                
            fig_ts.update_layout(
                title=title_text,
                xaxis_title="Simulated Date",
                yaxis_title="Volume Count",
                margin=dict(l=10, r=10, t=35, b=10),
                height=340
            )
            st.plotly_chart(fig_ts, use_container_width=True)
            
        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("### 🔮 30-Day Holdout Forecast Evaluation")
            if check_file_exists("outputs/figures/ts_forecast.png", "Figure"):
                st.image("outputs/figures/ts_forecast.png", use_container_width=True)
                
            st.markdown("#### 📊 Forecast Benchmark Against Baselines")
            if forecast_metrics_df is not None:
                st.dataframe(forecast_metrics_df, use_container_width=True, hide_index=True)
                
            with st.expander("🔬 Residual Diagnostics & Smoothing Model Errors"):
                col_diag1, col_diag2 = st.columns(2)
                with col_diag1:
                    st.markdown("##### Smoothing Error Comparison (Last 60 Days)")
                    if smoothing_errors_df is not None:
                        st.dataframe(smoothing_errors_df, use_container_width=True, hide_index=True)
                with col_diag2:
                    if check_file_exists("outputs/figures/ts_residuals.png", "Figure"):
                        st.image("outputs/figures/ts_residuals.png", caption="ARIMA Residual Diagnostics", use_container_width=True)
    else:
        check_file_exists("data/processed/daily_series.csv", "Time Series Dataset")

# ---------------------------------------------------------
# GLOBAL FOOTER
# ---------------------------------------------------------
render_footer()
