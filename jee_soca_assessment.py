import streamlit as st
import google.generativeai as genai  # Use Gemini API
from fpdf import FPDF
import base64
import sqlite3
import datetime

# Gemini API Key (Replace with your key or use env variables)
GEMINI_API_KEY = "AIzaSyCk3hl_nA2c0uRAYK8Y0eYwDz0KBMCxP-M"
genai.configure(api_key=GEMINI_API_KEY)

# Set up SQLite database
def init_db():
    conn = sqlite3.connect("jee_soca.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    responses TEXT,
                    soca_report TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Enhanced questionnaire
def get_questions():
    return [
        {"question": "How confident are you in Physics?", "type": "scale", "options": [1, 2, 3, 4, 5]},
        {"question": "Which topic in Mathematics do you find most challenging?", "type": "text"},
        {"question": "How many hours do you study daily?", "type": "mcq", "options": ["<2", "2-4", "4-6", "6+"]},
        {"question": "How do you handle stress during exam preparation?", "type": "text"},
        {"question": "How well do you manage your time while solving exam papers?", "type": "scale", "options": [1, 2, 3, 4, 5]},
        {"question": "Which Chemistry topics do you find most challenging?", "type": "text"},
        {"question": "What is your preferred study technique? (e.g., notes, videos, group study, etc.)", "type": "text"},
        {"question": "How often do you take mock tests?", "type": "mcq", "options": ["Never", "Rarely", "Once a week", "More than once a week"]},
        {"question": "Do you revise your mistakes after taking a test?", "type": "mcq", "options": ["Always", "Sometimes", "Rarely", "Never"]},
    ]

# Function to generate SOCA analysis
def generate_soca_analysis(responses):
    prompt = f"""Analyze the following JEE student responses and provide a structured SOCA analysis:
    {responses}
    Format the output using Markdown for better readability. Use bullet points and bold text for key sections.
    """
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text  # Updated for Gemini API

# Function to generate and download PDF
def generate_pdf(report_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, report_text)
    
    pdf_filename = "SOCA_Report.pdf"
    pdf.output(pdf_filename)
    
    with open(pdf_filename, "rb") as f:
        pdf_data = f.read()
    return pdf_data

# Function to save responses to database
def save_to_db(responses, soca_report):
    conn = sqlite3.connect("jee_soca.db")
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO responses (timestamp, responses, soca_report) VALUES (?, ?, ?)",
              (timestamp, str(responses), soca_report))
    conn.commit()
    conn.close()

# Function to retrieve past reports
def get_past_reports():
    conn = sqlite3.connect("jee_soca.db")
    c = conn.cursor()
    c.execute("SELECT timestamp, soca_report FROM responses ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return data

# Streamlit UI
st.set_page_config(page_title="JEE SOCA Analysis", layout="wide")
st.title("📘 JEE Skill Assessment - SOCA Analysis")
st.markdown("---")

questions = get_questions()
responses = {}

# Questionnaire UI
with st.container():
    st.header("📝 Answer the following questions:")
    for q in questions:
        if q["type"] == "scale":
            responses[q["question"]] = st.slider(q["question"], min_value=1, max_value=5)
        elif q["type"] == "mcq":
            responses[q["question"]] = st.selectbox(q["question"], q["options"])
        else:
            responses[q["question"]] = st.text_input(q["question"], "")

# Generate Analysis Button
if st.button("🚀 Generate SOCA Analysis"):
    with st.spinner("Analyzing your responses..."):
        soca_report = generate_soca_analysis(responses)
        st.success("✅ Analysis Completed!")
        st.subheader("📊 Your SOCA Report")
        st.markdown(soca_report, unsafe_allow_html=True)
        
        # Save to database
        save_to_db(responses, soca_report)
        
        # Generate and provide PDF download option
        pdf_data = generate_pdf(soca_report)
        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="SOCA_Report.pdf">📥 Download Your SOCA Report</a>'
        st.markdown(href, unsafe_allow_html=True)

# Show past reports
st.markdown("---")
st.subheader("📜 Past SOCA Reports")
past_reports = get_past_reports()
if past_reports:
    for timestamp, report in past_reports:
        with st.expander(f"📅 {timestamp}"):
            st.markdown(report, unsafe_allow_html=True)
else:
    st.info("No past reports found.")
