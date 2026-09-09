<div align="center">

🤖 AI Resume Analyzer

Intelligent Resume Analysis, Scoring, Recommendations & Admin Analytics

A Streamlit-based resume analysis application that extracts useful information from resumes, evaluates resume quality, provides recommendations, and presents analytics for users and administrators.






Developed & customized by Utsav Singh

</div>

📌 Overview

AI Resume Analyzer is a resume analysis application built with Python and Streamlit. It parses uploaded resumes using Natural Language Processing techniques, identifies important resume information and skills, and provides useful recommendations to help users improve their resumes.

The project also includes an Admin section for viewing user data, exported records, feedback, ratings, and analytical charts.

✨ Main Features

👤 User / Client Side

Upload and analyze a resume

Extract basic resume information

Identify skills and important keywords

Predict suitable job field / role

Recommend additional skills

Recommend courses and certifications

Generate resume improvement tips

Calculate an overall resume score

Provide interview and resume-related recommendations

Show personalized analysis based on the uploaded resume

🧑‍💼 Admin Dashboard

View applicant/user data

View total user count

Export user information to CSV

View feedback and ratings

Analyze predicted fields / roles

Analyze experience levels

Analyze resume score distribution

View location-based analytics

View city, state and country statistics

💬 Feedback Module

Submit user feedback

Give ratings from 1 to 5

View rating analytics

View previous feedback/comments

🛠️ Tech Stack

Area

Technologies

Frontend / UI

Streamlit, HTML, CSS

Backend

Python

NLP & Resume Parsing

NLTK, pyresparser, pdfminer3

Data Processing

Pandas

Visualization

Plotly

Database

Local application database / configured database layer

Version Control

Git & GitHub

📂 Project Structure

AI-Resume-Analyzer/
│
├── App/
│   ├── app.py
│   ├── App1.py
│   ├── Courses.py
│   ├── nlp_loader.py
│   ├── resume_parser.py
│   ├── utils.py
│   ├── requirements.txt
│   │
│   └── Logo/
│       ├── Resume-Analyzer.mp4
│       ├── Updatedarkmode.jpeg
│       ├── Updatelightmode.jpeg
│       └── recommend.png
│
├── screenshots/
│   ├── user/
│   ├── admin/
│   └── feedback/
│
├── .gitignore
├── LICENSE
└── README.md

Uploaded resumes, virtual environments and local database files are intentionally excluded from the public repository.

📸 Application Screenshots

👤 User Side

1. Main Screen

<p align="center">
  <img src="screenshots/user/1-main-screen.jpeg" width="900" alt="AI Resume Analyzer Main Screen">
</p>

2. Resume Analysis

<p align="center">
  <img src="screenshots/user/2-analysis.png" width="900" alt="Resume Analysis">
</p>

3. Skill Recommendation

<p align="center">
  <img src="screenshots/user/3-recom.jpeg" width="900" alt="Skill Recommendation">
</p>

4. Course / Recommendation Section

<p align="center">
  <img src="screenshots/user/4-recomm.jpeg" width="900" alt="Course Recommendation">
</p>

5. Resume Recommendations

<p align="center">
  <img src="screenshots/user/5-recomm.png" width="900" alt="Resume Recommendations">
</p>

💬 Feedback Screens

Feedback Form

<p align="center">
  <img src="screenshots/feedback/1-form.png" width="900" alt="Feedback Form">
</p>

Feedback Analytics

<p align="center">
  <img src="screenshots/feedback/2-analytics.png" width="900" alt="Feedback Analytics">
</p>

🧑‍💼 Admin Dashboard

1. Admin / User Data Dashboard

<p align="center">
  <img src="screenshots/admin/1-main-user-data.png" width="900" alt="Admin Dashboard">
</p>

2. User Data

<p align="center">
  <img src="screenshots/admin/2-user-data.png" width="900" alt="User Data">
</p>

3. Exported CSV Data

<p align="center">
  <img src="screenshots/admin/3-user-datacsv.png" width="900" alt="Exported CSV Data">
</p>

4. Feedback Data

<p align="center">
  <img src="screenshots/admin/4-feed-data.png" width="900" alt="Feedback Data">
</p>

5. Experience Analytics

<p align="center">
  <img src="screenshots/admin/5-pieexp.png" width="900" alt="Experience Analytics">
</p>

6. Resume Score Analytics

<p align="center">
  <img src="screenshots/admin/6-piescre.png" width="900" alt="Resume Score Analytics">
</p>

7. Location Analytics

<p align="center">
  <img src="screenshots/admin/7-pielocation.png" width="900" alt="Location Analytics">
</p>

8. Country Analytics

<p align="center">
  <img src="screenshots/admin/8-piecountry.png" width="900" alt="Country Analytics">
</p>

🚀 Installation & Setup

1. Clone the repository

git clone https://github.com/utsavsingh1920/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

2. Create a virtual environment

python -m venv venv

3. Activate the virtual environment

Windows

venv\Scripts\activate

macOS / Linux

source venv/bin/activate

4. Install dependencies

cd App
pip install -r requirements.txt

5. Install the spaCy English model if required

python -m spacy download en_core_web_sm

6. Run the application

streamlit run app.py

Streamlit will display the local URL in the terminal, usually:

http://localhost:8501

💡 How It Works

Upload Resume
      ↓
Resume Parsing
      ↓
Information & Skill Extraction
      ↓
NLP-Based Analysis
      ↓
Role / Skill Recommendations
      ↓
Resume Score & Improvement Tips
      ↓
Analytics / Feedback

🔐 Privacy & Repository Safety

The public GitHub repository does not include:

Uploaded user resumes

Virtual environment (venv)

Local database files

Environment or secret files

This keeps personal and machine-specific data outside version control.

🔮 Future Improvements

Improve resume parsing accuracy

Add support for more job roles

Improve recommendation quality

Add more advanced skill matching

Improve resume scoring

Add more dashboard analytics

Add cloud deployment

Improve UI responsiveness

Add multilingual resume support

Add ATS-focused analysis

🎓 Project Purpose

This project was developed/customized as an academic and portfolio project to demonstrate practical skills in:

Python • Streamlit • NLP • Resume Parsing • Data Analysis • Visualization • Git • GitHub

🙏 Acknowledgements

This project uses and builds upon open-source tools and ideas from the resume parsing / NLP ecosystem, including:

pyresparser

NLTK

Streamlit

Plotly

The project was customized and developed further for academic and portfolio use. Existing third-party licenses and attribution should be preserved where applicable.

👨‍💻 Developer

Utsav Singh

B.Sc. Information Technology Graduate
Interested in Software Development, Flutter, Full-Stack Development and AI-based applications

GitHub: utsavsingh1920

Project Repository: AI-Resume-Analyzer

⭐ Support

If you find this project useful, consider giving the repository a ⭐ Star.

<div align="center">

🤖 AI RESUME ANALYZER

Built & customized with ❤️ by Utsav Singh

© 2026 Utsav Singh

</div>
