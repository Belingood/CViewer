export function formatDate(dateValue) {
  if (!dateValue) {
    return 'Brak daty'
  }

  const date = new Date(dateValue)

  if (Number.isNaN(date.getTime())) {
    return dateValue
  }

  return new Intl.DateTimeFormat('pl-PL', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

export function getStatusLabel(status) {
  if (!status) {
    return 'Nieznany'
  }

  const labels = {
    processed: 'Przetworzono',
    pending: 'Oczekuje',
    processing: 'Przetwarzanie',
    failed: 'Błąd'
  }

  return labels[status] || status
}