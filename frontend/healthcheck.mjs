#!/usr/bin/env node

/**
 * TalentVector Frontend Health Check
 * Verifies all dependencies and configuration
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

console.log('\n🔍 TalentVector Frontend Health Check\n')

// Check 1: package.json exists
console.log('✓ Checking package.json...')
const pkgPath = path.join(__dirname, 'package.json')
if (!fs.existsSync(pkgPath)) {
  console.error('❌ package.json not found')
  process.exit(1)
}
const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'))
console.log(`   Version: ${pkg.version}`)
console.log(`   Scripts: ${Object.keys(pkg.scripts).join(', ')}`)

// Check 2: Critical files exist
console.log('\n✓ Checking critical files...')
const criticalFiles = [
  'src/main.jsx',
  'src/App.jsx',
  'src/store/index.js',
  'src/services/api.js',
  'vite.config.js',
  'tailwind.config.js',
  'index.html'
]

let allFilesExist = true
for (const file of criticalFiles) {
  const filePath = path.join(__dirname, file)
  if (fs.existsSync(filePath)) {
    console.log(`   ✓ ${file}`)
  } else {
    console.log(`   ❌ ${file}`)
    allFilesExist = false
  }
}

if (!allFilesExist) {
  console.error('\n❌ Some critical files are missing!')
  process.exit(1)
}

// Check 3: Page components
console.log('\n✓ Checking page components...')
const pages = [
  'HiringManager',
  'Dashboard',
  'ResumeIntelligence',
  'JobIntelligence',
  'MatchAnalysis',
  'Screening',
  'Feedback'
]

for (const page of pages) {
  const pagePath = path.join(__dirname, `src/pages/${page}.jsx`)
  if (fs.existsSync(pagePath)) {
    console.log(`   ✓ ${page}.jsx`)
  } else {
    console.log(`   ❌ ${page}.jsx`)
  }
}

// Check 4: UI components
console.log('\n✓ Checking UI components...')
const components = [
  'Navbar',
  'Sidebar',
  'LoadingSpinner',
  'Alert',
  'ScoreCard'
]

for (const component of components) {
  const compPath = path.join(__dirname, `src/components/${component}.jsx`)
  if (fs.existsSync(compPath)) {
    console.log(`   ✓ ${component}.jsx`)
  } else {
    console.log(`   ❌ ${component}.jsx`)
  }
}

// Check 5: Dependencies
console.log('\n✓ Checking dependencies...')
const requiredDeps = [
  'react',
  'react-dom',
  'zustand',
  'axios',
  'pdfjs-dist'
]

for (const dep of requiredDeps) {
  const depPath = path.join(__dirname, 'node_modules', dep)
  if (fs.existsSync(depPath)) {
    console.log(`   ✓ ${dep}`)
  } else {
    console.log(`   ⚠️  ${dep} - install with: npm install`)
  }
}

console.log('\n✅ Frontend health check complete!\n')
console.log('Next steps:')
console.log('1. npm install (if dependencies missing)')
console.log('2. npm run dev (start development server)')
console.log('3. Visit http://localhost:5173\n')
