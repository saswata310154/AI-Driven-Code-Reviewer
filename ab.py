import streamlit as st
import time

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="AI Driven Python Code Reviewer",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------------------------
# Imports (UNCHANGED)
# -------------------------------------------------
try:
    from code_parser import parse_code
    from style_checker import show_style_corrected
    from error_detector import detect_errors
    from ai_suggester import get_ai_suggestions
except ImportError:
    def parse_code(code): return {"success": True}
    def show_style_corrected(code):
        return {"success": True, "corrected_code": code}
    def detect_errors(code):
        return {"success": True, "error_count": 0, "errors": []}
    def get_ai_suggestions(code):
        return "AI suggestions unavailable."

# -------------------------------------------------
# SEMI-DARK, HIGH-READABILITY THEME
# -------------------------------------------------
st.markdown("""
<style>

/* ===== Base ===== */
html, body, [data-testid="stApp"] {
    background-color: #1e293b;   /* slate */
    color: #e5e7eb;              /* soft white */
}

/* ===== Headings ===== */
h1, h2, h3 {
    color: #f8fafc;
}

/* ===== Text Area ===== */
.stTextArea textarea {
    background-color: #f8fafc;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    font-family: Consolas, monospace;
}

/* ===== Buttons ===== */
.stButton button {
    background: linear-gradient(90deg, #3b82f6, #6366f1);
    color: #ffffff;
    border-radius: 10px;
    border: none;
    font-weight: 600;
}

/* ===== Cards ===== */
.card {
    background-color: #334155;
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 1rem;
}

/* ===== Metrics ===== */
[data-testid="stMetric"] {
    background-color: #334155;
    border-radius: 12px;
    padding: 1rem;
}

/* ===== Tabs ===== */
button[data-baseweb="tab"] {
    color: #cbd5e1;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff;
    border-bottom: 3px solid #93c5fd;
}

/* ===== Code Blocks (VERY IMPORTANT FIX) ===== */
pre {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border-radius: 12px;
    border: 1px solid #cbd5e1;
    padding: 1rem;
}

/* ===== AI Chat ===== */
[data-testid="stChatMessage"] {
    background-color: #475569;
    color: #f8fafc;
    border-radius: 14px;
    padding: 1rem;
}

/* ===== Status Widget ===== */
[data-testid="stStatusWidget"] {
    background-color: #334155;
    border-radius: 14px;
}

/* ===== Footer ===== */
footer {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("""
<div style="text-align:center; padding:1.2rem 0;">
    <h1>🧠 AI Driven Python Code Reviewer</h1>
    <p style="color:#cbd5e1;">
        Bug detection • Style correction • AI-powered insights
    </p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Layout
# -------------------------------------------------
col_input, col_output = st.columns([1.15, 1])

# -------------------------------------------------
# Input
# -------------------------------------------------
with col_input:
    st.subheader("📥 Code Input")
    code = st.text_area(
        "Paste Python code",
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
# Processing (UNCHANGED)
# -------------------------------------------------
if analyze_btn and code:
    with col_output:
        st.subheader("📊 Analysis Report")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.status("Running analysis pipeline...", expanded=True) as status:
            st.write("Parsing Python syntax")
            parse_result = parse_code(code)

            if not parse_result["success"]:
                status.update(label="Syntax Error", state="error")
                st.error("Invalid Python syntax.")
                st.stop()

            st.write("Detecting logical issues")
            error_result = detect_errors(code)
            issues = error_result.get("error_count", 0)

            if issues > 0:
                suggestions = (
                    "Fix detected errors before requesting AI improvements.\n\n"
                    "AI suggestions will include:\n"
                    "- Readability improvements\n"
                    "- Optimization tips\n"
                    "- Best practices"
                )
            else:
                st.write("Generating AI insights")
                suggestions = get_ai_suggestions(code)

            status.update(label="Analysis Completed", state="complete")
        st.markdown('</div>', unsafe_allow_html=True)

        m1, m2 = st.columns(2)
        m1.metric("Lines of Code", len(code.split("\n")))
        m2.metric("Issues Detected", issues)

        st.divider()

    # -------------------------------------------------
    # Tabs
    # -------------------------------------------------
    tab_errors, tab_style, tab_ai = st.tabs(
        ["🐞 Bugs & Errors", "🎨 Style Fixes", "🤖 AI Advice"]
    )

    with tab_errors:
        if issues == 0:
            st.success("No bugs or errors detected.")
        else:
            for err in error_result.get("errors", []):
                st.warning(f"{err.get('type')}: {err.get('message')}")
                st.info(f"Fix: {err.get('suggestion')}")

    with tab_style:
        style_result = show_style_corrected(code)
        if style_result.get("success"):
            st.code(style_result["corrected_code"], language="python")
        else:
            st.info("No formatting changes required.")

    with tab_ai:
        if suggestions:
            with st.chat_message("assistant"):
                st.write_stream(stream_data(suggestions))
        else:
            st.info("No AI advice available.")

elif analyze_btn and not code:
    st.toast("Please paste some code to analyze.", icon="⚠️")

else:
    with col_output:
        st.info("Waiting for Python code input…")
        st.markdown("""
        **Features**
        - Syntax & logical error detection
        - PEP8 style correction
        - AI-powered review suggestions
        """)
