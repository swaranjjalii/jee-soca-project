
# JEE SOCA Skill Assessment System

## Overview
The **JEE SOCA Skill Assessment System** is an AI-powered tool designed to help JEE aspirants assess their preparation strategies. It uses a **SOCA (Strengths, Opportunities, Challenges, and Action Plan)** analysis based on student responses to provide personalized feedback and recommendations.

## Features
✅ **User Authentication** (Secure login & signup)  
✅ **AI-Generated SOCA Reports** (Strengths, Weaknesses, and Actionable Insights)  
✅ **Past Reports Storage** (Retrieve and review previous assessments)  
✅ **Downloadable PDF Reports** (Save and share your SOCA analysis)  
✅ **Interactive Web UI** (Built using **Streamlit** for easy access)  

## Technology Stack
| Component          | Technology Used      |
|-------------------|---------------------|
| Web Framework    | **Streamlit**        |
| AI Model        | **Google Gemini API** |
| Database        | **SQLite**            |
| Authentication  | **SQLite & Hashlib**  |
| PDF Generation  | **FPDF**              |

## Installation Guide
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/yourusername/jee-soca-assessment.git
   cd jee-soca-assessment

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
3. **Set up the Database**
   ```bash
   python setup_db.py  # (Creates required tables)
4. **Run the Application**
   ```bash
   Run the Application

## Usage Instructions
1. Login or Register to access the assessment.
2. Answer the questionnaire to evaluate your JEE preparation.
3. Generate SOCA Analysis using AI-powered insights.
4. Download your SOCA report for future reference.
5. Review past reports to track progress.
