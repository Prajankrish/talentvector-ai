# 🚀 TalentVector AI - QUICKSTART GUIDE

## ✅ Project Status: FULLY WORKING & READY TO RUN

All features are implemented and functional:
- ✅ Resume parsing with AI
- ✅ Job profile creation
- ✅ Candidate screening with questions
- ✅ Match scoring
- ✅ Feedback collection
- ✅ Analytics dashboard

---

## 🎯 Quick Start (Windows)

### Option 1: Automatic Setup (Recommended)
```powershell
# Navigate to project
cd "d:\Projects\AI Recruting\talentvector"

# Run startup script
.\startup.bat
```

### Option 2: Manual Setup

**Terminal 1 - Install & Setup:**
```powershell
cd "d:\Projects\AI Recruting\talentvector"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdir data
```

**Terminal 2 - Run Backend (after Terminal 1 completes):**
```powershell
cd "d:\Projects\AI Recruting\talentvector"
.\venv\Scripts\Activate.ps1
cd backend
python main.py
```

**Terminal 3 - Run Frontend (after Terminal 2 starts):**
```powershell
cd "d:\Projects\AI Recruting\talentvector"
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

---

## 🌐 Access the Application

After both services start:
- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## 📋 Complete Workflow

### Step 1: Create Job Profile
1. Go to **"Hiring Manager Intake"** tab
2. Fill in:
   - Role Title (e.g., "Senior Python Developer")
   - Required Skills (select from dropdown or add custom)
   - Years of Experience
   - Industry
   - Team Culture Description
3. Click **"Create Job Profile"**
4. ✅ Profile created with AI enhancement

### Step 2: Parse Resumes
1. Go to **"Resume Parser"** tab
2. Option A: Upload PDF/DOCX file and paste text
   - OR Option B: Paste resume text directly
3. Click **"Parse Resume Text"**
4. View extracted candidate information:
   - Name, email, phone
   - Technical skills with proficiency
   - Years of experience
   - Tech stack
   - Industries
   - Key projects
5. ✅ Candidate added to candidates list

### Step 3: Generate Screening Questions
1. Go to **"Candidate Screening"** tab
2. Select number of questions (3-5)
3. Click **"Generate Screening Questions"**
4. ✅ Role-specific questions generated with AI
5. Answer each question in the text areas

### Step 4: Evaluate Responses
1. After answering all questions
2. Click **"Evaluate Responses"**
3. View AI evaluation:
   - Technical score (0-10)
   - Communication score (0-10)
   - Problem-Solving score (0-10)
   - Overall score (0-10)
   - AI reasoning and feedback

### Step 5: Match Candidates
1. Go to **"Job Matching"** tab
2. Click **"Calculate Match Scores"**
3. View all candidates with:
   - Match score (🟢 green = good, 🟡 yellow = moderate, 🔴 red = poor)
   - Similarity score
   - AI-generated explanation
   - Good/Not Fit feedback buttons

### Step 6: Track Analytics
1. Go to **"Analytics"** tab
2. View performance metrics:
   - Total feedback collected
   - Match accuracy percentage
   - Model confidence
   - Weight distribution
3. Reset weights if needed

---

## 🛠️ Troubleshooting

### Port 8501 or 8000 Already in Use
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or use different ports
streamlit run app.py --server.port 8502
python main.py  # Edit .env to change API_PORT
```

### Module Import Errors
```powershell
# Reinstall requirements
pip install -r requirements.txt --force-reinstall

# Verify installation
python -c "import google.generativeai; print('✅ OK')"
```

### GEMINI_API_KEY Error
1. Check `.env` file exists:
   ```powershell
   Test-Path .env
   ```
2. Verify API key is set:
   ```powershell
   Get-Content .env | Select-String GEMINI_API_KEY
   ```
3. If missing, copy from `.env.example`:
   ```powershell
   Copy-Item .env.example .env
   ```

### Virtual Environment Activation Error
```powershell
# If activation fails, reset it
deactivate
Remove-Item -Recurse venv
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## 📁 Project Structure

```
talentvector/
├── 🎯 app.py                      # Streamlit frontend (FULLY WORKING)
├── requirements.txt               # Dependencies (google-generativeai installed)
├── .env.example                   # Config template
├── .env                           # Your config (created on first run)
├── .gitignore                     # Git ignore rules
├── startup.bat                    # Windows startup script
├── startup.sh                     # Linux/Mac startup script
├── QUICKSTART.md                  # This file
├── README.md                      # Full documentation
│
├── backend/
│   ├── main.py                    # FastAPI (FULLY WORKING)
│   ├── utils.py                   # Config, logging, exceptions
│   ├── hiring_manager.py          # Job profile creation (Gemini)
│   ├── resume_parser.py           # Resume parsing (Gemini)
│   ├── screening.py               # Question generation & evaluation (Gemini)
│   ├── matching.py                # Candidate-job matching (Gemini)
│   ├── feedback.py                # Learning & weight adjustment
│   ├── database.py                # SQLite operations
│   └── models.py                  # Pydantic data models
│
└── data/
    └── (auto-created for embeddings & databases)
