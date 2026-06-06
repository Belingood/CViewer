import { useEffect, useState } from 'react'
import { deleteCv, getCvList } from '../api/cvApi.js'
import Alert from '../components/Alert.jsx'
import CvTable from '../components/CvTable.jsx'
import EmptyState from '../components/EmptyState.jsx'
import LoadingState from '../components/LoadingState.jsx'

export default function DashboardPage({ onNavigateToUpload, onOpenDetails }) {
  const [items, setItems] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  async function loadItems() {
    setIsLoading(true)
    setError('')

    try {
      const data = await getCvList()
      setItems(Array.isArray(data) ? data : [])
    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  async function handleDelete(cvId) {
    const confirmed = window.confirm('Czy na pewno usunąć ten dokument CV? Tej operacji nie da się cofnąć.')

    if (!confirmed) {
      return
    }

    setError('')
    setSuccess('')

    try {
      await deleteCv(cvId)
      setItems((current) => current.filter((item) => item.id !== cvId))
      setSuccess('Dokument CV został usunięty.')
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => {
    loadItems()
  }, [])

  if (isLoading) {
    return <LoadingState text="Pobieranie listy CV..." />
  }

  return (
    <main className="page">
      <section className="page-heading">
        <div>
          <p className="eyebrow">Dashboard</p>
          <h1>Przetworzone dokumenty CV</h1>
          <p>Lista dokumentów pobrana z endpointu GET /api/v1/cv/.</p>
        </div>

        <button className="primary-button" type="button" onClick={onNavigateToUpload}>
          Dodaj nowe CV
        </button>
      </section>

      <Alert type="error">{error}</Alert>
      <Alert type="success">{success}</Alert>

      {items.length === 0 ? (
        <EmptyState
          title="Brak dokumentów CV"
          text="Dodaj pierwszy obraz CV, aby rozpocząć ekstrakcję informacji przez OCR."
          actionLabel="Przejdź do uploadu"
          onAction={onNavigateToUpload}
        />
      ) : (
        <CvTable items={items} onOpenDetails={onOpenDetails} onDelete={handleDelete} />
      )}
    </main>
  )
}