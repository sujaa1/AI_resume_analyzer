AI Resume Analyzer & Career Assistant

An AI-powered web application that analyzes resumes against job descriptions using Google Gemini AI, provides ATS scoring, skill gap analysis, job comparison, and an interactive career chatbot.

 Features
 Resume Analysis
Upload resume (PDF)
ATS score generation (0–100)
Matched & missing skills detection
Strengths & weaknesses analysis
Career improvement suggestions
⚖️ Multiple Job Comparison
Compare resume against multiple job roles
Role-based scoring system
Visual bar chart comparison
Helps choose best job match
💬 AI Career Assistant (Chatbot)
Chat with AI about your resume
Ask career-related questions:
Skill improvement
Career roadmap
Job readiness
Infinite conversation memory
🧠 Tech Stack
Frontend: Streamlit
AI Model: Google Gemini (gemini-2.5-flash)
Backend: Python
PDF Parsing: PyPDF
Visualization: Plotly, Pandas
Environment: python-dotenv
📁 Project Structure
AI-RESUME-ANALYZER/
│
├── app.py                # Main Streamlit application
├── utils.py              # PDF text extraction
├── requirements.txt      # Dependencies
├── .env                  # API key storage
└── README.md
⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
2️⃣ Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Add API Key

Create a .env file:

GEMINI_API_KEY=your_api_key_here

👉 Get API key from:
https://aistudio.google.com/

5️⃣ Run the application
streamlit run app.py
🧪 How It Works
Upload your resume (PDF)
Paste job description(s)
AI analyzes resume using Gemini
Get:
ATS Score
Skill gap analysis
Career suggestions
Chat with AI assistant for guidance
📊 Example Output
ATS Score: 78/100
Matched Skills: Python, SQL, Machine Learning
Missing Skills: Docker, AWS
Final Verdict: Strong Match
💬 AI Chat Examples

Ask things like:

"How can I improve my resume?"
"What skills should I learn next?"
"Am I ready for data analyst role?"
"Give me a roadmap for AI engineer"

🔥 Future Improvements
Resume PDF download report
Voice-based AI assistant
Resume rewrite generator
Login system + user history
Deployment as SaaS platform