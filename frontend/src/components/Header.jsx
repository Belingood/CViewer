import { FileSearch } from 'lucide-react'

export default function Header({ currentPage, onNavigate }) {
  return (
    <header className="app-header">
      <button className="brand" type="button" onClick={() => onNavigate('dashboard')}>
        <span className="brand-icon"><FileSearch size={26} /></span>
        <span>
          <strong>CViewer</strong>
          <small>OCR i analiza dokumentów CV</small>
        </span>
      </button>

      <nav className="main-nav" aria-label="Główna nawigacja">
        <button
          className={currentPage === 'dashboard' ? 'active' : ''}
          type="button"
          onClick={() => onNavigate('dashboard')}
        >
          Dashboard
        </button>

        <button
          className={currentPage === 'upload' ? 'active' : ''}
          type="button"
          onClick={() => onNavigate('upload')}
        >
          Dodaj CV
        </button>
      </nav>
    </header>
  )
}