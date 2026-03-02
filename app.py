import streamlit as st
from graph.pipeline import run_research_pipeline
from utils.s3_handler import save_report_to_s3

st.set_page_config(
    page_title="Research Assistant",
    page_icon="◎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Jost:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background: #F5F4F0 !important;
    font-family: 'Jost', sans-serif;
    color: #1C1C2E;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}

[data-testid="stSidebar"] { display: none !important; }

.block-container {
    max-width: 680px !important;
    padding: 0 24px !important;
    margin: 0 auto !important;
}

/* ── Top bar ── */
.topbar {
    width: 100%;
    padding: 32px 0 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 80px;
}

.topbar-logo {
    font-family: 'Jost', sans-serif;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #1C1C2E;
}

.topbar-tag {
    font-size: 11px;
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #9B9B9B;
}

/* ── Hero ── */
.hero-block {
    margin-bottom: 64px;
}

.hero-overline {
    font-size: 11px;
    font-weight: 400;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #9B9B9B;
    margin-bottom: 20px;
}

.hero-heading {
    font-family: 'Cormorant Garamond', serif;
    font-size: 58px;
    font-weight: 300;
    line-height: 1.08;
    color: #1C1C2E;
    margin-bottom: 24px;
    letter-spacing: -0.5px;
}

.hero-heading em {
    font-style: italic;
    color: #14305A;
}

.hero-body {
    font-size: 14px;
    font-weight: 300;
    line-height: 1.85;
    color: #6B6B7B;
    max-width: 460px;
}

/* ── Divider ── */
.thin-rule {
    width: 100%;
    height: 1px;
    background: #DDDBD5;
    margin: 48px 0;
}

/* ── Input label ── */
.input-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #9B9B9B;
    margin-bottom: 12px;
}

/* ── Streamlit input ── */
.stTextInput > div > div > input {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 22px !important;
    font-weight: 300 !important;
    color: #1C1C2E !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 1.5px solid #1C1C2E !important;
    border-radius: 0 !important;
    padding: 10px 0 14px !important;
    box-shadow: none !important;
    outline: none !important;
    letter-spacing: 0.2px;
}

.stTextInput > div > div > input::placeholder {
    color: #BDBDBD !important;
    font-style: italic;
}

.stTextInput > div > div > input:focus {
    border-bottom-color: #14305A !important;
    box-shadow: none !important;
}

.stTextInput label { display: none !important; }
.stTextInput > div { border: none !important; box-shadow: none !important; }

/* ── Depth toggle ── */
.stRadio > label { display: none !important; }
.stRadio > div {
    display: flex !important;
    gap: 8px !important;
    flex-direction: row !important;
}

.stRadio > div > label {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #6B6B7B !important;
    cursor: pointer !important;
    padding: 8px 20px !important;
    border: 1px solid #DDDBD5 !important;
    border-radius: 100px !important;
    background: transparent !important;
    transition: all 0.2s !important;
}

.stRadio > div > label:hover {
    border-color: #1C1C2E !important;
    color: #1C1C2E !important;
}

/* ── Button ── */
.stButton > button {
    font-family: 'Jost', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    background: #1C1C2E !important;
    color: #F5F4F0 !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 16px 48px !important;
    width: 100% !important;
    transition: background 0.2s !important;
}

.stButton > button:hover {
    background: #14305A !important;
}

.stButton > button:disabled {
    background: #DDDBD5 !important;
    color: #9B9B9B !important;
}

/* ── Status box ── */
[data-testid="stStatus"] {
    background: white !important;
    border: 1px solid #DDDBD5 !important;
    border-radius: 0 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 13px !important;
}

/* ── Report ── */
.report-container {
    margin-top: 56px;
    padding-top: 48px;
    border-top: 1px solid #DDDBD5;
}

.report-container h1 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 38px !important;
    font-weight: 300 !important;
    color: #1C1C2E !important;
    line-height: 1.2 !important;
    margin-bottom: 32px !important;
    letter-spacing: -0.3px !important;
}

