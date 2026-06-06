import { useEffect, useState } from 'react'
import { ArrowLeft, ImageOff } from 'lucide-react'
import { buildStaticFileUrl, getCvDetails, updateCandidate } from '../api/cvApi.js'
import { formatDate, getStatusLabel } from '../utils/formatters.js'
import Alert from '../components/Alert.jsx'
import CandidateForm from '../components/CandidateForm.jsx'
import LoadingState from '../components/LoadingState.jsx'
import RawTextBox from '../components/RawTextBox.jsx'

export default function CvDetailsPage({ cvId, onBack }) {
  const [cv, setCv] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  async function loadDetails() {
    setIsLoading(true)
    setError('')

    try {
      const data = await getCvDetails(cvId)
      setCv(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  async function handleSaveCandidate(candidateData) {
    setIsSaving(true)
    setError('')
    setSuccess('')

    try {
      const updatedCandidate = await updateCandidate(cvId, candidateData)

      setCv((current) => ({
        ...current,
        candidate: updatedCandidate
      }))

      setSuccess('Dane kandydata zostały zaktualizowane.')
    } catch (err) {
      setError(err.message)
    } finally {
      setIsSaving(false)
    }
  }

  useEffect(() => {
    loadDetails()
  }, [cvId])

  if (isLoading) {
    return <LoadingState text="Pobieranie szczegółów CV..." />
  }

  if (!cv) {
    return (
      <main className="page">
        <button className="secondary-button" type="button" onClick={onBack}>
          <ArrowLeft size={18} /> Wróć
        </button>
        <Alert type="error">{error || 'Nie udało się pobrać szczegółów dokumentu.'}</Alert>
      </main>
    )
  }

  const photoUrl = buildStaticFileUrl(cv.candidate?.photo_path)

  return (
    <main className="page">
      <button className="secondary-button back-button" type="button" onClick={onBack}>
        <ArrowLeft size={18} /> Wróć do dashboardu
      </button>

      <section className="details-hero">
        <div>
          <p className="eyebrow">Szczegóły CV #{cv.id}</p>
          <h1>{cv.filename}</h1>
          <p>Przesłano: {formatDate(cv.upload_date)}</p>
        </div>

        <span className={`status-badge status-${cv.status || 'unknown'}`}>
          {getStatusLabel(cv.status)}
        </span>
      </section>

      <Alert type="error">{error}</Alert>
      <Alert type="success">{success}</Alert>

      <section className="details-grid">
        <article className="card candidate-card">
          <h2>Dane kandydata</h2>
          <p className="muted">Te pola można poprawić po automatycznej ekstrakcji OCR.</p>
          <CandidateForm candidate={cv.candidate} onSave={handleSaveCandidate} isSaving={isSaving} />
        </article>

        <article className="card photo-card">
          <h2>Zdjęcie kandydata</h2>
          {photoUrl ? (
            <img src={photoUrl} alt="Zdjęcie kandydata wykryte w CV" onError={(event) => { event.currentTarget.style.display = 'none' }} />
          ) : (
            <div className="photo-placeholder">
              <ImageOff size={42} />
              <p>Brak ścieżki zdjęcia.</p>
            </div>
          )}
          {cv.candidate?.photo_path && <p className="muted path-text">{cv.candidate.photo_path}</p>}
        </article>
      </section>

      <section className="card raw-text-section">
        <h2>Surowy tekst OCR</h2>
        <p className="muted">Tekst odczytany z obrazu dokumentu CV.</p>
        <RawTextBox text={cv.raw_text} />
      </section>
    </main>
  )
}