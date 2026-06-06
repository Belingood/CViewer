export default function RawTextBox({ text }) {
  return (
    <div className="raw-text-box">
      {text ? <pre>{text}</pre> : <p className="muted">Brak surowego tekstu OCR.</p>}
    </div>
  )
}