import { useState } from 'react'
import Header from './components/Header.jsx'
import DashboardPage from './pages/DashboardPage.jsx'
import UploadPage from './pages/UploadPage.jsx'
import CvDetailsPage from './pages/CvDetailsPage.jsx'
import { getApiBaseUrl } from './api/cvApi.js'

export default function App() {
  const [page, setPage] = useState('dashboard')
  const [selectedCvId, setSelectedCvId] = useState(null)

  function navigate(nextPage) {
    setPage(nextPage)

    if (nextPage !== 'details') {
      setSelectedCvId(null)
    }
  }

  function openDetails(cvId) {
    setSelectedCvId(cvId)
    setPage('details')
  }

  function handleUploaded(cvId) {
    if (cvId) {
      openDetails(cvId)
      return
    }

    navigate('dashboard')
  }

  return (
    <div className="app-shell">
      <Header currentPage={page} onNavigate={navigate} />

      <div className="api-strip">
        Backend API: <code>{getApiBaseUrl()}</code>
      </div>

      {page === 'dashboard' && (
        <DashboardPage onNavigateToUpload={() => navigate('upload')} onOpenDetails={openDetails} />
      )}

      {page === 'upload' && <UploadPage onUploaded={handleUploaded} />}

      {page === 'details' && selectedCvId && (
        <CvDetailsPage cvId={selectedCvId} onBack={() => navigate('dashboard')} />
      )}
    </div>
  )
}