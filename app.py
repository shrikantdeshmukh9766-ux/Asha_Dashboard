import streamlit as st
from koboextractor import KoboExtractor
import pandas as pd
import io
import requests
import matplotlib.colors as mcolors

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="आशा मॉनिटरिंग डॅशबोर्ड",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================
# CUSTOM CSS
# =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Baloo 2', 'Noto Sans Devanagari', sans-serif;
}

.stApp {
    background: #eaf4fb;
    min-height: 100vh;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, #b8d9f0 1px, transparent 1px);
    background-size: 28px 28px;
    opacity: 0.35;
    pointer-events: none;
    z-index: 0;
}

.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 2rem !important;
    position: relative;
    z-index: 1;
}

.hero-banner {
    background: linear-gradient(135deg, #1b4f72 0%, #1a6fa6 50%, #2e86c1 100%);
    border-radius: 22px;
    padding: 34px 40px;
    margin-bottom: 26px;
    box-shadow: 0 8px 32px rgba(27,79,114,0.18), inset 0 1px 0 rgba(255,255,255,0.12);
    position: relative;
    overflow: hidden;
}

.hero-banner::before {
    content: '🌸';
    position: absolute;
    right: 44px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 72px;
    opacity: 0.12;
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 7px 0;
    line-height: 1.2;
    text-shadow: 0 2px 8px rgba(0,0,0,0.18);
}

.hero-subtitle {
    color: rgba(255,255,255,0.72);
    font-size: 13.5px;
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.4px;
}

.metrics-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 26px;
}

.metric-card {
    border-radius: 16px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 18px rgba(27,79,114,0.10);
    transition: transform 0.2s, box-shadow 0.2s;
    border: 1px solid rgba(255,255,255,0.7);
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 28px rgba(27,79,114,0.15);
}