.report-container h2 {
    font-family: 'Jost', sans-serif !important;
    font-size: 10px !important;
    font-weight: 500 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    color: #9B9B9B !important;
    margin: 40px 0 16px !important;
    padding-top: 32px !important;
    border-top: 1px solid #DDDBD5 !important;
}

.report-container p {
    font-size: 15px !important;
    font-weight: 300 !important;
    line-height: 1.9 !important;
    color: #3D3D52 !important;
    margin-bottom: 16px !important;
}

.report-container li {
    font-size: 14px !important;
    font-weight: 300 !important;
    line-height: 1.85 !important;
    color: #3D3D52 !important;
    margin-bottom: 8px !important;
    padding-left: 4px !important;
}

.report-container ul {
    padding-left: 18px !important;
    margin-bottom: 16px !important;
}

/* ── Download ── */
.stLinkButton > a {
    font-family: 'Jost', sans-serif !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 3px !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: #1C1C2E !important;
    border: 1px solid #1C1C2E !important;
    border-radius: 0 !important;
    padding: 14px 40px !important;
    text-decoration: none !important;
    display: inline-block !important;
    transition: all 0.2s !important;
    margin-top: 40px !important;
}

.stLinkButton > a:hover {
    background: #1C1C2E !important;
    color: #F5F4F0 !important;
}

/* ── Footer ── */
.footer {
    margin-top: 96px;
    padding-bottom: 48px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #DDDBD5;
    padding-top: 24px;
}

.footer-left {
    font-size: 11px;
    font-weight: 300;
    color: #BDBDBD;
    letter-spacing: 1px;
}

.footer-right {
    font-size: 11px;
    font-weight: 300;
    color: #BDBDBD;
    letter-spacing: 1px;
}

.stSpinner > div {
    border-color: #1C1C2E transparent transparent transparent !important;
}

.stSuccess, .stWarning {
    font-family: 'Jost', sans-serif !important;
    border-radius: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">Research Assistant</div>
    <div class="topbar-tag">Multi-Agent · AI</div>
</div>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-block">
    <div class="hero-overline">Intelligent Research</div>
    <div class="hero-heading">Ask anything.<br><em>Know everything.</em></div>
    <div class="hero-body">
        Four specialized AI agents work in sequence, searching the live web, 
        reading every source, cross-referencing facts, and composing a 
        structured report with citations. All in under sixty seconds. With a report to download!
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="thin-rule"></div>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-label">Your question</div>', unsafe_allow_html=True)

topic = st.text_input(
    "topic",
    placeholder="What would you like to research?",
    label_visibility="collapsed"
)

depth = st.radio(
    "depth",
    ["quick", "deep"],
    format_func=lambda x: "Quick  —  5 sources" if x == "quick" else "Deep  —  10 sources",
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
generate = st.button("Generate Report", disabled=not topic)

# ── Pipeline ──────────────────────────────────────────────────────────────────
# Validation
MIN_WORDS = 3

# Validation
if generate and topic:
    words = topic.strip().split()
    too_short = len(words) < 3
    too_vague = len(topic.strip()) < 15
    gibberish = all(len(w) < 3 for w in words)

    if too_short or too_vague or gibberish:
        st.markdown("""
        <div style="
            font-family: 'Jost', sans-serif;
            font-size: 13px;
            font-weight: 300;
            color: #9B9B9B;
            letter-spacing: 0.5px;
            padding: 16px 0;
            border-top: 1px solid #DDDBD5;
        ">
            Please enter a specific research topic, try something like 
            <em style="color: #1C1C2E;">"impact of AI on healthcare 2024"</em> 
            or <em style="color: #1C1C2E;">"best programming languages to learn in 2025"</em>.
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # pipeline continues below...
# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-left">LangGraph · Groq · Tavily · AWS S3</div>
    <div class="footer-right">© 2026</div>
</div>
""", unsafe_allow_html=True)