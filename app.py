import os, io, re, datetime
import fitz
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="SynthMed", page_icon="stethoscope", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*, *::before, *::after { font-family: Inter, sans-serif; box-sizing: border-box; }
.stApp { background: radial-gradient(ellipse at 20% 20%, #0d1f2d 0%, #0a0a0f 40%, #0d0a1e 100%); }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #080d14, #0d1117, #0a0d1a) !important; border-right: 1px solid rgba(16,185,129,0.15) !important; }
.hero-wrap { padding: 2.5rem 0 2rem; border-bottom: 1px solid rgba(16,185,129,0.1); margin-bottom: 2rem; }
.hero-eyebrow { font-size:0.68rem; font-weight:700; letter-spacing:0.2em; text-transform:uppercase; color:#10b981; margin-bottom:0.6rem; }
.hero-title { font-size:3.5rem; font-weight:800; line-height:1; background:linear-gradient(135deg,#10b981,#06b6d4,#6366f1); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:0.75rem; }
.hero-desc { color:#475569; font-size:0.95rem; line-height:1.6; max-width:640px; }
.badge-live { display:inline-flex; align-items:center; gap:0.4rem; padding:0.3rem 0.9rem; background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:100px; font-size:0.68rem; font-weight:700; color:#10b981; letter-spacing:0.08em; text-transform:uppercase; margin-left:0.75rem; vertical-align:middle; }
.pulse { width:6px; height:6px; background:#10b981; border-radius:50%; display:inline-block; animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.4;transform:scale(1.4)} }
.stat-row { display:flex; gap:1rem; margin-bottom:2rem; flex-wrap:wrap; }
.stat-card { flex:1; min-width:120px; background:linear-gradient(135deg,rgba(16,185,129,0.06),rgba(6,182,212,0.03)); border:1px solid rgba(16,185,129,0.15); border-radius:14px; padding:1.1rem 1.4rem; }
.stat-value { font-size:1.5rem; font-weight:700; color:#10b981; line-height:1; margin-bottom:0.25rem; }
.stat-label { font-size:0.68rem; font-weight:500; color:#475569; text-transform:uppercase; letter-spacing:0.1em; }
.result-card { background:linear-gradient(135deg,rgba(13,17,23,0.95),rgba(10,13,26,0.95)); border:1px solid rgba(16,185,129,0.2); border-radius:18px; padding:2rem; margin-bottom:1.5rem; position:relative; overflow:hidden; }
.result-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,#10b981,#06b6d4,#6366f1); }
.result-tag { display:inline-flex; align-items:center; gap:0.4rem; font-size:0.63rem; font-weight:700; letter-spacing:0.15em; text-transform:uppercase; color:#10b981; background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.2); border-radius:6px; padding:0.3rem 0.75rem; margin-bottom:1.1rem; }
.result-body { color:#94a3b8; font-size:0.9rem; line-height:1.85; }
.result-body strong { color:#e2e8f0; font-weight:600; }
.timeline-item { display:flex; gap:1.25rem; padding:1rem 0; border-bottom:1px solid rgba(255,255,255,0.04); }
.timeline-dot { width:12px; height:12px; border-radius:50%; background:#10b981; flex-shrink:0; margin-top:4px; box-shadow:0 0 8px rgba(16,185,129,0.5); }
.timeline-dot.yellow { background:#f59e0b; box-shadow:0 0 8px rgba(245,158,11,0.5); }
.timeline-dot.red { background:#ef4444; box-shadow:0 0 8px rgba(239,68,68,0.5); }
.timeline-text { color:#94a3b8; font-size:0.88rem; line-height:1.5; }
.history-item { background:rgba(16,185,129,0.04); border:1px solid rgba(16,185,129,0.12); border-radius:10px; padding:0.85rem 1rem; margin-bottom:0.5rem; }
.history-time { font-size:0.65rem; color:#475569; font-weight:600; }
.history-title { font-size:0.82rem; color:#94a3b8; margin-top:0.2rem; }
.disclaimer { background:rgba(245,158,11,0.05); border:1px solid rgba(245,158,11,0.15); border-radius:10px; padding:0.75rem 1rem; font-size:0.77rem; color:#78350f; margin-top:1.5rem; }
.stButton > button { background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(6,182,212,0.08)) !important; color:#10b981 !important; border:1px solid rgba(16,185,129,0.25) !important; border-radius:10px !important; font-weight:600 !important; font-size:0.8rem !important; width:100% !important; margin-bottom:0.35rem !important; }
.stButton > button:hover { background:linear-gradient(135deg,rgba(16,185,129,0.25),rgba(6,182,212,0.18)) !important; border-color:rgba(16,185,129,0.55) !important; color:#fff !important; }
div[data-testid="stFileUploader"] { background:rgba(16,185,129,0.03); border:1px dashed rgba(16,185,129,0.25); border-radius:12px; padding:0.25rem; }
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

def extract_text(pdf_file) -> str:
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

def md_to_html(text: str) -> str:
    text = re.sub(r"={3,}", "", text)
    text = re.sub(r"^#### (.+)$", r"<div style='font-size:0.88rem;font-weight:700;color:#06b6d4;margin:0.9rem 0 0.3rem;'>\1</div>", text, flags=re.MULTILINE)
    text = re.sub(r"^### (.+)$", r"<div style='font-size:0.95rem;font-weight:700;color:#10b981;margin:1rem 0 0.4rem;padding-top:0.5rem;border-top:1px solid rgba(16,185,129,0.1);'>\1</div>", text, flags=re.MULTILINE)
    text = re.sub(r"^## (.+)$", r"<div style='font-size:1.05rem;font-weight:700;color:#06b6d4;margin:1.25rem 0 0.5rem;'>\1</div>", text, flags=re.MULTILINE)
    text = re.sub(r"^# (.+)$", r"<div style='font-size:1.15rem;font-weight:800;color:#a78bfa;margin:1.5rem 0 0.6rem;'>\1</div>", text, flags=re.MULTILINE)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong style='color:#e2e8f0;font-weight:600;'>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em style='color:#cbd5e1;'>\1</em>", text)
    text = re.sub(r"^\* (.+)$", r"<div style='display:flex;gap:0.6rem;padding:0.2rem 0;align-items:flex-start;'><span style='color:#10b981;font-size:0.6rem;margin-top:5px;'>&#9679;</span><span>\1</span></div>", text, flags=re.MULTILINE)
    text = re.sub(r"^- (.+)$", r"<div style='display:flex;gap:0.6rem;padding:0.2rem 0;align-items:flex-start;'><span style='color:#10b981;font-size:0.6rem;margin-top:5px;'>&#9679;</span><span>\1</span></div>", text, flags=re.MULTILINE)
    text = re.sub(r"^(\d+)\. (.+)$", r"<div style='display:flex;gap:0.6rem;padding:0.2rem 0;'><span style='color:#06b6d4;font-weight:600;min-width:20px;'>\1.</span><span>\2</span></div>", text, flags=re.MULTILINE)
    text = re.sub(r"^---+$", r"<hr style='border:none;border-top:1px solid rgba(16,185,129,0.12);margin:1rem 0;'>", text, flags=re.MULTILINE)
    text = re.sub(r">> (.+)", r"<div style='background:rgba(245,158,11,0.08);border-left:3px solid #f59e0b;padding:0.6rem 1rem;border-radius:0 8px 8px 0;color:#92400e;font-size:0.82rem;margin-top:1rem;'>\1</div>", text)
    text = re.sub(r"\n{2,}", "<br><br>", text)
    text = text.replace("\n", "<br>")
    return text

def ask_groq(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1500,
        temperature=0.3,
    )
    return response.choices[0].message.content

def make_pdf(content: str) -> bytes:
    clean = re.sub(r"<[^>]+>", "", content)
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), clean[:3000], fontsize=9)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()

def save_history(title: str, content: str):
    st.session_state.history.append({
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "title": title,
        "content": content,
    })

SYSTEM = """You are SynthMed, a world-class medical AI assistant for clinical report analysis.
Analyze reports with precision, clarity, and empathy.
Use markdown: ### for section headers, ** for bold key terms, - for bullet points, numbered lists where appropriate.
Bold all critical findings and abnormal values.
End with: >> Always consult a qualified healthcare professional before making any medical decisions.
Never fabricate information not in the report."""

with st.sidebar:
    st.markdown("<div style='font-size:1.35rem;font-weight:800;background:linear-gradient(135deg,#10b981,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;padding:0.5rem 0 0.25rem;'>SynthMed</div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#1e3a2f;font-size:0.7rem;margin-bottom:1.25rem;'>Medical Report AI</div>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.6rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#1e3a2f;border-bottom:1px solid rgba(16,185,129,0.1);padding-bottom:0.4rem;margin-bottom:0.6rem;'>Primary Report</div>", unsafe_allow_html=True)
    pdf1 = st.file_uploader("Report 1", type=["pdf"], label_visibility="collapsed")

    st.markdown("<div style='font-size:0.6rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#1e3a2f;border-bottom:1px solid rgba(16,185,129,0.1);padding-bottom:0.4rem;margin:0.75rem 0 0.6rem;'>Compare Report (optional)</div>", unsafe_allow_html=True)
    pdf2 = st.file_uploader("Report 2", type=["pdf"], label_visibility="collapsed")

    st.markdown("<div style='font-size:0.6rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#1e3a2f;border-bottom:1px solid rgba(16,185,129,0.1);padding-bottom:0.4rem;margin:0.75rem 0 0.6rem;'>Analyze</div>", unsafe_allow_html=True)
    run_summary  = st.button("Summarize Report")
    run_diagnose = st.button("Diagnosis Insights")
    run_risks    = st.button("Risk Factors")
    run_meds     = st.button("Medications Review")
    run_timeline = st.button("Patient Timeline")
    run_compare  = st.button("Compare Reports")

    st.markdown("<div style='font-size:0.6rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#1e3a2f;border-bottom:1px solid rgba(16,185,129,0.1);padding-bottom:0.4rem;margin:0.75rem 0 0.6rem;'>Ask</div>", unsafe_allow_html=True)
    user_question = st.text_area("", placeholder="What does the LDL result mean?", height=80, label_visibility="collapsed")
    run_qa = st.button("Ask SynthMed")

    if st.session_state.history:
        st.markdown("<div style='font-size:0.6rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#1e3a2f;border-bottom:1px solid rgba(16,185,129,0.1);padding-bottom:0.4rem;margin:0.75rem 0 0.6rem;'>Session History</div>", unsafe_allow_html=True)
        for item in reversed(st.session_state.history[-5:]):
            st.markdown(f"<div class='history-item'><div class='history-time'>{item['time']}</div><div class='history-title'>{item['title']}</div></div>", unsafe_allow_html=True)

st.markdown("""
<div class='hero-wrap'>
    <div class='hero-eyebrow'>Medical AI Platform</div>
    <div class='hero-title'>SynthMed</div>
    <div class='hero-desc'>Upload any medical report and get AI-powered clinical insights, diagnosis analysis, risk identification, patient timelines, and multi-report comparisons.
    <span class='badge-live'><span class='pulse'></span>Live</span></div>
</div>
""", unsafe_allow_html=True)

if not pdf1:
    col1, col2 = st.columns([3, 2])
    with col1:
        steps = [("Upload","any medical report PDF from the sidebar"),("Summarize","get a plain-English clinical overview"),("Diagnosis Insights","deep analysis of all findings"),("Risk Factors","identify health risks and warnings"),("Patient Timeline","chronological view of findings"),("Compare Reports","upload 2 PDFs and diff them"),("Ask SynthMed","natural language Q&A on the report"),("Export PDF","download your analysis")]
        html = "".join(f"<div style='display:flex;align-items:flex-start;gap:1rem;padding:0.8rem 0;border-bottom:1px solid rgba(255,255,255,0.04);'><div style='width:26px;height:26px;background:linear-gradient(135deg,#10b981,#06b6d4);border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:0.72rem;font-weight:700;color:white;flex-shrink:0;'>{i+1}</div><div style='color:#94a3b8;font-size:0.86rem;line-height:1.5;'><span style='color:#e2e8f0;font-weight:600;'>{t}</span> - {d}</div></div>" for i,(t,d) in enumerate(steps))
        st.markdown(f"<div style='background:rgba(16,185,129,0.03);border:1px solid rgba(16,185,129,0.1);border-radius:18px;padding:2rem;'><div style='font-size:0.63rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#10b981;margin-bottom:1.25rem;'>How It Works</div>{html}</div>", unsafe_allow_html=True)
    with col2:
        caps = ["Clinical Summary Generation","Diagnosis & Test Result Analysis","Health Risk Identification","Medication & Drug Review","Patient Timeline Builder","Multi-Report Comparison","Natural Language Q&A","PDF Export of Analysis"]
        ch = "".join(f"<div style='color:#94a3b8;font-size:0.84rem;padding:0.55rem 0;border-bottom:1px solid rgba(255,255,255,0.04);'>{c}</div>" for c in caps)
        st.markdown(f"<div style='background:rgba(16,185,129,0.03);border:1px solid rgba(16,185,129,0.1);border-radius:18px;padding:2rem;'><div style='font-size:0.63rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#10b981;margin-bottom:1.25rem;'>Capabilities</div>{ch}</div>", unsafe_allow_html=True)

else:
    text1 = extract_text(pdf1)
    text2 = extract_text(pdf2) if pdf2 else None
    wc = len(text1.split())
    cc = len(text1)
    pc = text1.count("\x0c") + 1

    extra = f"<div class='stat-card'><div class='stat-value' style='font-size:0.85rem;color:#6366f1;'>{pdf2.name[:16]}</div><div class='stat-label'>Compare Loaded</div></div>" if pdf2 else ""
    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-card'><div class='stat-value'>{pc}</div><div class='stat-label'>Pages</div></div>
        <div class='stat-card'><div class='stat-value'>{wc:,}</div><div class='stat-label'>Words</div></div>
        <div class='stat-card'><div class='stat-value'>{cc:,}</div><div class='stat-label'>Characters</div></div>
        <div class='stat-card'><div class='stat-value' style='font-size:0.85rem;color:#06b6d4;'>{pdf1.name[:16]}</div><div class='stat-label'>Report Loaded</div></div>
        {extra}
    </div>""", unsafe_allow_html=True)

    def render(tag: str, content: str):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        save_history(tag, content[:80] + "...")
        st.markdown(f"""
        <div class='result-card'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;'>
                <div class='result-tag'>{tag}</div>
                <div style='font-size:0.65rem;color:#334155;'>{ts}</div>
            </div>
            <div class='result-body'>{md_to_html(content)}</div>
        </div>""", unsafe_allow_html=True)
        st.download_button(f"Export as PDF", data=make_pdf(content), file_name=f"synthmed_{tag.lower().replace(' ','_')}.pdf", mime="application/pdf", key=f"dl_{tag}_{ts}")

    if run_summary:
        with st.spinner("Generating summary..."):
            r = ask_groq(SYSTEM, f"Provide a comprehensive plain-English summary of this medical report:\n\n{text1[:8000]}")
        render("Report Summary", r)

    if run_diagnose:
        with st.spinner("Extracting clinical findings..."):
            r = ask_groq(SYSTEM, f"Extract and explain all diagnoses, test results, lab values, and clinical findings. Bold abnormal values:\n\n{text1[:8000]}")
        render("Diagnosis Insights", r)

    if run_risks:
        with st.spinner("Identifying risks..."):
            r = ask_groq(SYSTEM, f"Identify all health risk factors and abnormal values. Rate each as LOW / MEDIUM / HIGH risk:\n\n{text1[:8000]}")
        render("Risk Factors", r)

    if run_meds:
        with st.spinner("Reviewing medications..."):
            r = ask_groq(SYSTEM, f"List and explain all medications, dosages, purposes, and any noted side effects or interactions:\n\n{text1[:8000]}")
        render("Medications Review", r)

    if run_timeline:
        with st.spinner("Building timeline..."):
            r = ask_groq(SYSTEM, f"Extract all medical events chronologically. Format each as: [DATE] - [EVENT] - [SEVERITY: low/medium/high]\n\n{text1[:8000]}")
        save_history("Patient Timeline", r[:80] + "...")
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        st.markdown("<div class='result-card'><div class='result-tag'>Patient Timeline</div>", unsafe_allow_html=True)
        for line in [l.strip() for l in r.split("\n") if l.strip()]:
            dot = "red" if "high" in line.lower() else ("yellow" if "medium" in line.lower() else "")
            st.markdown(f"<div class='timeline-item'><div class='timeline-dot {dot}'></div><div class='timeline-text'>{md_to_html(line)}</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button("Export Timeline as PDF", data=make_pdf(r), file_name="synthmed_timeline.pdf", mime="application/pdf")

    if run_compare:
        if not text2:
            st.warning("Sidebar mein dono PDFs upload karo.")
        else:
            with st.spinner("Comparing reports..."):
                r = ask_groq(SYSTEM, f"Compare these two reports. Identify differences in diagnoses, lab values, new findings, resolved conditions:\nReport 1:\n{text1[:4000]}\n\nReport 2:\n{text2[:4000]}")
            render("Comparison Analysis", r)

    if run_qa:
        if user_question.strip():
            with st.spinner("Thinking..."):
                r = ask_groq(SYSTEM, f"Medical report:\n{text1[:8000]}\n\nQuestion: {user_question}")
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            save_history(f"Q: {user_question[:40]}", r[:80])
            st.markdown(f"""
            <div class='result-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem;'>
                    <div class='result-tag'>Answer</div>
                    <div style='font-size:0.65rem;color:#334155;'>{ts}</div>
                </div>
                <div style='color:#475569;font-size:0.78rem;font-style:italic;margin-bottom:0.75rem;'>Q: {user_question}</div>
                <div class='result-body'>{md_to_html(r)}</div>
            </div>""", unsafe_allow_html=True)
            st.download_button("Export Answer as PDF", data=make_pdf(r), file_name="synthmed_answer.pdf", mime="application/pdf", key=f"qa_{ts}")
        else:
            st.warning("Sidebar mein question type karo.")

    st.markdown("<div class='disclaimer'>SynthMed is an AI assistant for informational purposes only. Always consult a qualified healthcare professional for medical advice, diagnosis, or treatment.</div>", unsafe_allow_html=True)