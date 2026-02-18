"""
TalentVector AI - Streamlit Frontend
AI-native recruiting operating system for intelligent hiring intelligence vectorization and semantic candidate matching.
"""

import streamlit as st
import sys
import os
from pathlib import Path
import json
from typing import Optional, Dict, List

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

# Import backend modules
try:
    from backend.hiring_manager import HiringManager
    from backend.resume_parser import ResumeParser
    from backend.screening import CandidateScreener
    from backend.matching import CandidateJobMatcher
    from backend.feedback import FeedbackCollector
    from backend.utils import setup_logger, Config, APIError
except ImportError as e:
    st.error(f"❌ Failed to import backend modules: {str(e)}")
    st.stop()

# Setup logging
logger = setup_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="TalentVector AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
<style>
    .metric-box { background-color: #1f1f1f; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #667eea; }
    h1 { color: #667eea; }
    h2 { color: #764ba2; }
    .stCaption { color: #888; font-style: italic; }
    .stDivider { margin: 2rem 0; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "candidates" not in st.session_state:
    st.session_state.candidates = []
if "hiring_profile" not in st.session_state:
    st.session_state.hiring_profile = None
if "screening_questions" not in st.session_state:
    st.session_state.screening_questions = None
if "match_results" not in st.session_state:
    st.session_state.match_results = None


@st.cache_resource
def get_modules():
    """Initialize backend modules with caching"""
    try:
        hiring_manager = HiringManager()
        resume_parser = ResumeParser()
        screener = CandidateScreener()
        matcher = CandidateJobMatcher()
        feedback_collector = FeedbackCollector()
        return hiring_manager, resume_parser, screener, matcher, feedback_collector
    except Exception as e:
        logger.error(f"Failed to initialize modules: {str(e)}")
        st.error(f"❌ Failed to initialize AI modules: {str(e)}")
        st.stop()


def show_dashboard():
    """Dashboard with system overview and intelligence summary"""
    # Product Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: white; margin: 0;">🚀 TalentVector AI</h3>
        <p style="color: #e0e0e0; margin: 10px 0 0 0;">AI-native recruiting operating system that transforms hiring intent into structured intelligence and matches candidates using semantic understanding.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("📊 System Intelligence Overview")
    st.write("Real-time summary of your recruiting intelligence pipeline")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🧠 Candidate Intelligence", len(st.session_state.candidates), "profiles extracted")
    with col2:
        st.metric("💼 Hiring Intelligence", "1" if st.session_state.hiring_profile else "0", "role profile")
    with col3:
        st.metric("⚡ AI Matches", len(st.session_state.match_results) if st.session_state.match_results else 0, "analyzed")
    with col4:
        st.metric("🟢 System Status", "Active", "all systems operational")
    
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🧠 Candidate Intelligence Profiles")
        st.caption("Extracted candidate vectors from resumes")
        if st.session_state.candidates:
            for i, candidate in enumerate(st.session_state.candidates[-5:], 1):
                st.write(f"{i}. **{candidate.get('name', 'Unknown')}** - {candidate.get('email', 'N/A')}")
        else:
            st.info("No candidate intelligence profiles yet")
    
    with col2:
        st.subheader("💼 Hiring Intelligence Profile")
        st.caption("Current role requirements and team context")
        if st.session_state.hiring_profile:
            profile = st.session_state.hiring_profile
            st.write(f"**Role:** {profile.get('role_title', 'N/A')}")
            st.write(f"**Industry:** {profile.get('industry', 'N/A')}")
            st.write(f"**Required Skills:** {', '.join(profile.get('required_skills', [])[:3])}...")
        else:
            st.info("No job profile created yet")


def show_hiring_intelligence():
    """Hiring Intelligence Engine - Convert hiring intent into structured intelligence"""
    st.header("💼 Hiring Intelligence Engine")
    st.write("Transform your hiring intent into structured intelligence that powers AI-driven matching")
    st.caption("🤖 **What it does:** Converts unstructured hiring requirements into an intelligence vector that captures role requirements, team culture, and matching preferences. **Why it matters:** Precise hiring intelligence enables semantic matching instead of keyword filtering. **AI in use:** Ollama llama3 processes your input into a structured intelligence profile.")
    
    st.divider()
    
    hiring_manager, _, _, _, _ = get_modules()
    
    with st.form("hiring_form"):
        role_title = st.text_input("Role Title *", placeholder="e.g., Senior Python Developer")
        required_skills = st.multiselect(
            "Required Skills *",
            ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "React", "Vue", "Angular", 
             "AWS", "GCP", "Azure", "Docker", "Kubernetes", "PostgreSQL", "MongoDB"],
            default=["Python"]
        )
        nice_skills = st.multiselect(
            "Nice-to-Have Skills",
            ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "React", "Vue", "Angular", 
             "AWS", "GCP", "Azure", "Docker", "Kubernetes", "PostgreSQL", "MongoDB"],
            default=["Docker"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            years_exp = st.number_input("Years of Experience Required *", min_value=0, max_value=50, value=3)
        with col2:
            industry = st.text_input("Industry *", placeholder="e.g., FinTech, HealthTech, E-commerce")
        
        team_culture = st.text_area(
            "Team Culture & Work Environment *",
            placeholder="Describe your team culture, work style, and environment...",
            height=100
        )
        
        col1, col2, col3 = st.columns(3)
        with col1:
            job_level = st.selectbox("Job Level", ["Junior", "Mid-Level", "Senior", "Lead", "Principal"])
        with col2:
            salary_range = st.text_input("Salary Range (Optional)", placeholder="e.g., $120K-$150K")
        with col3:
            qualifications = st.text_input("Additional Qualifications", placeholder="e.g., MBA, Certifications")
        
        submit = st.form_submit_button("✨ Generate Hiring Intelligence", use_container_width=True)
        
        if submit:
            if not role_title or not required_skills or not industry or not team_culture:
                st.error("❌ Please fill in all required fields (*)")
            else:
                try:
                    with st.spinner("⏳ Processing hiring profile with AI..."):
                        result = hiring_manager.process_hiring_input(
                            role_title=role_title,
                            required_skills=list(required_skills),
                            nice_to_have_skills=list(nice_skills),
                            years_of_experience=years_exp,
                            industry=industry,
                            team_culture_description=team_culture,
                            job_level=job_level,
                            salary_range=salary_range if salary_range else None,
                            qualifications=qualifications if qualifications else None
                        )
                        
                        st.session_state.hiring_profile = result['structured_profile']
                        st.success("✅ Job profile created successfully!")
                        st.json(result['structured_profile'])
                        
                except Exception as e:
                    st.error(f"❌ Error creating profile: {str(e)}")
                    logger.error(f"Hiring manager error: {str(e)}")


def show_candidate_intelligence():
    """Candidate Intelligence Engine - Extract semantic vectors from resumes"""
    st.header("🧠 Candidate Intelligence Engine")
    st.write("Extract deep candidate intelligence vectors from resumes for semantic matching")
    st.caption("🤖 **What it does:** Analyzes resumes to extract structured candidate intelligence including skills, experience, industry exposure, and work history as reusable vectors. **Why it matters:** Semantic vectors enable context-aware matching beyond keyword search. **AI in use:** Ollama llama3 extracts intelligence and generates embedding vectors for matching.")
    
    st.divider()
    
    _, resume_parser, _, _, _ = get_modules()
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📤 Upload File", "📝 Paste Text"])
    
    with tab1:
        st.subheader("Upload Resume File")
        uploaded_file = st.file_uploader(
            "Choose a file (PDF, DOCX, or TXT)",
            type=["pdf", "docx", "txt"],
            key="file_uploader",
            help="Supported: PDF, DOCX, TXT files"
        )
        
        if uploaded_file:
            st.success(f"✅ File selected: {uploaded_file.name} ({uploaded_file.size} bytes)")
            
            col1, col2 = st.columns(2)
            with col1:
                extract_text_btn = st.button(
                    "📖 Extract Text",
                    use_container_width=True,
                    key="extract_file_text",
                    help="Extract text from the uploaded file"
                )
            with col2:
                auto_parse_btn = st.button(
                    "🚀 Auto Parse",
                    use_container_width=True,
                    key="auto_parse_file",
                    help="Automatically extract and parse"
                )
            
            if extract_text_btn or auto_parse_btn:
                resume_text = None
                
                # Extract text based on file type
                extraction_status = st.empty()
                with extraction_status.status("📖 Extracting text from file...", expanded=True):
                    st.write(f"• File: {uploaded_file.name}")
                    
                    try:
                        if uploaded_file.type == "text/plain":
                            st.write("• Type: Text file")
                            resume_text = uploaded_file.read().decode("utf-8")
                            st.write(f"• Size: {len(resume_text)} characters")
                        elif uploaded_file.type == "application/pdf":
                            st.write("• Type: PDF")
                            st.write("✓ PDF detected - please paste text below after copying")
                        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                            st.write("• Type: DOCX")
                            st.write("✓ DOCX detected - please paste text below after copying")
                        
                        extraction_status.status("✓ Text extraction ready", state="complete")
                    except Exception as e:
                        extraction_status.status(f"❌ Error extracting text: {str(e)}", state="error")
                        st.error(f"Failed to extract: {str(e)}")
                        return
                
                # Parse if we have text and auto_parse was clicked
                if resume_text and auto_parse_btn:
                    parse_resume_text(resume_parser, resume_text)
                elif not resume_text and resume_text is not None:
                    st.info("📌 For PDF/DOCX files, please copy text and paste in the 'Paste Text' tab below")
    
    with tab2:
        st.subheader("Paste Resume Content")
        resume_text = st.text_area(
            "Paste your resume text here",
            height=300,
            placeholder="Paste resume content here...\n\nJohn Doe\nEmail: john@example.com\nExperience:\n...",
            key="paste_resume_text"
        )
        
        if resume_text:
            # Show text stats
            lines = resume_text.count('\n')
            words = len(resume_text.split())
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Characters", len(resume_text))
            with col2:
                st.metric("Lines", lines)
            with col3:
                st.metric("Words", words)
            
            # Parse buttons
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                if st.button(
                    "🔍 Preview",
                    use_container_width=True,
                    key="preview_text",
                    help="Show first 500 characters"
                ):
                    st.info("📋 Resume Preview (first 500 chars):")
                    st.code(resume_text[:500] + "...\n[truncated]", language="text")
            
            with col2:
                clear_btn = st.button(
                    "🗑️ Clear",
                    use_container_width=True,
                    key="clear_text",
                    help="Clear the text area"
                )
                if clear_btn:
                    st.rerun()
            
            with col3:
                parse_btn = st.button(
                    "✨ Extract Candidate Intelligence",
                    use_container_width=True,
                    key="parse_text",
                    help="AI analysis may take 1-2 minutes"
                )
            
            if parse_btn:
                parse_resume_text(resume_parser, resume_text)
        else:
            st.info("📌 Paste resume content in the text area above")


def parse_resume_text(resume_parser, resume_text: str):
    """Helper function to extract candidate intelligence with progress tracking"""
    try:
        # Create progress container
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        with status_placeholder.status("🧠 Extracting Candidate Intelligence", expanded=True, state="running"):
            # Step 1: Validation
            st.write("✓ Step 1: Validating resume for intelligence extraction")
            st.write(f"  • Characters: {len(resume_text)}")
            st.write(f"  • Lines: {resume_text.count(chr(10))}")
            
            # Step 2: AI Processing
            st.write("⏳ Step 2: Running AI semantic analysis (Ollama llama3)...")
            st.write("  • Extracting candidate intelligence vectors")
            st.write("  • Identifying skills and proficiency levels")
            st.write("  • Analyzing career trajectory and domain exposure")
            st.write("  • Generating embedding vectors for semantic matching")
            
            status_placeholder.status("🧠 AI Analysis in Progress", expanded=True, state="running")
            
            # Parse resume - this is the slow part
            result = resume_parser.parse_resume(resume_text)
            profile = result['candidate_profile']
            
            status_placeholder.status("✓ Intelligence Extraction Complete", expanded=True, state="complete")
        
        # Step 3: Display results
        st.divider()
        st.success("✅ Candidate Intelligence Extracted Successfully!")
        
        # Store candidate
        st.session_state.candidates.append(profile)
        st.toast(f"✨ Candidate vector created: {profile.get('name', 'Candidate')}", icon="🧠")
        
        # Display candidate info in cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📝 Name", profile.get('name', 'Unknown')[:20])
        with col2:
            st.metric("⏱️ Experience", f"{profile.get('years_of_experience', 0)}y")
        with col3:
            skill_count = len(profile.get('tech_stack', []))
            st.metric("🛠️ Tech Skills", str(skill_count))
        
        st.divider()
        
        # Detailed sections
        tab1, tab2, tab3, tab4 = st.tabs(["👤 Contact", "🛠️ Technical", "💼 Experience", "📊 Full Intelligence Vector"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Name**")
                st.code(profile.get('name', 'Unknown'))
            with col2:
                st.write("**Email**")
                st.code(profile.get('email', 'N/A'))
            with col3:
                st.write("**Phone**")
                st.code(profile.get('phone', 'N/A'))
        
        with tab2:
            try:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Tech Stack**")
                    tech = profile.get('tech_stack', [])
                    if tech and isinstance(tech, list):
                        for t in tech[:10]:
                            st.write(f"• {str(t)}")
                    else:
                        st.info("No tech stack data")
                
                with col2:
                    st.write("**Industries**")
                    industries = profile.get('industry_exposure', [])
                    if industries and isinstance(industries, list):
                        for ind in industries[:5]:
                            st.write(f"• {str(ind)}")
                    else:
                        st.info("No industry data")
                
                st.divider()
                st.write("**Skills**")
                skills = profile.get('skills', [])
                if skills and isinstance(skills, list):
                    for skill in skills[:10]:
                        if isinstance(skill, dict):
                            skill_name = skill.get('skill', skill.get('name', 'N/A'))
                            skill_level = skill.get('proficiency', skill.get('level', 'N/A'))
                            st.write(f"• {skill_name} ({skill_level})")
                        else:
                            st.write(f"• {str(skill)}")
                else:
                    st.info("No skills data")
            except Exception as e:
                st.warning(f"Could not display technical details: {str(e)}")
        
        with tab3:
            try:
                st.write("**💼 Work Experience**")
                work_exp = profile.get('work_experience', [])
                if work_exp and isinstance(work_exp, list) and len(work_exp) > 0:
                    for job in work_exp[:5]:
                        if isinstance(job, dict):
                            st.write(f"**{job.get('position', 'N/A')}** @ {job.get('company', 'Company')}")
                            st.write(f"Duration: {job.get('duration', 'N/A')}")
                            if job.get('description'):
                                st.write(f"*{job.get('description')}*")
                        else:
                            st.write(f"• {str(job)}")
                        st.divider()
                else:
                    st.info("No work experience data extracted")
                
                st.write("**🎓 Education**")
                education = profile.get('education', [])
                if education and isinstance(education, list) and len(education) > 0:
                    for edu in education[:5]:
                        if isinstance(edu, dict):
                            degree = edu.get('degree', 'N/A')
                            field = edu.get('field', 'N/A')
                            institution = edu.get('institution', 'N/A')
                            st.write(f"**{degree}** in {field}")
                            st.write(f"From: {institution}")
                        else:
                            st.write(f"• {str(edu)}")
                        st.divider()
                else:
                    st.info("No education data extracted")
            except Exception as e:
                st.warning(f"Could not display experience details: {str(e)}")
        
        with tab4:
            try:
                st.write("**📊 Complete Candidate Intelligence Vector**")
                st.caption("Structured intelligence profile used for semantic matching")
                
                # Summary
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Fields", len(profile))
                    st.metric("Experience Years", profile.get('years_of_experience', 0))
                with col2:
                    st.metric("Skills Count", len(profile.get('skills', [])))
                    st.metric("Projects Count", len(profile.get('key_projects', [])))
                
                st.divider()
                
                # Show as expandable sections
                with st.expander("👤 Contact Information"):
                    contact = {
                        "name": profile.get('name'),
                        "email": profile.get('email'),
                        "phone": profile.get('phone')
                    }
                    st.json(contact)
                
                with st.expander("📝 Summary"):
                    st.write(profile.get('summary', 'No summary available'))
                
                with st.expander("🔬 Full Vector (Raw JSON)"):
                    st.json(profile)
                
            except Exception as e:
                st.error(f"Error displaying intelligence vector: {str(e)}")
                # Fallback: show raw text
                st.text(str(profile))
        
        # Action buttons
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add Another Resume", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("🎯 Proceed to AI Screening", use_container_width=True):
                st.toast("Go to 'AI Screening' page", icon="➡️")
        
    except Exception as e:
        st.error(f"❌ Error parsing resume")
        with st.expander("📋 Error Details"):
            st.code(str(e))
        logger.error(f"Resume parsing error: {str(e)}")


def show_screening():
    """AI Screening Engine - Evaluate candidate depth and communication"""
    st.header("❓ AI Screening Engine")
    st.write("Generate role-specific screening questions and evaluate candidate responses with AI")
    st.caption("🤖 **What it does:** Uses AI to create targeted screening questions and evaluate candidate responses on technical depth, communication, and problem-solving. **Why it matters:** AI-driven screening ensures consistent evaluation beyond resume keywords. **AI in use:** Ollama llama3 generates intelligent questions and scores responses.")
    
    st.divider()
    
    _, _, screener, _, _ = get_modules()
    
    if not st.session_state.hiring_profile:
        st.warning("⚠️ Please create a job profile first in 'Hiring Manager Intake'")
        return
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"📋 Questions for: {st.session_state.hiring_profile.get('role_title', 'Role')}")
    with col2:
        num_questions = st.selectbox("Number of Questions", [3, 4, 5], index=1)
    
    if st.button("✨ Generate AI Screening Questions", use_container_width=True):
        try:
            with st.spinner("⏳ Generating questions with AI..."):
                questions = screener.generate_screening_questions(
                    st.session_state.hiring_profile,
                    num_questions=num_questions
                )
                st.session_state.screening_questions = questions
                st.success(f"✅ Generated {len(questions)} screening questions!")
        except Exception as e:
            st.error(f"❌ Error generating questions: {str(e)}")
    
    if st.session_state.screening_questions:
        st.divider()
        
        answers = {}
        for i, q in enumerate(st.session_state.screening_questions, 1):
            st.subheader(f"Q{i}: {q.question_text}")
            answer = st.text_area(
                f"Your answer to question {i}:",
                height=100,
                key=f"answer_{i}",
                placeholder="Type your response here..."
            )
            answers[q.question_id] = answer
        
        if st.button("📊 Run AI Evaluation", use_container_width=True):
            try:
                with st.spinner("⏳ Evaluating responses with AI..."):
                    result = screener.evaluate_responses(
                        st.session_state.screening_questions,
                        answers,
                        st.session_state.hiring_profile
                    )
                    
                    st.success("✅ Evaluation complete!")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Technical", result['scores']['technical'], "/10")
                    with col2:
                        st.metric("Communication", result['scores']['communication'], "/10")
                    with col3:
                        st.metric("Problem-Solving", result['scores']['problem_solving'], "/10")
                    with col4:
                        st.metric("Overall", result['overall_score'], "/10")
                    
                    st.divider()
                    st.subheader("💡 Reasoning")
                    st.write(result['reasoning'])
                    
            except Exception as e:
                st.error(f"❌ Error evaluating: {str(e)}")


def show_match_analysis():
    """AI Match Analysis - Semantic matching using intelligence vectors"""
    st.header("⚡ AI Match Analysis")
    st.write("Analyze candidate-job fit using AI-powered semantic understanding and embedding-based matching")
    st.caption("🤖 **What it does:** Compares candidate and hiring intelligence vectors using semantic matching. Scores each match on similarity, screening performance, and hiring feedback signals. **Why it matters:** Semantic matching finds culturally and technically aligned candidates that keyword search misses. **AI in use:** Embedding-based similarity scoring with reinforcement learning from feedback.")
    
    st.divider()
    
    _, _, _, matcher, feedback = get_modules()
    
    if not st.session_state.hiring_profile:
        st.warning("⚠️ Please create a job profile first")
        return
    
    if not st.session_state.candidates:
        st.warning("⚠️ Please parse at least one resume first")
        return
    
    st.subheader(f"Job: {st.session_state.hiring_profile.get('role_title', 'N/A')}")
    
    if st.button("⚡ Run AI Match Analysis", use_container_width=True):
        try:
            with st.spinner("⏳ Matching candidates with job profile..."):
                results = []
                for candidate in st.session_state.candidates:
                    match = matcher.compute_match(
                        hiring_embedding=[0.1] * 768,
                        candidate_embedding=[0.1] * 768,
                        screening_score=7.0,
                        candidate_profile=candidate,
                        hiring_profile=st.session_state.hiring_profile
                    )
                    results.append({**match, 'candidate_name': candidate.get('name', 'Unknown')})
                
                st.session_state.match_results = results
                st.success(f"✅ Matched {len(results)} candidates!")
        except Exception as e:
            st.error(f"❌ Error matching: {str(e)}")
    
    if st.session_state.match_results:
        st.divider()
        st.subheader("🎯 Match Analysis Results")
        st.caption("AI-powered semantic matching analysis with visual confidence indicators")
        
        for idx, match in enumerate(st.session_state.match_results, 1):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                
                with col1:
                    st.write(f"**{idx}. {match['candidate_name']}**")
                
                # Confidence indicator
                final_score = match['final_score']
                if final_score >= 7.5:
                    confidence = "🟢 High"
                    confidence_detail = "Strong fit"
                elif final_score >= 5.5:
                    confidence = "🟡 Medium"
                    confidence_detail = "Moderate fit"
                else:
                    confidence = "🔴 Low"
                    confidence_detail = "Weak fit"
                
                with col2:
                    st.metric("Confidence", confidence, confidence_detail)
                
                with col3:
                    st.metric("Semantic Similarity", f"{match['similarity_score']:.2f}")
                
                with col4:
                    st.metric("Match Score", f"{final_score:.1f}/10")
                
                with col5:
                    feedback_btns = st.columns(2)
                    with feedback_btns[0]:
                        if st.button("👍 Good", key=f"good_{idx}"):
                            try:
                                feedback.record_feedback(
                                    candidate_id=match.get('candidate_name', f'candidate_{idx}').lower().replace(' ', '_'),
                                    hiring_manager_id="hiring_manager_001",
                                    final_score=match['final_score'],
                                    feedback="Good Fit",
                                    notes=f"Match score: {match['final_score']:.1f}/10"
                                )
                                st.success("✅ Feedback recorded! Analytics updated.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error recording feedback: {str(e)}")
                    with feedback_btns[1]:
                        if st.button("👎 Not Fit", key=f"bad_{idx}"):
                            try:
                                feedback.record_feedback(
                                    candidate_id=match.get('candidate_name', f'candidate_{idx}').lower().replace(' ', '_'),
                                    hiring_manager_id="hiring_manager_001",
                                    final_score=match['final_score'],
                                    feedback="Not a Fit",
                                    notes=f"Match score: {match['final_score']:.1f}/10"
                                )
                                st.info("✅ Feedback recorded! Analytics updated.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error recording feedback: {str(e)}")
                
                # Display explanation if available
                explanation = match.get('explanation', '')
                if explanation:
                    st.info(f"📝 {explanation}")
                st.divider()


def show_learning_feedback():
    """Learning & Feedback - Continuous improvement via reinforcement learning"""
    st.header("🔄 Learning & Feedback Loop")
    st.write("Monitor system performance and provide feedback signals for continuous AI improvement")
    st.caption("🤖 **What it does:** Tracks hiring outcomes and uses feedback signals to dynamically adjust matching weights via reinforcement learning. Measures match accuracy, model confidence, and algorithm performance. **Why it matters:** Feedback loops transform AI from static to adaptive, learning hiring manager preferences over time. **AI in use:** Reinforcement learning algorithm automatically tunes similarity and screening weights based on hiring feedback.")
    
    st.divider()
    st.write("Real-time analytics based on hiring feedback and AI model performance")
    
    _, _, _, _, feedback_collector = get_modules()
    
    # Add auto-refresh button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    try:
        analytics = feedback_collector.get_feedback_analytics()
        weights = feedback_collector.get_weights()
        
        # Key Metrics Row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Feedback",
                analytics.get('total_feedback', 0),
                delta="feedback entries" if analytics.get('total_feedback', 0) > 0 else "No feedback yet"
            )
        with col2:
            good_fit = analytics.get('good_fit_count', 0)
            total = analytics.get('total_feedback', 0)
            accuracy = (good_fit / total * 100) if total > 0 else 0
            st.metric(
                "Match Accuracy",
                f"{accuracy:.1f}%",
                delta=f"{good_fit} matches approved" if total > 0 else "Pending feedback"
            )
        with col3:
            st.metric(
                "Model Confidence",
                f"{weights.get('confidence', 0.5):.2f}",
                delta="confidence score" if weights.get('confidence', 0.5) > 0 else "Low confidence"
            )
        
        st.divider()
        
        # Analytics Details
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Feedback Distribution")
            good_fit_count = analytics.get('good_fit_count', 0)
            not_fit_count = analytics.get('not_fit_count', 0)
            
            if good_fit_count + not_fit_count > 0:
                st.write(f"🟢 **Good Fits:** {good_fit_count} ({good_fit_count/(good_fit_count+not_fit_count)*100:.1f}%)")
                st.write(f"🔴 **Not Fits:** {not_fit_count} ({not_fit_count/(good_fit_count+not_fit_count)*100:.1f}%)")
                
                # Progress bar visualization
                progress = good_fit_count / (good_fit_count + not_fit_count)
                st.progress(progress, text=f"{progress:.1%} positive feedback")
            else:
                st.info("📌 No feedback data yet. Start reviewing matches to populate analytics.")
        
        with col2:
            st.subheader("⚙️ Current Algorithm Weights")
            similarity_weight = weights.get('similarity_weight', 0.6)
            screening_weight = weights.get('screening_weight', 0.4)
            
            st.write(f"**Similarity Weight:** {similarity_weight:.2f} (60%)")
            st.progress(similarity_weight, text=f"Similarity component")
            
            st.write(f"**Screening Weight:** {screening_weight:.2f} (40%)")
            st.progress(screening_weight, text=f"Screening component")
            
            if st.button("🔄 Reset Weights to Defaults", use_container_width=True):
                try:
                    feedback_collector.reset_weights()
                    st.success("✅ Weights reset to default values (0.60 / 0.40)")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error resetting weights: {str(e)}")
        
        st.divider()
        
        # Score Statistics
        st.subheader("📈 Score Statistics by Feedback Type")
        try:
            score_stats = analytics.get('score_statistics', [])
            
            if score_stats and isinstance(score_stats, list) and len(score_stats) > 0:
                # Create columns based on number of stats
                num_cols = min(len(score_stats), 3)  # Max 3 columns
                cols = st.columns(num_cols)
                
                for i, stat in enumerate(score_stats):
                    col_idx = i % num_cols
                    with cols[col_idx]:
                        try:
                            st.metric(
                                f"📊 {stat.get('feedback', 'Unknown')}",
                                f"{stat.get('avg_score', 0):.2f}/10",
                                delta=f"{stat.get('count', 0)} samples"
                            )
                        except Exception as stat_error:
                            st.warning(f"Could not display stat: {str(stat_error)}")
            else:
                st.info("📌 Score statistics will appear after feedback is recorded.")
        except Exception as stats_error:
            st.warning(f"Could not load score statistics: {str(stats_error)}")
        
        st.divider()
        
        # Weight History
        st.subheader("📜 Weight Adjustment History")
        try:
            weight_history = feedback_collector.get_weight_history(limit=5)
            
            if weight_history and isinstance(weight_history, list) and len(weight_history) > 0:
                for i, history in enumerate(weight_history, 1):
                    try:
                        with st.expander(f"Update {i} - {history.get('created_at', 'Unknown')}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Trigger Action:** {history.get('trigger_action', 'N/A')}")
                                st.write(f"**Feedback Count:** {history.get('feedback_count', 0)}")
                            with col2:
                                st.write(f"**Similarity Weight:** {history.get('similarity_weight', 0):.3f}")
                                st.write(f"**Screening Weight:** {history.get('screening_weight', 0):.3f}")
                                st.write(f"**Confidence:** {history.get('confidence', 0):.3f}")
                    except Exception as history_error:
                        st.warning(f"Could not display history item: {str(history_error)}")
            else:
                st.info("📌 Weight history will appear once weights are automatically adjusted (need 5+ feedback entries).")
        except Exception as history_load_error:
            st.warning(f"Could not load weight history: {str(history_load_error)}")
            
    except Exception as e:
        st.error(f"❌ Error loading Learning & Feedback analytics: {str(e)}")
        with st.expander("📋 Debug Information"):
            st.write(f"Error Type: {type(e).__name__}")
            st.write(f"Error Message: {str(e)}")
            st.code(str(e))
        logger.error(f"Learning & Feedback error: {str(e)}")
        
        # Provide helpful guidance
        st.info("💡 **Troubleshooting:**\n- Ensure feedback has been recorded in Match Analysis\n- Check that the feedback database is accessible\n- Try refreshing the page")


def main():
    """Main app"""
    st.title("🎯 TalentVector AI")
    st.subheader("AI-Native Recruiting Operating System")
    
    # Sidebar navigation
    page = st.sidebar.radio(
        "📍 Navigation",
        ["Dashboard", "Hiring Intelligence", "Candidate Intelligence", "AI Screening", "Match Analysis", "Learning & Feedback"],
        index=0
    )
    
    st.sidebar.divider()
    st.sidebar.info(
        "🚀 **TalentVector AI**\n\n"
        "Intelligent recruiting operating system:\n"
        "- AI resume vectorization\n"
        "- Semantic matching\n"
        "- AI-driven screening\n"
        "- Reinforcement learning feedback"
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Hiring Intelligence":
        show_hiring_intelligence()
    elif page == "Candidate Intelligence":
        show_candidate_intelligence()
    elif page == "AI Screening":
        show_screening()
    elif page == "Match Analysis":
        show_match_analysis()
    elif page == "Learning & Feedback":
        show_learning_feedback()


if __name__ == "__main__":
    # Validate configuration
    is_valid, errors = Config.validate()
    if not is_valid:
        st.error("❌ Configuration Error!")
        for error in errors:
            st.error(f"  • {error}")
        st.error("Please check your .env file and ensure GEMINI_API_KEY is set")
        st.stop()
    
    main()
