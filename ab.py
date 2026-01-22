import streamlit as st
import time

# --- Configuration & Imports ---
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Imports Logic (Preserves your functionality) ---
# We try to import your modules. If they don't exist (e.g., for this demo), 
# we create dummy functions so the UI still works.
try:
    from code_parser import parse_code
    from style_checker import show_style_corrected
    from error_detector import detect_errors
    from ai_suggester import get_ai_suggestions
except ImportError:
    # Mock functions for UI demonstration purposes
    def parse_code(code):
        return {"success": True}
    
    def show_style_corrected(code):
        return {"success": True, "corrected_code": "# PEP8 Corrected\n" + code.replace("  ", "    ")}
    
    def detect_errors(code):
        # Mocking a random error for visual demonstration
        if "def" in code and ":" not in code:
             return {"success": True, "error_count": 1, "errors": [{"type": "SyntaxError", "message": "Missing colon", "suggestion": "Add a ':' at the end of the line."}]}
        return {"success": True, "error_count": 0, "errors": []}
    
    def get_ai_suggestions(code):
        return [{"type": "AISuggestion", "message": "This code looks good, but consider adding docstrings to your functions for better readability."}]

# --- Custom CSS for Beauty ---
st.markdown("""
<style>
    /* Gradient Button */
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #4b6cb7, #182848);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(45deg, #182848, #4b6cb7);
        box-shadow: 0 6px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Code Area Styling */
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        background-color: #f0f2f6; 
        color: #0e1117;
    }
    /* Dark mode adjustment for text area */
    @media (prefers-color-scheme: dark) {
        .stTextArea textarea {
            background-color: #262730;
            color: #fafafa;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2115/2115955.png", width=60) # Placeholder logo
    st.title("Settings")
    
    st.markdown("---")
    if st.button("🔄 Reset App", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    st.caption("v2.0 • AI Code Reviewer")

# --- Main Hero Section ---
st.title("⚡ AI Code Reviewer")
st.markdown("Transform your messy scripts into **production-ready** code. Paste below to detect bugs, fix style, and get AI insights.")

# --- Layout ---
col_input, col_output = st.columns([1, 1], gap="medium")

# --- Logic ---
with col_input:
    st.subheader("Input Code")
    code = st.text_area("Paste Python Code:", height=450, placeholder="def hello_world():\n    print('Hello!')")
    
    analyze_btn = st.button("Analyze Code", type="primary", use_container_width=True)

# Helper function for typewriter effect
def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

if analyze_btn and code:
    with col_output:
        st.subheader("🔍 Analysis Report")
        
        # 1. Processing Status
        with st.status("Running diagnostics...", expanded=True) as status:
            st.write("Parsing syntax...")
            time.sleep(0.5) # UX Delay
            parse_result = parse_code(code)
            
            if not parse_result["success"]:
                status.update(label="Syntax Error Detected!", state="error", expanded=True)
                st.error("Your code has syntax errors.")
                st.code(parse_result.get("error", {}).get("message", "Unknown Syntax Error"))
                st.stop()

            st.write("Checking PEP8 compliance...")
            error_result = detect_errors(code)
            
            st.write("Generating AI insights...")
            st.write("🧪 Detecting issues")
            error_result = detect_errors(code)

# ✅ DEFINE issues HERE
            issues = error_result.get("error_count", 0)

            if issues > 0:
                suggestions = (
        "⚠️ Syntax errors detected.\n\n"
        "Please fix the errors listed above before requesting AI improvements.\n"
        "Once the code runs correctly, the AI can suggest optimizations, "
        "readability improvements, and best practices."
    )
            else:
                suggestions = get_ai_suggestions(code)

            status.update(label="Analysis Complete!", state="complete", expanded=False)

        # 2. Metrics Dashboard
        m1, m2, m3 = st.columns(3)
        num_lines = len(code.split('\n'))
        err_count = error_result.get('error_count', 0)
        
        m1.metric("Lines of Code", num_lines)
        m2.metric("Issues Found", err_count, delta=-err_count, delta_color="inverse")
        m3.metric("Style Score", "Good" if err_count == 0 else "Needs Work")

        st.divider()

    # 3. Results Tabs
    tab_errors, tab_style, tab_ai = st.tabs(["Bugs & Errors", "Style Fixes", "AI Advice"])

    with tab_errors:
        if err_count == 0:
            st.success("Clean code! No static errors found.")
        else:
            for error in error_result.get("errors", []):
                st.warning(f"**{error.get('type', 'Issue')}**: {error.get('message', '')}")
                st.info(f"Suggestion: {error.get('suggestion', '')}")

    with tab_style:
        try:
            style_result = show_style_corrected(code)
            if style_result["success"]:
                st.code(style_result["corrected_code"], language="python")
                if st.button("Copy Formatted Code"):
                    st.toast("Code copied to clipboard! (simulated)")
            else:
                st.info("No styling changes needed.")
        except Exception:
            st.error("Style checker unavailable.")

    with tab_ai:
        for suggestion in suggestions:
            if suggestion.get("type") == "AISuggestion":
                with st.chat_message("assistant"):
                    st.write_stream(stream_data(suggestion.get("message", "")))
            elif suggestion.get("type") == "Error":
                st.error(suggestion.get("message"))

elif analyze_btn and not code:
    st.toast("⚠️ Please enter some code to analyze!", icon="⚠️")
else:
    # Empty state for the output column
    with col_output:
        st.info("Waiting for input... Hit 'Analyze' when ready.")
        st.markdown(
            """
            **Features:**
            - **Syntax Check:** Catches breaking errors instantly.
            - **PEP8 Formatting:** Auto-formats messy code.
            - **AI Suggestions:** Intelligent advice on logic & optimization.
            """
        )