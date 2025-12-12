import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import base64
from urllib.parse import quote_plus


# ═════════════════════════════════════════════════════════════════
# 1. PAGE CONFIGURATION
# ═════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Competitor Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═════════════════════════════════════════════════════════════════
# 2. ROBUST IMAGE LOADING
# ═════════════════════════════════════════════════════════════════
def get_base64_of_bin_file(bin_file):
    """Reads a binary file and converts it to base64 for CSS injection"""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# Get the absolute path of the folder where this script runs
current_folder = os.path.dirname(os.path.abspath(__file__))

# Define image paths using the absolute path
bg_texture_file = os.path.join(current_folder, "BG.png")

texture_b64 = get_base64_of_bin_file(bg_texture_file)

# CSS Logic
bg_css = ""

# Debugging: If images fail, we show a warning instead of a blue screen
if not texture_b64:
    bg_css = ".stApp { background-color: #333; }"
else:
    bg_css = f"""
    .stApp {{
        background-image: url("data:image/png;base64,{texture_b64}");
        background-position: center center;
        background-repeat: no-repeat;
        background-size: cover;
        background-attachment: fixed;
    }}
    """

# ═════════════════════════════════════════════════════════════════
# KEC LOGO (Top Right)
# ═════════════════════════════════════════════════════════════════
st.markdown("""
<style>
.logo-container {
    position: absolute;
    top: -75px;
    left: -50px;
    width: 50px;
    height: 30px;
    z-index: 999;
}
.logo-container img {
    width: 100%;
    height: auto;
    object-fit: contain;
}
</style>
""", unsafe_allow_html=True)

logo_path = os.path.join(current_folder, "KEC Logo.png")

if os.path.exists(logo_path):
    with open(logo_path, 'rb') as img_file:
        logo_b64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/jpeg;base64,{logo_b64}" alt="KEC Logo">
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="logo-container">
        <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/KEC%20Logo.jpg" alt="KEC Logo">
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════
# RPG LOGO (Top Right)
# ═════════════════════════════════════════════════════════════════
st.markdown("""
<style>
.logo-container-rpg {
    position: absolute;      /* attach to viewport */
    top: -110px;            /* visible area */
    right: -47px;          /* a bit inset from the edge */
    width: 90px;
    height: auto;
    z-index: 1000;        /* above other elements */
}
.logo-container-rpg img {
    width: 100%;
    height: auto;
    object-fit: contain;
}
</style>
""", unsafe_allow_html=True)

# IMPORTANT: match the actual filename exactly (case-sensitive on Streamlit Cloud)
logo_path_rpg = os.path.join(current_folder, "RPG logo.png")

if os.path.exists(logo_path_rpg):
    with open(logo_path_rpg, 'rb') as img_file:
        logo_b64_rpg = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <div class="logo-container-rpg">
            <img src="data:image/png;base64,{logo_b64_rpg}" alt="RPG logo">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    # Optional: temporary debug info
    st.write("RPG logo file not found at:", logo_path_rpg)

# ═════════════════════════════════════════════════════════════════
# 3. STYLING
# ═════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
/* APPLY BACKGROUND */
{bg_css}

/* FONTS */
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
html, body, [class*="css"] {{
    font-family: 'Calibri', 'Open Sans', sans-serif !important;
}}

/* HIDE STREAMLIT UI */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}
div[data-testid="stHeader"] {{background: transparent;}}

/* TITLE STYLES */
.main-title {{
    color: black;
    text-align: left;
    margin-left:-40px;
    font-size: 2.5rem;
    font-weight: 600;
    text-transform: uppercase;
    margin-top: -125px;
    letter-spacing: 2px;
}}

.sub-caption {{
    color: #000000;
    text-align: left;
    font-size: 1.2rem;
    font-weight: 400;
    margin-top: -90px;
    margin-bottom: -30px;
    margin-left:-40px;
    letter-spacing: 1px;
}}

/* ═══ CUSTOM TABS STYLING ═══ */
.custom-tabs-container {{
    margin-top: 10px;
}}

