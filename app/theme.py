import streamlit as st

# Color Palette Tokens
NAVY = "#1F2A44"
TEAL = "#0F766E"
TEAL_LIGHT = "#CCFBF1"
SPAM_RED = "#BE123C"
SPAM_BG = "#FFE4E6"
HAM_GREEN = "#15803D"
HAM_BG = "#DCFCE7"
AMBER = "#B45309"
AMBER_BG = "#FEF3C7"
CARD_BG = "#FFFFFF"
CARD_BORDER = "#E2E8F0"
TEXT_PRIMARY = "#0F172A"
TEXT_MUTED = "#64748B"

def apply_custom_css():
    """Injects premium styling, typography, card layout, and component tokens."""
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    
    /* Global Container Spacing */
    .block-container {{
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        max-width: 1400px;
    }}

    /* Streamlit Bordered Container Overrides */
    [data-testid="stVerticalBlockBorderWrapper"] > div {{
        border-radius: 12px !important;
        border: 1px solid {CARD_BORDER} !important;
        background: {CARD_BG} !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        padding: 22px !important;
    }}
    
    /* Top Header Bar */
    .header-bar {{
        background: linear-gradient(135deg, {NAVY} 0%, #0F172A 100%);
        border-radius: 14px;
        padding: 22px 28px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 15px -1px rgba(0, 0, 0, 0.08), 0 2px 6px -2px rgba(0, 0, 0, 0.04);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }}
    .header-title-box h1 {{
        color: white !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 0 !important;
        letter-spacing: -0.02em;
    }}
    .header-subtitle {{
        color: #94A3B8;
        font-size: 14px;
        margin-top: 4px;
        font-weight: 400;
    }}
    .header-badge {{
        background: rgba(15, 118, 110, 0.25);
        color: #5EEAD4;
        border: 1px solid rgba(94, 234, 212, 0.4);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }}

    /* Card Component */
    .metric-card {{
        background: {CARD_BG};
        border: 1px solid {CARD_BORDER};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.07);
    }}
    .metric-title {{
        color: {TEXT_MUTED};
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }}
    .metric-value {{
        color: {NAVY};
        font-size: 28px;
        font-weight: 800;
        line-height: 1.1;
    }}
    .metric-subtitle {{
        color: {TEAL};
        font-size: 12px;
        font-weight: 500;
        margin-top: 6px;
    }}

    /* Pipeline Strip */
    .pipeline-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 14px;
        margin-top: 16px;
        margin-bottom: 24px;
    }}
    .pipeline-step {{
        background: #FFFFFF;
        border: 1px solid {CARD_BORDER};
        border-top: 4px solid {TEAL};
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        transition: transform 0.15s ease;
    }}
    .pipeline-step:hover {{
        transform: translateY(-2px);
    }}
    .pipeline-step-num {{
        font-size: 11px;
        font-weight: 700;
        color: {TEAL};
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }}
    .pipeline-step-name {{
        font-size: 16px;
        font-weight: 700;
        color: {NAVY};
        margin-top: 4px;
    }}
    .pipeline-step-desc {{
        font-size: 12px;
        color: {TEXT_MUTED};
        margin-top: 6px;
        line-height: 1.4;
    }}

    /* Verdict Badges */
    .badge-spam {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: {SPAM_BG};
        color: {SPAM_RED};
        border: 2px solid {SPAM_RED};
        padding: 10px 24px;
        border-radius: 12px;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 0.04em;
    }}
    .badge-ham {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: {HAM_BG};
        color: {HAM_GREEN};
        border: 2px solid {HAM_GREEN};
        padding: 10px 24px;
        border-radius: 12px;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 0.04em;
    }}

    /* Word Chips */
    .word-chip {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
    }}
    .word-chip-spam {{
        background-color: {SPAM_BG};
        color: {SPAM_RED};
        border: 1px solid rgba(190, 18, 60, 0.35);
    }}
    .word-chip-ham {{
        background-color: {HAM_BG};
        color: {HAM_GREEN};
        border: 1px solid rgba(21, 128, 61, 0.35);
    }}
    .word-chip-neutral {{
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #CBD5E1;
    }}

    /* Tabs Styling */
    div[data-testid="stTabs"] button[role="tab"] {{
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 20px !important;
        border-radius: 8px 8px 0 0 !important;
    }}
    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: {TEAL} !important;
        border-bottom: 3px solid {TEAL} !important;
    }}

    /* Buttons */
    button[kind="primary"] {{
        background-color: {TEAL} !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }}

    /* Simulated Alert Banner */
    .simulated-banner {{
        background-color: {AMBER_BG};
        border: 1px solid {AMBER};
        border-left: 5px solid {AMBER};
        border-radius: 10px;
        padding: 14px 20px;
        color: #78350F;
        font-size: 14px;
        font-weight: 500;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    /* Footer */
    .app-footer {{
        border-top: 1px solid {CARD_BORDER};
        margin-top: 48px;
        padding-top: 24px;
        text-align: center;
        color: {TEXT_MUTED};
        font-size: 13px;
        line-height: 1.6;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
