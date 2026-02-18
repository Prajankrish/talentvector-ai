# TalentVector AI - Complete Integration Guide

## 🎯 Quick Start (5 Minutes)

### Terminal 1: Start Frontend
```bash
cd d:\Projects\AI\ Recurting\talentvector\frontend
npm install
npm run dev
```
✅ Frontend running on: **http://localhost:5173**

### Terminal 2: Start Backend
```bash
cd d:\Projects\AI\ Recurting\talentvector
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```
✅ Backend running on: **http://localhost:8000**
📚 API Docs: **http://localhost:8000/docs**

### Terminal 3: Start Ollama (if not running)
```bash
ollama serve
# Or in another terminal:
ollama pull mistral
```
✅ Ollama running on: **http://localhost:11434**

---

## 📱 Using the Application

### 1. Authentication
```
URL: http://localhost:5173
- Create account or login
- Email: test@example.com
- Password: any password
- Company: My Company
```

### 2. Upload Resume
```
Go to: Resume Intelligence
- Upload PDF/DOCX/TXT file
- Or paste resume text
- Click "Extract Candidate Intelligence"
```

### 3. Create Job Profile
```
Go to: Job Intelligence
- Enter job title & description
- Add required skills
- Set years of experience
- Click "Generate Hiring Profile"
```

### 4. Analyze Match
```
Go to: Match Analysis
- View candidate & job profiles
- Click "Analyze Match"
- See match score & breakdown
```

### 5. Generate Screening
```
Go to: Screening
- Click "Generate Questions"
- Answer all questions
- Click "Evaluate Answers"
- See evaluation results
```

### 6. Submit Feedback
```
Go to: Feedback
- See candidate summary
- Click "Good Fit" or "Not Fit"
- Add optional notes
- System learns from feedback
```

---

## 🔄 Complete Workflow Example

### Scenario: Hiring Senior React Developer

```
STEP 1: Login
├─ Email: recruiter@techcorp.com
├─ Password: SecurePass123
└─ Company: TechCorp Inc.

STEP 2: Upload Resume (Resume Intelligence)
├─ Upload: john_doe_resume.pdf
├─ Extract: Name, Skills, Experience
└─ Result: John Doe (5 years React, 3 years Node.js)

STEP 3: Create Job Profile (Job Intelligence)
├─ Title: Senior React Engineer
├─ Description: Build scalable web applications...
├─ Skills: React, TypeScript, Node.js, GraphQL
├─ Experience: 5+ years
└─ Result: Hiring profile with ideal candidate description

STEP 4: Match Analysis (Match Analysis)
├─ Candidate: John Doe
├─ Job: Senior React Engineer
├─ Algorithm: Semantic matching + skill analysis
└─ Result: 82% match (STRONG_FIT)
    ├─ Skills match: 95%
    ├─ Experience: 100%
    ├─ Growth potential: 75%
    └─ Culture fit: TBD

STEP 5: Screen Candidate (Screening)
├─ Generate: 4 role-specific questions
├─ Questions:
│  1. Describe your approach to state management
│  2. How do you optimize React performance?
│  3. Tell us about your GraphQL experience
│  4. What's your debugging process?
├─ Candidate answers all questions
└─ AI Evaluation:
    ├─ Q1: Excellent (95%)
    ├─ Q2: Good (85%)
    ├─ Q3: Good (80%)
    └─ Q4: Excellent (90%)
    └─ Overall: 87.5% (STRONG_CANDIDATE)

STEP 6: Feedback (Feedback)
├─ Review: John Doe, 82% match, 87.5% screening
├─ Decision: "Good Fit"
├─ Notes: "Excellent technical depth, great communicator"
└─ System learns: Update ML models with feedback
```

---

## 🛠️ API Endpoints Reference

### Resume Parsing
```
POST /parse-resume
Request:
  { "resume_text": "John Doe, Senior Engineer..." }
Response:
  {
    "candidate_profile": {
      "name": "John Doe",
      "email": "john@example.com",
      "skills": ["React", "Node.js", ...],
      "years_of_experience": 5,
      "work_experience": [...]
    }
  }
```

### Hiring Profile Generation
```
POST /generate-hiring-profile
Request:
  {
    "job_description": "Looking for a Senior React...",
    "required_skills": ["React", "TypeScript"],
    "years_of_experience": 5
  }
Response:
  {
    "hiring_profile": {
      "position": "Senior React Engineer",
      "required_skills": [...],
      "ideal_candidate_profile": "Motivated engineer with...",
      "screening_questions": [...]
    }
  }
```

