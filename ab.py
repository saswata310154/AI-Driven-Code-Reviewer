import streamlit as st
import time

# -------------------------------------------------
# Page Configuration (NO sidebar)
# -------------------------------------------------
st.set_page_config(
    page_title="AI Python Code Reviewer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# Imports with fallback (UNCHANGED LOGIC)
# -------------------------------------------------
try:
    from code_parser import parse_code
    from style_checker import show_style_corrected
    from error_detector import detect_errors
    from ai_suggester import get_ai_suggestions
except ImportError:
    def parse_code(code):
        return {"success": True}

    def show_style_corrected(code):
        return {
            "success": True,
            "corrected_code": "# PEP8 Corrected\n" + code.replace("  ", "    ")
        }

    def detect_errors(code):
        return {"success": True, "error_count": 0, "errors": []}

    def get_ai_suggestions(code):
        return "AI suggestions unavailable."

# -------------------------------------------------
# Global Dark Theme Styling (CUSTOM, UNIQUE)
# -------------------------------------------------
st.markdown("""
<style>

/* ---- App Background ---- */
html, body, [data-testid="stApp"] {
    background-color: #0f172a;
    color: #e5e7eb;
}

/* ---- Headings ---- */
h1, h2, h3 {
    color: #f8fafc;
}

/* ---- Text Area ---- */
.stTextArea textarea {
    background-color: #020617;
    color: #e5e7eb;
    border: 1px solid #334155;
    font-family: Consolas, monospace;
}

/* ---- Buttons ---- */
div.stButton > button {
    background: linear-gradient(90deg, #2563eb, #4f46e5);
    color: white;
    border-radius: 10px;
    border: none;
    height: 3rem;
    font-weight: 600;
}

/* ---- Status Box ---- */
[data-testid="stStatusWidget"] {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 10px;
}

/* ---- Metrics ---- */
[data-testid="stMetric"] {
    background-color: #020617;
    border-radius: 10px;
    padding: 1rem;
}

/* ---- Tabs ---- */
button[data-baseweb="tab"] {
    color: #cbd5f5;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff;
    border-bottom: 2px solid #6366f1;
}

/* ---- Code Blocks ---- */
pre {
    background-color: #020617 !important;
    border-radius: 10px;
    border: 1px solid #1e293b;
}

/* ---- Footer removal ---- */
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Header Section (NEW)
# -------------------------------------------------
st.markdown("""
<div style="text-align:center; padding:1.5rem 0;">
    <h1>🧠 AI Python Code Reviewer</h1>
    <p style="color:#94a3b8; font-size:1.05rem;">
        Static analysis • PEP8 formatting • AI-powered insights
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Layout
# -------------------------------------------------
col_input, col_output = st.columns([1.1, 1])

# -------------------------------------------------
# Input Section
# -------------------------------------------------
with col_input:
    st.subheader("📥 Code Input")
    code = st.text_area(
        "Paste Python code below",
        height=450,
        placeholder="def hello():\n    print('Hello World')",
        label_visibility="collapsed"
    )
    analyze_btn = st.button("🚀 Analyze Code", use_container_width=True)

# -------------------------------------------------
# Typewriter Effect (UNCHANGED)
# -------------------------------------------------
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# -------------------------------------------------
# Processing Logic (UNCHANGED)
# -------------------------------------------------
if analyze_btn and code:
    with col_output:
        st.subheader("📊 Analysis Report")

        with st.status("Running analysis pipeline...", expanded=True) as status:
            st.write("• Parsing Python syntax")
            parse_result = parse_code(code)

            if not parse_result["success"]:
                status.update(label="Syntax Error", state="error")
                st.error("Invalid Python syntax.")
                st.stop()

            st.write("• Detecting logical issues")
            error_result = detect_errors(code)
            issues = error_result.get("error_count", 0)

            if issues > 0:
                suggestions = (
                    "⚠️ Fix the detected errors before requesting AI improvements.\n\n"
                    "Once corrected, AI will provide:\n"
                    "- Readability improvements\n"
                    "- Optimization tips\n"
                    "- Best practices"
                )
            else:
                st.write("• Generating AI insights")
                suggestions = get_ai_suggestions(code)

            status.update(label="Analysis Completed", state="complete")

        # ---- Metrics (Style Score REMOVED) ----
        m1, m2 = st.columns(2)
        m1.metric("Lines of Code", len(code.split("\n")))
        m2.metric("Issues Detected", issues)

        st.divider()

    # -------------------------------------------------
    # Tabs Section
    # -------------------------------------------------
    tab_errors, tab_style, tab_ai = st.tabs(
        ["🐞 Bugs & Errors", "🎨 Style Fixes", "🤖 AI Advice"]
    )

    with tab_errors:
        if issues == 0:
            st.success("No bugs or errors detected.")
