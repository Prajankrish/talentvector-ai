# 📤 GitHub Deployment Guide

## How to Push TalentVector AI to GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com)
2. Click **"New repository"** button
3. Fill in details:
   - **Repository name**: `talentvector-ai`
   - **Description**: "AI-powered recruiting platform with resume parsing, job profiling, and semantic matching"
   - **Public/Private**: Choose based on your preference (public for hackathon exposure recommended)
   - **Add .gitignore**: Already added ✓
   - **Add README.md**: Already added ✓
   - **License**: MIT (optional)
4. Click **"Create repository"**

### Step 2: Copy Repository URL

The new repository page will show:
```
https://github.com/YOUR_USERNAME/talentvector-ai.git
```

**Copy this URL** - you'll need it in the next step.

### Step 3: Add Remote and Push

Run these commands in PowerShell (from talentvector directory):

```powershell
# Add GitHub as remote origin
cd "d:\Projects\AI Recruting\talentvector"

git remote add origin https://github.com/YOUR_USERNAME/talentvector-ai.git

# Push all commits to GitHub
git branch -M main
git push -u origin main
```

**Or if creating on main branch directly:**
```powershell
git remote add origin https://github.com/YOUR_USERNAME/talentvector-ai.git
git push -u origin master
```

### Step 4: Verify on GitHub

1. Go to your GitHub repository URL
2. You should see:
   - ✅ All files and folders
   - ✅ 6 commits in commit history
   - ✅ README.md displayed on main page
   - ✅ .env and .env.example files

### Step 5: Add GitHub URL to README

Update README.md with GitHub link:

```markdown
## 🚀 Getting Started

### View on GitHub
⭐ **[View on GitHub](https://github.com/YOUR_USERNAME/talentvector-ai)**

### Live Demo (Coming Soon)
- Frontend: [Deploy to Vercel](#deployment)
- Backend: [Deploy to Railway](#deployment)
```

### Step 6: Deploy Frontend (Optional - for Live Demo Link)

**Deploy to Vercel (Free & Easy)**:

```powershell
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy frontend
cd frontend
vercel --prod
```

You'll get a live URL like: `https://talentvector-ai.vercel.app`

### Step 7: Deploy Backend (Optional - for Live Demo Link)

**Option A: Deploy to Railway (Recommended - Free tier available)**

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize and deploy
cd backend
railway init
railway up
```

**Option B: Deploy to Heroku**

```powershell
# Install Heroku CLI
# (download from heroku.com)

heroku login
heroku create talentvector-ai-backend

# Set environment variables
heroku config:set GEMINI_API_KEY=your_key_here

# Deploy
git push heroku main
```

### Step 8: Update README with Deployment Links

```markdown
## 🚀 Live Demo

- **Frontend**: https://talentvector-ai.vercel.app
- **Backend API**: https://your-backend.railway.app
- **Swagger Docs**: https://your-backend.railway.app/docs
- **GitHub**: https://github.com/YOUR_USERNAME/talentvector-ai
```

---

## 🔐 Security Checklist Before Pushing

- ✅ `.env` is in `.gitignore` and not pushed
- ✅ No API keys in `.env.example`
- ✅ No hardcoded secrets in source code
- ✅ `.gitignore` includes: `.env`, `__pycache__/`, `node_modules/`, `.venv/`
- ✅ Database files excluded (`.db` files)

**Verify before push**:
```powershell
# Check what will be pushed
git status

# Should show: "nothing to commit, working tree clean"
```

---

## 📝 After Pushing to GitHub

### Essential Documentation
1. ✅ Update README with GitHub & deployment links
2. ✅ Create GitHub Releases for versions (if needed)
3. ✅ Enable GitHub Pages if desired
4. ✅ Add GitHub repository settings:
   - Set default branch to `main` (if not already)
   - Protection rules for production branches (optional)
   - Allow discussions for community (recommended)

### Optional GitHub Features
- Add GitHub Actions for CI/CD
- Enable branch protection
- Set up GitHub Packages for Docker images
- Create GitHub Project board for task tracking

---

## 🎯 Hackathon Submission

### Final Checklist
- [ ] Repository pushed to GitHub
- [ ] README.md complete with:
  - [ ] Problem statement
  - [ ] Architecture diagram
  - [ ] Setup instructions
  - [ ] Tech stack
  - [ ] Deployment link
  - [ ] AI safeguards documentation
- [ ] All 6 commits in history with meaningful messages
- [ ] `.env.example` has no real API keys
- [ ] `.gitignore` prevents secret commits
- [ ] Frontend and backend deployments live (or noted as "coming soon")
- [ ] HACKATHON_COMPLIANCE.md confirms all 13 best practices

### Submission Details Required
- **Repository URL**: `https://github.com/YOUR_USERNAME/talentvector-ai`
- **Live Demo URL**: (Frontend + Backend if deployed)
- **Documentation**: See README.md
- **Team**: List team members in README

---

## 🆘 Troubleshooting

### "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/talentvector-ai.git
```

### "Push rejected - need to pull first"
```powershell
# If GitHub repo had auto-created files (like README):
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### ".env file was accidentally pushed"
```powershell
# Remove from history (use BFG Repo-Cleaner or contact GitHub support)
# NEVER use this file again - rotate all API keys!
```

### "Cannot connect to Ollama during deployment"
- Ollama must be running locally OR
- Use Gemini API key in production (set in `.env`)
- Add `USE_OLLAMA=false` to production `.env`

---

## 💡 Tips for Success

1. **Star your own repo** to get community attention
2. **Share on social media** with link to GitHub
3. **Write a blog post** about the development process
4. **Add badges** to README (build status, MIT license, etc.)
5. **Engage with community** - respond to issues/discussions
6. **Keep improving** - continuous deployment on pushes

---

**You're all set! 🎉 TalentVector AI is production-ready and hackathon-compliant.**

Good luck with your submission! 🚀