### Candidate-Job Matching
```
POST /match-candidate
Request:
  {
    "candidate_profile": {...},
    "hiring_profile": {...}
  }
Response:
  {
    "overall_score": 82,
    "skills_match": 95,
    "experience_match": 100,
    "cultural_fit": 75,
    "recommendation": "STRONG_FIT",
    "breakdown": {...}
  }
```

### Screening Questions
```
POST /generate-screening
Request:
  {
    "hiring_profile": {...},
    "num_questions": 4
  }
Response:
  {
    "questions": [
      "Describe your approach to...",
      "How do you handle...",
      ...
    ]
  }
```

### Feedback Submission
```
POST /submit-feedback
Request:
  {
    "candidate_id": "john_doe",
    "final_score": 82,
    "feedback": "Good Fit",
    "notes": "Excellent technical skills"
  }
Response:
  {
    "success": true,
    "message": "Feedback recorded"
  }
```

---

## 🔍 Troubleshooting

### Issue: Frontend won't start
```
Error: VITE CLI not found

Solution:
npm install          # Reinstall dependencies
npm run dev         # Use npx explicitly in package.json
```

### Issue: PDF upload fails
```
Error: Failed to extract text from PDF

Solution:
- Check file is valid PDF
- Try text/paste option instead
- Check browser console for details
```

### Issue: Backend returns 500 error
```
Error: Internal Server Error

Solution:
- Check if Ollama is running: ollama serve
- Check backend logs
- Verify .env configuration
```

### Issue: Connection refused (localhost:8000)
```
Error: Cannot connect to backend

Solution:
- Start backend: python -m uvicorn backend.main:app --reload
- Check port 8000 is not in use
- Check firewall settings
```

### Issue: Ollama model not found
```
Error: Model 'mistral' not found

Solution:
ollama pull mistral
```

---

## 📊 Performance Tips

### For Development
- Keep dev tools closed to reduce memory usage
- Use Firefox or Chrome (not Edge for now)
- Disable extensions for better performance

### For Production
- Use `.env` to configure API_URL
- Set `NODE_ENV=production`
- Enable gzip compression
- Use CDN for static assets
- Cache API responses

### For Large Files
- Max resume file: 10MB (adjust in backend)
- Batch processing available (TODO)
- Incremental parse mode (TODO)

---

## 🧪 Testing Scenarios

### Test 1: Happy Path
```
1. Login ✓
2. Upload resume ✓
3. Create job profile ✓
4. Match candidates ✓
5. Screen questions ✓
6. Submit feedback ✓
```

### Test 2: Error Handling
```
1. Upload invalid file → Error message
2. Missing job profile → Cannot match error
3. Backend offline → Graceful degradation
4. Invalid auth → Redirect to login
```

### Test 3: Performance
```
1. Large resume (5MB) → Parse time < 10s
2. Rapid clicking → Debounced, no errors
3. Multiple tabs → State syncs correctly
4. Network slow (3G) → Loading states visible
```

---

## 🚀 Production Deployment

### Docker Setup
```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ENV VITE_API_BASE_URL=https://api.example.com
RUN npm run build
```

### Environment Variables
```
.env
VITE_API_BASE_URL=http://localhost:8000
VITE_LOG_LEVEL=debug
```

### Backend Configuration
```
.env
OLLAMA_URL=http://localhost:11434
DATABASE_URL=postgresql://user:pass@localhost/talentvector
LOG_LEVEL=info
```

---

## 📞 Support & Debugging

### Check Frontend Status
```bash
# Check if running
curl http://localhost:5173

# Check API connectivity
curl http://localhost:5173/api/health
# This internally calls http://localhost:8000/health
```

### Check Backend Status
```bash
# API is running
curl http://localhost:8000/health

# View API docs
curl http://localhost:8000/docs

# Check Ollama
curl http://localhost:11434
```

### View Logs
```
Frontend: Browser DevTools (F12)
Backend: Terminal where uvicorn is running
Ollama: Terminal where ollama serve is running
```

---

## ✅ Verification Checklist

Before going live, verify:

- [ ] Frontend loads without errors
- [ ] API docs accessible at /docs
- [ ] Resume upload works
- [ ] Candidate profile extracts correctly
- [ ] Job profile generates
- [ ] Match score calculates
- [ ] Screening questions generate
- [ ] Feedback saves
- [ ] No 404 errors in console
- [ ] Loading states work
- [ ] Error alerts display correctly
- [ ] Navigation between pages works
- [ ] Logout clears session

---

## 🎉 You're Ready!

Your TalentVector AI platform is now fully operational.

Start recruiting smarter! 🚀