.metric-card-1 { background: linear-gradient(135deg, #dbeeff, #c2dcf7); }
.metric-card-2 { background: linear-gradient(135deg, #dff5ec, #c2ead8); }
.metric-card-3 { background: linear-gradient(135deg, #fef3dc, #fde5b4); }

.metric-icon  { font-size: 26px; margin-bottom: 9px; display: block; }

.metric-value-1 { font-size: 32px; font-weight: 800; color: #1a6fa6; line-height:1; margin-bottom:3px; }
.metric-value-2 { font-size: 32px; font-weight: 800; color: #1a8a5a; line-height:1; margin-bottom:3px; }
.metric-value-3 { font-size: 32px; font-weight: 800; color: #b5770a; line-height:1; margin-bottom:3px; }

.metric-label {
    font-size: 11.5px;
    color: #4a6070;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

.section-card {
    background: rgba(255,255,255,0.96);
    border-radius: 18px;
    padding: 26px 30px;
    margin-bottom: 22px;
    box-shadow: 0 4px 20px rgba(27,79,114,0.08);
    border: 1px solid #d6eaf8;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 2px solid #eaf4fb;
}

.section-icon {
    width: 40px;
    height: 40px;
    border-radius: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    flex-shrink: 0;
}

.icon-blue1  { background: #d6eaf8; }
.icon-blue2  { background: #d1f0e8; }
.icon-blue3  { background: #e2dcff; }

.section-title {
    font-size: 18px;
    font-weight: 700;
    color: #1b4f72;
    margin: 0;
}

.section-desc {
    font-size: 12.5px;
    color: #7f9aaa;
    margin: 2px 0 0 0;
}

.asha-selector-card {
    background: linear-gradient(135deg, #1b4f72, #2e86c1);
    border-radius: 18px;
    padding: 24px 30px;
    margin-bottom: 24px;
    box-shadow: 0 6px 24px rgba(27,79,114,0.20);
}

.asha-selector-title {
    color: white;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: 0.3px;
}

.stButton > button {
    background: linear-gradient(135deg, #1a6fa6, #2e86c1) !important;
    color: white !important;
    border: none !important;
    border-radius: 11px !important;
    padding: 9px 26px !important;
    font-family: 'Baloo 2', sans-serif !important;
    font-size: 14.5px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(26,111,166,0.28) !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(26,111,166,0.36) !important;
}

.stDownloadButton > button {
    border-radius: 11px !important;
    padding: 9px 22px !important;
    font-family: 'Baloo 2', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}

.stSelectbox > div > div {
    border-radius: 11px !important;
    border: 2px solid #a9cfe8 !important;
    font-family: 'Baloo 2', sans-serif !important;
    background: white !important;
}

.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 2px 14px rgba(27,79,114,0.07) !important;
}

hr {
    border: none !important;
    height: 2px !important;
    background: linear-gradient(90deg, #a9cfe8, #b8e8d4, #c4b8f0) !important;
    border-radius: 2px !important;
    margin: 22px 0 !important;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =====================
# CONSTANTS
# =====================
TOKEN = "23801d339dd6d16509a79250731f126401d5f7a3"
BASE_URL  = "https://kobo.humanitarianresponse.info/api/v2"
asset_uid = "aGGHAxMxBz67ScRohaf3vw"
MASTER_URL = "https://raw.githubusercontent.com/shrikantdeshmukh9766-ux/Asha_Dashboard/main/Participant%20list.xlsx"

# =====================
# COLOR MAPS
# =====================
def cmap_blue():
    return mcolors.LinearSegmentedColormap.from_list("lb", ["#ffffff", "#cce5f6"])

def cmap_teal():
    return mcolors.LinearSegmentedColormap.from_list("lt", ["#ffffff", "#c2ead8"])

def cmap_amber():
    return mcolors.LinearSegmentedColormap.from_list("la", ["#ffffff", "#fde5b4"])

# =====================
# LOAD DATA
# =====================
@st.cache_data(show_spinner=False)
def load_kobo_data():
    kobo = KoboExtractor(TOKEN, BASE_URL)
    start, limit, all_records = 0, 1000, []
    while True:
        data    = kobo.get_data(asset_uid, start=start, limit=limit)
        records = data["results"]
        if not records:
            break
        all_records.extend(records)
        start += limit

    df = pd.json_normalize(all_records)
    df = df.rename(columns={
        'group_og9hq60/asha':       'asha',
        'group_og9hq60/Paticipant': 'Paticipant'
    })
    df.columns = [
        col if col in ['asha', 'Paticipant']
        else col.split('/')[-1]
        for col in df.columns
    ]
    return df

@st.cache_data(show_spinner=False)
def load_master_data():
    resp = requests.get(MASTER_URL, timeout=15)
    resp.raise_for_status()
    master_df = pd.read_excel(io.BytesIO(resp.content))
    master_df.columns = master_df.columns.str.strip()
    col_map = {}
    for c in master_df.columns:
        if c.lower() == 'asha':
            col_map[c] = 'asha'
        elif c.lower() in ['paticipant', 'participant']:
            col_map[c] = 'Paticipant'
    master_df = master_df.rename(columns=col_map)
    master_df['asha']       = master_df['asha'].astype(str).str.strip()
    master_df['Paticipant'] = master_df['Paticipant'].astype(str).str.strip()
    return master_df

# =====================
# SESSION STATE — load data
# =====================
if "df" not in st.session_state:
    with st.spinner("KoboToolbox मधून डेटा लोड होत आहे..."):
        st.session_state.df = load_kobo_data()

if "master_df" not in st.session_state:
    with st.spinner("GitHub वरून मास्टर यादी लोड होत आहे..."):
        try:
            st.session_state.master_df = load_master_data()
        except Exception as e:
            st.error(f"⚠️ मास्टर यादी लोड करताना त्रुटी: {e}")

# =====================
# HERO HEADER
# =====================
st.markdown("""
<div class="hero-banner">
    <h1 class="hero-title">🌸 आशा मॉनिटरिंग डॅशबोर्ड</h1>
    <p class="hero-subtitle">KoboToolbox &nbsp;·&nbsp; रिअल-टाइम डेटा विश्लेषण &nbsp;·&nbsp; सहभागी नोंदी</p>
</div>
""", unsafe_allow_html=True)

# =====================
# REFRESH BUTTON
# =====================
col_btn, _ = st.columns([1, 5])
with col_btn:
    if st.button("🔄 डेटा रिफ्रेश करा"):
        st.cache_data.clear()
        with st.spinner("नवीनतम डेटा आणत आहे..."):
            st.session_state.df        = load_kobo_data()
            st.session_state.master_df = load_master_data()
        st.success("✅ डेटा यशस्वीरित्या अपडेट झाला!")
        st.rerun()

# =====================
# GUARD
# =====================
df = st.session_state.df
for col in ['asha', 'Paticipant', '_submission_time']:
    if col not in df.columns:
        st.error(f"⚠️ '{col}' कॉलम सापडला नाही.")
        st.stop()

# =====================
# DATE PROCESSING
# =====================
df['_submission_time'] = pd.to_datetime(df['_submission_time'])
df['Month']            = df['_submission_time'].dt.strftime('%b')
df['Month_num']        = df['_submission_time'].dt.month
df['asha']             = df['asha'].astype(str).str.strip()
df['Paticipant']       = df['Paticipant'].astype(str).str.strip()

# =====================
# ASHA SELECTOR
# =====================
all_ashas = sorted(df['asha'].unique())

st.markdown('<div class="asha-selector-card"><div class="asha-selector-title">👩‍⚕️ आशा निवडा</div>', unsafe_allow_html=True)
selected_asha = st.selectbox(
    label="आशा",
    options=all_ashas,
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# =====================
# FILTER DATA FOR SELECTED ASHA
# =====================
asha_df = df[df['asha'] == selected_asha].copy()

# Master data for selected ASHA
master_df = st.session_state.get("master_df")
if master_df is not None:
    master_participants = set(master_df[master_df['asha'] == selected_asha]['Paticipant'])
else:
    master_participants = set()

submitted_participants = set(asha_df['Paticipant'])
submitted_in_master   = submitted_participants & master_participants
remaining_participants = sorted(master_participants - submitted_participants)

total_target    = len(master_participants)
total_filled    = len(submitted_in_master)
total_remaining = len(remaining_participants)

# =====================
# METRIC CARDS
# =====================
st.markdown(f"""
<div class="metrics-row">
    <div class="metric-card metric-card-1">
        <span class="metric-icon">📋</span>
        <div class="metric-value-1">{total_target}</div>
        <div class="metric-label">एकूण टार्गेट</div>
    </div>
    <div class="metric-card metric-card-2">
        <span class="metric-icon">✅</span>
        <div class="metric-value-2">{total_filled}</div>
        <div class="metric-label">नोंदवलेले</div>
    </div>
    <div class="metric-card metric-card-3">
        <span class="metric-icon">⏳</span>
        <div class="metric-value-3">{total_remaining}</div>
        <div class="metric-label">उर्वरित</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================
# TABLE 1 — MONTH-WISE CALENDAR
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-blue1">📅</div>
        <div>
            <p class="section-title">तक्ता १ · महिन्यानुसार भरलेल्या फॉर्मची संख्या</p>
            <p class="section-desc">निवडलेल्या आशाच्या महिनानिहाय नोंदी</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if asha_df.empty:
    st.info("या आशासाठी कोणत्याही नोंदी आढळल्या नाहीत.")
else:
    month_counts = (
        asha_df.groupby(['Month', 'Month_num'])['Paticipant']
        .count()
        .reset_index()
        .sort_values('Month_num')
        .rename(columns={'Month': 'महिना', 'Paticipant': 'नोंदी संख्या'})
        .drop(columns='Month_num')
    )
    month_counts.index = range(1, len(month_counts) + 1)
    month_counts.index.name = 'अ.क्र.'

    styled1 = (
        month_counts.style
        .background_gradient(cmap=cmap_blue(), subset=['नोंदी संख्या'])
        .format({'नोंदी संख्या': '{:.0f}'})
        .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '14px', 'color': '#1b4f72'})
        .set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'),
                                          ('font-weight', '700'), ('font-size', '13px'),
                                          ('border', '1px solid #b8d9f0')]},
            {'selector': 'td', 'props': [('border', '1px solid #eaf4fb')]},
        ])
    )

    st.dataframe(styled1, use_container_width=True, height=min(420, (len(month_counts) + 1) * 42 + 10))

    # Download
    buf1 = io.BytesIO()
    with pd.ExcelWriter(buf1, engine='openpyxl') as w:
        month_counts.to_excel(w, sheet_name='महिनानिहाय नोंदी', index=True)
    st.download_button(
        label="⬇️ Excel डाउनलोड",
        data=buf1.getvalue(),
        file_name=f"{selected_asha}_महिनानिहाय_नोंदी.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("</div>", unsafe_allow_html=True)

# =====================
# TABLE 2 — TARGET vs FILLED vs REMAINING
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-blue2">🎯</div>
        <div>
            <p class="section-title">तक्ता २ · टार्गेट विरुद्ध प्रगती</p>
            <p class="section-desc">एकूण टार्गेट, नोंदवलेले आणि उर्वरित सहभागी</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if master_df is None:
    st.warning("⚠️ मास्टर यादी उपलब्ध नाही.")
else:
    progress_pct = round((total_filled / total_target * 100), 1) if total_target > 0 else 0

    progress_data = pd.DataFrame([{
        '👩‍⚕️ आशा':         selected_asha,
        '📋 एकूण टार्गेट':   total_target,
        '✅ नोंदवलेले':      total_filled,
        '⏳ उर्वरित':        total_remaining,
        '📊 प्रगती (%)':     f"{progress_pct}%"
    }])
    progress_data.index = ['']

    styled2 = (
        progress_data.style
        .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '14px',
                           'color': '#1b4f72', 'text-align': 'center'})
        .set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'),
                                          ('font-weight', '700'), ('font-size', '13px'),
                                          ('border', '1px solid #b8d9f0'), ('text-align', 'center')]},
            {'selector': 'td', 'props': [('border', '1px solid #eaf4fb'), ('text-align', 'center')]},
        ])
    )

    st.dataframe(styled2, use_container_width=True, height=80)

    # Progress bar
    st.markdown(f"""
    <div style="margin: 14px 0 6px 0; font-size:13px; color:#4a6070; font-weight:600;">
        प्रगती: {progress_pct}%
    </div>
    <div style="background:#d6eaf8; border-radius:20px; height:18px; overflow:hidden; margin-bottom:10px;">
        <div style="width:{progress_pct}%; height:100%;
                    background: linear-gradient(90deg, #1a8a5a, #27ae60);
                    border-radius:20px; transition: width 0.5s;">
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =====================
# TABLE 3 — REMAINING PARTICIPANTS LIST
# =====================
st.markdown("""
<div class="section-card">
    <div class="section-header">
        <div class="section-icon icon-blue3">📝</div>
        <div>
            <p class="section-title">तक्ता ३ · उर्वरित सहभागी यादी</p>
            <p class="section-desc">मास्टर यादीतील सहभागी जे अद्याप नोंदवले नाहीत</p>
        </div>
    </div>
""", unsafe_allow_html=True)

if master_df is None:
    st.warning("⚠️ मास्टर यादी उपलब्ध नाही.")
elif total_remaining == 0:
    st.success(f"✅ {selected_asha} यांनी मास्टर यादीतील सर्व सहभागी नोंदवले आहेत!")
else:
    remaining_df = pd.DataFrame({
        '👩‍⚕️ आशा':   selected_asha,
        '👤 सहभागी': remaining_participants
    })
    remaining_df.index = range(1, len(remaining_df) + 1)
    remaining_df.index.name = 'अ.क्र.'

    styled3 = (
        remaining_df.style
        .set_properties(**{'font-family': 'Baloo 2, sans-serif', 'font-size': '14px', 'color': '#1b4f72'})
        .set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#d6eaf8'), ('color', '#1b4f72'),
                                          ('font-weight', '700'), ('font-size', '13px'),
                                          ('border', '1px solid #b8d9f0')]},
            {'selector': 'td', 'props': [('border', '1px solid #eaf4fb')]},
        ])
    )

    st.dataframe(styled3, use_container_width=True,
                 height=min(420, (len(remaining_df) + 1) * 42 + 10))

    buf3 = io.BytesIO()
    with pd.ExcelWriter(buf3, engine='openpyxl') as w:
        remaining_df.to_excel(w, sheet_name='उर्वरित सहभागी', index=True)
    st.download_button(
        label="⬇️ उर्वरित यादी Excel मध्ये डाउनलोड करा",
        data=buf3.getvalue(),
        file_name=f"उर्वरित_सहभागी_{selected_asha}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("</div>", unsafe_allow_html=True)

# =====================
# FOOTER
# =====================
st.markdown("""
<hr/>
<div style="text-align:center; color:#5a8aaa; font-size:13px; padding:6px 0 14px 0;">
    🌸 आशा मॉनिटरिंग डॅशबोर्ड &nbsp;·&nbsp; KoboToolbox द्वारे &nbsp;·&nbsp; Streamlit
</div>
""", unsafe_allow_html=True)
