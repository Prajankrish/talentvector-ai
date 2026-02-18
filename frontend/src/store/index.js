import { create } from 'zustand'

export const useStore = create((set) => ({
  // Hiring Manager state
  hiringManager: null,
  setHiringManager: (manager) => set({ hiringManager: manager }),

  // Resume/Candidate state
  candidateProfile: null,
  setCandidateProfile: (profile) => set({ candidateProfile: profile }),
  
  // Job/Hiring state
  hiringProfile: null,
  setHiringProfile: (profile) => set({ hiringProfile: profile }),
  
  // Match result state
  matchResult: null,
  setMatchResult: (result) => set({ matchResult: result }),
  
  // Screening state
  screeningQuestions: [],
  setScreeningQuestions: (questions) => set({ screeningQuestions: questions }),
  
  // UI state
  loading: false,
  setLoading: (loading) => set({ loading }),
  
  error: null,
  setError: (error) => set({ error }),
  
  success: null,
  setSuccess: (success) => set({ success }),
  
  // System status
  backendConnected: false,
  setBackendConnected: (connected) => set({ backendConnected: connected }),
  
  ollamaStatus: false,
  setOllamaStatus: (status) => set({ ollamaStatus: status }),
  
  // Reset function
  reset: () => set({
    candidateProfile: null,
    hiringProfile: null,
    matchResult: null,
    screeningQuestions: [],
    error: null,
    success: null,
  }),
}))
