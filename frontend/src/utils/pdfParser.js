import * as pdfjsLib from 'pdfjs-dist'

// Initialize PDF worker using Vite's /@fs/ protocol to serve local files
// This avoids CORS issues with external CDNs
pdfjsLib.GlobalWorkerOptions.workerSrc = '/@fs/' + String(new URL('pdfjs-dist/build/pdf.worker.min.mjs', import.meta.url).pathname)
console.log(' PDF worker configured at:', pdfjsLib.GlobalWorkerOptions.workerSrc)

export const extractTextFromPDF = async (file) => {
  try {
    const arrayBuffer = await file.arrayBuffer()
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise
    let text = ''

    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i)
      const content = await page.getTextContent()
      const pageText = content.items.map((item) => item.str || '').join(' ')
      text += pageText + '\n'
    }

    console.log(' PDF text extracted successfully')
    return text.trim()
  } catch (error) {
    console.error(' Error extracting PDF text:', error)
    throw new Error('Failed to extract text from PDF: ' + error.message)
  }
}

export const extractTextFromFile = async (file) => {
  console.log(' Processing file:', file.name, 'Type:', file.type)
  
  if (file.type === 'application/pdf') {
    return await extractTextFromPDF(file)
  } else if (
    file.type === 'text/plain' ||
    file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  ) {
    const text = await file.text()
    console.log(' Text file extracted successfully')
    return text.trim()
  } else {
    throw new Error('Unsupported file type. Please upload PDF, DOCX, or TXT')
  }
}
