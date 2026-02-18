import React, { useState } from 'react'
import { FiX, FiTrash2 } from 'react-icons/fi'
import { apiService } from '../services/api'
import { useStore } from '../store'
import LoadingSpinner from '../components/LoadingSpinner'
import Alert from '../components/Alert'

const PREDEFINED_SKILLS = [
  'Python', 'JavaScript', 'Java', 'C++', 'Go', 'Rust', 'React', 'Vue', 'Angular',
  'AWS', 'GCP', 'Azure', 'Docker', 'Kubernetes', 'PostgreSQL', 'MongoDB',
  'TypeScript', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring Boot'
]

const JOB_LEVELS = ['Junior', 'Mid-Level', 'Senior', 'Lead', 'Principal']

export default function JobIntelligence() {
  const [jobTitle, setJobTitle] = useState('')
  const [requiredSkills, setRequiredSkills] = useState([])
  const [niceSkills, setNiceSkills] = useState([])
  const [yearsOfExp, setYearsOfExp] = useState(3)
  const [industry, setIndustry] = useState('')
  const [teamCulture, setTeamCulture] = useState('')
  const [jobLevel, setJobLevel] = useState('Mid-Level')
  const [salaryRange, setSalaryRange] = useState('')
  const [qualifications, setQualifications] = useState('')
  const [skillInput, setSkillInput] = useState('')
  const [niceSkillInput, setNiceSkillInput] = useState('')

  const loading = useStore((state) => state.loading)
  const setLoading = useStore((state) => state.setLoading)
  const hiringProfile = useStore((state) => state.hiringProfile)
  const setHiringProfile = useStore((state) => state.setHiringProfile)
  const error = useStore((state) => state.error)
  const setError = useStore((state) => state.setError)
  const success = useStore((state) => state.success)
  const setSuccess = useStore((state) => state.setSuccess)


  const handleAddSkill = (skill, isNice = false) => {
    if (isNice) {
      if (!niceSkills.includes(skill)) {
        setNiceSkills([...niceSkills, skill])
      }
      setNiceSkillInput('')
    } else {
      if (!requiredSkills.includes(skill)) {
        setRequiredSkills([...requiredSkills, skill])
      }
      setSkillInput('')
    }
  }

  const handleRemoveSkill = (skill, isNice = false) => {
    if (isNice) {
      setNiceSkills(niceSkills.filter(s => s !== skill))
    } else {
      setRequiredSkills(requiredSkills.filter(s => s !== skill))
    }
  }

  const handleGenerateProfile = async () => {
    if (!jobTitle.trim() || requiredSkills.length === 0 || !industry.trim() || !teamCulture.trim()) {
      setError('Please fill in all required fields: Job Title, Required Skills, Industry, and Team Culture')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const response = await apiService.generateHiringProfile({
        role_title: jobTitle,
        required_skills: requiredSkills,
        nice_to_have_skills: niceSkills,
        years_of_experience: yearsOfExp,
        industry: industry,
        team_culture_description: teamCulture,
        job_level: jobLevel,
        salary_range: salaryRange || null,
        qualifications: qualifications || null,
      })
      setHiringProfile(response.data.hiring_profile || response.data)
      setSuccess('Job profile generated successfully!')
    } catch (err) {
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to generate job profile'
      console.error('Job profile generation error:', errorMsg)
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setJobTitle('')
    setRequiredSkills([])
    setNiceSkills([])
    setYearsOfExp(3)
    setIndustry('')
    setTeamCulture('')
    setJobLevel('Mid-Level')
    setSalaryRange('')
    setQualifications('')
    setSkillInput('')
    setNiceSkillInput('')
    setHiringProfile(null)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-white">💼 Job Intelligence Engine</h1>
        {hiringProfile && (
          <button
            onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2 text-slate-300 hover:text-slate-100 transition"
          >
            <FiTrash2 className="w-4 h-4" /> Clear All
          </button>
        )}
      </div>

      <p className="text-slate-400">
        Transform your hiring intent into structured intelligence that powers AI-driven matching
      </p>

      {error && <Alert type="error" title="Error" message={error} onClose={() => setError(null)} />}
      {success && <Alert type="success" title="Success" message={success} onClose={() => setSuccess(null)} />}

      {!hiringProfile ? (
        <div className="space-y-6">
          {/* Job Title */}
          <div className="glass-card-hover p-6 rounded-xl">
            <label className="block text-white font-semibold mb-3">Job Title *</label>
            <input
              type="text"
              value={jobTitle}
              onChange={(e) => setJobTitle(e.target.value)}
              placeholder="e.g., Senior Python Developer"
              className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
            />
          </div>

          {/* Required Skills */}
          <div className="glass-card-hover p-6 rounded-xl">
            <label className="block text-white font-semibold mb-3">Required Skills *</label>
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={skillInput}
                onChange={(e) => setSkillInput(e.target.value)}
                placeholder="Type skill name..."
                className="flex-1 bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-cyan-400"
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && skillInput.trim()) {
                    handleAddSkill(skillInput.trim())
                  }
                }}
              />
              <button
                onClick={() => handleAddSkill(skillInput.trim())}
                disabled={!skillInput.trim()}
                className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 disabled:opacity-50 text-white rounded-lg transition"
              >
                Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2 mb-3">
              {requiredSkills.map((skill) => (
                <div key={skill} className="flex items-center gap-2 bg-cyan-900/40 text-cyan-300 px-3 py-1 rounded-full">
                  {skill}
                  <button
                    onClick={() => handleRemoveSkill(skill)}
                    className="ml-1 hover:text-cyan-100"
                  >
                    <FiX className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
            <div className="text-slate-400 text-sm mb-2">Quick select:</div>
            <div className="flex flex-wrap gap-2">
              {PREDEFINED_SKILLS.filter(s => !requiredSkills.includes(s)).slice(0, 8).map((skill) => (
                <button
                  key={skill}
                  onClick={() => handleAddSkill(skill)}
                  className="text-xs px-2 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded"
                >
                  + {skill}
                </button>
              ))}
            </div>
          </div>

          {/* Nice-to-Have Skills */}
          <div className="glass-card-hover p-6 rounded-xl">
            <label className="block text-white font-semibold mb-3">Nice-to-Have Skills</label>
            <div className="flex gap-2 mb-3">
              <input
                type="text"
                value={niceSkillInput}
                onChange={(e) => setNiceSkillInput(e.target.value)}
                placeholder="Type skill name..."
                className="flex-1 bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-cyan-400"
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && niceSkillInput.trim()) {
                    handleAddSkill(niceSkillInput.trim(), true)
                  }
                }}
              />
              <button
                onClick={() => handleAddSkill(niceSkillInput.trim(), true)}
                disabled={!niceSkillInput.trim()}
                className="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white rounded-lg transition"
              >
                Add
              </button>
            </div>
            <div className="flex flex-wrap gap-2">
              {niceSkills.map((skill) => (
                <div key={skill} className="flex items-center gap-2 bg-purple-900/40 text-purple-300 px-3 py-1 rounded-full">
                  {skill}
                  <button
                    onClick={() => handleRemoveSkill(skill, true)}
                    className="ml-1 hover:text-purple-100"
                  >
                    <FiX className="w-4 h-4" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Years of Experience and Industry */}
          <div className="grid grid-cols-2 gap-6">
            <div className="glass-card-hover p-6 rounded-xl">
              <label className="block text-white font-semibold mb-3">Years of Experience *</label>
              <input
                type="number"
                min="0"
                max="50"
                value={yearsOfExp}
                onChange={(e) => setYearsOfExp(parseInt(e.target.value) || 0)}
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>
            <div className="glass-card-hover p-6 rounded-xl">
              <label className="block text-white font-semibold mb-3">Industry *</label>
              <input
                type="text"
                value={industry}
                onChange={(e) => setIndustry(e.target.value)}
                placeholder="e.g., FinTech, HealthTech"
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          {/* Team Culture */}
          <div className="glass-card-hover p-6 rounded-xl">
            <label className="block text-white font-semibold mb-3">Team Culture & Work Environment *</label>
            <textarea
              value={teamCulture}
              onChange={(e) => setTeamCulture(e.target.value)}
              placeholder="Describe your team culture, work style, and environment..."
              rows="5"
              className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400 resize-none"
            />
          </div>

          {/* Job Level, Salary, and Qualifications */}
          <div className="grid grid-cols-3 gap-6">
            <div className="glass-card-hover p-6 rounded-xl">
              <label className="block text-white font-semibold mb-3">Job Level</label>
              <select
                value={jobLevel}
                onChange={(e) => setJobLevel(e.target.value)}
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              >
                {JOB_LEVELS.map((level) => (
                  <option key={level} value={level}>
                    {level}
                  </option>
                ))}
              </select>
            </div>
            <div className="glass-card-hover p-6 rounded-xl">
              <label className="block text-white font-semibold mb-3">Salary Range (Optional)</label>
              <input
                type="text"
                value={salaryRange}
                onChange={(e) => setSalaryRange(e.target.value)}
                placeholder="e.g., $120K-$150K"
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>
            <div className="glass-card-hover p-6 rounded-xl">
              <label className="block text-white font-semibold mb-3">Additional Qualifications</label>
              <input
                type="text"
                value={qualifications}
                onChange={(e) => setQualifications(e.target.value)}
                placeholder="e.g., MBA, Certifications"
                className="w-full bg-slate-900 text-slate-200 border border-slate-600 rounded-lg px-4 py-3 focus:outline-none focus:border-cyan-400"
              />
            </div>
          </div>

          {/* Generate Button */}
          {loading ? (
            <LoadingSpinner text="Generating job profile..." />
          ) : (
            <button onClick={handleGenerateProfile} className="btn-primary w-full text-lg py-4">
              ✨ Generate Hiring Intelligence Profile
            </button>
          )}
        </div>
      ) : (
        <div className="glass-card-hover p-8 rounded-2xl">
          <h2 className="text-2xl font-bold text-white mb-6">✅ Job Profile Created</h2>
          
          <div className="grid grid-cols-2 gap-6 mb-6">
            <div>
              <p className="text-slate-500 text-sm font-medium">Role Title</p>
              <p className="text-white text-lg font-semibold mt-1">{hiringProfile.role_title || 'N/A'}</p>
            </div>
            <div>
              <p className="text-slate-500 text-sm font-medium">Industry</p>
              <p className="text-white text-lg font-semibold mt-1">{hiringProfile.industry || 'N/A'}</p>
            </div>
            <div>
              <p className="text-slate-500 text-sm font-medium">Job Level</p>
              <p className="text-white text-lg font-semibold mt-1">{hiringProfile.job_level || 'N/A'}</p>
            </div>
            <div>
              <p className="text-slate-500 text-sm font-medium">Years of Experience</p>
              <p className="text-white text-lg font-semibold mt-1">{hiringProfile.years_of_experience || 'N/A'}</p>
            </div>
          </div>

          {hiringProfile.required_skills && (
            <div className="mb-4">
              <p className="text-slate-500 text-sm font-medium mb-2">Required Skills</p>
              <div className="flex flex-wrap gap-2">
                {hiringProfile.required_skills.map((skill) => (
                  <span key={skill} className="bg-cyan-900/40 text-cyan-300 px-3 py-1 rounded-full text-sm">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {hiringProfile.nice_to_have_skills && hiringProfile.nice_to_have_skills.length > 0 && (
            <div className="mb-6">
              <p className="text-slate-500 text-sm font-medium mb-2">Nice-to-Have Skills</p>
              <div className="flex flex-wrap gap-2">
                {hiringProfile.nice_to_have_skills.map((skill) => (
                  <span key={skill} className="bg-purple-900/40 text-purple-300 px-3 py-1 rounded-full text-sm">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}

          {hiringProfile.qualifications && (
            <div className="mb-4">
              <p className="text-slate-500 text-sm font-medium">Qualifications</p>
              <p className="text-slate-300 mt-1">{hiringProfile.qualifications}</p>
            </div>
          )}

          <div className="pt-6 border-t border-slate-700">
            <button
              onClick={handleReset}
              className="w-full flex items-center justify-center gap-2 bg-slate-700 hover:bg-slate-600 text-white font-semibold py-3 rounded-lg transition"
            >
              <FiX className="w-4 h-4" /> Create New Job Profile
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
