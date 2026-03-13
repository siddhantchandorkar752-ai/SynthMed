import os
import fitz
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="SynthMed", page_icon="https://img.icons8.com/fluency/48/caduceus.png", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { font-family: 'Inter', sans-serif; box-sizing: border-box; }

.stApp {
    background: radial-gradient(ellipse at 20% 20%, #0d1f2d 0%, #0a0a0f 40%, #0d0a1e 100%);
    min-height: 100vh;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d14 0%, #0d1117 60%, #0a0d1a 100%) !important;
    border-right: 1px solid rgba(16,185,129,0.15) !important;
}

section[data-testid="stSidebar"] > div { padding-top: 1.5rem; }

div[data-testid="stFileUploader"] {
    background: rgba(16,185,129,0.04);
    border: 1px dashed rgba(16,185,129,0.3);
    border-radius: 12px;
    padding: 0.5rem;
}

.hero-wrap {
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid rgba(16,185,129,0.1);
    margin-bottom: 2.5rem;
}

.hero-eyebrow {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #10b981;
    margin-bottom: 0.75rem;
}

.hero-title {
    font-size: 4rem;
    font-weight: 800;
    line-height: 1;
    background: linear-gradient(135deg, #10b981 0%, #06b6d4 50%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}

.hero-desc {
    color: #475569;
    font-size: 1rem;
    line-height: 1.6;
    max-width: 600px;
}

.badge-live {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.9rem;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 700;
    color: #10b981;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-left: 0.75rem;
    vertical-align: middle;
}

.pulse {
    width: 6px; height: 6px;
    background: #10b981;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(1.4); }
}

.stat-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}

.stat-card {
    flex: 1;
    background: linear-gradient(135deg, rgba(16,185,129,0.06), rgba(6,182,212,0.03));
    border: 1px solid rgba(16,185,129,0.15);
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    transition: border-color 0.3s;
}

.stat-card:hover { border-color: rgba(16,185,129,0.4); }

.stat-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #10b981;
    line-height: 1;
    margin-bottom: 0.3rem;
}

.stat-label {
    font-size: 0.7rem;
    font-weight: 500;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.result-card {
    background: linear-gradient(135deg, rgba(13,17,23,0.9), rgba(10,13,26,0.9));
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 18px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #10b981, #06b6d4, #6366f1);
}

.result-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #10b981;
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 6px;
    padding: 0.3rem 0.75rem;
    margin-bottom: 1.25rem;
}

.result-body {
    color: #94a3b8;
    font-size: 0.92rem;
    line-height: 1.85;
}

.result-body strong, .result-body b {
    color: #e2e8f0;
    font-weight: 600;
}

.howto-card {
    background: rgba(16,185,129,0.03);
    border: 1px solid rgba(16,185,129,0.1);
    border-radius: 18px;
    padding: 2rem 2.5rem;
}

.howto-step {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 0.9rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

.howto-step:last-child { border-bottom: none; }

.step-num {
    width: 28px; height: 28px;
    background: linear-gradient(135deg, #10b981, #06b6d4);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; color: white;
    flex-shrink: 0; margin-top: 1px;
}

.step-text { color: #94a3b8; font-size: 0.88rem; line-height: 1.5; }
.step-text span { color: #e2e8f0; font-weight: 600; }

.file-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 100px;
    padding: 0.4rem 1rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: #10b981;
    margin-bottom: 1.5rem;
}

.sidebar-logo {
    font-size: 1.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #10b981, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sidebar-sub {
    color: #334155;
    font-size: 0.72rem;
    margin-top: 0.2rem;
    margin-bottom: 1.5rem;
}

.sidebar-label {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #1e3a2f;
    border-bottom: 1px solid rgba(16,185,129,0.1);
    padding-bottom: 0.5rem;
    margin-bottom: 0.75rem;
    margin-top: 1rem;
}

.stButton > button {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(6,182,212,0.1)) !important;
    color: #10b981 !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    width: 100% !important;
    margin-bottom: 0.4rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(16,185,129,0.3), rgba(6,182,212,0.2)) !important;
    border-color: rgba(16,185,129,0.6) !important;
    color: #fff !important;
}

textarea {
    background: rgba(16,185,129,0.04) !important;
    border: 1px solid rgba(16,185,129,0.2) !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
}

.disclaimer {
    background: rgba(245,158,11,0.05);
    border: 1px solid rgba(245,158,11,0.15);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-size: 0.78rem;
    color: #92400e;
    margin-top: 1.5rem;
}

div[data-testid="stSpinner"] { color: #10b981 !important; }
</style>
""", unsafe_allow_html=True)


def extract_text(pdf_file) -> str:
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)


def ask_groq(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        max_tokens=1500,
        temperature=0.3,
    )
    return response.choices[0].message.content


SYSTEM = """You are SynthMed, a world-class medical AI assistant built for clinical report analysis.
Your job is to analyze medical reports with precision, clarity, and empathy.
Always structure your response with clear headers and bullet points.
Highlight critical findings in bold.
End every response with: ">> Always consult a qualified healthcare professional before making any medical decisions."
Never fabricate information not present in the report."""


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>SynthMed</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-sub'>Medical Report AI Assistant</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-label'>Upload Report</div>", unsafe_allow_html=True)
    pdf = st.file_uploader("PDF only", type=["pdf"], label_visibility="collapsed")

    st.markdown("<div class='sidebar-label'>Analyze</div>", unsafe_allow_html=True)
    run_summary  = st.button("Summarize Report")
    run_diagnose = st.button("Diagnosis Insights")
    run_risks    = st.button("Risk Factors")
    run_meds     = st.button("Medications Review")

    st.markdown("<div class='sidebar-label'>Ask Anything</div>", unsafe_allow_html=True)
    user_question = st.text_area("Your question", placeholder="What does the LDL result mean?", height=90, label_visibility="collapsed")
    run_qa = st.button("Ask SynthMed")

    st.markdown("""
    <div style='margin-top:2rem; padding:0.75rem; background:rgba(16,185,129,0.04);
         border:1px solid rgba(16,185,129,0.1); border-radius:10px;'>
        <div style='font-size:0.65rem; color:#1e3a2f; font-weight:700;
             letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.5rem;'>Stack</div>
        <div style='font-size:0.72rem; color:#334155; line-height:1.9;'>
            Groq LLaMA 3.3 70B<br>PyMuPDF<br>Streamlit
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-wrap'>
    <div class='hero-eyebrow'>Medical AI Platform</div>
    <div class='hero-title'>SynthMed</div>
    <div class='hero-desc'>
        Upload any medical report and get instant AI-powered clinical insights, 
        diagnosis analysis, risk identification, and natural language Q&A.
        <span class='badge-live'><span class='pulse'></span>Live</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── No PDF uploaded ───────────────────────────────────────────────────────────
if not pdf:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        <div class='howto-card'>
            <div style='font-size:0.65rem; font-weight:700; letter-spacing:0.18em;
                 text-transform:uppercase; color:#10b981; margin-bottom:1.25rem;'>
                How It Works
            </div>
            <div class='howto-step'>
                <div class='step-num'>1</div>
                <div class='step-text'><span>Upload</span> any medical report PDF from the sidebar</div>
            </div>
            <div class='howto-step'>
                <div class='step-num'>2</div>
                <div class='step-text'>Click <span>Summarize Report</span> for a plain-English overview</div>
            </div>
            <div class='howto-step'>
                <div class='step-num'>3</div>
                <div class='step-text'>Click <span>Diagnosis Insights</span> for deep clinical analysis</div>
            </div>
            <div class='howto-step'>
                <div class='step-num'>4</div>
                <div class='step-text'>Click <span>Risk Factors</span> to identify health risks</div>
            </div>
            <div class='howto-step'>
                <div class='step-num'>5</div>
                <div class='step-text'>Click <span>Medications Review</span> for drug analysis</div>
            </div>
            <div class='howto-step'>
                <div class='step-num'>6</div>
                <div class='step-text'>Type any question and click <span>Ask SynthMed</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background:rgba(16,185,129,0.03); border:1px solid rgba(16,185,129,0.1);
             border-radius:18px; padding:2rem;'>
            <div style='font-size:0.65rem; font-weight:700; letter-spacing:0.18em;
                 text-transform:uppercase; color:#10b981; margin-bottom:1.25rem;'>
                Capabilities
            </div>
            <div style='display:flex; flex-direction:column; gap:0.75rem;'>
                <div style='color:#94a3b8; font-size:0.85rem; padding:0.6rem 0;
                     border-bottom:1px solid rgba(255,255,255,0.04);'>
                    Clinical Summary Generation
                </div>
                <div style='color:#94a3b8; font-size:0.85rem; padding:0.6rem 0;
                     border-bottom:1px solid rgba(255,255,255,0.04);'>
                    Diagnosis & Test Result Analysis
                </div>
                <div style='color:#94a3b8; font-size:0.85rem; padding:0.6rem 0;
                     border-bottom:1px solid rgba(255,255,255,0.04);'>
                    Health Risk Identification
                </div>
                <div style='color:#94a3b8; font-size:0.85rem; padding:0.6rem 0;
                     border-bottom:1px solid rgba(255,255,255,0.04);'>
                    Medication & Drug Review
                </div>
                <div style='color:#94a3b8; font-size:0.85rem; padding:0.6rem 0;'>
                    Natural Language Q&A
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── PDF uploaded ──────────────────────────────────────────────────────────────
else:
    text = extract_text(pdf)
    char_count = len(text)
    word_count = len(text.split())
    page_count = text.count("\x0c") + 1

    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-card'>
            <div class='stat-value'>{page_count}</div>
            <div class='stat-label'>Pages</div>
        </div>
        <div class='stat-card'>
            <div class='stat-value'>{word_count:,}</div>
            <div class='stat-label'>Words</div>
        </div>
        <div class='stat-card'>
            <div class='stat-value'>{char_count:,}</div>
            <div class='stat-label'>Characters</div>
        </div>
        <div class='stat-card'>
            <div class='stat-value' style='font-size:0.95rem; color:#06b6d4;'>{pdf.name[:20]}</div>
            <div class='stat-label'>File Loaded</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if run_summary:
        with st.spinner("Analyzing report..."):
            result = ask_groq(SYSTEM, f"Provide a comprehensive plain-English summary of this medical report. Structure it clearly:\n\n{text[:8000]}")
        st.markdown(f"""
        <div class='result-card'>
            <div class='result-tag'>Report Summary</div>
            <div class='result-body'>{result.replace(chr(10), '<br>')}</div>
        </div>""", unsafe_allow_html=True)

    if run_diagnose:
        with st.spinner("Extracting clinical findings..."):
            result = ask_groq(SYSTEM, f"Extract and explain all diagnoses, test results, lab values, and clinical findings. Highlight abnormal values:\n\n{text[:8000]}")
        st.markdown(f"""
        <div class='result-card'>
            <div class='result-tag'>Diagnosis Insights</div>
            <div class='result-body'>{result.replace(chr(10), '<br>')}</div>
        </div>""", unsafe_allow_html=True)

    if run_risks:
        with st.spinner("Identifying risk factors..."):
            result = ask_groq(SYSTEM, f"Identify all health risk factors, abnormal values, and warning signs in this report. Explain the clinical significance of each:\n\n{text[:8000]}")
        st.markdown(f"""
        <div class='result-card'>
            <div class='result-tag'>Risk Factors</div>
            <div class='result-body'>{result.replace(chr(10), '<br>')}</div>
        </div>""", unsafe_allow_html=True)

    if run_meds:
        with st.spinner("Reviewing medications..."):
            result = ask_groq(SYSTEM, f"List and explain all medications mentioned in this report. Include dosage, purpose, and any noted side effects or interactions:\n\n{text[:8000]}")
        st.markdown(f"""
        <div class='result-card'>
            <div class='result-tag'>Medications Review</div>
            <div class='result-body'>{result.replace(chr(10), '<br>')}</div>
        </div>""", unsafe_allow_html=True)

    if run_qa:
        if user_question.strip():
            with st.spinner("Thinking..."):
                result = ask_groq(SYSTEM, f"Medical report:\n{text[:8000]}\n\nPatient question: {user_question}")
            st.markdown(f"""
            <div class='result-card'>
                <div class='result-tag'>Answer</div>
                <div style='color:#64748b; font-size:0.8rem; margin-bottom:0.75rem;
                     font-style:italic;'>Q: {user_question}</div>
                <div class='result-body'>{result.replace(chr(10), '<br>')}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.warning("Please type a question in the sidebar first.")

    st.markdown("""
    <div class='disclaimer'>
        SynthMed is an AI assistant for informational purposes only. 
        Always consult a qualified healthcare professional for medical advice, diagnosis, or treatment.
    </div>
    """, unsafe_allow_html=True)