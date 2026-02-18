#!/usr/bin/env python3
"""Test script to verify resume parsing improvements"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from resume_parser import ResumeParser
from ollama_client import safe_json_parse

# Prajan's resume
resume_text = """PRAJAN G
Machine Learning & Data Science Enthusiast | AI Developer | Python & Power BI Practitioner
6383783267 | prajanofficial7@gmail.com | github.com/Prajankrish | linkedin.com/in/prajankrish | Coimbatore
 
PROFESSIONAL SUMMARY
Machine Learning Engineering student passionate about building AI solutions using predictive modeling and neural networks. Proven experience in developing ML pipelines, automating workflows, and translating data insights into business value.
EDUCATION
  Currently pursuing B.Tech Artificial Intelligence and Machine Learning at SNS College of Technology (Expected: May 2026) with CGPA 8.22 
  HSC in Hillfort Matric Hr.Sec School, Kotagiri - TN State Board (May 2022) : 83.6%
  SSLC in St. Mary's Home Matriculation school, Kotagiri - TN State Board (Apr 2020) : 77.8%
SKILLS
  Programming: Python, SQL  
  ML/DL: Supervised/Unsupervised Learning, NLP, TensorFlow, PyTorch  
  Data Tools: Pandas, Power BI, Tableau, Excel (Advanced)  
  Databases: MongoDB, SQL  
  Other: GitHub, Streamlit, n8n (Workflow Automation)  
EXPERIENCE:
Data Analyst Intern | INFOTACT Solutions | Jun 2025 – Aug 2025
Analyzed and visualized business data using Python and Power BI to drive decision-making.
Automated reports and improved data workflows, enhancing efficiency for stakeholders.
Data Science and Analyst Intern | Future Interns | May 2025 – Jun 2025
Built interactive dashboards and performed business analysis using real-world datasets. Tools: Power BI, Excel
Machine Learning Intern | Accent Techno Soft | Jul 2024 – Sep 2024
Worked on ML algorithms using Python; handled data preprocessing, model training, and evaluation.
Tools: Python, Scikit-learn, Pandas
PROJECTS
  Cold Mail Generation Tool – Developed a tool using Llama 3.1 and Streamlit to auto-generate corporate emails for brands based on job roles and hiring needs.
  LEXAI (Legal Expert AI Chatbot using Generative AI)-Built LEXAI, a legal chatbot using the Mistral model and RAG with Ollama and Streamlit to answer queries on Indian laws.
  Qore – AI-Enhanced Quantum ML Platform: Built an interactive hybrid platform combining classical and quantum ML with automated training, evaluation, and error mitigation workflows.
  Image Classification (Sports Celebrities) – Built a pipeline using classical ML to classify sports celebrity images with web scraping, face detection, and model training.
  Blinkit Sales & Operations Analysis (Power BI)-Designed an interactive Power BI dashboard to visualize Blinkit's order trends, category-wise sales, delivery times, and customer behavior, enabling data-driven insights for business decision-making."""

print("=" * 70)
print("RESUME PARSING TEST")
print("=" * 70)
print()

# Test 1: Test safe_json_parse with various formats
print("Test 1: Testing safe_json_parse with various formats")
print("-" * 70)

test_cases = [
    ('{"name": "Test"}', "Simple JSON"),
    ('```json\n{"name": "Test"}\n```', "Markdown JSON"),
    ('Some text {"name": "Test"} more text', "JSON with surrounding text"),
    ('{"name": "John", "age": 30,}', "JSON with trailing comma"),
    ('{"name":"John","age":30}', "JSON without spaces"),
]

for json_text, description in test_cases:
    result = safe_json_parse(json_text)
    status = "✓" if result else "✗"
    print(f"{status} {description}: {result}")

print()

# Test 2: Test resume parsing
print("Test 2: Parsing actual resume")
print("-" * 70)

try:
    parser = ResumeParser()
    print("✓ ResumeParser initialized")
    print()
    print("Starting resume parsing with improved extraction...")
    
    result = parser.parse_resume(resume_text)
    profile = result['candidate_profile']
    
    print("✓ Resume parsed successfully!")
    print()
    print("EXTRACTED PROFILE:")
    print("-" * 70)
    
    # Display extracted profile
    print(f"Name:              {profile.get('name', 'Unknown')}")
    print(f"Email:             {profile.get('email', 'N/A')}")
    print(f"Phone:             {profile.get('phone', 'N/A')}")
    print(f"Experience:        {profile.get('years_of_experience', 0)} years")
    print(f"Summary:           {profile.get('summary', 'N/A')[:60]}...")
    print()
    print(f"Tech Stack:        {profile.get('tech_stack', [])}")
    print(f"Skills:            {profile.get('skills', [])[:3]}...")
    print(f"Industries:        {profile.get('industry_exposure', [])}")
    print()
    print(f"Work Experience:   {len(profile.get('work_experience', []))} entries")
    for i, job in enumerate(profile.get('work_experience', [])[:2], 1):
        print(f"  {i}. {job}")
    
    print()
    print(f"Education:         {len(profile.get('education', []))} entries")
    for i, edu in enumerate(profile.get('education', []), 1):
        print(f"  {i}. {edu}")
    
    print()
    print(f"Key Projects:      {len(profile.get('key_projects', []))} entries")
    for i, proj in enumerate(profile.get('key_projects', [])[:2], 1):
        print(f"  {i}. {proj}")
    
    print()
    print("✓ All parsing successful!")
    
except Exception as e:
    print(f"✗ Error during parsing: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("=" * 70)
