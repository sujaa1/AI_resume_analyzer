import streamlit as st
import os
import re
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv
from google import genai
from utils import extract_text_from_pdf

# ------------------ LOAD API ------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ------------------ SESSION STATE INIT ------------------
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "chat_visible" not in st.session_state:
    st.session_state.chat_visible = False

if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------ GEMINI ANALYSIS ------------------
def analyze_resume(resume_text, job_desc):

    prompt = f"""
You are an ATS Resume Analyzer.

Return STRICT format:

ATS Score: X/100

Matched Skills:
- ...

Missing Skills:
- ...

Strengths:
- ...

Weaknesses:
- ...

Improvement Suggestions:
- ...

Final Verdict:
Strong / Medium / Weak Match

Resume:
{resume_text}

Job Description:
{job_desc}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ------------------ CHAT FUNCTION (FIXED) ------------------
def ask_ai(resume_text, history, question):

    prompt = f"""
You are a Career AI Assistant.

RULES:
- Answer ONLY the question
- Be short and clear
- Focus on career, skills, roadmap
- Use resume only if needed

Resume:
{resume_text}

Chat History:
{history}

User Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


# ------------------ SCORE EXTRACTION ------------------
def extract_score(text):
    match = re.search(r"(\d+)\s*/\s*100", text)
    if match:
        return int(match.group(1))
    return 0


# ------------------ GAUGE ------------------
def show_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "ATS Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 40], 'color': "red"},
                {'range': [40, 70], 'color': "orange"},
                {'range': [70, 100], 'color': "lightgreen"},
            ]
        }
    ))

    st.plotly_chart(fig)


# ------------------ UI ------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title(" AI Resume Analyzer")

menu = st.sidebar.selectbox(
    "Select Feature",
    ["Single Job Analysis", "Multiple Job Comparison"]
)

# =========================================================
# 1. SINGLE JOB ANALYSIS
# =========================================================
if menu == "Single Job Analysis":

    st.header(" Single Job Analysis")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_desc = st.text_area("Paste Job Description")

    if st.button("Analyze Resume"):

        if uploaded_file and job_desc:

            with st.spinner("Analyzing..."):

                resume_text = extract_text_from_pdf(uploaded_file)

                st.session_state.resume_text = resume_text
                st.session_state.chat_visible = True

                result = analyze_resume(resume_text, job_desc)

                st.success("Analysis Done")

                st.subheader(" Report")
                st.markdown(result)

                score = extract_score(result)
                show_gauge(score)

        else:
            st.warning("Please upload resume and job description")


# =========================================================
# 2. MULTIPLE JOB COMPARISON
# =========================================================
elif menu == "Multiple Job Comparison":

    st.header(" Compare Resume with Multiple Jobs")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    job1 = st.text_area("Job Description 1")
    job2 = st.text_area("Job Description 2")
    job3 = st.text_area("Job Description 3 (optional)")

    if st.button("Compare Jobs"):

        if uploaded_file and job1:

            resume_text = extract_text_from_pdf(uploaded_file)

            jobs = [job1, job2, job3]
            results = []

            for i, job in enumerate(jobs):

                if job.strip():

                    result = analyze_resume(resume_text, job)
                    score = extract_score(result)

                    results.append({
                        "Job": f"Job {i+1}",
                        "Score": score
                    })

            df = pd.DataFrame(results)

            st.subheader("📊 Comparison Chart")
            st.bar_chart(df.set_index("Job"))
            st.dataframe(df)

        else:
            st.warning("Upload resume and at least 1 job description")


# =========================================================
# 3. INFINITE CHATBOT (FIXED PRO VERSION)
# =========================================================
if st.session_state.chat_visible:

    st.sidebar.markdown("---")
    st.sidebar.subheader("💬 Career AI Assistant")

    # show chat history
    for msg in st.session_state.messages:
        with st.sidebar.chat_message(msg["role"]):
            st.sidebar.write(msg["content"])

    # input box (infinite chat)
    user_q = st.sidebar.chat_input("Ask about skills, roadmap, career...")

    if user_q:

        # save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_q
        })

        # build history string
        history_text = "\n".join(
            [f"{m['role']}: {m['content']}" for m in st.session_state.messages]
        )

        # AI response
        answer = ask_ai(
            st.session_state.resume_text,
            history_text,
            user_q
        )

        # save AI message
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()