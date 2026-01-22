import streamlit as st
import time

# --- Configuration ---
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Imports with fallback ---
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
        if "def" in code and ":" not in code:
            return {
                "success": True,
                "error_count": 1,
                "errors": [{
                    "type": "SyntaxError",
                    "message": "Missing colon",
                    "suggestion": "Add ':' at the end of the line."
                }]
            }
        return {"success": True, "error_count": 0, "errors": []}

    # IMPORTANT: mock returns STRING
    def get_ai_suggestions(code):
        return (
            "Consider adding docstrings.\n"
            "Use clearer variable names.\n"
            "Follow PEP8 formatting."
        )

# --- Styling ---
st.markdown("""
<style>
div.stButton > button:first-child {
    background: linear-gradient(45deg, #4b6cb7, #182848);
    color: white;
    border-radius: 8px;
}
.stTextArea textarea {
    font-family: Consolas, monospace;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("Settings")
    if st.button("🔄 Reset App", use_container_width=True):
        st.rerun()
    st.caption("v2.0 • AI Code Reviewer")

# --- Header ---
st.title("⚡ AI Code Reviewer")
st.markdown("Paste Python code to detect bugs, fix style, and get AI insights.")

# --- Layout ---
col_input, col_output = st.columns([1, 1])

# --- Input ---
with col_input:
    code = st.text_area(
        "Paste Python Code:",
        height=450,
        placeholder="def hello():\n    print('Hello')"
    )
    analyze_btn = st.button("Analyze Code", type="primary", use_container_width=True)

# --- Typewriter ---
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# --- Processing ---
if analyze_btn and code:
    with col_output:
        st.subheader("🔍 Analysis Report")

        with st.status("Running diagnostics...", expanded=True) as status:
            st.write("Parsing syntax...")
            parse_result = parse_code(code)

            if not parse_result["success"]:
                status.update(label="Syntax Error", state="error")
                st.error("Invalid Python syntax.")
                st.stop()

            st.write("Detecting issues...")
            error_result = detect_errors(code)
            issues = error_result.get("error_count", 0)

            if issues > 0:
                suggestions = (
                    "⚠️ **Syntax errors detected**\n\n"
                    "Fix the errors shown above before requesting AI improvements.\n\n"
                    "Once the code runs correctly, the AI will suggest:\n"
                    "- Robustness improvements\n"
                    "- Readability (PEP 8)\n"
                    "- Optimization tips"
                )
            else:
                st.write("Generating AI insights...")
                suggestions = get_ai_suggestions(code)

            status.update(label="Analysis Complete!", state="complete")

        # --- Metrics ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Lines of Code", len(code.split("\n")))
        m2.metric("Issues Found", issues)
        m3.metric("Style Score", "Good" if issues == 0 else "Needs Work")

        st.divider()

    # --- Tabs ---
    tab_errors, tab_style, tab_ai = st.tabs(
        ["Bugs & Errors", "Style Fixes", "AI Advice"]
    )

    with tab_errors:
        if issues == 0:
            st.success("No issues found.")
        else:
            for err in error_result.get("errors", []):
                st.warning(f"**{err.get('type')}**: {err.get('message')}")
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
    st.toast("⚠️ Please enter some code!", icon="⚠️")

else:
    with col_output:
        st.info("Waiting for input…")
        st.markdown("""
        **Features**
        - Syntax checking
        - PEP8 formatting
        - AI-powered suggestions
        """)
