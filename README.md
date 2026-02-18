# 🚀 TalentVector AI

## Professional AI-Powered Recruiting Platform

Transform talent acquisition with AI-driven resume parsing, intelligent job profiling, semantic candidate-job matching, and adaptive screening.

---

## 📋 Problem Statement

**Challenge**: Traditional recruiting processes are time-consuming and inefficient. Companies struggle to:
- Parse and structure resume data from multiple formats
- Quickly identify top candidates from large applicant pools  
- Create comprehensive job profiles and screening questions
- Match candidates to roles based on skills and cultural fit
- Handle rejection bias in evaluation

**Solution**: TalentVector AI provides an intelligent, unbiased recruiting platform that automates resume parsing, job profiling, and candidate-job matching using advanced AI and semantic similarity algorithms. All processing is done locally or via secure APIs, ensuring data privacy and responsible AI usage.

---

## ✨ Key Features

### 🔐 **Hiring Manager Authentication**
- Professional login/signup system
- Company context tracking
- Session management
- Secure access control

### 📄 **Resume Intelligence**
- PDF/DOCX/TXT file upload
- Automatic text extraction (pdfjs-dist)
- AI-powered candidate profile extraction
- Structured data: name, email, skills, experience

### 💼 **Job Intelligence**
- Job description analysis
- Hiring profile auto-generation
- Ideal candidate description
- Screening question suggestions

### 🎯 **Smart Matching**
- Semantic similarity scoring
- Skill compatibility analysis
- Experience level alignment
- Cultural fit assessment
- Recommendation system

### ❓ **AI Screening**
- Role-specific question generation
- Candidate answer evaluation
- Response quality scoring
- Interview insights

### 📈 **Feedback Learning**
- Decision recording (Fit/Not Fit)
- Model improvement
- Feedback tracking
- Decision history

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│        React Frontend (Vite)            │
│   5173 | Zustand | Tailwind CSS         │
└─────────────────┬───────────────────────┘
                  │ REST API
                  ▼