.tab-content {{
    margin-top: -150px;
}}
</style>
""", unsafe_allow_html=True)


# Custom CSS to match KEC branding (Blue theme)
st.markdown("""
<style>
    /* KEC Blue Colors */
    :root {
        --kec-blue-dark: #4A4A4A;
        --kec-blue-main: #666666;
        --kec-blue-light: #E8E8E8;
        --kec-accent: #808080;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Background */
    .stApp {
        background-color: transparent;
    }

    .header-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 50%;
    }
    
    .header-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    
    .header-text {
        color: white;
    }
    
    .header-title {
        font-size: 28px;
        font-weight: 700;
        width: 50%;
        margin-left: 10px;
        color: white;
    }
    
    .header-caption {
        font-size: 14px;
        margin: 4px 0 0 0;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
    }
    
    .header-logo {
        max-height: 60px;
        background: rgba(255, 255, 255, 0.95);
        padding: 8px 12px;
        border-radius: 6px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Executive Summary Cards */
    .exec-summary-card {
        background: white;
        border-left: -5px solid #0066cc;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0, 51, 102, 0.1);
        transition: all 0.3s ease;
    }
    
    .exec-summary-card:hover {
        box-shadow: 0 4px 16px rgba(0, 51, 102, 0.2);
        transform: translateY(-2px);
    }
    
    .exec-summary-title {
        font-size: 16px;
        font-weight: 700;
        color: #003366;
        margin: 0 0 12px 0;
        line-height: 1.4;
    }
    .exec-title-link {
    color: inherit;
    text-decoration: none;
}

.exec-title-link:hover {
    text-decoration: none;
}
    
    .exec-summary-text {
        font-size: 14px;
        color: #555;
        margin: 12px 0;
        line-height: 1.6;
        font-style: italic;
    }
    
    .exec-tags-container {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 12px;
    }
    
    .exec-tag {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
    }
    
    .exec-tag-competitor {
        background-color: #E8F4F8;
        color: #0066cc;
        border: 1px solid #0066cc;
    }
    
    .exec-tag-competitor:hover {
        background-color: #0066cc;
        color: white;
        transform: scale(1.05);
    }
    
    .exec-tag-category {
        background-color: #FFF3E0;
        color: #FF6B35;
        border: 1px solid #FF6B35;
    }
    
    .exec-tag-category:hover {
        background-color: #FF6B35;
        color: white;
        transform: scale(1.05);
    }
    
    .exec-tag-sbu {
        background-color: #F0F4FF;
        color: #003366;
        border: 1px solid #003366;
    }
    
    .exec-tag-sbu:hover {
        background-color: #003366;
        color: white;
        transform: scale(1.05);
    }
    
   /* Reduce vertical gap between filter groups */
    .filter-group {
        margin-bottom: 1px;   /* default would be larger; this tightens spacing */
    }

    /* Make filter select boxes rounded (only within the filter panel) */
    .filter-panel [data-testid="stSelectbox"] > div {
        border-radius: 12px !important;
        overflow: hidden;
    }

    /* Tighten vertical spacing inside the filter panel */

    /* Reduce space under "Filters", "Business Unit", etc. labels */
    .filter-panel div[data-testid="stMarkdown"] {
        margin-bottom: 1px !important;
    }

    /* Reduce space around each selectbox */
    .filter-panel div[data-testid="stSelectbox"] {
        margin-top: 0 !important;
        margin-bottom: 2px !important;
        border-left: -40px;
        padding-top: 0 !important;
        margin-left: -1500px;
        padding-bottom: 0 !important;
    }

    /* Optional: if you also use text inputs in the filter panel */
    .filter-panel div[data-testid="stTextInput"] {
        margin-top: 0 !important;
        margin-bottom: 0px !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    /* If you ever have text inputs in the filter panel, round them too */
    .filter-panel [data-testid="stTextInput"] > div {
        border-radius: 12px !important;
        overflow: hidden;
    }

    .filter-title {
        font-size: 14px;
        font-weight: 700;
        color: #003366;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #E8F4F8 0%, #bbdefb 100%);
        border: 2px solid #0066cc;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.15);
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        border-color: #003366;
        box-shadow: 0 8px 20px rgba(0, 51, 102, 0.25);
        transform: translateY(-4px);
    }
    
    .kpi-label {
        font-size: 12px;
        color: #003366;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 8px;
        letter-spacing: 0.5px;
    }
    
    .kpi-value {
        font-size: 36px;
        font-weight: 800;
        background: linear-gradient(135deg, #003366, #0066cc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .kpi-subtext {
        font-size: 12px;
        color: #004B9F;
        font-weight: 500;
    }
    
    /* Filter section */
    .stSelectbox, .stTextInput {
        background-color: white;
    }
    
    /* Table styling */
    .dataframe {
        font-size: 13px;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
        background: linear-gradient(135deg, #E8F4F8, #90caf9);
        color: #003366;
        border: 1px solid #0066cc;
    }
    
    .badge-competitor {
        background: linear-gradient(135deg, #004B9F, #0066cc);
        color: white;
        border: 1px solid #003366;
    }
    
    /* Status indicator */
    .sync-status {
        display: inline-block;
        padding: 8px 16px;
        background: linear-gradient(135deg, rgba(0, 102, 204, 0.2), rgba(0, 75, 159, 0.1));
        color: #004B9F;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        border: 2px solid #0066cc;
    }
    
    .sync-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: linear-gradient(135deg, #004B9F, #0066cc);
        animation: pulse 2s infinite;
        margin-right: 8px;
        box-shadow: 0 0 8px rgba(0, 102, 204, 0.6);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #004B9F, #0066cc);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #003366, #004B9F);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 51, 102, 0.3);
    }
    
    /* Section headers */
    h3 {
        color: #003366 !important;
        font-weight: 700 !important;
        margin-top: -35px !important;
        margin-right: -500px;
    }
    
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #004B9F, #0066cc);
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background: linear-gradient(135deg, #003366, #004B9F);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 51, 102, 0.3);
    }
    
    /* Category Header Box */
    .category-header-box {
        background: transparent;
        color: black;
        padding: 12px 20px;
        border-radius: 10px;
        margin-bottom: 16px;
        font-size: 16px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(0, 51, 102, 0.3);
    }
    
    .category-header-box:first-of-type {
        margin-top: 0;
    }

    /* ===== Custom Top Tabs ===== */
    .custom-tab-container {
        display: flex;
        justify-content: center;
        gap: 12px;
        width: 110%;          /* wider bar */
        margin-top: -110px;
        margin-left: -75px;
        margin-bottom: 4px;
    }

    .custom-tab {
        flex: 1;
        text-align: center;
        padding: 8px 16px;
        border-radius: 10px 10px 0 0;
        border: 2px solid black;
        border-bottom: none;
        background-color: transparent;
        color: black;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        font-size: 16px;
    }
    .custom-tab:hover {
        text-decoration: none !important;
}
    .custom-tab.active {
        background-color: #004B9F;  /* active blue */
        color: white;
        border-color: #004B9F;      /* blue border for active tab */
    }

    .custom-line {
        width: 110%;
        height: 2px;
        margin-left: -75px;
        background-color: black;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
/* Remove underline in normal state */
a.exec-title-link,
a.exec-title-link:link,
a.exec-title-link:visited,
a.exec-title-link:active,
a.exec-title-link:hover,
a.exec-title-link:focus {
    text-decoration: none !important;
    color: inherit;
}

/* Add underline only on hover */
a.exec-title-link:hover,
a.exec-title-link:focus {
    text-decoration: underline !important;
}
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = None
# Separate data for Executive Summary sheet
if 'exec_summary_data' not in st.session_state:
    st.session_state.exec_summary_data = None
if 'active_competitor' not in st.session_state:
    st.session_state.active_competitor = None
if 'active_sbu' not in st.session_state:
    st.session_state.active_sbu = None
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Executive Summary"

# Track applied filters for Competitor & SBU tab
if 'selected_sbu_filter' not in st.session_state:
    st.session_state.selected_sbu_filter = "All"
if 'selected_competitor_filter' not in st.session_state:
    st.session_state.selected_competitor_filter = "All"
if 'selected_category_filter' not in st.session_state:
    st.session_state.selected_category_filter = "All"

# Handle filters and tab coming from clickable links via URL query parameters
params = st.query_params  # new, non-experimental API

def _first_value(v):
    # st.query_params may give a string or a list; normalize to a single string
    if isinstance(v, list):
        return v[0] if v else None
    return v

# 1) Sub-tab clicks (Competitor / SBU / Category inside article cards)
#    → set both the dropdown UI and the applied filter state
if "competitor" in params:
    comp_param = _first_value(params["competitor"])
    if comp_param:
        # UI dropdowns
        st.session_state.filter_competitor = comp_param
        st.session_state.filter_sbu = "All"
        st.session_state.filter_category = "All"
        # Applied filters
        st.session_state.selected_competitor_filter = comp_param
        st.session_state.selected_sbu_filter = "All"
        st.session_state.selected_category_filter = "All"
        # Jump to Competitor & SBU tab
        st.session_state.active_tab = "Competitor & SBU"
        # IMPORTANT: consume this param so it doesn't override filters forever
        try:
            del st.query_params["competitor"]
        except KeyError:
            pass

elif "sbu" in params:
    sbu_param = _first_value(params["sbu"])
    if sbu_param:
        # UI dropdowns
        st.session_state.filter_sbu = sbu_param
        st.session_state.filter_competitor = "All"
        st.session_state.filter_category = "All"
        # Applied filters
        st.session_state.selected_sbu_filter = sbu_param
        st.session_state.selected_competitor_filter = "All"
        st.session_state.selected_category_filter = "All"
        # Jump to Competitor & SBU tab
        st.session_state.active_tab = "Competitor & SBU"
        # Consume param
        try:
            del st.query_params["sbu"]
        except KeyError:
            pass

elif "category" in params:
    cat_param = _first_value(params["category"])
    if cat_param:
        # UI dropdowns
        st.session_state.filter_category = cat_param
        st.session_state.filter_sbu = "All"
        st.session_state.filter_competitor = "All"
        # Applied filters
        st.session_state.selected_category_filter = cat_param
        st.session_state.selected_sbu_filter = "All"
        st.session_state.selected_competitor_filter = "All"
        # Jump to Competitor & SBU tab
        st.session_state.active_tab = "Competitor & SBU"
        # Consume param
        try:
            del st.query_params["category"]
        except KeyError:
            pass

# 2) Top tab clicks (our custom tabs use ?tab=... in the URL)
elif "tab" in params:
    tab_param = _first_value(params["tab"])
    valid_tabs = ["Executive Summary", "Competitor & SBU", "Industry"]
    if tab_param in valid_tabs:
        st.session_state.active_tab = tab_param

# Header WITH KEC logo on right
st.markdown("""
<div style="
    background: linear-gradient(to right, transparent 0%, #004B9F 40%, #004B9F 50%, #004B9F 60%, transparent 100%);
    padding: 15px 0px;
    margin: -190px -80px 0 -80px;
    display: flex;
    align-items: center;
">
    <div style="width: 100%; text-align:center; margin-top: -5px;">
        <h1 style="font-size: 18px; line-height: 1.0; margin: 0; padding: 0; color: white; font-family: 'Calibri', sans-serif; text-transform: uppercase;">
            Competitor Intelligence Dashboard
        </h1>
        <p style="font-size: 11px; line-height: 1.0; margin: 2px 0 0 0; padding: 0; color: rgba(255,255,255,0.9); font-family: 'Calibri', sans-serif;">
            Competition &amp; industry updates
        </p>
    </div>
</div>
""", unsafe_allow_html=True)# ═════════════════════════════════════════════════════════════════
# ═════════════════════════════════════════════════════════════════
# LOAD DEFAULT EXCEL FILE
# ═════════════════════════════════════════════════════════════════
def _process_news_dataframe(input_df: pd.DataFrame) -> pd.DataFrame:
    """Convert a raw sheet into the standard columns used by the app."""
    # Map normalized column names → real names (e.g. "summary " → "Summary")
    col_map = {str(c).strip().lower(): c for c in input_df.columns}

    processed_data = []
    for _, row in input_df.iterrows():
        sbu_list = str(row.get(col_map.get('sbu', 'SBU'), '')).split(',') if pd.notna(row.get(col_map.get('sbu', 'SBU'))) else []
        sbu_list = [s.strip() for s in sbu_list if s.strip()]

        comp_list = str(row.get(col_map.get('competitor', 'Competitor'), '')).split(',') if pd.notna(row.get(col_map.get('competitor', 'Competitor'))) else []
        comp_list = [c.strip() for c in comp_list if c.strip()]

        # ---- Link column (Link / link / LINK / with spaces) ----
        link_col_name = col_map.get('link')
        link_cell = row.get(link_col_name, None) if link_col_name else None
        link_value = str(link_cell).strip() if link_cell is not None else '#'
        if not link_value:
            link_value = '#'

        # ---- Summary column (Summary / summary / SUMMARY / with spaces) ----
        summary_col_name = col_map.get('summary')
        summary_cell = row.get(summary_col_name, '') if summary_col_name else ''
        if pd.isna(summary_cell):
            summary_cell = ''
        summary_text = str(summary_cell).strip()

        processed_data.append({
            'keyword': str(row.get(col_map.get('keyword', 'keyword'), '')).strip(),
            'category': str(row.get(col_map.get('category', 'Category'), row.get(col_map.get('keyword', 'keyword'), ''))).strip(),
            'newstitle': str(row.get(col_map.get('newstitle', 'newstitle'), 'No title')),
            'sbu_list': sbu_list,
            'competitor_list': comp_list,
            'publishedate': pd.to_datetime(row.get(col_map.get('publishedate', 'publishedate'), datetime.now())),
            'source': str(row.get(col_map.get('source', 'source'), 'Unknown')).strip(),
            'link': link_value,
            'summary': summary_text,   # <- from the Summary column in Excel
        })

    return pd.DataFrame(processed_data)

def load_default_data():
    """
    Load data from default Excel file stored in project.
    Returns: (all_articles_df, exec_summary_df)
    """
    excel_file_path = "competitor_data.xlsx"

    if os.path.exists(excel_file_path):
        try:
            xls = pd.ExcelFile(excel_file_path)

            # Sheet with all articles
            df_all_raw = pd.read_excel(xls, sheet_name="All")
            # Executive Summary sheet
            df_exec_raw = pd.read_excel(xls, sheet_name="Executive Summary")

            all_data = _process_news_dataframe(df_all_raw)
            exec_data = _process_news_dataframe(df_exec_raw)

            return all_data, exec_data

        except Exception as e:
            st.warning(f"Could not load default file: {str(e)}")
            return None, None

    return None, None


# Load default data on first run
if st.session_state.raw_data is None:
    default_all, default_exec = load_default_data()
    if default_all is not None:
        # "All" sheet → used by Competitor & SBU and Industry
        st.session_state.raw_data = default_all
        st.session_state.filtered_data = default_all.copy()
        # "Executive Summary" sheet → used only in Executive Summary tab
        st.session_state.exec_summary_data = default_exec


# Helper function to render article cards (Executive Summary style)
def render_article_card(article):
    """Render an article in the Executive Summary card format with clickable metadata tags"""
    competitor_list = article.get('competitor_list', []) or []
    sbu_list = article.get('sbu_list', []) or []

    competitor = competitor_list[0] if competitor_list else "Unknown"
    category = article.get('category', article.get('keyword', ''))
    sbu = sbu_list[0] if sbu_list else "General"

    # URL-encoded values for query params
    comp_q = quote_plus(competitor) if competitor_list else None
    cat_q = quote_plus(str(category)) if category else None
    sbu_q = quote_plus(sbu) if sbu_list else None

    # Build HTML for tags, keeping same classes/formatting
    competitor_tag_html = (
        f'<a class="exec-tag exec-tag-competitor" '
        f'href="?competitor={comp_q}" target="_self">{competitor}</a>'
        if comp_q else
        f'<span class="exec-tag exec-tag-competitor">{competitor}</span>'
    )

    category_tag_html = (
        f'<a class="exec-tag exec-tag-category" '
        f'href="?category={cat_q}" target="_self">{str(category).title()}</a>'
        if cat_q else
        f'<span class="exec-tag exec-tag-category">{str(category).title()}</span>'
    )

    sbu_tag_html = (
        f'<a class="exec-tag exec-tag-sbu" '
        f'href="?sbu={sbu_q}" target="_self">{sbu}</a>'
        if sbu_q else
        f'<span class="exec-tag exec-tag-sbu">{sbu}</span>'
    )

    # Title link (opens in a new tab if link exists)
    title_text = str(article.get('newstitle', 'No title'))
    link = str(article.get('link', '') or '').strip()

    if link and link != '#':
        title_html = f'<a href="{link}" target="_blank" class="exec-title-link">{title_text}</a>'
    else:
        title_html = title_text

    # ---- Use Summary column from Excel ----
    summary = str(article.get('summary', '') or '').strip()
    # Optional: simple fallback if Summary cell is empty
    if not summary:
        summary = "Summary not available."

    st.markdown(
        f"""
        <div class="exec-summary-card">
            <div class="exec-summary-title">{title_html}</div>
            <div class="exec-summary-text">
                {summary}
            </div>
            <div class="exec-tags-container">
                {competitor_tag_html}
                {category_tag_html}
                {sbu_tag_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Main dashboard
if st.session_state.raw_data is not None:
    # "All" sheet
    df_all = st.session_state.raw_data
    # "Executive Summary" sheet (fallback to All if missing)
    df_exec = (
        st.session_state.exec_summary_data
        if st.session_state.exec_summary_data is not None
        else df_all
    )

    # Main tabs - custom HTML tabs
    tab_labels = ["Executive Summary", "Competitor & SBU", "Industry"]
    current_tab = st.session_state.get("active_tab", "Executive Summary")

    tabs_html = []
    for label in tab_labels:
        is_active = (label == current_tab)
        css_class = "custom-tab active" if is_active else "custom-tab"
        href = f"?tab={quote_plus(label)}"
        tabs_html.append(f'<a class="{css_class}" href="{href}" target="_self">{label}</a>')

    st.markdown(
        f"""
        <div class="custom-tab-container">
            {''.join(tabs_html)}
        </div>
        <div class="custom-line"></div>
        """,
        unsafe_allow_html=True,
    )
# ==================== EXECUTIVE SUMMARY TAB ====================
    if current_tab == "Executive Summary":
        st.markdown(
            """
            <div style="margin-top: -60px; margin-bottom: 20px;">
                <h3 style="margin: 0; padding: 0; font-size: 24px;">Major Moves & Recent Developments</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Get all articles sorted by date
        all_articles = df_exec.sort_values('publishedate', ascending=False).copy()

        # Normalize category to lower case for comparison
        all_articles['category_normalized'] = (
            all_articles['category'].astype(str).str.strip().str.lower()
        )

        # Desired display order (must match normalized form)
        category_order = [
            "order wins",
            "new market entry",
            "mergers & acquisitions",
            "partnerships & alliances",
            "financial",
            "stock market",
            "leadership/management",
            "industry",
        ]

        # Show categories in the specified order
        for cat_norm in category_order:
            group_df = all_articles[all_articles['category_normalized'] == cat_norm]
            if group_df.empty:
                continue

            display_name = group_df['category'].iloc[0]  # original casing
            st.markdown(
                f'<div class="category-header-box">{str(display_name).upper()}</div>',
                unsafe_allow_html=True,
            )
            for _, article in group_df.iterrows():
                render_article_card(article)

        # Any remaining categories not in the list, appended at the end
        remaining = all_articles[~all_articles['category_normalized'].isin(category_order)]
        if not remaining.empty:
            grouped_other = remaining.groupby('category')
            for category, group_df in grouped_other:
                st.markdown(
                    f'<div class="category-header-box">{str(category).upper()}</div>',
                    unsafe_allow_html=True,
                )
                for _, article in group_df.iterrows():
                    render_article_card(article)
    # ==================== COMPETITOR & SBU TAB (COMBINED) ====================
    elif current_tab == "Competitor & SBU":
        st.markdown(
            """
            <div style="margin-top: -60px; margin-bottom: 20px;">
                <h3 style="margin: 0; padding: 0; font-size: 24px;">Competitor & Business Unit Analysis</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Get all unique values for filters (from "All" sheet)
        all_competitors = set()
        for comp_list in df_all['competitor_list']:
            all_competitors.update(comp_list)

        all_sbus = set()
        for sbu_list in df_all['sbu_list']:
            all_sbus.update(sbu_list)

        # Use 'category' column we created earlier (not 'keyword')
        all_categories = set(df_all['category'].unique())

        # Layout: Filter panel on left, articles on right
        col_filter, col_articles = st.columns([1, 3])

        # ---------- LEFT: FILTERS ----------
        with col_filter:
            st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
            st.markdown('<p class="filter-title">Filters</p>', unsafe_allow_html=True)

            # SBU Filter (UI only)
            st.markdown('<div class="filter-group">', unsafe_allow_html=True)
            st.markdown("**Business Unit**")
            ui_sbu = st.selectbox(
                "Select SBU",
                options=["All"] + sorted(list(all_sbus)),
                key="filter_sbu",
                label_visibility="collapsed",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Competitor Filter (UI only)
            st.markdown('<div class="filter-group">', unsafe_allow_html=True)
            st.markdown("**Competitor**")
            ui_competitor = st.selectbox(
                "Select Competitor",
                options=["All"] + sorted(list(all_competitors)),
                key="filter_competitor",
                label_visibility="collapsed",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Category Filter (UI only)
            st.markdown('<div class="filter-group">', unsafe_allow_html=True)
            st.markdown("**Category**")
            ui_category = st.selectbox(
                "Select Category",
                options=["All"] + sorted(list(all_categories)),
                key="filter_category",
                label_visibility="collapsed",
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Apply / Clear buttons in one row
            st.markdown("<br>", unsafe_allow_html=True)
            btn_col_apply, btn_col_clear = st.columns(2)
            with btn_col_apply:
                apply_clicked = st.button("Apply Filters", key="apply_filters_button")
            with btn_col_clear:
                clear_clicked = st.button("Clear Filters", key="clear_filters_button")

            st.markdown("</div>", unsafe_allow_html=True)

            # Handle Apply / Clear actions
            if apply_clicked:
                # Copy current UI selections into applied filter state
                st.session_state.selected_sbu_filter = ui_sbu
                st.session_state.selected_competitor_filter = ui_competitor
                st.session_state.selected_category_filter = ui_category

            if clear_clicked:
                # Reset applied filters to show all articles
                st.session_state.selected_sbu_filter = "All"
                st.session_state.selected_competitor_filter = "All"
                st.session_state.selected_category_filter = "All"

        # ---------- RIGHT: ARTICLES ----------
        with col_articles:
            # Apply filters based on applied filter state (not dropdowns directly)
            filtered_df = df_all.copy()

            sbu_filter = st.session_state.selected_sbu_filter
            comp_filter = st.session_state.selected_competitor_filter
            cat_filter = st.session_state.selected_category_filter

            if sbu_filter != "All":
                filtered_df = filtered_df[
                    filtered_df["sbu_list"].apply(lambda x: sbu_filter in x)
                ]

            if comp_filter != "All":
                filtered_df = filtered_df[
                    filtered_df["competitor_list"].apply(lambda x: comp_filter in x)
                ]

            if cat_filter != "All":
                filtered_df = filtered_df[filtered_df["category"] == cat_filter]

            # Sort by date
            filtered_df = filtered_df.sort_values("publishedate", ascending=False)

            st.markdown("<br>", unsafe_allow_html=True)

            # Display articles
            if len(filtered_df) > 0:
                for _, article in filtered_df.head(50).iterrows():
                    render_article_card(article)
            else:
                st.info("No articles match the selected filters. Try adjusting your filter criteria.")

    # ==================== INDUSTRY TAB (RENAMED) ====================
    elif current_tab == "Industry":
        st.markdown(
            """
            <div style="margin-top: -60px; margin-bottom: 20px;">
                <h3 style="margin: 0; padding: 0; font-size: 24px;">Industry Updates</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Sort by date descending
        all_articles_sorted = df_all.sort_values('publishedate', ascending=False).copy()

        # Define a "primary SBU" per article (first SBU in the list, or "General")
        all_articles_sorted['primary_sbu'] = all_articles_sorted['sbu_list'].apply(
            lambda x: x[0] if isinstance(x, list) and len(x) > 0 else "General"
        )

        # ===== Custom SBU display order =====
    # Put your desired SBU order here – these must match values in 'primary_sbu'
    sbu_order = ["Intl T&D", "India T&D", "Transportation", "Civil", "Renewables", "Oil & Gas", "General"]  # <-- edit this list

    # First, render SBUs in the specified order
    for sbu in sbu_order:
        group_df = all_articles_sorted[all_articles_sorted['primary_sbu'] == sbu]
        if group_df.empty:
            continue

        st.markdown(
            f'<div class="category-header-box">{str(sbu).upper()}</div>',
            unsafe_allow_html=True,
        )

        for _, article in group_df.iterrows():
            render_article_card(article)

    # Then, render any remaining SBUs that were not in sbu_order
    remaining = all_articles_sorted[
        ~all_articles_sorted['primary_sbu'].isin(sbu_order)
    ]
    if not remaining.empty:
        for sbu, group_df in remaining.groupby('primary_sbu'):
            st.markdown(
                f'<div class="category-header-box">{str(sbu).upper()}</div>',
                unsafe_allow_html=True,
            )

            for _, article in group_df.iterrows():
                render_article_card(article)
else:
    st.info("📂 Upload an Excel file using the button below to get started")
    st.markdown(
        """
        ### Expected Excel Format:
        Your Excel file should contain these columns:
        - **keyword**: The search keyword or topic
        - **newstitle**: Article title
        - **SBU**: Strategic Business Unit (comma-separated if multiple)
        - **Competitor**: Competitor names (comma-separated if multiple)
        - **publishedate**: Publication date
        - **source**: News source/publication
        - **link**: (Optional) Article link
        """
    )

# ═════════════════════════════════════════════════════════════════
# FILE UPLOADER AT BOTTOM (ALWAYS VISIBLE)
# ═════════════════════════════════════════════════════════════════
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("📁 Browse for files", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        xls = pd.ExcelFile(uploaded_file)

        # Read both sheets
        df_all_raw = pd.read_excel(xls, sheet_name="All")
        df_exec_raw = pd.read_excel(xls, sheet_name="Executive Summary")

        # Process both into standard format
        all_data = _process_news_dataframe(df_all_raw)
        exec_data = _process_news_dataframe(df_exec_raw)

        # Store in session
        st.session_state.raw_data = all_data                      # "All" sheet
        st.session_state.filtered_data = all_data.copy()
        st.session_state.exec_summary_data = exec_data            # "Executive Summary" sheet

        st.success(f"✅ File uploaded successfully! {len(all_data)} articles loaded from 'All' sheet.")
        st.rerun()

    except Exception as e:
        st.error(f"Error loading file: {str(e)}")

if st.session_state.raw_data is not None:
    st.markdown(
        '<div class="sync-status"><span class="sync-indicator"></span>Data Synced</div>',
        unsafe_allow_html=True,
    )




























