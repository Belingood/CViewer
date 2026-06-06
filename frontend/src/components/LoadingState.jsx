export default function LoadingState({ text = 'Ładowanie danych...' }) {
  return (
    <div className="loading-box" aria-live="polite">
      <div className="spinner" />
      <p>{text}</p>
    </div>
  )
}