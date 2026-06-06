import { Inbox } from 'lucide-react'

export default function EmptyState({ title, text, actionLabel, onAction }) {
  return (
    <section className="empty-state">
      <Inbox size={44} />
      <h2>{title}</h2>
      <p>{text}</p>
      {actionLabel && onAction && (
        <button className="primary-button" type="button" onClick={onAction}>
          {actionLabel}
        </button>
      )}
    </section>
  )
}