"""
Hassan Traders CRM — Production Build v3.0 Dark Edition
=========================================================
✅ Dark Mode — Full Premium Dark Theme
✅ Beautiful animated UI with glassmorphism accents
✅ All original modules preserved & enhanced
✅ Receipts & Payments with credit/debit management
✅ Advance Sales with full payment tracking
✅ Customer balance auto-sync across all modules
✅ POS → Stock → Ledger → CRM fully interlinked
✅ Daily download (Excel + CSV)
✅ Auto-cleanup with 3-day rolling archive
✅ HRM, Livestock, Finance, Inventory, Production
✅ Enhanced Dashboard with real-time KPIs
✅ Full inter-module data linkage
"""

import streamlit as st
import pandas as pd
import json, os, hashlib, uuid, io
from datetime import datetime, date, timedelta
from io import BytesIO
import base64

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hassan Traders",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS — FULL DARK MODE PREMIUM THEME ─────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ══════════════════════════════════════
   DARK MODE — FULL FORCE OVERRIDE
═══════════════════════════════════════ */
html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
    color-scheme: dark !important;
    background-color: #0D0F14 !important;
    color: #E2E8F0 !important;
}
[data-testid="stApp"]            { background: #0D0F14 !important; }
[data-testid="stAppViewContainer"]{ background: #0D0F14 !important; }
.main .block-container {
    background: #0D0F14 !important;
    padding: 1.5rem 2rem 2rem !important;
    max-width: 100% !important;
}

/* ── Base Typography ── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: #E2E8F0 !important;
}

/* ── Streamlit default text overrides ── */
p, span, label, div, h1, h2, h3, h4, h5, h6, li, td, th {
    color: #E2E8F0 !important;
}
.stMarkdown p { color: #CBD5E1 !important; }

/* ══════════════════════════════════════
   SIDEBAR — DEEP DARK NAVY
═══════════════════════════════════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080A12 0%, #0A0D18 40%, #0D1020 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.15) !important;
    min-width: 248px !important;
    box-shadow: 4px 0 32px rgba(0,0,0,0.5);
}
section[data-testid="stSidebar"] * { color: #94A3B8 !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: none !important;
    color: #94A3B8 !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    padding: 7px 14px !important;
    text-align: left !important;
    border-radius: 8px !important;
    transition: all 0.18s ease !important;
    width: 100%;
    margin: 1px 0;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(99,102,241,0.15) !important;
    color: #C7D2FE !important;
    padding-left: 20px !important;
    border-left: 2px solid #6366F1 !important;
}
section[data-testid="stSidebar"] .stExpander {
    border: none !important;
    background: transparent !important;
}
section[data-testid="stSidebar"] .stExpander summary {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    font-size: 11.5px !important;
    font-weight: 700 !important;
    letter-spacing: 0.7px !important;
    color: #6366F1 !important;
    border: 1px solid rgba(99,102,241,0.12) !important;
    text-transform: uppercase !important;
}
section[data-testid="stSidebar"] .stExpander summary:hover {
    background: rgba(99,102,241,0.1) !important;
}

/* ══════════════════════════════════════
   SECTION HEADER
═══════════════════════════════════════ */
.ht-section-header {
    display: flex;
    align-items: center;
    gap: 14px;
    background: linear-gradient(135deg, #13151F 0%, #161B2E 100%);
    border-radius: 16px;
    padding: 18px 26px;
    margin-bottom: 22px;
    border: 1px solid rgba(99,102,241,0.2);
    border-left: 4px solid #6366F1;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), 0 0 0 1px rgba(99,102,241,0.05);
    animation: slideDown 0.35s ease;
}
.ht-section-header h1 {
    font-size: 1.4rem;
    font-weight: 800;
    color: #F1F5F9 !important;
    margin: 0;
    background: linear-gradient(135deg, #E2E8F0, #A5B4FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.ht-section-icon { font-size: 1.6rem; }

/* ══════════════════════════════════════
   METRIC CARDS — GLASSMORPHISM
═══════════════════════════════════════ */
.metric-grid { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 18px; }
.metric-card {
    background: linear-gradient(135deg, #13151F 0%, #161B2E 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 18px 20px;
    flex: 1;
    min-width: 130px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    transition: all 0.25s ease;
    animation: fadeUp 0.4s ease both;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366F1, #8B5CF6);
    border-radius: 16px 16px 0 0;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at top left, rgba(99,102,241,0.06) 0%, transparent 60%);
    pointer-events: none;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.2);
    border-color: rgba(99,102,241,0.3);
}
.metric-card .mc-value {
    font-size: 1.55rem;
    font-weight: 800;
    color: #F1F5F9 !important;
    line-height: 1;
    margin-bottom: 7px;
}
.metric-card .mc-label {
    font-size: 0.69rem;
    font-weight: 600;
    color: #64748B !important;
    text-transform: uppercase;
    letter-spacing: 0.9px;
}
.metric-card.green::before  { background: linear-gradient(90deg, #10B981, #34D399); }
.metric-card.red::before    { background: linear-gradient(90deg, #EF4444, #F87171); }
.metric-card.amber::before  { background: linear-gradient(90deg, #F59E0B, #FCD34D); }
.metric-card.purple::before { background: linear-gradient(90deg, #8B5CF6, #A78BFA); }
.metric-card.blue::before   { background: linear-gradient(90deg, #3B82F6, #60A5FA); }

/* ══════════════════════════════════════
   MAIN BUTTONS
═══════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 9px 22px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 10px rgba(99,102,241,0.3) !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4338CA, #4F46E5) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(99,102,241,0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ══════════════════════════════════════
   FORMS & INPUTS
═══════════════════════════════════════ */
.stForm {
    background: #13151F !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    padding: 20px !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input {
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    background: #1A1D2E !important;
    color: #E2E8F0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13.5px !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
    caret-color: #6366F1 !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.18) !important;
    background: #1E2236 !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #475569 !important;
}
.stSelectbox > div > div,
.stSelectbox > div > div > div {
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    background: #1A1D2E !important;
    color: #E2E8F0 !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.18) !important;
}
/* Selectbox dropdown options */
[data-baseweb="select"] > div { background: #1A1D2E !important; }
[data-baseweb="menu"] { background: #1A1D2E !important; border: 1px solid rgba(99,102,241,0.2) !important; }
[data-baseweb="option"] { background: #1A1D2E !important; color: #E2E8F0 !important; }
[data-baseweb="option"]:hover { background: rgba(99,102,241,0.2) !important; }
/* Labels */
label, .stTextInput label, .stSelectbox label,
.stNumberInput label, .stDateInput label,
.stTextArea label, .stCheckbox label,
.stRadio label, [data-testid="stWidgetLabel"] {
    color: #94A3B8 !important;
    font-size: 12.5px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
}

/* ══════════════════════════════════════
   TABS
═══════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: #13151F !important;
    border-radius: 12px !important;
    padding: 5px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #64748B !important;
    padding: 8px 20px !important;
    transition: all 0.18s !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4F46E5, #6366F1) !important;
    color: #FFFFFF !important;
    box-shadow: 0 2px 12px rgba(99,102,241,0.35) !important;
}
.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    background: rgba(99,102,241,0.1) !important;
    color: #A5B4FC !important;
}

/* ══════════════════════════════════════
   DATAFRAME / TABLE
═══════════════════════════════════════ */
.stDataFrame {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}
[data-testid="stDataFrame"] {
    background: #13151F !important;
}
[data-testid="stDataFrame"] th {
    background: #1A1D2E !important;
    font-weight: 700 !important;
    font-size: 11.5px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
    color: #6366F1 !important;
    border-bottom: 1px solid rgba(99,102,241,0.2) !important;
    padding: 10px 12px !important;
}
[data-testid="stDataFrame"] td {
    background: #13151F !important;
    color: #CBD5E1 !important;
    font-size: 13px !important;
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    padding: 8px 12px !important;
}
[data-testid="stDataFrame"] tr:hover td {
    background: rgba(99,102,241,0.08) !important;
}

/* ══════════════════════════════════════
   ALERTS / MESSAGES
═══════════════════════════════════════ */
.stAlert { border-radius: 12px !important; }
div[data-testid="stSuccessMessage"],
div[data-testid="stErrorMessage"],
div[data-testid="stWarningMessage"],
div[data-testid="stInfoMessage"] {
    border-radius: 12px !important;
}
/* success */
div[data-testid="stSuccessMessage"] {
    background: rgba(16,185,129,0.12) !important;
    border: 1px solid rgba(16,185,129,0.25) !important;
    color: #6EE7B7 !important;
}
/* error */
div[data-testid="stErrorMessage"] {
    background: rgba(239,68,68,0.12) !important;
    border: 1px solid rgba(239,68,68,0.25) !important;
    color: #FCA5A5 !important;
}
/* warning */
div[data-testid="stWarningMessage"] {
    background: rgba(245,158,11,0.12) !important;
    border: 1px solid rgba(245,158,11,0.25) !important;
    color: #FCD34D !important;
}
/* info */
div[data-testid="stInfoMessage"] {
    background: rgba(99,102,241,0.12) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    color: #A5B4FC !important;
}

/* ══════════════════════════════════════
   BADGES
═══════════════════════════════════════ */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11.5px;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.badge-green  { background: rgba(16,185,129,0.15);  color: #6EE7B7; border: 1px solid rgba(16,185,129,0.2); }
.badge-red    { background: rgba(239,68,68,0.15);   color: #FCA5A5; border: 1px solid rgba(239,68,68,0.2); }
.badge-amber  { background: rgba(245,158,11,0.15);  color: #FCD34D; border: 1px solid rgba(245,158,11,0.2); }
.badge-blue   { background: rgba(59,130,246,0.15);  color: #93C5FD; border: 1px solid rgba(59,130,246,0.2); }
.badge-purple { background: rgba(139,92,246,0.15);  color: #C4B5FD; border: 1px solid rgba(139,92,246,0.2); }

/* ══════════════════════════════════════
   INFO PANELS
═══════════════════════════════════════ */
.info-panel {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.22);
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 16px;
    font-size: 13.5px;
    color: #A5B4FC !important;
}
.info-panel.green {
    background: rgba(16,185,129,0.08);
    border-color: rgba(16,185,129,0.22);
    color: #6EE7B7 !important;
}
.info-panel.amber {
    background: rgba(245,158,11,0.08);
    border-color: rgba(245,158,11,0.22);
    color: #FCD34D !important;
}
.info-panel.red {
    background: rgba(239,68,68,0.08);
    border-color: rgba(239,68,68,0.22);
    color: #FCA5A5 !important;
}

/* ══════════════════════════════════════
   DOWNLOAD BUTTON
═══════════════════════════════════════ */
.dl-btn a {
    background: linear-gradient(135deg, #059669, #047857) !important;
    color: #FFF !important;
    padding: 9px 22px !important;
    border-radius: 10px !important;
    text-decoration: none !important;
    font-weight: 600 !important;
    display: inline-block;
    margin: 4px 4px 4px 0;
    font-size: 13px;
    box-shadow: 0 2px 10px rgba(5,150,105,0.3);
    transition: all 0.2s;
    border: 1px solid rgba(16,185,129,0.3);
}
.dl-btn a:hover { opacity: 0.88; transform: translateY(-1px); }

/* ══════════════════════════════════════
   LOGIN PAGE
═══════════════════════════════════════ */
.login-container {
    background: linear-gradient(135deg, #13151F 0%, #161B2E 100%);
    border-radius: 24px;
    padding: 50px 44px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 0 1px rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.12);
    animation: fadeUp 0.5s ease;
    backdrop-filter: blur(20px);
}
.login-logo {
    font-size: 4rem;
    text-align: center;
    margin-bottom: 10px;
    animation: bounce 2s ease infinite;
    filter: drop-shadow(0 0 20px rgba(99,102,241,0.4));
}
.login-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #A5B4FC, #818CF8, #6366F1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.login-subtitle {
    text-align: center;
    color: #475569 !important;
    font-size: 13.5px;
    margin-bottom: 32px;
}

/* ══════════════════════════════════════
   RECEIPT CARD
═══════════════════════════════════════ */
.receipt-card {
    background: #13151F;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.07);
    padding: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

/* ══════════════════════════════════════
   EXPANDERS
═══════════════════════════════════════ */
.streamlit-expanderHeader,
[data-testid="stExpander"] summary {
    background: #13151F !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    color: #CBD5E1 !important;
    font-weight: 600 !important;
}
[data-testid="stExpander"] summary:hover {
    background: #1A1D2E !important;
    border-color: rgba(99,102,241,0.3) !important;
}
[data-testid="stExpander"] > div > div {
    background: #13151F !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ══════════════════════════════════════
   METRICS (native streamlit)
═══════════════════════════════════════ */
[data-testid="stMetric"] {
    background: #13151F !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 16px !important;
}
[data-testid="stMetricLabel"]  { color: #64748B !important; }
[data-testid="stMetricValue"]  { color: #F1F5F9 !important; }
[data-testid="stMetricDelta"]  { color: #10B981 !important; }

/* ══════════════════════════════════════
   CHECKBOXES & RADIO
═══════════════════════════════════════ */
.stCheckbox > label, .stRadio > label { color: #94A3B8 !important; }
.stCheckbox [data-testid="stCheckbox"] > div { background: #1A1D2E !important; border-color: rgba(99,102,241,0.4) !important; }

/* ══════════════════════════════════════
   DIVIDERS
═══════════════════════════════════════ */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* ══════════════════════════════════════
   CHARTS
═══════════════════════════════════════ */
[data-testid="stArrowVegaLiteChart"],
[data-testid="stVegaLiteChart"] {
    background: transparent !important;
}

/* ══════════════════════════════════════
   ANIMATIONS
═══════════════════════════════════════ */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes slideDown {
    from { opacity: 0; transform: translateY(-12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes bounce {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-10px); }
}
@keyframes pulse {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.55; }
}
@keyframes glowPulse {
    0%,100% { box-shadow: 0 0 10px rgba(99,102,241,0.15); }
    50%      { box-shadow: 0 0 25px rgba(99,102,241,0.4); }
}

/* ══════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════ */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0D0F14; }
::-webkit-scrollbar-thumb { background: #1E2337; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2D3456; }

/* ══════════════════════════════════════
   MOBILE RESPONSIVE
═══════════════════════════════════════ */
@media (max-width: 768px) {
    .metric-card { min-width: 140px; }
    .metric-card .mc-value { font-size: 1.2rem; }
    .main .block-container { padding: 1rem !important; }
    section[data-testid="stSidebar"] { min-width: 200px !important; }
}

/* ══════════════════════════════════════
   MISC STREAMLIT OVERRIDES
═══════════════════════════════════════ */
/* Toolbar / top header */
[data-testid="stHeader"] { background: #0D0F14 !important; }
/* Bottom toolbar */
[data-testid="stStatusWidget"] { display: none !important; }
/* Hamburger menu */
[data-testid="baseButton-headerNoPadding"] svg { fill: #6366F1 !important; }
/* Column borders */
[data-testid="column"] { background: transparent !important; }
/* stWrite / st.write text */
.stWrite { color: #CBD5E1 !important; }
/* Caption */
.stCaption { color: #475569 !important; }
/* Code blocks */
code, pre { background: #1A1D2E !important; color: #A5B4FC !important; border-radius: 6px !important; }
/* Number input buttons */
.stNumberInput button { background: #1A1D2E !important; border-color: rgba(255,255,255,0.1) !important; color: #E2E8F0 !important; }
/* Date picker popup */
[data-baseweb="calendar"] { background: #1A1D2E !important; border: 1px solid rgba(99,102,241,0.2) !important; }
/* Spinners */
[data-testid="stSpinner"] { color: #6366F1 !important; }
/* Subheader */
.stSubheader { color: #A5B4FC !important; }
/* Divider */
[data-testid="stDecoration"] { background: linear-gradient(90deg, #6366F1, #8B5CF6, transparent) !important; height: 2px !important; }
/* Toast / notification */
[data-testid="stNotification"] { background: #13151F !important; border: 1px solid rgba(99,102,241,0.25) !important; color: #E2E8F0 !important; border-radius: 12px !important; }
/* Popover / tooltip */
[data-testid="stTooltipContent"] { background: #1A1D2E !important; border: 1px solid rgba(99,102,241,0.2) !important; color: #E2E8F0 !important; }
/* Multiselect */
[data-testid="stMultiSelect"] > div { background: #1A1D2E !important; border-color: rgba(255,255,255,0.1) !important; }
[data-baseweb="tag"] { background: rgba(99,102,241,0.2) !important; color: #A5B4FC !important; }

</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA LAYER
# ══════════════════════════════════════════════════════════════════════════════
DATA_DIR = "hassan_traders_data"
os.makedirs(DATA_DIR, exist_ok=True)

PERSISTENT_TABLES = [
    "customers","suppliers","employees","products","livestock","categories","units",
    "warehouses","company_settings","users","bmi_plans","price_lists","tax_settings",
    "notes","tasks","audit_log","attendance","salaries","loans","installments",
    "purchase_orders","stock_adjustments","damage_records","breeding_records",
    "livestock_health","feed_records","milk_records","batches","serials",
    "production","pos_sales_archive"
]

TRANSIENT_TABLES = [
    "pos_sales","transactions","receipts","payments","expenses",
    "livestock_sales","sale_orders","advance_sales","vehicle_trips"
]

def _path(name): return os.path.join(DATA_DIR, f"{name}.json")

def load_table(name):
    p = _path(name)
    if os.path.exists(p):
        try:
            with open(p) as f: return json.load(f)
        except: return []
    return []

def save_table(name, data):
    with open(_path(name), "w") as f:
        json.dump(data, f, indent=2, default=str)

def gen_id(prefix=""):
    return f"{prefix}{uuid.uuid4().hex[:8].upper()}"

def now_str():   return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def today_str(): return date.today().isoformat()

def log_audit(user, action, detail=""):
    al = load_table("audit_log")
    al.append({"id":gen_id("AL"),"user":user,"action":action,"detail":detail,"ts":now_str()})
    if len(al) > 3000: al = al[-3000:]
    save_table("audit_log", al)

# ── AUTO-CLEANUP ───────────────────────────────────────────────────────────────
def auto_cleanup():
    cutoff = (date.today() - timedelta(days=3)).isoformat()
    for tbl in TRANSIENT_TABLES:
        data = load_table(tbl)
        keep, archive = [], []
        for row in data:
            row_date = str(row.get("date","") or row.get("created_at",""))[:10]
            (archive if row_date and row_date < cutoff else keep).append(row)
        if archive:
            arch = load_table(f"{tbl}_archive")
            arch.extend(archive)
            save_table(f"{tbl}_archive", arch)
            save_table(tbl, keep)

# ── EXPORT HELPERS ─────────────────────────────────────────────────────────────
def df_to_excel_bytes(sheets_dict):
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        for sheet_name, df in sheets_dict.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    return buf.getvalue()

def df_to_csv_bytes(df):
    return df.to_csv(index=False).encode()

def make_download_link(data_bytes, filename, label):
    b64 = base64.b64encode(data_bytes).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{label}</a>'

# ── AUTH ───────────────────────────────────────────────────────────────────────
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def init_default_user():
    users = load_table("users")
    if not users:
        users.append({"id":"U001","username":"admin","password":hash_pw("admin123"),
                      "role":"Admin","name":"Administrator","email":"admin@hassantraders.com",
                      "phone":"","active":True,"created":today_str()})
        save_table("users", users)

def authenticate(username, password):
    for u in load_table("users"):
        if u["username"]==username and u["password"]==hash_pw(password) and u.get("active",True):
            return u
    return None

# ── SETTINGS ───────────────────────────────────────────────────────────────────
def init_settings():
    s = load_table("company_settings")
    if not s:
        s = [{"id":"CS001","name":"Hassan Traders","address":"Karachi, Pakistan",
              "phone":"0300-0000000","email":"info@hassantraders.com","ntn":"",
              "currency":"PKR","tax_rate":17.0,"fiscal_year_start":"01-07",
              "logo":"","low_stock_threshold":10}]
        save_table("company_settings", s)
    return s[0]

def get_settings():
    s = load_table("company_settings")
    return s[0] if s else {}

def currency(val):
    cur = get_settings().get("currency","PKR")
    try: return f"{cur} {float(val):,.0f}"
    except: return f"{cur} 0"

# ── UI HELPERS ─────────────────────────────────────────────────────────────────
def section_header(icon, title):
    st.markdown(f"""
    <div class="ht-section-header">
        <span class="ht-section-icon">{icon}</span>
        <h1>{title}</h1>
    </div>""", unsafe_allow_html=True)

def metric_card(label, value, color="blue", delta=None):
    delta_html = f'<div style="font-size:11px;color:#475569;margin-top:5px;font-weight:500">{delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-card {color}">
        <div class="mc-value">{value}</div>
        <div class="mc-label">{label}</div>
        {delta_html}
    </div>""", unsafe_allow_html=True)

def info_panel(text, kind="blue"):
    st.markdown(f'<div class="info-panel {kind}">{text}</div>', unsafe_allow_html=True)

def df_display(df, height=420):
    if df is None or df.empty:
        st.markdown('<div class="info-panel">No records found.</div>', unsafe_allow_html=True)
    else:
        st.dataframe(df, use_container_width=True, height=height)

def badge(text, color="blue"):
    return f'<span class="badge badge-{color}">{text}</span>'

def ok(m):   st.success(f"✅ {m}")
def err(m):  st.error(f"❌ {m}")
def warn(m): st.warning(f"⚠️ {m}")

# ── UPDATE CUSTOMER BALANCE HELPER ─────────────────────────────────────────────
def adjust_customer_balance(customer_name, delta):
    """Add delta to customer balance (positive = more owed, negative = less owed)"""
    if not customer_name or customer_name == "Walk-in": return
    custs = load_table("customers")
    for c in custs:
        if c["name"] == customer_name:
            c["balance"] = max(0, float(c.get("balance", 0)) + delta)
    save_table("customers", custs)

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
def login_page():
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-logo">🐄</div>
            <div class="login-title">Hassan Traders</div>
            <div class="login-subtitle">Complete Business Management System — Dark Edition</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            if st.form_submit_button("Sign In →", use_container_width=True):
                user = authenticate(username, password)
                if user:
                    st.session_state.update({"logged_in": True, "user": user})
                    log_audit(username, "LOGIN")
                    st.rerun()
                else:
                    err("Invalid credentials. Default: admin / admin123")

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
MENU = {
    "🏠 Dashboard":    ["Overview"],
    "💰 Finance":      ["Ledger","Cashbook","Receipts & Payments","Expenses","Daily Profit Report"],
    "📦 Inventory":    ["Products","Stock Adjustment","Damage Records","Warehouses","Price Lists"],
    "🛒 Sales":        ["Point of Sale","Sale Orders","Advance Sales","English Billing"],
    "📥 Purchases":    ["Purchase Orders","Supplier Management"],
    "👥 CRM":          ["Customers","Debtors & Creditors","Tasks & Follow-ups","Notes"],
    "🐄 Livestock":    ["Livestock Register","Milk Production","Feed Records","Breeding","Health Records","Livestock Sales"],
    "🏭 Production":   ["Production Orders","Production Report"],
    "💳 Installments": ["BMI Plans","Installment Schedule"],
    "👨‍💼 HRM":         ["Employees","Attendance","Salary Management","Loans & Advances"],
    "📊 Reports":      ["Daily Download","Data Management"],
    "🏢 Company":      ["Settings","User Management","Audit Log"],
}

def render_sidebar():
    user = st.session_state.get("user", {})
    st.sidebar.markdown(f"""
    <div style="text-align:center; padding: 22px 0 14px;">
        <div style="font-size:2.8rem; margin-bottom:8px; filter:drop-shadow(0 0 18px rgba(99,102,241,0.5));">🐄</div>
        <div style="font-size:1.1rem; font-weight:800; color:#C7D2FE; letter-spacing:-0.3px;">Hassan Traders</div>
        <div style="font-size:10px; color:#4B5563; margin-top:3px; letter-spacing:1px; text-transform:uppercase;">Business Management</div>
    </div>
    <div style="background:rgba(99,102,241,0.1); border-radius:10px; padding:9px 14px;
         margin:0 8px 14px; font-size:12px; color:#94A3B8; border:1px solid rgba(99,102,241,0.15);">
        👤 <b style="color:#C7D2FE">{user.get('name','')}</b>
        <span style="float:right; background:rgba(99,102,241,0.25); border-radius:5px;
              padding:1px 8px; font-size:11px; color:#A5B4FC;">{user.get('role','')}</span>
    </div>""", unsafe_allow_html=True)

    if "nav_section" not in st.session_state: st.session_state["nav_section"] = "🏠 Dashboard"
    if "nav_page"    not in st.session_state: st.session_state["nav_page"]    = "Overview"

    for section, pages in MENU.items():
        with st.sidebar.expander(section, expanded=(st.session_state["nav_section"] == section)):
            for page in pages:
                if st.button(page, key=f"nav_{section}_{page}", use_container_width=True):
                    st.session_state["nav_section"] = section
                    st.session_state["nav_page"]    = page
                    st.rerun()

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Sign Out", use_container_width=True):
        log_audit(user.get("username", ""), "LOGOUT")
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    section_header("📊", "Business Dashboard")
    settings   = get_settings(); cur = settings.get("currency","PKR")
    pos_sales  = load_table("pos_sales")
    customers  = load_table("customers")
    products   = load_table("products")
    livestock  = load_table("livestock")
    expenses   = load_table("expenses")
    advance    = load_table("advance_sales")
    receipts   = load_table("receipts")
    today      = today_str()
    month_start= date.today().replace(day=1).isoformat()

    today_sales  = sum(float(s.get("total",0)) for s in pos_sales if s.get("date","")[:10]==today)
    month_sales  = sum(float(s.get("total",0)) for s in pos_sales if s.get("date","")[:10]>=month_start)
    today_exp    = sum(float(e.get("amount",0)) for e in expenses if e.get("date","")[:10]==today)
    month_rec    = sum(float(r.get("amount",0)) for r in receipts if r.get("date","")[:10]>=month_start)
    low_stock    = [p for p in products if float(p.get("stock",0)) < float(p.get("min_stock",10))]
    pending_adv  = sum(float(a.get("balance",0)) for a in advance if a.get("status") not in ("Fully Paid","Cancelled"))
    active_ls    = len([l for l in livestock if l.get("status")=="Active"])
    total_debtors= sum(float(c.get("balance",0)) for c in customers if float(c.get("balance",0))>0)

    cols = st.columns(4)
    with cols[0]: metric_card("Today's Sales",  f"{cur} {today_sales:,.0f}", "blue",  f"Month: {cur} {month_sales:,.0f}")
    with cols[1]: metric_card("Today's Expenses",f"{cur} {today_exp:,.0f}","red")
    with cols[2]: metric_card("Month Receipts",  f"{cur} {month_rec:,.0f}", "green")
    with cols[3]: metric_card("Pending Advances",f"{cur} {pending_adv:,.0f}","amber")

    cols2 = st.columns(4)
    with cols2[0]: metric_card("Active Livestock",active_ls, "purple")
    with cols2[1]: metric_card("Low Stock Items",  len(low_stock), "red")
    with cols2[2]: metric_card("Total Customers",  len(customers), "blue")
    with cols2[3]: metric_card("Total Debtors",    f"{cur} {total_debtors:,.0f}", "amber")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2])
    with col_l:
        st.markdown("**📈 Sales Trend — Last 14 Days**")
        if pos_sales:
            dates = [(date.today()-timedelta(days=i)).isoformat() for i in range(13,-1,-1)]
            chart_df = pd.DataFrame({
                "Date": dates,
                "Sales": [sum(float(s.get("total",0)) for s in pos_sales if s.get("date","")[:10]==d) for d in dates],
                "Expenses": [sum(float(e.get("amount",0)) for e in expenses if str(e.get("date",""))[:10]==d) for d in dates],
            }).set_index("Date")
            st.line_chart(chart_df)
        else:
            info_panel("No sales data yet. Start with Point of Sale →")

        st.markdown("<br>**📦 Top Products by Stock Value**", unsafe_allow_html=True)
        if products:
            top = sorted(products, key=lambda p: float(p.get("stock",0))*float(p.get("cost_price",0)), reverse=True)[:8]
            st.bar_chart(pd.DataFrame({
                "Product": [p["name"] for p in top],
                "Value":   [float(p.get("stock",0))*float(p.get("cost_price",0)) for p in top]
            }).set_index("Product"))

    with col_r:
        st.markdown("**⚠️ Low Stock Alerts**")
        if low_stock:
            for p in low_stock[:8]:
                st.markdown(
                    f'{badge(p["name"],"red")} Stock: <b>{p.get("stock",0)}</b> / Min: {p.get("min_stock",10)}',
                    unsafe_allow_html=True)
        else:
            info_panel("✅ All stock levels healthy!", "green")

        st.markdown("<br>**💳 Pending Advance Payments**", unsafe_allow_html=True)
        pend = [a for a in advance if a.get("status") not in ("Fully Paid","Cancelled")]
        if pend:
            for a in pend[:6]:
                bal = float(a.get("total",0)) - float(a.get("advance_paid",0))
                st.markdown(f'{badge(a.get("customer",""),"amber")} Balance: <b>{currency(bal)}</b>',
                            unsafe_allow_html=True)
        else:
            info_panel("No pending advance payments.", "green")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LEDGER
# ══════════════════════════════════════════════════════════════════════════════
def page_ledger():
    section_header("📒", "General Ledger")
    tab1, tab2 = st.tabs(["Transaction List", "Add Journal Entry"])
    with tab1:
        c1,c2,c3 = st.columns(3)
        with c1: d_from = st.date_input("From", date.today().replace(day=1), key="led_from")
        with c2: d_to   = st.date_input("To", date.today(), key="led_to")
        with c3: search = st.text_input("🔍 Search", key="led_search")
        transactions = load_table("transactions")
        filtered = [t for t in transactions if d_from.isoformat()<=str(t.get("date",""))[:10]<=d_to.isoformat()]
        if search: filtered = [t for t in filtered if search.lower() in str(t).lower()]
        if filtered:
            df = pd.DataFrame(filtered[::-1])
            cols = [c for c in ["date","ref","type","description","debit_account","credit_account","debit","credit","party"] if c in df.columns]
            df_display(df[cols])
            c1,c2,c3 = st.columns(3)
            total_d = sum(float(t.get("debit",0)) for t in filtered)
            total_c = sum(float(t.get("credit",0)) for t in filtered)
            c1.metric("Total Debits",currency(total_d))
            c2.metric("Total Credits",currency(total_c))
            c3.metric("Difference",currency(total_d-total_c))
        else: info_panel("No transactions in selected period.")

    with tab2:
        with st.form("journal"):
            c1,c2 = st.columns(2)
            with c1:
                j_date = st.date_input("Date", date.today())
                j_ref  = st.text_input("Reference", value=gen_id("JV"))
                j_desc = st.text_input("Description")
                j_party= st.text_input("Party")
            with c2:
                j_debit_acc  = st.text_input("Debit Account")
                j_credit_acc = st.text_input("Credit Account")
                j_amount     = st.number_input("Amount", 0.0, step=100.0)
                j_type       = st.selectbox("Type", ["Journal","Debit Note","Credit Note","Contra"])
            if st.form_submit_button("Post Entry →", use_container_width=True):
                if j_amount > 0 and j_debit_acc and j_credit_acc:
                    txns = load_table("transactions")
                    txns.append({"id":gen_id("TXN"),"ref":j_ref,"date":str(j_date),"type":j_type,
                                 "description":j_desc,"debit_account":j_debit_acc,"credit_account":j_credit_acc,
                                 "debit":j_amount,"credit":j_amount,"party":j_party,
                                 "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("transactions",txns)
                    ok("Journal entry posted!")
                    st.rerun()
                else: err("Fill all required fields.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CASHBOOK
# ══════════════════════════════════════════════════════════════════════════════
def page_cashbook():
    section_header("💵", "Cashbook")
    c1,c2 = st.columns(2)
    with c1: cb_from = st.date_input("From", date.today().replace(day=1))
    with c2: cb_to   = st.date_input("To", date.today())
    receipts = load_table("receipts"); payments = load_table("payments")
    rec_f = [r for r in receipts if cb_from.isoformat()<=str(r.get("date",""))[:10]<=cb_to.isoformat()]
    pay_f = [p for p in payments if cb_from.isoformat()<=str(p.get("date",""))[:10]<=cb_to.isoformat()]
    total_rec = sum(float(r.get("amount",0)) for r in rec_f)
    total_pay = sum(float(p.get("amount",0)) for p in pay_f)
    cols = st.columns(3)
    with cols[0]: metric_card("Total Receipts", currency(total_rec), "green")
    with cols[1]: metric_card("Total Payments", currency(total_pay), "red")
    with cols[2]: metric_card("Net Cash Balance", currency(total_rec-total_pay), "blue")
    st.markdown("<br>", unsafe_allow_html=True)
    rows = []
    for r in rec_f: rows.append({"Date":r.get("date",""),"Ref":r.get("ref",""),"Type":"Receipt","Narration":f"Receipt — {r.get('party','')}","Receipts":r.get("amount",0),"Payments":0,"Mode":r.get("mode","")})
    for p in pay_f: rows.append({"Date":p.get("date",""),"Ref":p.get("ref",""),"Type":"Payment","Narration":f"Payment — {p.get('party','')}","Receipts":0,"Payments":p.get("amount",0),"Mode":p.get("mode","")})
    if rows:
        df = pd.DataFrame(sorted(rows, key=lambda x: x["Date"]))
        df_display(df)
    else: info_panel("No cashbook entries in selected period.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: RECEIPTS & PAYMENTS
# ══════════════════════════════════════════════════════════════════════════════
def page_receipts_payments():
    section_header("💳", "Receipts & Payments")
    tab1, tab2, tab3 = st.tabs(["📋 Records", "➕ New Entry", "✏️ Edit / Correct"])

    with tab1:
        c0, = st.columns([1])
        view = st.radio("View", ["Receipts","Payments","Both"], horizontal=True)
        c1,c2 = st.columns(2)
        with c1: d_from = st.date_input("From", date.today().replace(day=1), key="rp_from")
        with c2: d_to   = st.date_input("To", date.today(), key="rp_to")
        receipts = load_table("receipts"); payments = load_table("payments")
        all_items = []
        if view in ("Receipts","Both"):
            for r in receipts:
                if d_from.isoformat()<=str(r.get("date",""))[:10]<=d_to.isoformat():
                    all_items.append({**r,"Category":"Receipt"})
        if view in ("Payments","Both"):
            for p in payments:
                if d_from.isoformat()<=str(p.get("date",""))[:10]<=d_to.isoformat():
                    all_items.append({**p,"Category":"Payment"})
        if all_items:
            df = pd.DataFrame(all_items)
            cols = [c for c in ["date","ref","party","amount","mode","Category","notes"] if c in df.columns]
            df_display(df[cols])
            tr = sum(float(r.get("amount",0)) for r in receipts if d_from.isoformat()<=str(r.get("date",""))[:10]<=d_to.isoformat())
            tp = sum(float(p.get("amount",0)) for p in payments if d_from.isoformat()<=str(p.get("date",""))[:10]<=d_to.isoformat())
            c1,c2,c3 = st.columns(3)
            c1.metric("Total Receipts", currency(tr))
            c2.metric("Total Payments", currency(tp))
            c3.metric("Net Cash Flow",  currency(tr-tp))
        else: info_panel("No records in selected period.")

    with tab2:
        etype = st.radio("Type", ["Receipt","Payment"], horizontal=True, key="rp_type")
        customers = load_table("customers"); cust_names = [c["name"] for c in customers]
        with st.form("rp_form"):
            c1,c2 = st.columns(2)
            with c1:
                rp_date    = st.date_input("Date", date.today())
                ref        = st.text_input("Reference", value=gen_id("RCP" if etype=="Receipt" else "PAY"))
                party      = st.selectbox("Party", ["— Type name —"]+cust_names) if cust_names else st.text_input("Party")
                party_name = st.text_input("Or enter party name manually") if cust_names else ""
                amount     = st.number_input("Amount", 0.0, step=100.0)
            with c2:
                mode       = st.selectbox("Payment Mode", ["Cash","Bank Transfer","Cheque","Online","Mobile Banking"])
                bank_ref   = st.text_input("Bank / Cheque Reference")
                inv_ref    = st.text_input("Invoice / Sale Reference")
                update_bal = st.checkbox("Update customer balance", value=True)
                notes      = st.text_area("Notes", height=70)
            if st.form_submit_button(f"Save {etype} →", use_container_width=True):
                final_party = party_name.strip() if party_name.strip() else (party if party != "— Type name —" else "")
                if amount > 0 and final_party:
                    rec = {"id":gen_id(),"ref":ref,"date":str(rp_date),"party":final_party,
                           "amount":amount,"mode":mode,"bank_ref":bank_ref,
                           "invoice_ref":inv_ref,"notes":notes,"type":etype,
                           "created_by":st.session_state["user"]["username"],"created_at":now_str()}
                    tbl = "receipts" if etype=="Receipt" else "payments"
                    d = load_table(tbl); d.append(rec); save_table(tbl, d)
                    # Post to ledger
                    txns = load_table("transactions")
                    txns.append({"id":gen_id("TXN"),"ref":ref,"date":str(rp_date),"type":etype,
                                 "description":f"{etype} — {final_party}",
                                 "debit_account":"Cash" if etype=="Receipt" else final_party,
                                 "credit_account":final_party if etype=="Receipt" else "Cash",
                                 "debit":amount,"credit":amount,"party":final_party,
                                 "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("transactions", txns)
                    # Update customer balance
                    if update_bal:
                        delta = -amount if etype=="Receipt" else amount
                        adjust_customer_balance(final_party, delta)
                    log_audit(st.session_state["user"]["username"], f"ADD_{etype.upper()}", f"{final_party}: {amount}")
                    ok(f"{etype} of {currency(amount)} saved!")
                    st.rerun()
                else: err("Party name and Amount required.")

    with tab3:
        st.subheader("✏️ Edit or Correct a Payment / Receipt")
        edit_type = st.radio("Select Type", ["Receipt","Payment"], horizontal=True, key="edit_rp_type")
        data = load_table("receipts" if edit_type=="Receipt" else "payments")
        if not data:
            info_panel("No records found."); return
        opts = {f"{r['id']} — {r.get('party','')} — {currency(r.get('amount',0))} ({r.get('date','')})": i for i,r in enumerate(data)}
        sel_key = st.selectbox("Select Record", list(opts.keys()))
        idx = opts[sel_key]; rec = data[idx]
        c1,c2 = st.columns(2)
        with c1:
            new_amount = st.number_input("Amount", value=float(rec.get("amount",0)), step=100.0, key="edit_rp_amt")
            new_mode   = st.selectbox("Payment Mode", ["Cash","Bank Transfer","Cheque","Online","Mobile Banking"],
                                      index=["Cash","Bank Transfer","Cheque","Online","Mobile Banking"].index(rec.get("mode","Cash")) if rec.get("mode","Cash") in ["Cash","Bank Transfer","Cheque","Online","Mobile Banking"] else 0)
        with c2:
            new_date   = st.date_input("Date", date.fromisoformat(str(rec.get("date",today_str()))[:10]))
            new_notes  = st.text_area("Notes", value=rec.get("notes",""), height=80)
        col_s, col_d = st.columns(2)
        with col_s:
            if st.button("💾 Save Changes", key="save_edit_rp"):
                old_amt = float(rec.get("amount",0))
                data[idx].update({"amount":new_amount,"mode":new_mode,"date":str(new_date),"notes":new_notes,
                                  "edited_by":st.session_state["user"]["username"],"edited_at":now_str()})
                save_table("receipts" if edit_type=="Receipt" else "payments", data)
                # Adjust customer balance for difference
                diff = new_amount - old_amt
                if diff != 0:
                    delta = -diff if edit_type=="Receipt" else diff
                    adjust_customer_balance(rec.get("party",""), delta)
                log_audit(st.session_state["user"]["username"], f"EDIT_{edit_type.upper()}", rec["id"])
                ok("Record updated!"); st.rerun()
        with col_d:
            if st.button("🗑️ Delete Record", key="del_edit_rp"):
                # Reverse balance effect
                amt = float(rec.get("amount",0))
                delta = amt if edit_type=="Receipt" else -amt
                adjust_customer_balance(rec.get("party",""), delta)
                data.pop(idx)
                save_table("receipts" if edit_type=="Receipt" else "payments", data)
                log_audit(st.session_state["user"]["username"], f"DELETE_{edit_type.upper()}", rec["id"])
                ok("Record deleted."); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EXPENSES
# ══════════════════════════════════════════════════════════════════════════════
def page_expenses():
    section_header("💸", "Expenses Management")
    CATS = ["Feed","Veterinary","Transport","Salaries","Utilities","Maintenance",
            "Fuel","Office","Marketing","Rent","Insurance","Miscellaneous"]
    tab1, tab2, tab3 = st.tabs(["Expense List", "Add Expense", "Analysis"])

    with tab1:
        expenses = load_table("expenses")
        c1,c2,c3 = st.columns(3)
        with c1: ef_from = st.date_input("From", date.today().replace(day=1), key="ex_from")
        with c2: ef_to   = st.date_input("To",   date.today(), key="ex_to")
        with c3: ef_cat  = st.selectbox("Category", ["All"]+CATS)
        filtered = [e for e in expenses if ef_from.isoformat()<=str(e.get("date",""))[:10]<=ef_to.isoformat()]
        if ef_cat != "All": filtered = [e for e in filtered if e.get("category","") == ef_cat]
        if filtered:
            df = pd.DataFrame(filtered)
            cols = [c for c in ["date","ref","category","description","amount","paid_by","vendor","notes"] if c in df.columns]
            df_display(df[cols])
            st.metric("Total Expenses", currency(sum(float(e.get("amount",0)) for e in filtered)))
        else: info_panel("No expenses in selected period.")

    with tab2:
        with st.form("add_exp"):
            c1,c2 = st.columns(2)
            with c1:
                exp_date    = st.date_input("Date", date.today())
                category    = st.selectbox("Category", CATS)
                amount      = st.number_input("Amount", 0.0, step=100.0)
                paid_by     = st.selectbox("Paid By", ["Cash","Bank","Credit Card","Mobile Banking"])
            with c2:
                description = st.text_area("Description", height=70)
                vendor      = st.text_input("Vendor / Payee")
                ref         = st.text_input("Bill Reference")
                notes       = st.text_input("Notes")
            if st.form_submit_button("Save Expense →", use_container_width=True):
                if amount > 0:
                    exps = load_table("expenses")
                    exps.append({"id":gen_id("EXP"),"ref":ref or gen_id("EXP"),"date":str(exp_date),
                                 "category":category,"description":description,"amount":amount,
                                 "paid_by":paid_by,"vendor":vendor,"notes":notes,
                                 "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("expenses", exps)
                    # Post to cashbook as payment
                    pmts = load_table("payments")
                    pmts.append({"id":gen_id("PAY"),"ref":ref or gen_id("EXP"),"date":str(exp_date),
                                 "party":vendor or category,"amount":amount,"mode":paid_by,
                                 "type":"Payment","notes":f"Expense: {description}","created_at":now_str()})
                    save_table("payments", pmts)
                    ok("Expense saved and posted to cashbook!")
                    st.rerun()

    with tab3:
        expenses = load_table("expenses")
        if expenses:
            cat_totals = {}
            for e in expenses:
                cat = e.get("category","Other")
                cat_totals[cat] = cat_totals.get(cat,0) + float(e.get("amount",0))
            df_chart = pd.DataFrame(list(cat_totals.items()), columns=["Category","Total"]).set_index("Category")
            st.bar_chart(df_chart)
            st.dataframe(df_chart.sort_values("Total", ascending=False), use_container_width=True)
        else: info_panel("No expense data yet.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DAILY PROFIT REPORT
# ══════════════════════════════════════════════════════════════════════════════
def page_daily_profit():
    section_header("📊", "Daily Profit Report")
    c1,c2 = st.columns(2)
    with c1: rep_from = st.date_input("From", date.today().replace(day=1))
    with c2: rep_to   = st.date_input("To",   date.today())
    pos_sales       = load_table("pos_sales")
    expenses        = load_table("expenses")
    livestock_sales = load_table("livestock_sales")
    rows = []
    d = rep_from
    while d <= rep_to:
        ds = d.isoformat()
        day_sales    = sum(float(s.get("total",0))       for s in pos_sales       if str(s.get("date",""))[:10]==ds)
        day_cost     = sum(float(s.get("cost_total",0))  for s in pos_sales       if str(s.get("date",""))[:10]==ds)
        day_ls_sales = sum(float(s.get("sale_price",0))  for s in livestock_sales if str(s.get("date",""))[:10]==ds)
        day_ls_cost  = sum(float(s.get("purchase_price",0)) for s in livestock_sales if str(s.get("date",""))[:10]==ds)
        day_exp      = sum(float(e.get("amount",0))      for e in expenses        if str(e.get("date",""))[:10]==ds)
        gross = (day_sales - day_cost) + (day_ls_sales - day_ls_cost)
        rows.append({"Date":ds,"Sales":day_sales,"COGS":day_cost,"LS Sales":day_ls_sales,
                     "LS Cost":day_ls_cost,"Expenses":day_exp,"Gross Profit":gross,"Net Profit":gross-day_exp})
        d += timedelta(days=1)
    if rows:
        df = pd.DataFrame(rows)
        c1,c2,c3,c4 = st.columns(4)
        with c1: metric_card("Total Sales",    currency(df["Sales"].sum()),        "blue")
        with c2: metric_card("Total Expenses", currency(df["Expenses"].sum()),     "red")
        with c3: metric_card("Gross Profit",   currency(df["Gross Profit"].sum()),"green")
        with c4: metric_card("Net Profit",     currency(df["Net Profit"].sum()),  "purple")
        st.markdown("<br>", unsafe_allow_html=True)
        df_display(df)
        st.line_chart(df.set_index("Date")[["Sales","Net Profit","Expenses"]])

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PRODUCTS
# ══════════════════════════════════════════════════════════════════════════════
def page_products():
    section_header("📦", "Product Management")
    cats  = load_table("categories"); cat_names  = [c["name"] for c in cats] if cats else ["Feed","Medicine","Equipment","Other"]
    units = load_table("units");      unit_names = [u["name"] for u in units] if units else ["KG","Gram","Liter","Piece","Box","Bag","Ton"]
    tab1, tab2, tab3, tab4 = st.tabs(["Product List","Add Product","Edit Price","Stock Summary"])

    with tab1:
        products = load_table("products")
        c1,c2,c3 = st.columns(3)
        with c1: search = st.text_input("🔍 Search", key="ps")
        with c2: cat_f  = st.selectbox("Category", ["All"]+cat_names)
        with c3: sf     = st.selectbox("Stock Filter", ["All","Low Stock","Out of Stock","In Stock"])
        filtered = products
        if search: filtered = [p for p in filtered if search.lower() in p.get("name","").lower() or search.lower() in p.get("sku","").lower()]
        if cat_f != "All": filtered = [p for p in filtered if p.get("category","") == cat_f]
        if sf == "Low Stock":    filtered = [p for p in filtered if 0 < float(p.get("stock",0)) < float(p.get("min_stock",10))]
        elif sf == "Out of Stock": filtered = [p for p in filtered if float(p.get("stock",0)) == 0]
        elif sf == "In Stock":     filtered = [p for p in filtered if float(p.get("stock",0)) > 0]
        if filtered:
            df = pd.DataFrame(filtered)
            cols = [c for c in ["sku","name","category","unit","stock","min_stock","cost_price","sale_price","barcode"] if c in df.columns]
            df_display(df[cols])
        else: info_panel("No products found.")

    with tab2:
        with st.form("add_prod"):
            c1,c2,c3 = st.columns(3)
            with c1:
                sku      = st.text_input("SKU", value=gen_id("PRD"))
                name     = st.text_input("Product Name *")
                category = st.selectbox("Category", cat_names)
                brand    = st.text_input("Brand")
                unit     = st.selectbox("Unit", unit_names)
            with c2:
                cost_price  = st.number_input("Cost Price", 0.0, step=1.0)
                sale_price  = st.number_input("Sale Price (Retail)", 0.0, step=1.0)
                sale_price2 = st.number_input("Sale Price 2 (Wholesale)", 0.0, step=1.0)
                tax_rate    = st.number_input("Tax Rate %", 0.0, 100.0, 0.0, step=0.5)
            with c3:
                opening_stock = st.number_input("Opening Stock", 0.0, step=1.0)
                min_stock     = st.number_input("Min Stock (Reorder)", 0.0, step=1.0)
                barcode       = st.text_input("Barcode")
                location      = st.text_input("Storage Location")
            description = st.text_area("Description", height=55)
            if st.form_submit_button("Save Product →", use_container_width=True):
                if name:
                    products = load_table("products")
                    products.append({"id":gen_id("PRD"),"sku":sku,"name":name,"category":category,
                                     "brand":brand,"unit":unit,"cost_price":cost_price,
                                     "sale_price":sale_price,"sale_price2":sale_price2,
                                     "tax_rate":tax_rate,"stock":opening_stock,"min_stock":min_stock,
                                     "barcode":barcode,"location":location,"description":description,
                                     "active":True,"created":today_str()})
                    save_table("products", products)
                    log_audit(st.session_state["user"]["username"],"ADD_PRODUCT",name)
                    ok(f"Product '{name}' added!")
                    st.rerun()
                else: err("Product name required.")

    with tab3:
        products = load_table("products")
        prod_names = [p["name"] for p in products]
        if prod_names:
            sel_prod = st.selectbox("Select Product to Update Price", prod_names)
            pdata = next((p for p in products if p["name"]==sel_prod), {})
            c1,c2,c3 = st.columns(3)
            with c1: new_cost  = st.number_input("Cost Price",      value=float(pdata.get("cost_price",0)),  step=1.0)
            with c2: new_sale  = st.number_input("Retail Price",     value=float(pdata.get("sale_price",0)),  step=1.0)
            with c3: new_whole = st.number_input("Wholesale Price",  value=float(pdata.get("sale_price2",0)), step=1.0)
            if st.button("💾 Update Prices"):
                for p in products:
                    if p["name"] == sel_prod:
                        p["cost_price"] = new_cost; p["sale_price"] = new_sale; p["sale_price2"] = new_whole
                save_table("products", products)
                ok(f"Prices updated for {sel_prod}!")
                st.rerun()
        else: info_panel("No products yet.")

    with tab4:
        products = load_table("products")
        if products:
            total_cv = sum(float(p.get("stock",0))*float(p.get("cost_price",0))  for p in products)
            total_sv = sum(float(p.get("stock",0))*float(p.get("sale_price",0)) for p in products)
            low      = len([p for p in products if float(p.get("stock",0)) < float(p.get("min_stock",10))])
            cols = st.columns(4)
            with cols[0]: metric_card("Total Products",  len(products),         "blue")
            with cols[1]: metric_card("Stock Cost Value",currency(total_cv),    "green")
            with cols[2]: metric_card("Stock Sale Value",currency(total_sv),    "purple")
            with cols[3]: metric_card("Low Stock Items", low,                   "red")
            by_cat = {}
            for p in products:
                cat = p.get("category","Other")
                by_cat[cat] = by_cat.get(cat,0) + float(p.get("stock",0))*float(p.get("cost_price",0))
            st.bar_chart(pd.DataFrame(list(by_cat.items()),columns=["Category","Value"]).set_index("Category"))

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: STOCK ADJUSTMENT
# ══════════════════════════════════════════════════════════════════════════════
def page_stock_adjustment():
    section_header("📦", "Stock Adjustment")
    products   = load_table("products"); prod_names = [p["name"] for p in products]
    tab1, tab2 = st.tabs(["Adjustment History","New Adjustment"])
    with tab1:
        adj = load_table("stock_adjustments")
        if adj: df_display(pd.DataFrame(adj))
        else: info_panel("No adjustments yet.")
    with tab2:
        if prod_names:
            with st.form("stock_adj"):
                c1,c2 = st.columns(2)
                with c1:
                    sa_prod = st.selectbox("Product", prod_names)
                    sa_type = st.selectbox("Adjustment Type", ["Add Stock","Remove Stock","Correction"])
                    sa_qty  = st.number_input("Quantity", 0.0, step=1.0)
                with c2:
                    sa_reason = st.selectbox("Reason", ["Purchase Received","Return","Damage Write-off","Count Correction","Transfer","Other"])
                    sa_date   = st.date_input("Date", date.today())
                    sa_notes  = st.text_area("Notes", height=60)
                if st.form_submit_button("Save Adjustment →", use_container_width=True):
                    if sa_qty > 0:
                        adj = load_table("stock_adjustments")
                        p_data    = next((p for p in products if p["name"]==sa_prod), {})
                        old_stock = float(p_data.get("stock",0))
                        new_stock = old_stock+sa_qty if sa_type=="Add Stock" else max(0,old_stock-sa_qty) if sa_type=="Remove Stock" else sa_qty
                        adj.append({"id":gen_id("SA"),"date":str(sa_date),"product":sa_prod,
                                    "type":sa_type,"qty":sa_qty,"old_stock":old_stock,"new_stock":new_stock,
                                    "reason":sa_reason,"notes":sa_notes,
                                    "by":st.session_state["user"]["username"],"created_at":now_str()})
                        save_table("stock_adjustments", adj)
                        for p in products:
                            if p["name"]==sa_prod: p["stock"] = new_stock
                        save_table("products", products)
                        ok(f"Stock adjusted: {old_stock} → {new_stock}")
                        st.rerun()
        else: warn("Add products first.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DAMAGE RECORDS
# ══════════════════════════════════════════════════════════════════════════════
def page_damage():
    section_header("⚠️", "Damage & Write-off Records")
    products   = load_table("products"); prod_names = [p["name"] for p in products]
    tab1, tab2 = st.tabs(["Damage Records","Record Damage"])
    with tab1:
        dr = load_table("damage_records")
        if dr: df_display(pd.DataFrame(dr))
        else: info_panel("No damage records.")
    with tab2:
        with st.form("dmg_rec"):
            c1,c2 = st.columns(2)
            with c1:
                d_prod   = st.selectbox("Product", prod_names) if prod_names else st.text_input("Product")
                d_qty    = st.number_input("Quantity", 0.0, step=1.0)
                d_date   = st.date_input("Date", date.today())
            with c2:
                d_reason = st.selectbox("Reason", ["Expired","Physical Damage","Water Damage","Fire","Theft","Quality Issue","Other"])
                d_value  = st.number_input("Estimated Loss Value", 0.0, step=10.0)
                d_notes  = st.text_area("Notes", height=60)
            if st.form_submit_button("Record Damage →", use_container_width=True):
                if d_qty > 0:
                    dr = load_table("damage_records")
                    dr.append({"id":gen_id("DMG"),"date":str(d_date),"product":d_prod,
                               "qty":d_qty,"reason":d_reason,"value":d_value,"notes":d_notes,
                               "by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("damage_records", dr)
                    for p in products:
                        if p["name"]==d_prod: p["stock"] = max(0, float(p.get("stock",0))-d_qty)
                    save_table("products", products)
                    ok("Damage recorded and stock adjusted!")
                    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: WAREHOUSES
# ══════════════════════════════════════════════════════════════════════════════
def page_warehouses():
    section_header("🏭", "Warehouse Management")
    tab1, tab2 = st.tabs(["Warehouse List","Add Warehouse"])
    with tab1:
        wh = load_table("warehouses")
        if wh: df_display(pd.DataFrame(wh))
        else: info_panel("No warehouses added yet.")
    with tab2:
        with st.form("wh_form"):
            c1,c2 = st.columns(2)
            with c1:
                wn = st.text_input("Warehouse Name *"); wcode = st.text_input("Code")
                wcity = st.text_input("City"); wcap = st.number_input("Capacity (units)", 0.0, step=1.0)
            with c2:
                waddr    = st.text_area("Address", height=70); wmanager = st.text_input("Manager")
                wphone   = st.text_input("Phone");             wnotes   = st.text_area("Notes", height=40)
            if st.form_submit_button("Save Warehouse →"):
                if wn:
                    wh = load_table("warehouses")
                    wh.append({"id":gen_id("WH"),"name":wn,"code":wcode,"city":wcity,
                               "capacity":wcap,"address":waddr,"manager":wmanager,
                               "phone":wphone,"notes":wnotes,"created":today_str()})
                    save_table("warehouses", wh); ok(f"Warehouse '{wn}' added!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PRICE LISTS
# ══════════════════════════════════════════════════════════════════════════════
def page_price_lists():
    section_header("💰", "Price Lists")
    products = load_table("products")
    if products:
        df = pd.DataFrame([{"SKU":p.get("sku",""),"Product":p.get("name",""),"Unit":p.get("unit",""),
                             "Cost":p.get("cost_price",0),"Retail":p.get("sale_price",0),
                             "Wholesale":p.get("sale_price2",0),"Stock":p.get("stock",0)} for p in products])
        df_display(df)
        xl = df_to_excel_bytes({"Price List": df})
        st.markdown('<div class="dl-btn">'+make_download_link(xl,"price_list.xlsx","📥 Download Price List (Excel)")+'</div>', unsafe_allow_html=True)
    else: info_panel("No products yet.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: POINT OF SALE
# ══════════════════════════════════════════════════════════════════════════════
def page_pos():
    section_header("🛒", "Point of Sale")
    products  = load_table("products")
    customers = load_table("customers")
    cust_names= ["Walk-in"] + [c["name"] for c in customers]
    prod_dict = {p["name"]: p for p in products}
    settings  = get_settings()

    if "pos_cart" not in st.session_state: st.session_state["pos_cart"] = []

    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.markdown("**🔍 Add Items to Cart**")
        c1,c2,c3 = st.columns([3,1,1])
        with c1:
            prod_names = [p["name"] for p in products if float(p.get("stock",0))>0]
            pos_prod   = st.selectbox("Product", prod_names if prod_names else ["No stock"], key="pos_prod")
        with c2: pos_qty   = st.number_input("Qty",   1.0, step=1.0, key="pos_qty")
        with c3:
            p_data    = prod_dict.get(pos_prod, {})
            pos_price = st.number_input("Price", 0.0, step=1.0, key="pos_price",
                                        value=float(p_data.get("sale_price",0)))
        if st.button("➕ Add to Cart", key="pos_add"):
            if pos_prod and pos_prod != "No stock" and pos_qty > 0:
                avail = float(prod_dict.get(pos_prod,{}).get("stock",0))
                if pos_qty > avail:
                    warn(f"Only {avail} units in stock!")
                else:
                    st.session_state["pos_cart"].append({
                        "product": pos_prod, "qty": pos_qty, "price": pos_price,
                        "total": pos_qty*pos_price,
                        "cost": float(prod_dict.get(pos_prod,{}).get("cost_price",0)) * pos_qty
                    })
                    st.rerun()

        if st.session_state["pos_cart"]:
            st.markdown("**🛒 Cart**")
            cart_df = pd.DataFrame(st.session_state["pos_cart"])
            st.dataframe(cart_df[["product","qty","price","total"]], use_container_width=True, height=200)
            for i, item in enumerate(st.session_state["pos_cart"]):
                if st.button(f"🗑️ Remove {item['product']}", key=f"rm_{i}"):
                    st.session_state["pos_cart"].pop(i); st.rerun()

    with col_r:
        st.markdown("**💰 Checkout**")
        subtotal     = sum(i["total"] for i in st.session_state["pos_cart"])
        cost_total   = sum(i["cost"]  for i in st.session_state["pos_cart"])
        customer     = st.selectbox("Customer", cust_names, key="pos_cust")
        discount_pct = st.number_input("Discount %", 0.0, 100.0, 0.0, step=0.5, key="pos_disc")
        use_tax      = st.checkbox("Apply Tax", value=False)
        tax_rate     = float(settings.get("tax_rate",0)) if use_tax else 0.0
        payment_mode = st.selectbox("Payment Mode", ["Cash","Credit","Bank Transfer","Mobile Banking","Cheque"])
        disc_amt     = subtotal * discount_pct / 100
        tax_amt      = (subtotal-disc_amt) * tax_rate / 100
        total        = subtotal - disc_amt + tax_amt
        amount_paid  = st.number_input("Amount Paid", 0.0, step=100.0, value=total, key="pos_paid")
        change       = amount_paid - total

        st.markdown(f"""
        <div class="receipt-card" style="margin-top:8px;">
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;">
                <span style="color:#64748B">Subtotal</span><b style="color:#E2E8F0">{currency(subtotal)}</b>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;">
                <span style="color:#64748B">Discount</span><b style="color:#F87171">-{currency(disc_amt)}</b>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;">
                <span style="color:#64748B">Tax ({tax_rate:.0f}%)</span><b style="color:#E2E8F0">{currency(tax_amt)}</b>
            </div>
            <hr style="border:none;border-top:1px solid rgba(255,255,255,0.08);margin:8px 0;">
            <div style="display:flex;justify-content:space-between;font-size:1.1rem;font-weight:800;">
                <span style="color:#E2E8F0">Total</span><span style="color:#818CF8">{currency(total)}</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:13px;margin-top:6px;">
                <span style="color:#64748B">Change</span>
                <b style="color:{'#6EE7B7' if change>=0 else '#F87171'}">{currency(change)}</b>
            </div>
        </div>""", unsafe_allow_html=True)

        if st.button("✅ Complete Sale", key="pos_complete", use_container_width=True):
            if not st.session_state["pos_cart"]:
                err("Cart is empty!")
            elif amount_paid < total and payment_mode == "Cash":
                err("Insufficient payment!")
            else:
                sale_id = gen_id("POS")
                pos_sales = load_table("pos_sales")
                pos_sales.append({
                    "id": sale_id, "date": today_str(), "time": now_str(),
                    "customer": customer, "items": st.session_state["pos_cart"],
                    "subtotal": subtotal, "discount_pct": discount_pct, "discount_amt": disc_amt,
                    "tax_rate": tax_rate, "tax_amt": tax_amt, "total": total,
                    "cost_total": cost_total, "amount_paid": amount_paid, "change": change,
                    "payment_mode": payment_mode, "created_by": st.session_state["user"]["username"]
                })
                save_table("pos_sales", pos_sales)
                # Deduct stock
                prods = load_table("products")
                for item in st.session_state["pos_cart"]:
                    for p in prods:
                        if p["name"] == item["product"]:
                            p["stock"] = max(0, float(p.get("stock",0)) - item["qty"])
                save_table("products", prods)
                # Update customer balance if credit
                if payment_mode == "Credit":
                    adjust_customer_balance(customer, total)
                else:
                    # Record receipt
                    recs = load_table("receipts")
                    recs.append({"id":gen_id("RCP"),"ref":sale_id,"date":today_str(),
                                 "party":customer,"amount":amount_paid,"mode":payment_mode,
                                 "type":"Receipt","notes":f"POS Sale {sale_id}","created_at":now_str()})
                    save_table("receipts", recs)
                log_audit(st.session_state["user"]["username"],"POS_SALE",f"{sale_id}: {currency(total)}")
                st.session_state["pos_cart"] = []
                ok(f"Sale {sale_id} completed! Change: {currency(change)}")
                st.rerun()

    st.divider()
    st.markdown("**📋 Today's Sales**")
    today_sales = [s for s in load_table("pos_sales") if s.get("date","")[:10] == today_str()]
    if today_sales:
        df_ts = pd.DataFrame([{
            "ID":s["id"],"Time":s.get("time",""),"Customer":s.get("customer",""),
            "Total":currency(s.get("total",0)),"Mode":s.get("payment_mode","")
        } for s in today_sales[::-1]])
        df_display(df_ts, 280)
        st.metric("Today's Revenue", currency(sum(float(s.get("total",0)) for s in today_sales)))

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SALE ORDERS
# ══════════════════════════════════════════════════════════════════════════════
def page_sale_orders():
    section_header("📋", "Sale Orders")
    tab1, tab2 = st.tabs(["Order List","New Order"])
    products  = load_table("products"); customers = load_table("customers")
    prod_dict = {p["name"]:p for p in products}
    cust_names = [c["name"] for c in customers]

    with tab1:
        orders = load_table("sale_orders")
        if orders:
            c1,c2 = st.columns(2)
            with c1: so_search = st.text_input("🔍 Search", key="so_s")
            with c2: so_status = st.selectbox("Status", ["All","Draft","Confirmed","Delivered","Cancelled"])
            filtered = orders
            if so_search: filtered = [o for o in filtered if so_search.lower() in str(o).lower()]
            if so_status != "All": filtered = [o for o in filtered if o.get("status","")==so_status]
            df = pd.DataFrame([{
                "ID":o["id"],"Date":o.get("date",""),"Customer":o.get("customer",""),
                "Total":currency(o.get("total",0)),"Status":o.get("status",""),"Type":o.get("type","Order")
            } for o in filtered[::-1]])
            df_display(df)
        else: info_panel("No sale orders yet.")

    with tab2:
        if "so_cart" not in st.session_state: st.session_state["so_cart"] = []
        c1,c2 = st.columns(2)
        with c1:
            so_id   = st.text_input("Order #", value=gen_id("SO"))
            so_cust = st.selectbox("Customer", cust_names) if cust_names else st.text_input("Customer")
            so_date = st.date_input("Order Date", date.today())
        with c2:
            so_del   = st.date_input("Delivery Date", date.today()+timedelta(days=3))
            so_stat  = st.selectbox("Status", ["Draft","Confirmed","Delivered","Cancelled"])
            so_notes = st.text_area("Notes", height=60)
        c1,c2,c3 = st.columns([3,1,1])
        with c1: so_prod  = st.selectbox("Product", [p["name"] for p in products], key="so_p")
        with c2: so_qty   = st.number_input("Qty",   1.0, step=1.0, key="so_q")
        with c3: so_price = st.number_input("Price", 0.0, step=1.0, key="so_pr",
                                             value=float(prod_dict.get(so_prod,{}).get("sale_price",0)) if products else 0.0)
        if st.button("➕ Add Item"):
            st.session_state["so_cart"].append({"product":so_prod,"qty":so_qty,"price":so_price,"total":so_qty*so_price})
            st.rerun()
        if st.session_state["so_cart"]:
            st.dataframe(pd.DataFrame(st.session_state["so_cart"]), use_container_width=True)
            so_total = sum(i["total"] for i in st.session_state["so_cart"])
            st.write(f"**Total: {currency(so_total)}**")
            if st.button("✅ Create Order", type="primary"):
                orders = load_table("sale_orders")
                orders.append({"id":so_id,"date":str(so_date),"customer":so_cust,
                                "delivery_date":str(so_del),"status":so_stat,
                                "items":st.session_state["so_cart"],"total":so_total,
                                "notes":so_notes,"type":"Order",
                                "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("sale_orders", orders)
                st.session_state["so_cart"] = []
                ok(f"Order {so_id} created!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ADVANCE SALES
# ══════════════════════════════════════════════════════════════════════════════
def page_advance_sales():
    section_header("🔄", "Advance Sales")
    tab1, tab2, tab3 = st.tabs(["Advance Sales List","New Advance Sale","Payments & Edit"])
    products  = load_table("products"); customers = load_table("customers")
    cust_names = [c["name"] for c in customers]
    prod_names = [p["name"] for p in products]

    with tab1:
        adv = load_table("advance_sales")
        if adv:
            c1,c2 = st.columns(2)
            with c1: adv_s = st.text_input("🔍 Search", key="adv_s")
            with c2: adv_f = st.selectbox("Status", ["All","Pending","Partially Paid","Fully Paid","Delivered","Cancelled"])
            filtered = adv
            if adv_s: filtered = [a for a in filtered if adv_s.lower() in str(a).lower()]
            if adv_f != "All": filtered = [a for a in filtered if a.get("status","") == adv_f]
            df = pd.DataFrame([{
                "ID":a["id"],"Customer":a.get("customer",""),
                "Product":a.get("product",""),"Total":currency(a.get("total",0)),
                "Paid":currency(a.get("advance_paid",0)),
                "Balance":currency(float(a.get("total",0))-float(a.get("advance_paid",0))),
                "Status":a.get("status",""),"Delivery":a.get("delivery_date","")
            } for a in filtered[::-1]])
            df_display(df)
            pending_total = sum(float(a.get("total",0))-float(a.get("advance_paid",0)) for a in adv if a.get("status") not in ("Fully Paid","Cancelled"))
            st.metric("Total Pending Balance", currency(pending_total))
        else: info_panel("No advance sales yet.")

    with tab2:
        with st.form("new_adv"):
            c1,c2 = st.columns(2)
            with c1:
                adv_cust    = st.selectbox("Customer", cust_names) if cust_names else st.text_input("Customer")
                adv_prod    = st.selectbox("Product",  prod_names) if prod_names else st.text_input("Product")
                adv_qty     = st.number_input("Quantity",     1.0, step=1.0)
                adv_price   = st.number_input("Price/Unit",   0.0, step=1.0)
            with c2:
                adv_advance = st.number_input("Advance Paid", 0.0, step=100.0)
                adv_del     = st.date_input("Delivery Date",  date.today()+timedelta(days=7))
                adv_mode    = st.selectbox("Payment Mode", ["Cash","Bank Transfer","Cheque","Mobile Banking"])
                adv_notes   = st.text_area("Notes", height=55)
            if st.form_submit_button("Save Advance Sale →", use_container_width=True):
                if adv_qty > 0 and adv_price > 0:
                    total  = adv_qty * adv_price
                    bal    = total - adv_advance
                    status = "Fully Paid" if bal <= 0 else ("Partially Paid" if adv_advance > 0 else "Pending")
                    adv_id = gen_id("ADV")
                    adv    = load_table("advance_sales")
                    payment_hist = []
                    if adv_advance > 0:
                        payment_hist.append({"date":today_str(),"amount":adv_advance,"mode":adv_mode,
                                             "notes":"Initial advance","by":st.session_state["user"]["username"]})
                    adv.append({"id":adv_id,"date":today_str(),"customer":adv_cust,
                                "product":adv_prod,"qty":adv_qty,"price":adv_price,
                                "total":total,"advance_paid":adv_advance,"balance":max(0,bal),
                                "status":status,"delivery_date":str(adv_del),
                                "payment_mode":adv_mode,"notes":adv_notes,"payments":payment_hist,
                                "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("advance_sales", adv)
                    if adv_advance > 0:
                        recs = load_table("receipts")
                        recs.append({"id":gen_id("RCP"),"ref":adv_id,"date":today_str(),
                                     "party":adv_cust,"amount":adv_advance,"mode":adv_mode,
                                     "type":"Receipt","notes":f"Advance for {adv_id}","created_at":now_str()})
                        save_table("receipts", recs)
                    if bal > 0:
                        adjust_customer_balance(adv_cust, bal)
                    log_audit(st.session_state["user"]["username"],"ADVANCE_SALE",f"{adv_id}: {currency(total)}")
                    ok(f"Advance sale {adv_id} created! Balance: {currency(max(0,bal))}")
                    st.rerun()

    with tab3:
        adv     = load_table("advance_sales")
        pending = [a for a in adv if a.get("status") not in ("Fully Paid","Cancelled")]
        if not pending:
            info_panel("No pending advance sales."); return
        adv_opts = {f"{a['id']} — {a.get('customer','')} — Bal: {currency(float(a.get('total',0))-float(a.get('advance_paid',0)))}": a for a in pending}
        sel = adv_opts[st.selectbox("Select Advance Sale", list(adv_opts.keys()))]
        c1,c2,c3 = st.columns(3)
        with c1: metric_card("Total",    currency(sel.get("total",0)),        "blue")
        with c2: metric_card("Paid",     currency(sel.get("advance_paid",0)), "green")
        with c3: metric_card("Balance",  currency(float(sel.get("total",0))-float(sel.get("advance_paid",0))), "red")

        if sel.get("payments"):
            st.markdown("**💳 Payment History**")
            df_display(pd.DataFrame(sel["payments"]), 180)

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**➕ Add Payment**")
            with st.form("add_adv_pay"):
                bal_due = float(sel.get("total",0)) - float(sel.get("advance_paid",0))
                pay_amt  = st.number_input("Payment Amount", 0.0, max_value=bal_due, step=100.0)
                pay_mode = st.selectbox("Mode", ["Cash","Bank Transfer","Cheque","Mobile Banking"])
                pay_date = st.date_input("Date", date.today())
                pay_note = st.text_area("Notes", height=55)
                if st.form_submit_button("Record Payment →", use_container_width=True):
                    if pay_amt > 0:
                        new_paid   = float(sel.get("advance_paid",0)) + pay_amt
                        new_bal    = float(sel.get("total",0)) - new_paid
                        new_status = "Fully Paid" if new_bal <= 0 else "Partially Paid"
                        for a in adv:
                            if a["id"] == sel["id"]:
                                a["advance_paid"] = new_paid; a["balance"] = max(0,new_bal); a["status"] = new_status
                                if "payments" not in a: a["payments"] = []
                                a["payments"].append({"date":str(pay_date),"amount":pay_amt,
                                                      "mode":pay_mode,"notes":pay_note,
                                                      "by":st.session_state["user"]["username"]})
                        save_table("advance_sales", adv)
                        recs = load_table("receipts")
                        recs.append({"id":gen_id("RCP"),"ref":sel["id"],"date":str(pay_date),
                                     "party":sel.get("customer",""),"amount":pay_amt,"mode":pay_mode,
                                     "type":"Receipt","notes":f"Advance payment {sel['id']}","created_at":now_str()})
                        save_table("receipts", recs)
                        adjust_customer_balance(sel.get("customer",""), -pay_amt)
                        ok(f"Payment of {currency(pay_amt)} recorded! New balance: {currency(max(0,new_bal))}"); st.rerun()

        with c2:
            st.markdown("**✏️ Edit Details**")
            with st.form("edit_adv"):
                new_del    = st.date_input("Delivery Date", date.fromisoformat(str(sel.get("delivery_date",today_str()))[:10]))
                new_notes  = st.text_area("Notes", value=sel.get("notes",""), height=55)
                new_status = st.selectbox("Status", ["Pending","Partially Paid","Fully Paid","Delivered","Cancelled"],
                                          index=["Pending","Partially Paid","Fully Paid","Delivered","Cancelled"].index(sel.get("status","Pending")))
                if st.form_submit_button("Save Changes →"):
                    for a in adv:
                        if a["id"] == sel["id"]:
                            a["delivery_date"] = str(new_del); a["notes"] = new_notes; a["status"] = new_status
                    save_table("advance_sales", adv)
                    ok("Updated!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ENGLISH BILLING / INVOICE
# ══════════════════════════════════════════════════════════════════════════════
def page_english_billing():
    section_header("🧾", "Invoice Generator")
    products  = load_table("products"); customers = load_table("customers"); settings = get_settings()
    prod_names = [p["name"] for p in products]; cust_names = [c["name"] for c in customers]
    tab1, tab2 = st.tabs(["Create Invoice","Invoice History"])
    with tab1:
        if "bill_items" not in st.session_state: st.session_state["bill_items"] = []
        c1,c2,c3 = st.columns(3)
        with c1:
            inv_no   = st.text_input("Invoice #", value=gen_id("INV"))
            inv_date = st.date_input("Date", date.today())
            due_date = st.date_input("Due Date", date.today()+timedelta(days=30))
        with c2:
            bill_cust = st.selectbox("Bill To", cust_names) if cust_names else st.text_input("Customer")
            inv_cur   = st.selectbox("Currency", ["PKR","USD","EUR","GBP"])
            tax_rate  = st.number_input("Tax %", 0.0, 100.0, settings.get("tax_rate",17.0))
        with c3:
            inv_notes = st.text_area("Terms", height=80, value="Payment due within 30 days.")
        c1,c2,c3,c4 = st.columns([3,1,1,1])
        with c1: bp  = st.selectbox("Product/Service", prod_names+["Custom Item"], key="bp")
        with c2: bq  = st.number_input("Qty",   1.0, step=1.0, key="bq")
        p_ = next((x for x in products if x["name"]==bp), {})
        with c3: bpr = st.number_input("Unit Price", 0.0, step=1.0, key="bpr", value=float(p_.get("sale_price",0)))
        with c4: bd  = st.number_input("Disc%", 0.0, 100.0, 0.0, key="bd")
        if st.button("➕ Add Line Item"):
            da = bq*bpr*bd/100
            st.session_state["bill_items"].append({"Description":bp,"Qty":bq,"Unit Price":bpr,"Disc%":bd,"Amount":bq*bpr-da})
            st.rerun()
        if st.session_state["bill_items"]:
            df = pd.DataFrame(st.session_state["bill_items"]); st.dataframe(df, use_container_width=True)
            sub = sum(i["Amount"] for i in st.session_state["bill_items"])
            tax = sub*tax_rate/100; grand = sub+tax
            st.markdown(f"**Subtotal:** {inv_cur} {sub:,.2f}  |  **Tax:** {inv_cur} {tax:,.2f}  |  **Grand Total:** {inv_cur} {grand:,.2f}")
            c1,c2 = st.columns(2)
            with c1:
                if st.button("💾 Save Invoice", type="primary", use_container_width=True):
                    so = load_table("sale_orders")
                    so.append({"id":inv_no,"date":str(inv_date),"due_date":str(due_date),
                               "customer":bill_cust,"items":st.session_state["bill_items"],
                               "subtotal":sub,"tax_rate":tax_rate,"tax_amt":tax,"total":grand,
                               "currency":inv_cur,"notes":inv_notes,"status":"Confirmed","type":"Invoice",
                               "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("sale_orders", so)
                    st.session_state["bill_items"] = []
                    adjust_customer_balance(bill_cust, grand)
                    ok(f"Invoice {inv_no} saved!"); st.rerun()
            with c2:
                if st.button("🗑️ Clear", use_container_width=True):
                    st.session_state["bill_items"] = []; st.rerun()
    with tab2:
        orders = load_table("sale_orders")
        invs = [o for o in orders if o.get("type")=="Invoice"]
        if invs:
            df = pd.DataFrame([{"Invoice#":i["id"],"Date":i.get("date",""),"Customer":i.get("customer",""),
                                 "Total":currency(i.get("total",0)),"Status":i.get("status","")} for i in invs])
            df_display(df)
        else: info_panel("No invoices yet.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PURCHASE ORDERS
# ══════════════════════════════════════════════════════════════════════════════
def page_purchase_orders():
    section_header("📥", "Purchase Orders")
    products  = load_table("products"); suppliers = load_table("suppliers")
    sup_names = [s["name"] for s in suppliers]; prod_names = [p["name"] for p in products]
    prod_dict = {p["name"]:p for p in products}
    tab1, tab2, tab3 = st.tabs(["PO List","New Purchase Order","Receive Stock"])

    with tab1:
        pos_list = load_table("purchase_orders")
        if pos_list:
            df = pd.DataFrame([{"PO#":p["id"],"Date":p.get("date",""),"Supplier":p.get("supplier",""),
                                 "Total":currency(p.get("total",0)),"Status":p.get("status",""),
                                 "Received":p.get("received",False)} for p in pos_list])
            df_display(df)
        else: info_panel("No purchase orders yet.")

    with tab2:
        if "po_cart" not in st.session_state: st.session_state["po_cart"] = []
        c1,c2 = st.columns(2)
        with c1:
            po_sup  = st.selectbox("Supplier", sup_names) if sup_names else st.text_input("Supplier")
            po_date = st.date_input("PO Date", date.today())
            po_del  = st.date_input("Expected Delivery", date.today()+timedelta(days=5))
        with c2:
            po_stat  = st.selectbox("Status", ["Draft","Sent","Received","Partially Received","Cancelled"])
            po_notes = st.text_area("Notes", height=60)
        c1,c2,c3 = st.columns([3,1,1])
        with c1: po_prod  = st.selectbox("Add Product", prod_names, key="po_ap") if prod_names else st.text_input("Product",key="po_ap")
        with c2: po_qty   = st.number_input("Qty", 1.0, step=1.0, key="po_qty")
        with c3: po_price = st.number_input("Cost Price", 0.0, step=1.0, key="po_pr",
                                             value=float(prod_dict.get(po_prod,{}).get("cost_price",0)) if prod_names else 0.0)
        if st.button("➕ Add to PO"):
            st.session_state["po_cart"].append({"product":po_prod,"qty":po_qty,"price":po_price,"total":po_qty*po_price}); st.rerun()
        if st.session_state["po_cart"]:
            st.dataframe(pd.DataFrame(st.session_state["po_cart"]), use_container_width=True)
            total = sum(i["total"] for i in st.session_state["po_cart"])
            st.write(f"**Total: {currency(total)}**")
            if st.button("✅ Create PO", type="primary"):
                pos_list = load_table("purchase_orders"); oid = gen_id("PO")
                pos_list.append({"id":oid,"date":str(po_date),"supplier":po_sup,
                                  "delivery_date":str(po_del),"status":po_stat,
                                  "items":st.session_state["po_cart"],"total":total,"notes":po_notes,
                                  "received":po_stat=="Received",
                                  "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("purchase_orders", pos_list)
                if po_stat == "Received":
                    prods = load_table("products")
                    for item in st.session_state["po_cart"]:
                        for p in prods:
                            if p["name"]==item["product"]: p["stock"] = float(p.get("stock",0))+item["qty"]
                    save_table("products", prods)
                st.session_state["po_cart"] = []
                ok(f"Purchase Order {oid} created!"); st.rerun()

    with tab3:
        pos_list = load_table("purchase_orders")
        pending_pos = [p for p in pos_list if not p.get("received") and p.get("status") not in ("Cancelled",)]
        if pending_pos:
            po_opts = {f"{p['id']} — {p.get('supplier','')} — {currency(p.get('total',0))}": p for p in pending_pos}
            sel_po  = po_opts[st.selectbox("Select PO to Receive", list(po_opts.keys()))]
            st.dataframe(pd.DataFrame(sel_po.get("items",[])), use_container_width=True)
            if st.button("✅ Mark as Received & Update Stock"):
                prods = load_table("products")
                for item in sel_po.get("items",[]):
                    for p in prods:
                        if p["name"]==item["product"]: p["stock"] = float(p.get("stock",0))+item["qty"]
                save_table("products", prods)
                for po in pos_list:
                    if po["id"] == sel_po["id"]: po["received"] = True; po["status"] = "Received"
                save_table("purchase_orders", pos_list)
                ok("Stock received and updated!"); st.rerun()
        else: info_panel("No pending purchase orders to receive.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SUPPLIER MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
def page_supplier_management():
    section_header("🏪", "Supplier Management")
    tab1, tab2 = st.tabs(["Supplier List","Add Supplier"])
    with tab1:
        suppliers = load_table("suppliers")
        if suppliers:
            df = pd.DataFrame([{"Name":s.get("name",""),"Phone":s.get("phone",""),
                                 "City":s.get("city",""),"Balance":currency(s.get("balance",0)),
                                 "Category":s.get("category","")} for s in suppliers])
            df_display(df)
        else: info_panel("No suppliers yet.")
    with tab2:
        with st.form("add_sup"):
            c1,c2 = st.columns(2)
            with c1:
                sname = st.text_input("Supplier Name *"); sphone = st.text_input("Phone")
                semail = st.text_input("Email"); scity = st.text_input("City")
            with c2:
                scat     = st.text_input("Category / Products Supplied")
                saddress = st.text_area("Address", height=70)
                sbalance = st.number_input("Opening Balance (Payable)", 0.0, step=100.0)
                snotes   = st.text_area("Notes", height=40)
            if st.form_submit_button("Save Supplier →", use_container_width=True):
                if sname:
                    sups = load_table("suppliers")
                    sups.append({"id":gen_id("SUP"),"name":sname,"phone":sphone,"email":semail,
                                 "city":scity,"category":scat,"address":saddress,"balance":sbalance,
                                 "notes":snotes,"created":today_str()})
                    save_table("suppliers", sups)
                    ok(f"Supplier '{sname}' added!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: CUSTOMERS
# ══════════════════════════════════════════════════════════════════════════════
def page_customers():
    section_header("👥", "Customer Management")
    tab1, tab2, tab3, tab4 = st.tabs(["Customer List","Add Customer","Customer Ledger","Update Balance"])

    with tab1:
        customers = load_table("customers")
        c1,c2 = st.columns(2)
        with c1: cs = st.text_input("🔍 Search", key="cs")
        with c2: ct = st.selectbox("Type", ["All","Customer","Supplier","Both"])
        filtered = customers
        if cs: filtered = [c for c in filtered if cs.lower() in c.get("name","").lower() or cs.lower() in c.get("phone","").lower()]
        if ct != "All": filtered = [c for c in filtered if c.get("type","") == ct]
        if filtered:
            df = pd.DataFrame(filtered)
            cols = [c for c in ["name","phone","type","city","email","balance","credit_limit","group"] if c in df.columns]
            df_display(df[cols])
        else: info_panel("No customers found.")

    with tab2:
        with st.form("add_cust"):
            c1,c2,c3 = st.columns(3)
            with c1:
                cname  = st.text_input("Name *"); cphone = st.text_input("Phone *")
                cemail = st.text_input("Email"); ccity  = st.text_input("City")
            with c2:
                ctype    = st.selectbox("Type", ["Customer","Supplier","Both"])
                cgroup   = st.selectbox("Group", ["Retail","Wholesale","VIP","General","Corporate"])
                ccnic    = st.text_input("CNIC"); cbank = st.text_input("Bank Account")
            with c3:
                caddress = st.text_area("Address", height=70)
                ccredit  = st.number_input("Credit Limit", 0.0, step=1000.0)
                cbalance = st.number_input("Opening Balance", 0.0, step=100.0)
                cnotes   = st.text_area("Notes", height=40)
            if st.form_submit_button("Save Customer →", use_container_width=True):
                if cname and cphone:
                    custs = load_table("customers")
                    custs.append({"id":gen_id("CST"),"name":cname,"phone":cphone,"email":cemail,
                                  "city":ccity,"type":ctype,"group":cgroup,"cnic":ccnic,
                                  "bank":cbank,"address":caddress,"credit_limit":ccredit,
                                  "balance":cbalance,"notes":cnotes,"created":today_str()})
                    save_table("customers", custs)
                    log_audit(st.session_state["user"]["username"],"ADD_CUSTOMER",cname)
                    ok(f"Customer '{cname}' added!"); st.rerun()
                else: err("Name and Phone required.")

    with tab3:
        customers = load_table("customers"); cust_names = [c["name"] for c in customers]
        if cust_names:
            sel  = st.selectbox("Select Customer", cust_names, key="cust_led_sel")
            cdata= next((c for c in customers if c["name"]==sel), {})
            if cdata:
                c1,c2,c3 = st.columns(3)
                with c1: metric_card("Balance",     currency(cdata.get("balance",0)),      "red")
                with c2: metric_card("Credit Limit",currency(cdata.get("credit_limit",0)), "blue")
                with c3: metric_card("Type",        cdata.get("type",""),                  "green")
                pos_sales = load_table("pos_sales"); receipts = load_table("receipts"); adv_sales = load_table("advance_sales")
                rows = []
                for s in pos_sales:
                    if s.get("customer","") == sel:
                        rows.append({"Date":s.get("date",""),"Type":"POS Sale","Ref":s.get("id",""),"Debit":s.get("total",0),"Credit":0})
                for r in receipts:
                    if r.get("party","") == sel:
                        rows.append({"Date":r.get("date",""),"Type":"Receipt","Ref":r.get("ref",""),"Debit":0,"Credit":r.get("amount",0)})
                for a in adv_sales:
                    if a.get("customer","") == sel:
                        rows.append({"Date":a.get("date",""),"Type":"Advance Sale","Ref":a.get("id",""),"Debit":a.get("total",0),"Credit":a.get("advance_paid",0)})
                if rows:
                    rows.sort(key=lambda x: x["Date"])
                    bal = 0
                    for r in rows: bal += float(r["Debit"])-float(r["Credit"]); r["Running Balance"] = bal
                    df_display(pd.DataFrame(rows))
                else: info_panel("No transactions for this customer.")

    with tab4:
        customers = load_table("customers"); cust_names = [c["name"] for c in customers]
        if cust_names:
            sel_c = st.selectbox("Select Customer", cust_names, key="upd_bal_sel")
            cdata = next((c for c in customers if c["name"]==sel_c), {})
            c1,c2,c3 = st.columns(3)
            with c1:
                st.metric("Current Balance", currency(cdata.get("balance",0)))
            with c2:
                adj_type = st.selectbox("Adjustment Type", ["Add to Balance (Debit)","Subtract from Balance (Credit)"])
            with c3:
                adj_amt  = st.number_input("Amount", 0.0, step=100.0, key="bal_adj_amt")
            adj_note = st.text_input("Reason / Note")
            if st.button("💾 Update Balance"):
                if adj_amt > 0:
                    delta = adj_amt if "Add" in adj_type else -adj_amt
                    adjust_customer_balance(sel_c, delta)
                    log_audit(st.session_state["user"]["username"],"BALANCE_ADJUST",f"{sel_c}: {adj_type} {adj_amt}")
                    ok(f"Balance updated for {sel_c}!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DEBTORS & CREDITORS
# ══════════════════════════════════════════════════════════════════════════════
def page_debtors_creditors():
    section_header("⚖️", "Debtors & Creditors")
    customers = load_table("customers"); suppliers = load_table("suppliers")
    tab1, tab2 = st.tabs(["Debtors (Receivables)","Creditors (Payables)"])
    with tab1:
        debtors = [c for c in customers if float(c.get("balance",0)) > 0]
        if debtors:
            total = sum(float(c.get("balance",0)) for c in debtors)
            metric_card("Total Receivable", currency(total), "red")
            df = pd.DataFrame([{"Customer":d.get("name",""),"Phone":d.get("phone",""),
                                 "Balance":currency(d.get("balance",0)),"City":d.get("city",""),
                                 "Group":d.get("group","")} for d in sorted(debtors,key=lambda x:float(x.get("balance",0)),reverse=True)])
            df_display(df)
        else: info_panel("No debtors. All balances cleared! 🎉","green")
    with tab2:
        creditors = [s for s in suppliers if float(s.get("balance",0)) > 0]
        if creditors:
            total = sum(float(s.get("balance",0)) for s in creditors)
            metric_card("Total Payable", currency(total), "amber")
            df = pd.DataFrame([{"Supplier":s.get("name",""),"Phone":s.get("phone",""),
                                 "Balance":currency(s.get("balance",0)),"Category":s.get("category","")} for s in creditors])
            df_display(df)
        else: info_panel("No payables outstanding.", "green")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TASKS & FOLLOW-UPS
# ══════════════════════════════════════════════════════════════════════════════
def page_tasks():
    section_header("✅", "Tasks & Follow-ups")
    customers = load_table("customers"); cust_names = [""] + [c["name"] for c in customers]
    tab1, tab2 = st.tabs(["Task List","Add Task"])
    with tab1:
        tasks = load_table("tasks")
        c1,c2 = st.columns(2)
        with c1: tf = st.selectbox("Filter", ["All","Pending","In Progress","Completed","Overdue"])
        with c2: tp = st.selectbox("Priority", ["All","High","Medium","Low"])
        filtered = tasks
        if tf != "All": filtered = [t for t in filtered if t.get("status","")==tf]
        if tp != "All": filtered = [t for t in filtered if t.get("priority","")==tp]
        if filtered:
            df = pd.DataFrame(filtered[::-1])
            cols = [c for c in ["title","description","assigned_to","due_date","priority","status","customer"] if c in df.columns]
            df_display(df[cols])
        else: info_panel("No tasks found.")
        # Mark complete
        if tasks:
            task_opts = {f"{t['id']} — {t.get('title','')} [{t.get('status','')}]": t for t in tasks if t.get("status") != "Completed"}
            if task_opts:
                sel_t = st.selectbox("Mark Task as Complete", list(task_opts.keys()), key="task_complete_sel")
                if st.button("✅ Mark Complete"):
                    for t in tasks:
                        if t["id"] == task_opts[sel_t]["id"]: t["status"] = "Completed"; t["completed_at"] = now_str()
                    save_table("tasks", tasks); ok("Task marked complete!"); st.rerun()
    with tab2:
        with st.form("add_task"):
            c1,c2 = st.columns(2)
            with c1:
                title       = st.text_input("Task Title *")
                description = st.text_area("Description", height=60)
                customer    = st.selectbox("Related Customer", cust_names)
                assigned_to = st.text_input("Assigned To")
            with c2:
                due_date = st.date_input("Due Date", date.today()+timedelta(days=1))
                priority = st.selectbox("Priority", ["High","Medium","Low"])
                status   = st.selectbox("Status", ["Pending","In Progress"])
                notes    = st.text_area("Notes", height=55)
            if st.form_submit_button("Save Task →", use_container_width=True):
                if title:
                    tasks = load_table("tasks")
                    tasks.append({"id":gen_id("TSK"),"title":title,"description":description,
                                  "customer":customer,"assigned_to":assigned_to,"due_date":str(due_date),
                                  "priority":priority,"status":status,"notes":notes,
                                  "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("tasks", tasks); ok("Task added!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: NOTES
# ══════════════════════════════════════════════════════════════════════════════
def page_notes():
    section_header("📝", "Notes")
    tab1, tab2 = st.tabs(["All Notes","Add Note"])
    with tab1:
        notes = load_table("notes")
        if notes:
            for n in notes[::-1]:
                with st.expander(f"📌 {n.get('title','')} — {n.get('created_at','')[:10]}"):
                    st.write(n.get("content",""))
                    st.caption(f"By: {n.get('created_by','')} | Category: {n.get('category','')}")
        else: info_panel("No notes yet.")
    with tab2:
        with st.form("add_note"):
            title    = st.text_input("Title *")
            category = st.selectbox("Category", ["General","Customer","Finance","Livestock","Reminder","Other"])
            content  = st.text_area("Content", height=150)
            if st.form_submit_button("Save Note →", use_container_width=True):
                if title:
                    notes = load_table("notes")
                    notes.append({"id":gen_id("NOTE"),"title":title,"category":category,"content":content,
                                  "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("notes", notes); ok("Note saved!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LIVESTOCK REGISTER
# ══════════════════════════════════════════════════════════════════════════════
def page_livestock():
    section_header("🐄", "Livestock Register")
    tab1, tab2, tab3 = st.tabs(["Active Animals","Add Animal","Livestock Summary"])
    with tab1:
        livestock = load_table("livestock")
        c1,c2,c3 = st.columns(3)
        with c1: ls_search = st.text_input("🔍 Search", key="ls_s")
        with c2: ls_type   = st.selectbox("Animal Type", ["All","Cow","Buffalo","Goat","Sheep","Bull","Calf","Other"])
        with c3: ls_status = st.selectbox("Status", ["All","Active","Sold","Dead","Transferred"])
        filtered = livestock
        if ls_search: filtered = [l for l in filtered if ls_search.lower() in str(l).lower()]
        if ls_type != "All":   filtered = [l for l in filtered if l.get("animal_type","") == ls_type]
        if ls_status != "All": filtered = [l for l in filtered if l.get("status","") == ls_status]
        if filtered:
            df = pd.DataFrame(filtered)
            cols = [c for c in ["tag_no","name","animal_type","breed","gender","dob","purchase_price","status","shed","is_pregnant"] if c in df.columns]
            df_display(df[cols])
        else: info_panel("No animals found.")
    with tab2:
        with st.form("add_ls"):
            c1,c2,c3 = st.columns(3)
            with c1:
                tag_no      = st.text_input("Tag Number *", value=gen_id("TAG"))
                name        = st.text_input("Name / Nickname")
                animal_type = st.selectbox("Animal Type", ["Cow","Buffalo","Goat","Sheep","Bull","Calf","Other"])
                breed       = st.text_input("Breed")
            with c2:
                gender         = st.selectbox("Gender", ["Female","Male"])
                dob            = st.date_input("Date of Birth", date.today()-timedelta(days=365))
                purchase_price = st.number_input("Purchase Price", 0.0, step=100.0)
                purchase_date  = st.date_input("Purchase Date", date.today())
            with c3:
                shed       = st.text_input("Shed / Location")
                weight     = st.number_input("Weight (KG)", 0.0, step=1.0)
                is_pregnant= st.checkbox("Pregnant")
                notes      = st.text_area("Notes", height=55)
            if st.form_submit_button("Add Animal →", use_container_width=True):
                if tag_no:
                    ls = load_table("livestock")
                    if any(l["tag_no"]==tag_no for l in ls): err("Tag number already exists!")
                    else:
                        ls.append({"id":gen_id("LS"),"tag_no":tag_no,"name":name,
                                   "animal_type":animal_type,"breed":breed,"gender":gender,
                                   "dob":str(dob),"purchase_price":purchase_price,"purchase_date":str(purchase_date),
                                   "shed":shed,"weight":weight,"is_pregnant":is_pregnant,"notes":notes,
                                   "status":"Active","created_by":st.session_state["user"]["username"],"created_at":now_str()})
                        save_table("livestock", ls)
                        log_audit(st.session_state["user"]["username"],"ADD_LIVESTOCK",tag_no)
                        ok(f"Animal {tag_no} added!"); st.rerun()
    with tab3:
        livestock = load_table("livestock")
        if livestock:
            active = [l for l in livestock if l.get("status")=="Active"]
            c1,c2,c3,c4 = st.columns(4)
            with c1: metric_card("Total Animals",  len(livestock), "blue")
            with c2: metric_card("Active",          len(active), "green")
            with c3: metric_card("Sold",            len([l for l in livestock if l.get("status")=="Sold"]), "amber")
            with c4: metric_card("Pregnant Females",len([l for l in active if l.get("is_pregnant")]), "purple")
            by_type = {}
            for l in active: by_type[l.get("animal_type","Other")] = by_type.get(l.get("animal_type","Other"),0)+1
            if by_type:
                st.bar_chart(pd.DataFrame(list(by_type.items()),columns=["Type","Count"]).set_index("Type"))

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MILK PRODUCTION
# ══════════════════════════════════════════════════════════════════════════════
def page_milk():
    section_header("🥛", "Milk Production")
    livestock = load_table("livestock")
    females   = [l for l in livestock if l.get("gender")=="Female" and l.get("status")=="Active"]
    tab1, tab2 = st.tabs(["Milk Records","Record Milk"])
    with tab1:
        milk = load_table("milk_records")
        c1,c2 = st.columns(2)
        with c1: mf = st.date_input("From", date.today().replace(day=1), key="mf")
        with c2: mt = st.date_input("To",   date.today(), key="mt")
        filtered = [m for m in milk if mf.isoformat()<=str(m.get("date",""))[:10]<=mt.isoformat()]
        if filtered:
            df_display(pd.DataFrame(filtered))
            total = sum(float(m.get("quantity",0)) for m in filtered)
            st.metric("Total Milk Produced", f"{total:,.1f} Liters")
        else: info_panel("No milk records in period.")
    with tab2:
        with st.form("milk_rec"):
            c1,c2 = st.columns(2)
            with c1:
                animal_opts = [f"{l['tag_no']} - {l.get('name','')} ({l.get('breed','')})" for l in females]
                animal      = st.selectbox("Animal", animal_opts if animal_opts else ["No female animals"])
                milk_date   = st.date_input("Date", date.today())
                session     = st.selectbox("Session", ["Morning","Evening","Full Day"])
            with c2:
                quantity    = st.number_input("Quantity (Liters)", 0.0, step=0.1)
                fat_content = st.number_input("Fat Content %", 0.0, 10.0, step=0.1)
                price_per_l = st.number_input("Price per Liter", 0.0, step=1.0)
                notes       = st.text_area("Notes", height=55)
            if st.form_submit_button("Record Milk →"):
                milk = load_table("milk_records")
                milk.append({"id":gen_id("MLK"),"date":str(milk_date),
                             "animal":animal.split(" - ")[0] if animal_opts else "",
                             "session":session,"quantity":quantity,"fat_content":fat_content,
                             "price_per_liter":price_per_l,"revenue":quantity*price_per_l,
                             "notes":notes,"recorded_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("milk_records", milk); ok("Milk record saved!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FEED RECORDS
# ══════════════════════════════════════════════════════════════════════════════
def page_feed():
    section_header("🌾", "Feed Records")
    FEED_TYPES = ["Silage","Hay","Concentrate","Wheat Straw","Corn","Bran","Molasses","Mixed","Other"]
    tab1, tab2 = st.tabs(["Feed History","Add Feed Record"])
    with tab1:
        fr = load_table("feed_records")
        if fr:
            df_display(pd.DataFrame(fr))
            total_cost = sum(float(f.get("cost",0)) for f in fr)
            st.metric("Total Feed Cost", currency(total_cost))
        else: info_panel("No feed records yet.")
    with tab2:
        with st.form("feed_rec"):
            c1,c2 = st.columns(2)
            with c1:
                fd     = st.date_input("Date", date.today())
                ft2    = st.selectbox("Feed Type", FEED_TYPES)
                fq     = st.number_input("Quantity", 0.0, step=1.0)
                fu     = st.selectbox("Unit", ["KG","Ton","Bag","Bundle"])
            with c2:
                fuc   = st.number_input("Unit Cost", 0.0, step=1.0)
                fshed = st.text_input("Shed / Group")
                fsup  = st.text_input("Supplier")
                fn    = st.text_area("Notes", height=55)
            if st.form_submit_button("Save Feed Record →"):
                if fq > 0:
                    fr = load_table("feed_records")
                    fr.append({"id":gen_id("FD"),"date":str(fd),"feed_type":ft2,"quantity":fq,
                               "unit":fu,"unit_cost":fuc,"cost":fq*fuc,"shed":fshed,"supplier":fsup,
                               "notes":fn,"recorded_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("feed_records", fr)
                    if fuc > 0:
                        exps = load_table("expenses")
                        exps.append({"id":gen_id("EXP"),"date":str(fd),"category":"Feed",
                                     "description":f"{ft2} for {fshed}","amount":fq*fuc,"paid_by":"Cash",
                                     "vendor":fsup,"notes":fn,
                                     "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                        save_table("expenses", exps)
                    ok("Feed record saved and expense logged!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BREEDING
# ══════════════════════════════════════════════════════════════════════════════
def page_breeding():
    section_header("🐮", "Breeding Records")
    livestock = load_table("livestock")
    females   = [l for l in livestock if l.get("gender")=="Female" and l.get("status")=="Active"]
    males     = [l for l in livestock if l.get("gender")=="Male"   and l.get("status")=="Active"]
    tab1, tab2 = st.tabs(["Breeding History","Add Record"])
    with tab1:
        br = load_table("breeding_records")
        if br: df_display(pd.DataFrame(br))
        else: info_panel("No breeding records yet.")
    with tab2:
        with st.form("breed_rec"):
            c1,c2 = st.columns(2)
            with c1:
                female_opts = [f"{l['tag_no']} - {l.get('name','')} ({l.get('breed','')})" for l in females]
                female      = st.selectbox("Female Animal", female_opts if female_opts else ["No females"])
                male_opts   = [f"{l['tag_no']} - {l.get('name','')} ({l.get('breed','')})" for l in males]+["External Bull","AI"]
                male        = st.selectbox("Sire (Male)", male_opts)
                bd          = st.date_input("Breeding Date", date.today())
                method      = st.selectbox("Method", ["Natural","Artificial Insemination","Embryo Transfer"])
            with c2:
                exp_birth  = st.date_input("Expected Birth", date.today()+timedelta(days=280))
                status     = st.selectbox("Status", ["Pending","Confirmed Pregnant","Aborted","Delivered"])
                offspring  = st.number_input("Offspring Count", 0, step=1)
                notes      = st.text_area("Notes", height=60)
            if st.form_submit_button("Save Record →"):
                br = load_table("breeding_records")
                br.append({"id":gen_id("BR"),"female":female.split(" - ")[0] if female_opts else "",
                           "male":male,"breeding_date":str(bd),"method":method,
                           "expected_birth":str(exp_birth),"status":status,
                           "offspring_count":offspring,"notes":notes,
                           "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("breeding_records", br)
                if status == "Confirmed Pregnant" and female_opts:
                    tag = female.split(" - ")[0]
                    for l in livestock:
                        if l.get("tag_no","") == tag: l["is_pregnant"] = True
                    save_table("livestock", livestock)
                ok("Breeding record saved!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HEALTH RECORDS
# ══════════════════════════════════════════════════════════════════════════════
def page_health():
    section_header("💉", "Livestock Health Records")
    livestock    = load_table("livestock")
    animal_tags  = [f"{l['tag_no']} - {l.get('name','')} ({l.get('animal_type','')})" for l in livestock if l.get("status")=="Active"]
    tab1, tab2 = st.tabs(["Health History","Add Record"])
    with tab1:
        health = load_table("livestock_health")
        if health:
            c1,c2 = st.columns(2)
            with c1: hf = st.date_input("From", date.today().replace(day=1), key="hf")
            with c2: ht = st.date_input("To",   date.today(), key="ht")
            filtered = [h for h in health if hf.isoformat()<=str(h.get("date",""))[:10]<=ht.isoformat()]
            if filtered: df_display(pd.DataFrame(filtered))
            else: info_panel("No records in period.")
        else: info_panel("No health records yet.")
    with tab2:
        with st.form("health_rec"):
            c1,c2 = st.columns(2)
            with c1:
                animal    = st.selectbox("Animal", animal_tags if animal_tags else ["No active animals"])
                rec_date  = st.date_input("Date", date.today())
                rec_type  = st.selectbox("Type", ["Vaccination","Treatment","Deworming","Check-up","Surgery","Emergency"])
                diagnosis = st.text_input("Diagnosis / Condition")
            with c2:
                treatment  = st.text_area("Treatment / Medication", height=60)
                vet        = st.text_input("Veterinarian")
                cost       = st.number_input("Cost", 0.0, step=10.0)
                next_visit = st.date_input("Next Visit", date.today()+timedelta(days=30))
            if st.form_submit_button("Save Health Record →"):
                h = load_table("livestock_health")
                h.append({"id":gen_id("HLT"),"date":str(rec_date),
                          "animal":animal.split(" - ")[0] if animal_tags else "",
                          "type":rec_type,"diagnosis":diagnosis,"treatment":treatment,
                          "vet":vet,"cost":cost,"next_visit":str(next_visit),
                          "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("livestock_health", h)
                if cost > 0:
                    exps = load_table("expenses")
                    exps.append({"id":gen_id("EXP"),"date":str(rec_date),"category":"Veterinary",
                                 "description":f"{rec_type}: {diagnosis}","amount":cost,"paid_by":"Cash",
                                 "vendor":vet,"notes":"","created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("expenses", exps)
                ok("Health record saved!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LIVESTOCK SALES
# ══════════════════════════════════════════════════════════════════════════════
def page_livestock_sales():
    section_header("💰", "Livestock Sales")
    livestock  = load_table("livestock"); customers = load_table("customers")
    active     = [l for l in livestock if l.get("status")=="Active"]
    cust_names = [c["name"] for c in customers]
    tab1, tab2 = st.tabs(["Sales History","Record Sale"])
    with tab1:
        ls_sales = load_table("livestock_sales")
        if ls_sales:
            df = pd.DataFrame([{
                "Date":s.get("date",""),"Tag":s.get("tag_no",""),"Type":s.get("animal_type",""),
                "Customer":s.get("customer",""),"Purchase":currency(s.get("purchase_price",0)),
                "Sale":currency(s.get("sale_price",0)),
                "Profit":currency(float(s.get("sale_price",0))-float(s.get("purchase_price",0))),
                "Mode":s.get("payment_mode","")
            } for s in ls_sales[::-1]])
            df_display(df)
            total_profit = sum(float(s.get("sale_price",0))-float(s.get("purchase_price",0)) for s in ls_sales)
            st.metric("Total Profit from Livestock", currency(total_profit))
        else: info_panel("No livestock sales yet.")
    with tab2:
        if active:
            with st.form("ls_sale"):
                c1,c2 = st.columns(2)
                with c1:
                    animal_opts = [f"{l['tag_no']} - {l.get('name','')} ({l.get('animal_type','')})" for l in active]
                    animal      = st.selectbox("Animal", animal_opts)
                    sale_date   = st.date_input("Sale Date", date.today())
                    customer    = st.selectbox("Buyer", ["Walk-in"]+cust_names)
                    sale_price  = st.number_input("Sale Price", 0.0, step=100.0)
                with c2:
                    weight     = st.number_input("Weight at Sale (KG)", 0.0, step=1.0)
                    transport  = st.number_input("Transport Cost", 0.0, step=10.0)
                    commission = st.number_input("Commission", 0.0, step=10.0)
                    pm         = st.selectbox("Payment Mode", ["Cash","Bank Transfer","Credit","Cheque"])
                    notes      = st.text_area("Notes", height=55)
                if st.form_submit_button("Record Sale →", use_container_width=True):
                    if sale_price > 0:
                        tag   = animal.split(" - ")[0]
                        adata = next((l for l in active if l["tag_no"]==tag), {})
                        pp    = float(adata.get("purchase_price",0))
                        ls    = load_table("livestock_sales")
                        ls.append({"id":gen_id("LSS"),"date":str(sale_date),"tag_no":tag,
                                   "animal_type":adata.get("animal_type",""),"breed":adata.get("breed",""),
                                   "customer":customer,"purchase_price":pp,"sale_price":sale_price,
                                   "profit":sale_price-pp-transport-commission,
                                   "weight":weight,"transport_cost":transport,"commission":commission,
                                   "payment_mode":pm,"notes":notes,
                                   "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                        save_table("livestock_sales", ls)
                        for l in livestock:
                            if l["tag_no"] == tag: l["status"] = "Sold"
                        save_table("livestock", livestock)
                        recs = load_table("receipts")
                        recs.append({"id":gen_id("RCP"),"ref":gen_id("LSS"),"date":str(sale_date),
                                     "party":customer,"amount":sale_price,"mode":pm,"type":"Receipt",
                                     "notes":f"Livestock Sale: {tag}","created_at":now_str()})
                        save_table("receipts", recs)
                        if pm == "Credit": adjust_customer_balance(customer, sale_price)
                        ok(f"Animal {tag} sold for {currency(sale_price)}! Profit: {currency(sale_price-pp-transport-commission)}"); st.rerun()
        else: warn("No active animals available for sale.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PRODUCTION ORDERS
# ══════════════════════════════════════════════════════════════════════════════
def page_production():
    section_header("🏭", "Production Management")
    products = load_table("products"); prod_names = [p["name"] for p in products]
    tab1, tab2 = st.tabs(["Production Orders","New Order"])
    with tab1:
        prods = load_table("production")
        if prods:
            df = pd.DataFrame([{"Order#":p["id"],"Date":p.get("date",""),"Product":p.get("product",""),
                                 "Qty":p.get("qty",0),"Status":p.get("status",""),"Cost":currency(p.get("total_cost",0))} for p in prods])
            df_display(df)
        else: info_panel("No production orders.")
    with tab2:
        if "pm_items" not in st.session_state: st.session_state["pm_items"] = []
        c1,c2 = st.columns(2)
        with c1:
            pp  = st.selectbox("Product to Produce", prod_names) if prod_names else st.text_input("Product")
            pq  = st.number_input("Quantity", 1.0, step=1.0)
            pd_ = st.date_input("Production Date", date.today())
        with c2:
            pst = st.selectbox("Status", ["Planned","In Progress","Completed","Cancelled"])
            pn  = st.text_area("Notes", height=70)
        c1,c2,c3 = st.columns([3,1,1])
        with c1: mp = st.selectbox("Material", prod_names, key="mp") if prod_names else st.text_input("Material",key="mp")
        with c2: mq = st.number_input("Qty",       1.0, step=1.0, key="mq")
        with c3: mc = st.number_input("Unit Cost",  0.0, step=1.0, key="mc")
        if st.button("➕ Add Material"):
            st.session_state["pm_items"].append({"material":mp,"qty":mq,"unit_cost":mc,"total":mq*mc}); st.rerun()
        if st.session_state["pm_items"]:
            st.dataframe(pd.DataFrame(st.session_state["pm_items"]), use_container_width=True)
            tc = sum(m["total"] for m in st.session_state["pm_items"])
            st.write(f"**Total Cost: {currency(tc)}**")
            if st.button("✅ Create Production Order", type="primary"):
                prods = load_table("production"); oid = gen_id("PROD")
                prods.append({"id":oid,"date":str(pd_),"product":pp,"qty":pq,
                              "materials":st.session_state["pm_items"],"total_cost":tc,
                              "status":pst,"notes":pn,
                              "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("production", prods)
                if pst == "Completed":
                    ps = load_table("products")
                    for p in ps:
                        if p["name"] == pp: p["stock"] = float(p.get("stock",0)) + pq
                    save_table("products", ps)
                st.session_state["pm_items"] = []
                ok(f"Production order {oid} created!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PRODUCTION REPORT
# ══════════════════════════════════════════════════════════════════════════════
def page_production_report():
    section_header("📊", "Production Report")
    prods = load_table("production")
    if prods:
        c1,c2 = st.columns(2)
        with c1: pf = st.date_input("From", date.today().replace(day=1))
        with c2: pt = st.date_input("To",   date.today())
        filtered = [p for p in prods if pf.isoformat()<=str(p.get("date",""))[:10]<=pt.isoformat()]
        if filtered:
            df = pd.DataFrame([{"Date":p["date"],"Product":p.get("product",""),"Qty":p.get("qty",0),
                                 "Cost":currency(p.get("total_cost",0)),"Status":p.get("status","")} for p in filtered])
            df_display(df)
            c1,c2 = st.columns(2)
            with c1: metric_card("Total Produced", f"{sum(float(p.get('qty',0)) for p in filtered):.0f} units", "blue")
            with c2: metric_card("Total Cost",     currency(sum(float(p.get("total_cost",0)) for p in filtered)), "red")
        else: info_panel("No production in period.")
    else: info_panel("No production records.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BMI / INSTALLMENT PLANS
# ══════════════════════════════════════════════════════════════════════════════
def page_bmi_plans():
    section_header("💳", "BMI / Installment Plans")
    customers = load_table("customers"); cust_names = [c["name"] for c in customers]
    tab1, tab2, tab3 = st.tabs(["Plans","Create Plan","Calculator"])
    with tab1:
        bmi = load_table("bmi_plans")
        if bmi:
            for plan in bmi:
                si = "✅" if plan.get("status")=="Completed" else "🔄"
                with st.expander(f"{si} {plan.get('id','')} — {plan.get('customer','')} — {currency(plan.get('total_amount',0))}"):
                    c1,c2,c3,c4 = st.columns(4)
                    with c1: metric_card("Total",        currency(plan.get("total_amount",0)),       "blue")
                    with c2: metric_card("Down Payment",  currency(plan.get("down_payment",0)),       "green")
                    with c3: metric_card("Installments",  plan.get("installment_count",0),            "purple")
                    with c4: metric_card("Status",        plan.get("status",""),                      "amber")
                    inst = load_table("installments")
                    plan_inst = [i for i in inst if i.get("plan_id","") == plan["id"]]
                    if plan_inst: df_display(pd.DataFrame(plan_inst), 200)
                    # Mark installment paid
                    pending_inst = [i for i in plan_inst if i.get("status") != "Paid"]
                    if pending_inst:
                        inst_opts = {f"#{i.get('installment_no','')} — {currency(i.get('amount',0))} — Due: {i.get('due_date','')}": i["id"] for i in pending_inst}
                        sel_inst  = st.selectbox("Mark Installment Paid", list(inst_opts.keys()), key=f"inst_{plan['id']}")
                        if st.button("💰 Mark Paid", key=f"pay_inst_{plan['id']}"):
                            all_inst = load_table("installments")
                            for inst_row in all_inst:
                                if inst_row["id"] == inst_opts[sel_inst]:
                                    inst_row["status"] = "Paid"; inst_row["paid_date"] = today_str()
                            save_table("installments", all_inst)
                            recs = load_table("receipts")
                            recs.append({"id":gen_id("RCP"),"ref":plan["id"],"date":today_str(),
                                         "party":plan.get("customer",""),"amount":plan.get("installment_amount",0),
                                         "mode":"Cash","type":"Receipt",
                                         "notes":f"Installment payment: {plan['id']}","created_at":now_str()})
                            save_table("receipts", recs)
                            adjust_customer_balance(plan.get("customer",""), -float(plan.get("installment_amount",0)))
                            ok("Installment marked paid!"); st.rerun()
        else: info_panel("No BMI plans.")
    with tab2:
        with st.form("bmi_plan"):
            c1,c2 = st.columns(2)
            with c1:
                bc     = st.selectbox("Customer", cust_names) if cust_names else st.text_input("Customer")
                item   = st.text_input("Item / Product Description")
                total  = st.number_input("Total Amount", 0.0, step=100.0)
                dp     = st.number_input("Down Payment", 0.0, step=100.0)
            with c2:
                n_inst     = st.number_input("Number of Installments", 1, 60, 12, step=1)
                start_date = st.date_input("First Installment Date", date.today()+timedelta(days=30))
                freq       = st.selectbox("Frequency", ["Monthly","Weekly","Bi-weekly"])
                notes      = st.text_area("Notes", height=55)
            if st.form_submit_button("Create BMI Plan →", use_container_width=True):
                if total > 0:
                    remaining = total - dp
                    inst_amt  = remaining / n_inst if n_inst > 0 else remaining
                    plan_id   = gen_id("BMI")
                    bmi       = load_table("bmi_plans")
                    bmi.append({"id":plan_id,"customer":bc,"item":item,"total_amount":total,
                                "down_payment":dp,"installment_count":n_inst,"installment_amount":inst_amt,
                                "frequency":freq,"start_date":str(start_date),"status":"Active",
                                "notes":notes,"created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("bmi_plans", bmi)
                    # Generate installment schedule
                    inst      = load_table("installments")
                    freq_days = 30 if freq=="Monthly" else 7 if freq=="Weekly" else 14
                    for i in range(int(n_inst)):
                        due = start_date + timedelta(days=i*freq_days)
                        inst.append({"id":gen_id("INST"),"plan_id":plan_id,"customer":bc,
                                     "installment_no":i+1,"amount":inst_amt,"due_date":str(due),"status":"Pending"})
                    save_table("installments", inst)
                    if dp > 0:
                        recs = load_table("receipts")
                        recs.append({"id":gen_id("RCP"),"ref":plan_id,"date":today_str(),
                                     "party":bc,"amount":dp,"mode":"Cash","type":"Receipt",
                                     "notes":f"BMI Down Payment: {plan_id}","created_at":now_str()})
                        save_table("receipts", recs)
                    adjust_customer_balance(bc, remaining)
                    ok(f"BMI Plan {plan_id} created! {int(n_inst)} installments of {currency(inst_amt)}"); st.rerun()
    with tab3:
        st.markdown("**📐 Installment Calculator**")
        c1,c2 = st.columns(2)
        with c1:
            calc_total = st.number_input("Total Amount",   0.0, step=1000.0, key="calc_t")
            calc_dp    = st.number_input("Down Payment",   0.0, step=1000.0, key="calc_d")
            calc_n     = st.number_input("Installments",   1,   60, 12,     key="calc_n")
        with c2:
            calc_freq = st.selectbox("Frequency", ["Monthly","Weekly","Bi-weekly"], key="calc_f")
            calc_int  = st.number_input("Interest Rate % (per period)", 0.0, 50.0, 0.0, step=0.5, key="calc_i")
        if calc_total > 0 and calc_n > 0:
            remaining  = calc_total - calc_dp
            inst_amt   = remaining / calc_n
            if calc_int > 0:
                r = calc_int/100
                inst_amt_with_int = remaining * r * (1+r)**calc_n / ((1+r)**calc_n - 1)
            else:
                inst_amt_with_int = inst_amt
            c1,c2,c3 = st.columns(3)
            with c1: metric_card("Monthly Payment",   currency(inst_amt_with_int), "blue")
            with c2: metric_card("Total Payable",     currency(inst_amt_with_int*calc_n+calc_dp), "amber")
            with c3: metric_card("Total Interest",    currency(inst_amt_with_int*calc_n-remaining), "red")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: INSTALLMENT SCHEDULE
# ══════════════════════════════════════════════════════════════════════════════
def page_installment_schedule():
    section_header("📅", "Installment Schedule")
    inst = load_table("installments")
    if inst:
        c1,c2 = st.columns(2)
        with c1: ist = st.selectbox("Status", ["All","Pending","Paid","Overdue"])
        with c2: ic  = st.text_input("🔍 Search Customer")
        filtered = inst
        today = today_str()
        for i in filtered:
            if i.get("status")=="Pending" and str(i.get("due_date","")) < today: i["status_display"] = "Overdue"
            else: i["status_display"] = i.get("status","")
        if ist != "All": filtered = [i for i in filtered if i.get("status_display","") == ist]
        if ic: filtered = [i for i in filtered if ic.lower() in i.get("customer","").lower()]
        if filtered:
            df = pd.DataFrame([{"Plan":i.get("plan_id",""),"#":i.get("installment_no",""),
                                 "Customer":i.get("customer",""),"Amount":currency(i.get("amount",0)),
                                 "Due Date":i.get("due_date",""),"Status":i.get("status_display",i.get("status",""))} for i in filtered])
            df_display(df)
            pending_total = sum(float(i.get("amount",0)) for i in filtered if i.get("status")=="Pending")
            st.metric("Total Pending", currency(pending_total))
        else: info_panel("No installments found.")
    else: info_panel("No installment data.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EMPLOYEES
# ══════════════════════════════════════════════════════════════════════════════
def page_employees():
    section_header("👨‍💼", "Employee Management")
    tab1, tab2 = st.tabs(["Employee List","Add Employee"])
    with tab1:
        employees = load_table("employees")
        if employees:
            df = pd.DataFrame([{"ID":e.get("id",""),"Name":e.get("name",""),"Role":e.get("role",""),
                                 "Phone":e.get("phone",""),"Salary":currency(e.get("salary",0)),
                                 "Join Date":e.get("join_date",""),"Status":e.get("status","Active")} for e in employees])
            df_display(df)
        else: info_panel("No employees added yet.")
    with tab2:
        with st.form("add_emp"):
            c1,c2,c3 = st.columns(3)
            with c1:
                ename  = st.text_input("Full Name *"); eid_no = st.text_input("CNIC / ID")
                ephone = st.text_input("Phone");       eemail = st.text_input("Email")
            with c2:
                erole   = st.selectbox("Role", ["Manager","Cashier","Driver","Farm Worker","Accountant","Security","Cleaner","Other"])
                edept   = st.text_input("Department")
                esalary = st.number_input("Monthly Salary", 0.0, step=500.0)
                ejoin   = st.date_input("Join Date", date.today())
            with c3:
                eaddress = st.text_area("Address", height=70)
                ebank    = st.text_input("Bank Account")
                enotes   = st.text_area("Notes", height=40)
            if st.form_submit_button("Save Employee →", use_container_width=True):
                if ename:
                    employees = load_table("employees")
                    employees.append({"id":gen_id("EMP"),"name":ename,"cnic":eid_no,"phone":ephone,
                                      "email":eemail,"role":erole,"department":edept,"salary":esalary,
                                      "join_date":str(ejoin),"address":eaddress,"bank":ebank,
                                      "notes":enotes,"status":"Active","created":today_str()})
                    save_table("employees", employees)
                    log_audit(st.session_state["user"]["username"],"ADD_EMPLOYEE",ename)
                    ok(f"Employee '{ename}' added!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ATTENDANCE
# ══════════════════════════════════════════════════════════════════════════════
def page_attendance():
    section_header("📋", "Attendance Management")
    employees = load_table("employees"); emp_names = [e["name"] for e in employees if e.get("status")=="Active"]
    tab1, tab2 = st.tabs(["Attendance Log","Mark Attendance"])
    with tab1:
        att = load_table("attendance")
        c1,c2 = st.columns(2)
        with c1: af = st.date_input("From", date.today().replace(day=1), key="af")
        with c2: at_ = st.date_input("To",  date.today(), key="at")
        filtered = [a for a in att if af.isoformat()<=str(a.get("date",""))[:10]<=at_.isoformat()]
        if filtered: df_display(pd.DataFrame(filtered))
        else: info_panel("No attendance records in period.")
    with tab2:
        with st.form("mark_att"):
            att_date = st.date_input("Date", date.today())
            if emp_names:
                statuses = {}
                for emp in emp_names:
                    col1, col2 = st.columns([3,1])
                    with col1: st.write(emp)
                    with col2: statuses[emp] = st.selectbox("", ["Present","Absent","Half Day","Leave"], key=f"att_{emp}")
            if st.form_submit_button("Save Attendance →", use_container_width=True) and emp_names:
                att = load_table("attendance")
                for emp, status in statuses.items():
                    att.append({"id":gen_id("ATT"),"date":str(att_date),"employee":emp,"status":status,
                                "marked_by":st.session_state["user"]["username"],"created_at":now_str()})
                save_table("attendance", att); ok("Attendance saved!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SALARY MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
def page_salaries():
    section_header("💵", "Salary Management")
    employees = load_table("employees"); emp_names = [e["name"] for e in employees if e.get("status")=="Active"]
    emp_dict  = {e["name"]:e for e in employees}
    tab1, tab2 = st.tabs(["Salary History","Pay Salary"])
    with tab1:
        salaries = load_table("salaries")
        if salaries: df_display(pd.DataFrame(salaries))
        else: info_panel("No salary records yet.")
    with tab2:
        if emp_names:
            with st.form("pay_salary"):
                c1,c2 = st.columns(2)
                with c1:
                    sal_emp    = st.selectbox("Employee", emp_names)
                    sal_month  = st.text_input("Month", value=date.today().strftime("%B %Y"))
                    sal_basic  = st.number_input("Basic Salary", 0.0, step=100.0,
                                                  value=float(emp_dict.get(sal_emp,{}).get("salary",0)))
                    sal_bonus  = st.number_input("Bonus / Allowance", 0.0, step=100.0)
                with c2:
                    sal_deduct = st.number_input("Deductions", 0.0, step=100.0)
                    sal_mode   = st.selectbox("Payment Mode", ["Cash","Bank Transfer","Cheque"])
                    sal_date   = st.date_input("Payment Date", date.today())
                    sal_notes  = st.text_area("Notes", height=55)
                net = sal_basic + sal_bonus - sal_deduct
                st.metric("Net Salary", currency(net))
                if st.form_submit_button("Pay Salary →", use_container_width=True):
                    salaries = load_table("salaries")
                    salaries.append({"id":gen_id("SAL"),"employee":sal_emp,"month":sal_month,
                                     "basic":sal_basic,"bonus":sal_bonus,"deductions":sal_deduct,
                                     "net":net,"mode":sal_mode,"date":str(sal_date),"notes":sal_notes,
                                     "paid_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("salaries", salaries)
                    exps = load_table("expenses")
                    exps.append({"id":gen_id("EXP"),"date":str(sal_date),"category":"Salaries",
                                 "description":f"Salary: {sal_emp} — {sal_month}","amount":net,
                                 "paid_by":sal_mode,"vendor":sal_emp,"notes":sal_notes,
                                 "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("expenses", exps)
                    ok(f"Salary of {currency(net)} paid to {sal_emp}!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LOANS & ADVANCES
# ══════════════════════════════════════════════════════════════════════════════
def page_loans():
    section_header("💰", "Loans & Employee Advances")
    employees = load_table("employees"); emp_names = [e["name"] for e in employees if e.get("status")=="Active"]
    tab1, tab2 = st.tabs(["Loan Records","Add Loan / Advance"])
    with tab1:
        loans = load_table("loans")
        if loans:
            df = pd.DataFrame([{"ID":l.get("id",""),"Employee":l.get("employee",""),
                                 "Type":l.get("type",""),"Amount":currency(l.get("amount",0)),
                                 "Repaid":currency(l.get("repaid",0)),
                                 "Balance":currency(float(l.get("amount",0))-float(l.get("repaid",0))),
                                 "Status":l.get("status",""),"Date":l.get("date","")} for l in loans])
            df_display(df)
        else: info_panel("No loan records.")
    with tab2:
        with st.form("add_loan"):
            c1,c2 = st.columns(2)
            with c1:
                lemp   = st.selectbox("Employee", emp_names) if emp_names else st.text_input("Employee")
                ltype  = st.selectbox("Type", ["Salary Advance","Personal Loan","Emergency Advance"])
                lamt   = st.number_input("Amount", 0.0, step=500.0)
                ldate  = st.date_input("Date", date.today())
            with c2:
                lrep   = st.number_input("Monthly Repayment", 0.0, step=100.0)
                lnotes = st.text_area("Notes / Reason", height=80)
            if st.form_submit_button("Record Loan →", use_container_width=True):
                if lamt > 0:
                    loans = load_table("loans")
                    loans.append({"id":gen_id("LN"),"employee":lemp,"type":ltype,"amount":lamt,
                                  "repaid":0,"monthly_repayment":lrep,"status":"Active",
                                  "date":str(ldate),"notes":lnotes,
                                  "created_by":st.session_state["user"]["username"],"created_at":now_str()})
                    save_table("loans", loans)
                    ok(f"Loan of {currency(lamt)} recorded for {lemp}!"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
def page_settings():
    section_header("⚙️", "Company Settings")
    settings_data = load_table("company_settings"); s = settings_data[0] if settings_data else {}
    with st.form("company_settings"):
        c1,c2 = st.columns(2)
        with c1:
            sname    = st.text_input("Company Name",  value=s.get("name","Hassan Traders"))
            saddress = st.text_area( "Address",       value=s.get("address","Karachi, Pakistan"), height=70)
            sphone   = st.text_input("Phone",         value=s.get("phone",""))
            semail   = st.text_input("Email",         value=s.get("email",""))
        with c2:
            sntn      = st.text_input("NTN / Tax ID", value=s.get("ntn",""))
            scurrency = st.selectbox("Currency",      ["PKR","USD","EUR","GBP"],
                                     index=["PKR","USD","EUR","GBP"].index(s.get("currency","PKR")) if s.get("currency","PKR") in ["PKR","USD","EUR","GBP"] else 0)
            stax      = st.number_input("Default Tax Rate %", 0.0, 100.0, float(s.get("tax_rate",17.0)))
            slow      = st.number_input("Low Stock Alert Threshold", 0, 1000, int(s.get("low_stock_threshold",10)))
        if st.form_submit_button("Save Settings →", use_container_width=True):
            if settings_data:
                settings_data[0].update({"name":sname,"address":saddress,"phone":sphone,
                                          "email":semail,"ntn":sntn,"currency":scurrency,
                                          "tax_rate":stax,"low_stock_threshold":slow})
                save_table("company_settings", settings_data)
            ok("Settings saved!"); st.rerun()

    st.divider()
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("**📁 Categories**")
        cats = load_table("categories")
        if cats: st.write(", ".join(c["name"] for c in cats))
        with st.form("add_cat"):
            cn = st.text_input("Category Name", key="cat_name")
            if st.form_submit_button("➕ Add"):
                if cn:
                    cats = load_table("categories"); cats.append({"id":gen_id("CAT"),"name":cn})
                    save_table("categories", cats); ok("Added!"); st.rerun()
    with c2:
        st.markdown("**📏 Units of Measure**")
        units = load_table("units")
        if units: st.write(", ".join(u["name"] for u in units))
        with st.form("add_unit"):
            un = st.text_input("Unit Name", key="unit_name")
            if st.form_submit_button("➕ Add"):
                if un:
                    units = load_table("units"); units.append({"id":gen_id("UT"),"name":un})
                    save_table("units", units); ok("Added!"); st.rerun()
    with c3:
        st.markdown("**🏪 Tax Settings**")
        st.write(f"Current Tax Rate: **{s.get('tax_rate',17)}%**")
        info_panel("Tax is applied per-sale in POS and Invoices.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: USER MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
def page_users():
    section_header("👤", "User Management")
    current_user = st.session_state.get("user", {})
    tab1, tab2 = st.tabs(["User List","Add User"])
    with tab1:
        users = load_table("users")
        if users:
            for u in users:
                status_icon = "✅" if u.get("active") else "❌"
                with st.expander(f"{status_icon} {u['username']} — {u.get('role','')} — {u.get('name','')}"):
                    c1,c2,c3 = st.columns(3)
                    c1.write(f"**Email:** {u.get('email','')}"); c2.write(f"**Phone:** {u.get('phone','')}")
                    c3.write(f"**Created:** {u.get('created','')}")
                    if u["username"] != current_user.get("username",""):
                        cc1,cc2 = st.columns(2)
                        with cc1:
                            if u.get("active"):
                                if st.button("🔒 Deactivate", key=f"deact_{u['id']}"):
                                    all_u = load_table("users")
                                    for uu in all_u:
                                        if uu["username"]==u["username"]: uu["active"] = False
                                    save_table("users", all_u); st.rerun()
                        with cc2:
                            if not u.get("active"):
                                if st.button("🔓 Activate", key=f"act_{u['id']}"):
                                    all_u = load_table("users")
                                    for uu in all_u:
                                        if uu["username"]==u["username"]: uu["active"] = True
                                    save_table("users", all_u); st.rerun()
    with tab2:
        with st.form("add_user"):
            c1,c2 = st.columns(2)
            with c1:
                uu  = st.text_input("Username *"); un = st.text_input("Full Name *")
                ur  = st.selectbox("Role", ["Admin","Manager","Cashier","Accountant","Viewer","HRM"])
                upw = st.text_input("Password *", type="password")
            with c2:
                ue  = st.text_input("Email"); uph = st.text_input("Phone")
                ucpw= st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Create User →"):
                if uu and un and upw:
                    if upw != ucpw: err("Passwords don't match!")
                    else:
                        users = load_table("users")
                        if any(u["username"]==uu for u in users): err("Username exists!")
                        else:
                            users.append({"id":gen_id("USR"),"username":uu,"name":un,"role":ur,
                                          "email":ue,"phone":uph,"password":hash_pw(upw),
                                          "active":True,"created":today_str()})
                            save_table("users", users)
                            log_audit(current_user.get("username",""),"CREATE_USER",uu)
                            ok(f"User '{uu}' created!"); st.rerun()
                else: err("Username, Name, Password required.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AUDIT LOG
# ══════════════════════════════════════════════════════════════════════════════
def page_audit_log():
    section_header("📋", "Audit Log")
    al = load_table("audit_log")
    if al:
        c1,c2,c3 = st.columns(3)
        with c1: als  = st.text_input("🔍 Search", key="als")
        with c2: alu  = st.selectbox("User",   ["All"]+list(set(a.get("user","")  for a in al)))
        with c3: alact= st.selectbox("Action", ["All"]+list(set(a.get("action","") for a in al)))
        filtered = al
        if als:   filtered = [a for a in filtered if als.lower()  in str(a).lower()]
        if alu  != "All": filtered = [a for a in filtered if a.get("user","")   == alu]
        if alact!= "All": filtered = [a for a in filtered if a.get("action","") == alact]
        df_display(pd.DataFrame(filtered[::-1]))
    else: info_panel("No audit log entries.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DAILY DOWNLOAD
# ══════════════════════════════════════════════════════════════════════════════
def page_daily_download():
    section_header("📥", "Daily Data Download")
    info_panel("Select any date to download a complete report — all sales, expenses, receipts, payments, and P&L summary.")
    c1,c2 = st.columns(2)
    with c1: dl_date   = st.date_input("Select Date", date.today(), key="dl_date")
    with c2: dl_format = st.selectbox("Format", ["Excel (XLSX)","CSV (Multiple Files)"])
    ds = dl_date.isoformat()
    pos_sales       = load_table("pos_sales");       expenses        = load_table("expenses")
    receipts        = load_table("receipts");        payments        = load_table("payments")
    advance_sales   = load_table("advance_sales");   livestock_sales = load_table("livestock_sales")
    sale_orders     = load_table("sale_orders");     customers       = load_table("customers")
    products        = load_table("products");        livestock       = load_table("livestock")

    day_pos = [s for s in pos_sales       if str(s.get("date",""))[:10]==ds]
    day_exp = [e for e in expenses        if str(e.get("date",""))[:10]==ds]
    day_rec = [r for r in receipts        if str(r.get("date",""))[:10]==ds]
    day_pay = [p for p in payments        if str(p.get("date",""))[:10]==ds]
    day_adv = [a for a in advance_sales   if str(a.get("date",""))[:10]==ds]
    day_ls  = [l for l in livestock_sales if str(l.get("date",""))[:10]==ds]
    day_so  = [o for o in sale_orders     if str(o.get("date",""))[:10]==ds]

    total_sales    = sum(float(s.get("total",0))         for s in day_pos)
    total_exp      = sum(float(e.get("amount",0))        for e in day_exp)
    total_rec      = sum(float(r.get("amount",0))        for r in day_rec)
    total_pay      = sum(float(p.get("amount",0))        for p in day_pay)
    total_ls_sales = sum(float(l.get("sale_price",0))    for l in day_ls)
    total_ls_cost  = sum(float(l.get("purchase_price",0))for l in day_ls)
    gross_profit   = (total_sales + total_ls_sales) - (sum(float(s.get("cost_total",0)) for s in day_pos) + total_ls_cost)
    net_profit     = gross_profit - total_exp

    st.markdown(f"### Summary for {ds}")
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: metric_card("POS Txns",     len(day_pos),              "blue")
    with c2: metric_card("Revenue",      currency(total_sales),     "green")
    with c3: metric_card("Expenses",     currency(total_exp),       "red")
    with c4: metric_card("Receipts",     currency(total_rec),       "purple")
    with c5: metric_card("Gross Profit", currency(gross_profit),    "green")
    with c6: metric_card("Net Profit",   currency(net_profit),      "blue" if net_profit>=0 else "red")

    def safe_df(data, cols=None):
        if not data: return pd.DataFrame()
        df = pd.DataFrame(data)
        if cols: df = df[[c for c in cols if c in df.columns]]
        return df

    summary_df = pd.DataFrame([{"Date":ds,"Total Sales":total_sales,"POS Transactions":len(day_pos),
                                  "Expenses":total_exp,"Receipts":total_rec,"Payments":total_pay,
                                  "LS Sales":total_ls_sales,"Gross Profit":gross_profit,"Net Profit":net_profit}])
    pos_df = safe_df(day_pos, ["id","date","customer","subtotal","discount_amt","tax_amt","total","amount_paid","change","payment_mode"])
    exp_df = safe_df(day_exp, ["id","ref","category","description","amount","paid_by","vendor"])
    rec_df = safe_df(day_rec, ["id","ref","party","amount","mode","notes"])
    pay_df = safe_df(day_pay, ["id","ref","party","amount","mode","notes"])
    adv_df = safe_df(day_adv, ["id","customer","product","qty","price","total","advance_paid","balance","status"])
    ls_df  = safe_df(day_ls,  ["id","tag_no","animal_type","customer","purchase_price","sale_price","profit","payment_mode"])
    cust_df= safe_df(customers, ["name","phone","type","city","balance"])
    prod_df= safe_df(products,  ["sku","name","category","stock","min_stock","cost_price","sale_price"])
    live_df= safe_df([l for l in livestock if l.get("status")=="Active"],["tag_no","name","animal_type","breed","gender","status","shed"])

    items_rows = []
    for s in day_pos:
        for it in s.get("items",[]):
            items_rows.append({"Sale ID":s["id"],"Customer":s.get("customer",""),
                               "Product":it.get("product",""),"Qty":it.get("qty",0),
                               "Price":it.get("price",0),"Total":it.get("total",0)})
    items_df = pd.DataFrame(items_rows) if items_rows else pd.DataFrame()

    st.divider()
    if dl_format == "Excel (XLSX)":
        sheets = {"Day Summary":summary_df,"POS Sales":pos_df,"Sale Items":items_df,
                  "Expenses":exp_df,"Receipts":rec_df,"Payments":pay_df,
                  "Advance Sales":adv_df,"Livestock Sales":ls_df,
                  "Customers":cust_df,"Products & Stock":prod_df,"Active Livestock":live_df}
        xl_bytes = df_to_excel_bytes(sheets)
        fname    = f"hassan_traders_{ds}.xlsx"
        st.markdown('<div class="dl-btn">'+make_download_link(xl_bytes, fname, f"📥 Download Full Report — {ds}")+'</div>',
                    unsafe_allow_html=True)
        ok(f"Excel report ready with {sum(1 for v in sheets.values() if not v.empty)} data sheets!")
    else:
        st.markdown("**Download individual CSV files:**")
        csv_files = [("day_summary",summary_df),("pos_sales",pos_df),("sale_items",items_df),
                     ("expenses",exp_df),("receipts",rec_df),("payments",pay_df),
                     ("advance_sales",adv_df),("livestock_sales",ls_df),("customers",cust_df),("products",prod_df)]
        cols = st.columns(3)
        for i,(name,df_) in enumerate(csv_files):
            if not df_.empty:
                with cols[i%3]:
                    st.markdown('<div class="dl-btn">'+make_download_link(df_to_csv_bytes(df_),
                                f"{name}_{ds}.csv",f"📄 {name.replace('_',' ').title()}")+'</div>',
                                unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DATA MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
def page_data_management():
    section_header("🗃️", "Data Management")
    info_panel("✅ <b>Auto-Cleanup Policy:</b> Sales, expenses, receipts, and payment data older than 3 days is automatically archived. Customer data, inventory, livestock, employees, and all master data is <b>never deleted</b>.", "green")
    st.markdown("### 📊 Data Storage Overview")
    rows = []
    for tbl in PERSISTENT_TABLES + TRANSIENT_TABLES:
        data = load_table(tbl)
        rows.append({"Table":tbl,"Records":len(data),"Type":"Permanent" if tbl in PERSISTENT_TABLES else "Auto-cleaned (3 days)"})
    df_display(pd.DataFrame(rows))
    st.divider()
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("**🔄 Manual Cleanup**")
        if st.button("Run Auto-Cleanup Now"):
            auto_cleanup(); ok("Cleanup complete! Data older than 3 days archived."); st.rerun()
    with c2:
        st.markdown("**💾 Full Backup**")
        if st.button("Download Full Backup"):
            all_data = {}
            for tbl in PERSISTENT_TABLES + TRANSIENT_TABLES:
                data = load_table(tbl)
                if data: all_data[tbl] = pd.DataFrame(data)
            if all_data:
                xl = df_to_excel_bytes(all_data)
                st.markdown('<div class="dl-btn">'+make_download_link(xl,f"full_backup_{today_str()}.xlsx","📥 Download Full Backup")+'</div>',
                            unsafe_allow_html=True)
    with c3:
        st.markdown("**🗑️ Clear Transient Data**")
        if st.button("⚠️ Clear Today's Transient Data"):
            warn("This clears all transient tables regardless of date. Use with caution.")

# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
PAGE_MAP = {
    "Overview":             page_dashboard,
    "Ledger":               page_ledger,
    "Cashbook":             page_cashbook,
    "Receipts & Payments":  page_receipts_payments,
    "Expenses":             page_expenses,
    "Daily Profit Report":  page_daily_profit,
    "Products":             page_products,
    "Stock Adjustment":     page_stock_adjustment,
    "Damage Records":       page_damage,
    "Warehouses":           page_warehouses,
    "Price Lists":          page_price_lists,
    "Point of Sale":        page_pos,
    "Sale Orders":          page_sale_orders,
    "Advance Sales":        page_advance_sales,
    "English Billing":      page_english_billing,
    "Purchase Orders":      page_purchase_orders,
    "Supplier Management":  page_supplier_management,
    "Customers":            page_customers,
    "Debtors & Creditors":  page_debtors_creditors,
    "Tasks & Follow-ups":   page_tasks,
    "Notes":                page_notes,
    "Livestock Register":   page_livestock,
    "Milk Production":      page_milk,
    "Feed Records":         page_feed,
    "Breeding":             page_breeding,
    "Health Records":       page_health,
    "Livestock Sales":      page_livestock_sales,
    "Production Orders":    page_production,
    "Production Report":    page_production_report,
    "BMI Plans":            page_bmi_plans,
    "Installment Schedule": page_installment_schedule,
    "Employees":            page_employees,
    "Attendance":           page_attendance,
    "Salary Management":    page_salaries,
    "Loans & Advances":     page_loans,
    "Settings":             page_settings,
    "User Management":      page_users,
    "Audit Log":            page_audit_log,
    "Daily Download":       page_daily_download,
    "Data Management":      page_data_management,
}

def route():
    page = st.session_state.get("nav_page", "Overview")
    PAGE_MAP.get(page, page_dashboard)()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    init_default_user()
    init_settings()
    auto_cleanup()
    if not st.session_state.get("logged_in"):
        login_page()
    else:
        render_sidebar()
        route()

if __name__ == "__main__":
    main()