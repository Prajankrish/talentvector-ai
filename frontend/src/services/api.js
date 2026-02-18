import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 600000, // 10 minutes - Ollama/LLM processing can take considerable time on first run
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error Details:')
    console.error('- Status:', error.response?.status || error.code || 'Unknown')
    console.error('- Data:', error.response?.data || 'No response')
    console.error('- Message:', error.message)
    console.error('- Full error:', error)
    return Promise.reject(error)
  }
)

export const apiService = {
  // Hiring Intelligence - Explicit structure for consistent handling
  generateHiringProfile: (data) =>
    api.post('/api/hiring-profile', data)
      .then(res => {
        console.log('Hiring Profile API Response:', res.data)
        
        // Backend returns: { status, profile, summary, embedding_length }
        // We standardize to: { data: { hiring_profile }, status, summary }
        const hiringProfile = res.data.profile || res.data.structured_profile || res.data
        
        if (!hiringProfile) {
          console.error('No hiring profile in response:', res.data)
          throw new Error('No profile data in response')
        }
        
        console.log('Hiring Profile extracted:', hiringProfile)
        
        return {
          data: {
            hiring_profile: hiringProfile  // Explicitly wrap for component expectations
          },
          status: res.data.status || 'success',
          summary: res.data.summary || ''
        }
      })
      .catch(error => {
        console.error('Hiring profile generation failed:')
        console.error('Status:', error.response?.status)
        console.error('Data:', error.response?.data)
        console.error('Message:', error.message)
        throw error
      }),

  // Resume Intelligence - Standardized response structure
  parseResume: (resumeText) =>
    api.post('/api/parse-resume', { resume_text: resumeText })
      .then(res => {
        console.log('Resume Parsing API Response:', res.data)
        
        // Backend returns: { status, candidate, embedding_length }
        // We standardize to: { data: { candidate_profile }, status }
        const candidateProfile = res.data.candidate || res.data.candidate_profile || res.data
        
        if (!candidateProfile) {
          console.error('No candidate profile in response:', res.data)
          throw new Error('No profile data in response')
        }
        
        console.log('Candidate Profile extracted:', candidateProfile)
        
        return {
          data: {
            candidate_profile: candidateProfile
          },
          status: res.data.status || 'success'
        }
      })
      .catch(error => {
        console.error('Resume parsing failed:')
        console.error('Status:', error.response?.status)
        console.error('Data:', error.response?.data)
        console.error('Message:', error.message)
        throw error
      }),

  // Screening
  generateScreening: (hiringProfile, numQuestions = 4) =>
    api.post('/api/screening/generate-questions', {
      hiring_profile: hiringProfile,
      num_questions: numQuestions,
    }).catch(error => {
      console.error('Screening generation failed:', error.response?.data)
      throw error
    }),

  // Matching
  matchCandidate: (candidateProfile, hiringProfile, screeningScore = 7.0) =>
    api.post('/api/matching/compute', {
      candidate_profile: candidateProfile,
      hiring_profile: hiringProfile,
      screening_score: screeningScore,
    }).catch(error => {
      console.error('Matching failed:', error.response?.data)
      throw error
    }),

  // Feedback - Fixed to send as JSON body
  submitFeedback: (candidateId, hiringManagerId, finalScore, feedback, notes) =>
    api.post('/api/feedback/record', {
      candidate_id: candidateId,
      hiring_manager_id: hiringManagerId,
      final_score: finalScore,
      feedback: feedback,
      notes: notes,
    }).catch(error => {
      console.error('Feedback submission failed:', error.response?.data)
      throw error
    }),

  // Health check
  healthCheck: () =>
    api.get('/health'),
}

export default api