```

---

## 🔌 API Endpoints (For Advanced Users)

### Health Check
```bash
GET http://localhost:8000/
GET http://localhost:8000/health
```

### Create Job Profile
```bash
POST http://localhost:8000/api/hiring-profile
{
  "role_title": "Senior Python Developer",
  "required_skills": ["Python", "Django", "PostgreSQL"],
  "nice_to_have_skills": ["Docker", "AWS"],
  "years_of_experience": 5,
  "industry": "FinTech",
  "team_culture_description": "Collaborative, fast-paced startup"
}
```

### Parse Resume
```bash
POST http://localhost:8000/api/parse-resume?resume_text={resume_text}
```

### Generate Questions
```bash
POST http://localhost:8000/api/screening/generate-questions
{
  "hiring_profile": {...},
  "num_questions": 4
}
```

### Get Analytics
```bash
GET http://localhost:8000/api/feedback/analytics
```

See full API docs at: http://localhost:8000/docs

---

## 🎓 Sample Resume for Testing

```
John Doe
Email: john@example.com
Phone: 555-1234

EXPERIENCE:
- Senior Python Developer at TechCorp (2020-Present)
  Developed backend services using Django and PostgreSQL
  Managed team of 5 engineers
- Python Developer at StartupXYZ (2018-2020)
  Built microservices with FastAPI and Docker

SKILLS:
- Python (Expert)
- JavaScript (Intermediate)
- PostgreSQL (Advanced)
- Docker (Advanced)
- AWS (Intermediate)
- Django (Expert)
- FastAPI (Expert)

TECHNOLOGIES:
Python, JavaScript, PostgreSQL, MongoDB, Docker, Kubernetes, AWS, GCP

INDUSTRIES:
FinTech (3 years), SaaS (2 years), E-commerce (1 year)

PROJECTS:
- Payment Processing System: Led team to build real-time payment system using Django + PostgreSQL
- Microservices Migration: Redesigned monolithic app to microservices with FastAPI + Docker

EDUCATION:
BS Computer Science, State University (2018)
```

---

## 💡 Tips for Best Results

1. **Detailed Job Descriptions**: The more detailed your team culture description, the better the AI matching
2. **Complete Resumes**: Include all sections (skills, experience, projects) for accurate parsing
3. **Multiple Candidates**: Test with 3-5 candidates to see ranking and matching
4. **Feedback Loop**: Use the feedback buttons to train the system - it learns!
5. **Monitor Analytics**: Check analytics to see if match quality improves over time

---

## 📚 Additional Resources

- Full README: `README.md`
- Backend Configuration: `.env.example`
- API Documentation: http://localhost:8000/docs (when backend is running)
- Google Gemini Docs: https://ai.google.dev/

---

## ✨ Features Implemented

### Resume Parser
- ✅ Extract candidate name, email, phone
- ✅ Identify technical skills with proficiency levels
- ✅ Calculate years of experience
- ✅ Extract tech stack
- ✅ Identify industry exposure
- ✅ Extract projects and responsibilities
- ✅ Generate embedding vectors

### Job Profile
- ✅ Structure hiring requirements
- ✅ Generate role summaries
- ✅ Create profile embeddings
- ✅ Support for job levels (Junior to Principal)
- ✅ Salary range and qualifications

### Screening
- ✅ Generate role-specific questions
- ✅ Support 3-5 questions
- ✅ Evaluate responses with AI
- ✅ Score on 3 dimensions (Technical, Communication, Problem-Solving)
- ✅ Provide detailed reasoning

### Matching
- ✅ Vector similarity matching
- ✅ Combine with screening scores (60/40 split)
- ✅ Generate explanations for matches
- ✅ Ranking of candidates
- ✅ Recommendation text

### Feedback Collection
- ✅ Record hiring decisions
- ✅ SQLite persistence
- ✅ Reinforcement learning with 4 patterns
- ✅ Dynamic weight adjustment
- ✅ Analytics and statistics
- ✅ Weight history tracking

---

## 🚀 Next Steps

1. **Run the Project** using the commands above
2. **Test All Features** following the workflow
3. **Experiment** with different job profiles and resumes
4. **Provide Feedback** - this trains the system!
5. **Monitor Analytics** to see model improving

---

## 🤝 Support

If you encounter any issues:
1. Check the Troubleshooting section above
2. Verify `.env` file has `GEMINI_API_KEY` set
3. Ensure both services started without errors
4. Check terminal output for specific error messages
5. Review backend logs for API errors

---

**TalentVector AI is ready to use! 🎉**

Start with: `.\startup.bat` (Windows) or `bash startup.sh` (Linux/Mac)
