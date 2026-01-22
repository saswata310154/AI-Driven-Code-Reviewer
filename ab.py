import streamlit as st
import time

# --- App Configuration ---
st.set_page_config(
    page_title="AI Code Reviewer Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Preserve Existing Imports ---
try:
    from code_parser import parse_code
    from style_checker import show_style_corrected
    from error_detector import detect_errors
    from ai_suggester import get_ai_suggestions
except ImportError:
    # Mock functions (UI demo only)
    def parse_code(code):
        return {"success": True}

    def show_style_corrected(code):
        return {"success": True, "corrected_code": "# Auto-formatted Code\n" + code.replace("  ", "    ")}

    def detect_errors(code):
        if "def" in code and ":" not in code:
            return {
                "success": True,
                "error_count": 1,
                "errors": [{
                    "type": "SyntaxError",
                    "message": "Missing ':' in function definition",
                    "suggestion": "Add ':' at the end of the function line"
                }]
            }
        return {"success": True, "error_count": 0, "errors": []}

    def get_ai_suggestions(code):
        return [{
            "type": "AISuggestion",
            "message": "Consider adding docstrings and meaningful variable names for better readability."
        }]

# --- Custom UI Styling ---
st.markdown("""
<style>
button[kind="primary"] {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border-radius: 10px;
    font-weight: 600;
}
button[kind="primary"]:hover {
    transform: scale(1.02);
}
.stTextArea textarea {
    font-family: Consolas, monospace;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    st.caption("Configure & manage analysis")

    st.markdown("---")
    if st.button("♻️ Restart Session", use_container_width=True):
        st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption("AI Code Reviewer • v2.1")
    st.caption("Static analysis + AI insights")

# --- Header ---
st.markdown("# 🧠 AI-Driven Code Reviewer")
st.markdown(
    "Analyze Python code for **syntax issues**, **style problems**, "
    "and receive **AI-powered improvement suggestions**."
)

# --- Layout ---
left, right = st.columns([1, 1], gap="large")

# --- Input Section ---
with left:
    st.subheader("📝 Code Input")
    code = st.text_area(
        "Paste your Python code below",
        height=460,
        placeholder="def greet(name)\n    print(f'Hello {name}')"
    )

    analyze_btn = st.button(
        "🚀 Run Code Review",
        type="primary",
        use_container_width=True
    )

# --- Typewriter Effect ---
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# --- Processing ---
if analyze_btn and code:
    with right:
        st.subheader("📊 Review Summary")

        with st.status("Analyzing your code...", expanded=True) as status:
            st.write("🔍 Parsing syntax")
            time.sleep(0.4)
            parse_result = parse_code(code)

            if not parse_result["success"]:
                status.update(label="Syntax Error Found", state="error")
                st.error("Invalid Python syntax detected.")
                st.stop()

            st.write("🧪 Detecting issues")
            error_result = detect_errors(code)

            st.write("🤖 Generating AI feedback")
            suggestions = get_ai_suggestions(code)

            status.update(label="Analysis Completed", state="complete", expanded=False)

        # --- Metrics ---
        c1, c2, c3 = st.columns(3)
        lines = len(code.split("\n"))
        issues = error_result.get("error_count", 0)

        c1.metric("Total Lines", lines)
        c2.metric("Issues Detected", issues)
        c3.metric("Code Health", "Excellent" if issues == 0 else "Needs Attention")

        st.divider()

    # --- Results Tabs ---
    tab1, tab2, tab3 = st.tabs(
        ["🐞 Issues", "🎨 Formatting", "🤖 AI Feedback"]
    )

    with tab1:
        if issues == 0:
            st.success("No issues detected. Your code looks clean!")
        else:
            for err in error_result.get("errors", []):
                st.warning(f"**{err.get('type')}** — {err.get('message')}")
                st.info(f"💡 Fix: {err.get('suggestion')}")

    with tab2:
        style_result = show_style_corrected(code)
        if style_result.get("success"):
            st.code(style_result["corrected_code"], language="python")
            st.button("📋 Copy Clean Code")
        else:
            st.info("Code formatting already optimal.")

    with tab3:
        for s in suggestions:
            with st.chat_message("assistant"):
                st.write_stream(stream_data(s.get("message", "")))

elif analyze_btn and not code:
    st.toast("⚠️ Please paste some Python code first", icon="⚠️")

else:
    with right:
        st.info("👈 Paste code and click **Run Code Review**")
        st.markdown("""
        **What this tool checks:**
        - Python syntax validity
        - Static code issues
        - PEP8-style formatting
        - AI-powered improvement tips
        """)