┌─────────────────────────────────────────┐
│     FastAPI Backend (Python)            │
│   8000 | 6 Endpoints | CORS Enabled     │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│    Ollama (Local LLM Service)           │
│   11434 | Mistral 7B | Embeddings       │
└─────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js** 16+ with npm 8+
- **Python** 3.8+
- **Ollama** (download from https://ollama.ai)
- **2GB+ Disk Space** (for Mistral model)

### One-Command Startup (Windows)
```bash
START_ALL.bat
```

### One-Command Startup (Mac/Linux)
```bash
chmod +x start_all.sh
./start_all.sh
```

### Manual Startup (3 Terminals)

**Terminal 1: Ollama** (if not running)
```bash
ollama serve
# In another terminal:
ollama pull mistral
```

**Terminal 2: Backend**
```bash
cd talentvector
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

**Terminal 3: Frontend**
```bash
cd talentvector/frontend
npm install
npm run dev
```

### Access
```
Frontend: http://localhost:5173
Backend:  http://localhost:8000/docs
```

---

## 📋 Complete User Workflow

### 1. **Login/Signup**
```
Visit: http://localhost:5173
Email: your@email.com
Password: anypassword
Company: Your Company
```

### 2. **Upload Resume**
```
Page: Resume Intelligence
Action: Upload PDF/DOCX/TXT
Result: Candidate profile extracted
```

### 3. **Create Job Profile**
```
Page: Job Intelligence
Action: Enter job title & description
Result: Hiring profile generated
```

### 4. **Analyze Match**
```
Page: Match Analysis
Action: View match score
Result: 0-100% semantic match + recommendation
```

### 5. **Generate Screening**
```
Page: Screening
Action: Generate questions + answer them
Result: AI evaluation score
```

### 6. **Submit Feedback**
```
Page: Feedback
Action: Mark Good Fit or Not Fit
Result: System learns from decision
```

---

## 📊 Project Structure

```
talentvector/
├── frontend/                    # React + Vite
│   ├── src/
│   │   ├── pages/             # 7 professional pages
│   │   ├── components/        # 5 reusable components
│   │   ├── store/             # Zustand state management
│   │   ├── services/          # API service layer
│   │   ├── utils/             # PDF parser utility
│   │   ├── App.jsx            # Auth gate + routing
│   │   └── main.jsx           # Entry point
│   └── package.json
│
├── backend/                     # FastAPI
│   ├── main.py                # API endpoints
│   ├── resume_parser.py       # Resume analysis
│   ├── screening.py           # Question generation
│   ├── matching.py            # Semantic matching
│   ├── feedback.py            # Learning system
│   └── requirements.txt
│
├── docs/                        # Documentation
│   ├── COMPLETE_INTEGRATION_GUIDE.md
│   ├── PRODUCTION_STATUS.md
│   ├── PROJECT_OVERVIEW.md
│   └── README.md
│
├── START_ALL.bat              # Windows startup script
├── start_all.sh               # Mac/Linux startup script
└── README.md                  # This file
```

---

## 🧪 Testing

### Test the System
```
1. ✓ Login with: test@example.com / test123
2. ✓ Upload sample resume
3. ✓ Create job profile
4. ✓ Analyze match
5. ✓ Generate questions
6. ✓ Submit feedback
```

### Check Status
```bash
# Frontend
curl http://localhost:5173

# Backend
curl http://localhost:8000/health

# Ollama
curl http://localhost:11434
```

---

## 🐛 Troubleshooting

### Issue: Port in use
```bash
# Mac/Linux
lsof -i :5173 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Windows PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process
```

### Issue: Module not found
```bash
cd talentvector/frontend
npm install
npm install pdfjs-dist
```

### Issue: Backend won't connect
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check if Ollama is running
curl http://localhost:11434
```

---

## ⚙️ Technology Stack

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 18.2.0 | UI framework |
| Vite | 5.0.0 | Build tool |
| Tailwind CSS | 3.3.0 | Styling |
| Zustand | 4.4.0 | State management |
| Axios | 1.6.0 | HTTP client |
| pdfjs-dist | 4.0.0 | PDF parsing |

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.104.1 | API framework |
| Python | 3.8+ | Language |
| Pydantic | 2.5.0 | Data validation |
| Uvicorn | 0.24.0 | ASGI server |
| Ollama | Latest | LLM service |

---

## 📚 Documentation

- [**Complete Integration Guide**](./COMPLETE_INTEGRATION_GUIDE.md) - Detailed integration steps
- [**Production Status**](./PRODUCTION_STATUS.md) - Feature checklist
- [**Project Overview**](./PROJECT_OVERVIEW.md) - Architecture overview

---

## 🚀 Deployment

### Production Checklist
- [ ] Test end-to-end workflow
- [ ] Verify all API endpoints
- [ ] Load test with multiple users
- [ ] Set up monitoring
- [ ] Configure database
- [ ] Deploy to cloud (AWS/Azure/GCP)
- [ ] Set up SSL certificates
- [ ] Configure CI/CD pipeline

### Docker
```bash
docker build -t talentvector-ai .
docker run -p 5173:5173 -p 8000:8000 talentvector-ai
```

---

## 🎉 Ready to Transform Your Recruiting?

Start using TalentVector AI today!

```bash
# Windows
START_ALL.bat

# Mac/Linux
./start_all.sh
```

Then visit: **http://localhost:5173**

---

**Status**: 🚀 Production MVP Ready | **Version**: 1.0.0

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy `.env.example` to `.env` and fill in your configuration:
```bash
cp .env.example .env
```

Edit `.env` with your values:
```env
# Required - Get from https://ai.google.dev/
GEMINI_API_KEY=your_google_gemini_api_key_here

# Google Gemini Configuration (optional - defaults provided)
GEMINI_MODEL=gemini-1.5-pro
EMBEDDING_MODEL=models/embedding-001

# API Configuration (optional)
API_HOST=0.0.0.0
API_PORT=8000

# Database Configuration (optional)
DATABASE_PATH=./data/talentvector.db
FEEDBACK_DB_PATH=./data/feedback.db

# Application Settings (optional)
LOG_LEVEL=INFO
MAX_RETRIES=3
REQUEST_TIMEOUT=30
```

**⚠️ Important**: Never commit your `.env` file to version control. It contains sensitive API keys.

## Running the Application

### Start the Streamlit Frontend
```bash
streamlit run app.py
```
The frontend will open at `http://localhost:8501`

### Start the FastAPI Backend (Optional)
```bash
python backend/main.py
```
The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## Module Descriptions

### Resume Parser (`resume_parser.py`)
Extracts structured candidate information from resume text using Google Gemini's language models.

**Key Classes**:
- `ResumeParser`: Parses resumes and creates candidate profiles with embeddings
- `CandidateProfile`: Pydantic model for structured candidate data

**Extracted Information**:
- Skills with proficiency levels
- Years of experience
- Technical stack
- Industry exposure
- Key projects and achievements
- Work experience details
- Education
- Professional summary

### Screening (`screening.py`)
Generates role-specific screening questions and evaluates candidate answers.

**Key Classes**:
- `CandidateScreener`: Generates questions and scores responses
- `ScreeningQuestion`: Represents a screening question
- `ScreeningScore`: Contains evaluation scores

**Scoring Dimensions**:
- Technical Depth (0-10)
- Communication Clarity (0-10)
- Problem-Solving Ability (0-10)

### Matching (`matching.py`)
Computes candidate-to-role fit using embeddings and screening scores.

**Key Classes**:
- `CandidateJobMatcher`: Matches candidates with hiring profiles
- `MatchResult`: Contains match analysis results

**Matching Formula**:
```
final_score = (0.6 × similarity_score × 10) + (0.4 × screening_score)
```

### Feedback (`feedback.py`)
Collects hiring decisions and dynamically adjusts matching weights.

**Key Classes**:
- `FeedbackCollector`: Records feedback and manages weight adjustments
- `FeedbackEntry`: Represents hiring feedback
- `WeightParameters`: Contains current matching weights

**Reinforcement Learning**:
- Detects patterns in hiring outcomes
- Adjusts weights based on accuracy
- Tracks confidence levels
- Maintains weight history

### Hiring Manager (`hiring_manager.py`)
Creates and structures hiring profiles with AI enhancement.

**Key Classes**:
- `HiringManager`: Processes hiring inputs and generates profiles
- `HiringManagerProfile`: Structured hiring profile

**Features**:
- Structured profile generation from raw input
- Job description summary generation
- Embedding creation for profile similarity

### Utilities (`utils.py`)
Shared utilities, configuration management, and error handling.

**Features**:
- Environment configuration management
- Custom exceptions
- Logging setup
- Decorators for error handling and retries
- JSON parsing utilities
- Directory and score validation

## API Endpoints

### Health Check
```
GET /
GET /health
```

### Resume Management
```
POST /parse-resume
- Upload and parse resume files

POST /screen-candidate
- Screen a candidate for a job

POST /match-candidates
- Find matching candidates for a job position
```

## Data Models

### Candidate Profile
```python
{
    "name": str,
    "email": str,
    "phone": str (optional),
    "skills": [{"skill": str, "proficiency": str}],
    "years_of_experience": int,
    "tech_stack": [str],
    "industry_exposure": [str],
    "key_projects": [{"name": str, "description": str, "tech": str}],
    "work_experience": [{"company": str, "position": str, "duration": str}],
    "education": [{"institution": str, "degree": str, "field": str}],
    "summary": str
}
```

### Hiring Profile
```python
{
    "role_title": str,
    "required_skills": [str],
    "nice_to_have_skills": [str],
    "years_of_experience": int,
    "industry": str,
    "team_culture": str,
    "key_responsibilities": [str],
    "ideal_candidate_profile": str,
    "success_metrics": [str]
}
```

### Match Result
```python
{
    "similarity_score": float,    # 0-1 (cosine similarity)
    "screening_score": float,     # 0-10 (interview performance)
    "final_score": float,         # 0-10 (weighted combination)
    "explanation": str,           # AI-generated explanation
    "recommendation": str         # Hiring recommendation
}
```

## Error Handling

The system includes comprehensive error handling:

- **ConfigurationError**: Missing or invalid environment configuration
- **ResumeParsingError**: Resume parsing failures
- **ScreeningError**: Screening evaluation failures
- **MatchingError**: Matching computation failures
- **DatabaseError**: Database operation failures
- **APIError**: Google Gemini API call failures

All errors are logged with context for debugging.

## Logging

The application uses Python's standard logging with configuration from `.env`:

```python
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

Logs include:
- Module initialization
- API calls and retries
- Database operations
- Weight adjustments
- Error details with context

## Features

✅ Multi-format resume parsing (PDF, DOCX, TXT, MD)
✅ AI-powered skill and experience extraction
✅ Intelligent candidate screening
✅ Vector-based job matching
✅ Performance metrics and feedback loop
✅ SQLite data persistence
✅ REST API with full documentation
✅ Interactive web dashboard
✅ Dynamic weight adjustment via reinforcement learning
✅ Comprehensive error handling and logging
✅ Environment-based configuration
✅ Modular, reusable code architecture

## Configuration

### Environment Variables

**Critical** (must be set):
- `GEMINI_API_KEY`: Your Google Gemini API key from https://ai.google.dev/

**Optional** (defaults provided):
- `GEMINI_MODEL`: Gemini model to use (default: gemini-1.5-pro)
- `EMBEDDING_MODEL`: Embedding model (default: models/embedding-001)
- `API_HOST`: API server host (default: 0.0.0.0)
- `API_PORT`: API server port (default: 8000)
- `DATABASE_PATH`: SQLite database path (default: ./data/talentvector.db)
- `FEEDBACK_DB_PATH`: Feedback database path (default: ./data/feedback.db)
- `LOG_LEVEL`: Logging level (default: INFO)
- `MAX_RETRIES`: Max API retries (default: 3)
- `REQUEST_TIMEOUT`: API timeout in seconds (default: 30)

### Database

SQLite databases are automatically created on first initialization:
- **talentvector.db**: Candidates, jobs, screening results
- **feedback.db**: Hiring feedback and weight history

---

## 🤖 Responsible AI & Safeguards

### AI Hallucination Prevention
- **Output Validation**: All LLM responses are validated against structured prompts
- **JSON Parsing**: 7-step fallback JSON extraction ensures data integrity
- **Prompt Engineering**: Explicit instructions to "Return ONLY valid JSON with NO additional text"
- **Error Bounds**: Responses are bounded to expected field counts and types

### Prompt Injection Protection
- **Input Sanitization**: All user inputs are trimmed and validated
- **Structured Prompts**: System instructions define the exact output format
- **No Raw User Data in Prompts**: User text is processed through extraction pipelines
- **Type Checking**: Validates data types before LLM processing

### Bias & Fairness Measures
- **Skill-Based Matching**: Semantic similarity focuses on skills, not demographic data
- **Experience Weighting**: Transparent scoring that weights technical depth over years
- **Neutral Screening Questions**: AI generates role-specific, not bias-prone questions
- **Decision Logging**: All hiring decisions are tracked for audit trails

### Data Privacy
- **Local LLM Option**: Supports Ollama for completely local, on-premises processing (no cloud required)
- **No Data Retention**: LLM responses are not stored or used for training
- **Environment-Based Secrets**: All API keys loaded from `.env` (never hardcoded)
- **Database Security**: SQLite feedback DB is local-only by default

---

## ⚠️ Error Handling & Resilience

### Timeout Management
- **Frontend**: 600-second (10 min) timeout for LLM responses
- **Backend**: 900-second (15 min) timeout for Ollama inference
- **Graceful Degradation**: Meaningful error messages instead of blank responses

### Failure Scenarios Handled
| Scenario | Handling |
|----------|----------|
| PDF parsing fails | Shows user-friendly error, logs details |
| LLM timeout | Returns extended timeout, logs Ollama status |
| Invalid resume format | Validates file type, guides user to supported formats |
| Missing API key | Startup validation block prevents runtime crash |
| Database locked | Retry logic with exponential backoff |
| Network failure | Connection retry with detailed error messages |
| Malformed JSON | 7-step fallback extraction, graceful parsing |

### Logging & Debugging
```python
# All major operations log with context
logger.info(f"📄 Resume extracted: {filename}")
logger.error(f"❌ PDF parsing failed: {error_detail}")

# Enable detailed logging with:
# LOG_LEVEL=DEBUG python main.py
```

---

## 🧪 Testing & Validation

### Functional Testing
- Manual testing scripts: `test_matching_fix.py`, `test_resume_improvements.py`
- Resume extraction validation with PDF/DOCX/TXT formats
- Job profile generation with various test inputs
- Matching algorithm verification with known test cases

### AI Output Validation
- **Structured Tests**: Verify JSON responses match expected schema
- **Bounds Testing**: Check skill counts, experience ranges, text lengths
- **Semantic Tests**: Validate matching scores fall in [0,1] range

### Running Tests
```bash
# Backend tests
cd backend
python test_matching_fix.py
python test_resume_improvements.py

# Manual endpoint testing
curl -X POST http://localhost:8000/api/parse-resume \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "..."}'
```

---

## 👥 Team Contribution & Git Workflow

### Git Strategy
```bash
# Clone repository
git clone <repo-url>
cd talentvector

# Create feature branch
git checkout -b feat/feature-name

# Make incremental, meaningful commits
git commit -m "feat: description of change"

# Push and create pull request
git push origin feat/feature-name
```

### Commit Message Format
- `feat:` - New features
- `fix:` - Bug fixes  
- `refactor:` - Code restructuring
- `docs:` - Documentation updates
- `style:` - Code style changes
- `test:` - Test additions
- `chore:` - Dependency updates, build config

**Example Commit**:
```
feat: add PDF timeout error handling

- Increase frontend timeout to 600s
- Increase backend timeout to 900s  
- Add graceful LLM fallback for slow models
- Log timeout details for debugging
```

### Code Quality Standards
- Follow PEP 8 (Python) and ESLint (JavaScript)
- Document complex logic with comments
- Add type hints where applicable
- Test changes before pushing
- Update README for new features

## Security Notes

1. **Never commit `.env` file** - It contains sensitive API keys
2. **API Keys**: Manage API keys securely using environment variables
3. **Database**: Feedback database contains hiring-related data, keep it secure
4. **Logs**: May contain sensitive information, restrict log access

## Future Enhancements

- [ ] Multi-format resume support (PDF parsing with OCR)
- [ ] Real-time vector index updates
- [ ] Advanced filtering and search UI
- [ ] Interview scheduling integration
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Bias detection and fairness metrics
- [ ] Custom ML model training
- [ ] Multi-language support
- [ ] Integration with ATS/recruiting platforms

## Troubleshooting

### "GEMINI_API_KEY not set in environment"
**Solution**: Copy `.env.example` to `.env` and add your Gemini API key

### "Failed to parse JSON"
**Solution**: Check Gemini API connectivity and response format

### "Database locked"
**Solution**: Ensure only one instance is running, close other connections

### "Import errors for backend modules"
**Solution**: Ensure backend directory is in Python path (already configured in app.py)

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review error logs (check console for LOG_LEVEL=DEBUG output)
3. Open an issue on the project repository
4. Contact the development team

---

**Built with ❤️ for modern recruiting**
**TalentVector AI - Powered by Google Gemini**
