import { useState } from 'react'
import { uploadCv } from '../api/cvApi.js'
import Alert from '../components/Alert.jsx'
import UploadBox from '../components/UploadBox.jsx'

export default function UploadPage({ onUploaded }) {
  const [isUploading, setIsUploading] = useState(false)
  const [error, setError] = useState('')

  async function handleUpload(file) {
    setIsUploading(true)
    setError('')

    try {
      const result = await uploadCv(file)
      onUploaded(result?.id)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <main className="page narrow-page">
      <section className="page-heading centered-heading">
        <div>
          <p className="eyebrow">Upload</p>
          <h1>Dodaj CV do analizy obrazu i OCR</h1>
          <p>Plik zostanie wysłany jako multipart/form-data pod kluczem file.</p>
        </div>
      </section>

      <Alert type="error">{error}</Alert>

      <UploadBox onUpload={handleUpload} isUploading={isUploading} />
    </main>
  )
}