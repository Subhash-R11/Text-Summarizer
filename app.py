import streamlit as st
from summarizer import summarize

# Page Config
st.set_page_config(
    page_title="LLM Text Summarizer",
    page_icon="📝",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    h1, h2, h3 { font-family: 'DM Serif Display', serif; }

    .main { background: #0f0f0f; color: #f0ede8; }

    /* Sticky header */
    .sticky-header {
        position: sticky;
        top: 0;
        z-index: 999;
        background: var(--background-color, #ffffff);
        padding: 8px 0;
    }
    .sticky-header h1 {
        margin: 0;
    }
    .sticky-header em {
        font-size: 14px;
    }

    .stTextArea textarea {
        background: #ffffff !important;
        color: #111111 !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 15px !important;
    }
    .stat-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .stat-number { font-size: 2rem; font-weight: 700; color: #e8c97e; }
    .stat-label  { font-size: 0.8rem; color: #888; text-transform: uppercase; letter-spacing: 1px; }
    .summary-box {
        background: #111111;
        border-left: 3px solid #e8c97e;
        border-radius: 0 12px 12px 0;
        padding: 24px;
        font-size: 16px;
        line-height: 1.8;
        color: #f0ede8;
    }
    .key-point {
        background: #1e1e1e;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        border: 1px solid #2a2a2a;
        color: #d4d0ca;
    }
    .stButton > button {
        background: #e8c97e !important;
        color: #0f0f0f !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 32px !important;
        font-size: 16px !important;
        width: 100%;
    }
    .stButton > button:hover { background: #f0d890 !important; }
    div[data-testid="stSelectbox"] label { color: #888 !important; font-size: 13px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1>📝 Text Summarizer</h1>
    <em>Powered by Llama 3.3 via Groq API</em>
""", unsafe_allow_html=True)
st.divider()

# Layout
col1, col2 = st.columns([1.2, 1], gap="large", vertical_alignment="top")

with col1:
    st.markdown("### Input Text")

    text_input = st.text_area(
        "Text to summarize:",
        value="",
        height=300,
        placeholder="Paste any article, document, or text here...",
        label_visibility="collapsed",
    )

    word_count = len(text_input.split()) if text_input.strip() else 0
    st.caption(f"📊 {word_count} words entered")

    st.markdown("### Options")
    oc1, oc2 = st.columns(2)
    with oc1:
        style = st.selectbox("Summary Style", [
            ("concise",  "📄 Concise Prose"),
            ("bullets",  "• Bullet Points"),
            ("eli5",     "🧒 Explain Simply"),
            ("academic", "🎓 Academic"),
        ], format_func=lambda x: x[1])

    with oc2:
        length = st.selectbox("Length", [
            ("short",  "Short (~50 words)"),
            ("medium", "Medium (~120 words)"),
            ("long",   "Long (~230 words)"),
        ], format_func=lambda x: x[1])

    summarize_btn = st.button("✨ Summarize", use_container_width=True)

with col2:
    st.markdown("### Summary")

    if summarize_btn:
        if not text_input.strip():
            st.warning("Please enter some text first!")
        elif word_count < 20:
            st.warning("Text is too short. Please enter at least a paragraph.")
        else:
            with st.spinner("Summarizing with Llama 3.3..."):
                try:
                    result = summarize(text_input, style=style[0], length=length[0])

                    # Stats row
                    s1, s2, s3 = st.columns(3)
                    with s1:
                        st.markdown(f"""<div class="stat-card">
                            <div class="stat-number">{result['word_count_original']}</div>
                            <div class="stat-label">Original Words</div>
                        </div>""", unsafe_allow_html=True)
                    with s2:
                        st.markdown(f"""<div class="stat-card">
                            <div class="stat-number">{result['word_count_summary']}</div>
                            <div class="stat-label">Summary Words</div>
                        </div>""", unsafe_allow_html=True)
                    with s3:
                        st.markdown(f"""<div class="stat-card">
                            <div class="stat-number">{result['compression_ratio']}%</div>
                            <div class="stat-label">Compressed</div>
                        </div>""", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Summary
                    st.markdown(f'<div class="summary-box">{result["summary"]}</div>', unsafe_allow_html=True)

                    # Key Points
                    if result.get("key_points"):
                        st.markdown("<br>**Key Points**", unsafe_allow_html=True)
                        for point in result["key_points"]:
                            st.markdown(f'<div class="key-point">→ {point}</div>', unsafe_allow_html=True)

                    # Download button
                    st.download_button(
                        "📋 Download Summary",
                        data=f"Summary:\n{result['summary']}\n\nKey Points:\n" + "\n".join(f"• {p}" for p in result["key_points"]),
                        file_name="summary.txt",
                        mime="text/plain",
                    )

                except Exception as e:
                    st.error(f"Error: {e}\n\nMake sure your GROQ_API_KEY is set correctly.")
    else:
        st.markdown("""
        <div style="
            border: 2px dashed #2a2a2a;
            border-radius: 12px;
            padding: 60px 20px;
            text-align: center;
            color: #444;
        ">
            <div style="font-size: 3rem">📄</div>
            <div style="margin-top: 12px">Your summary will appear here</div>
            <div style="font-size: 13px; margin-top: 8px">Enter text and click Summarize</div>
        </div>
        """, unsafe_allow_html=True)

