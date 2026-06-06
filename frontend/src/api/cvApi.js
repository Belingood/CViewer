const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function handleResponse(response) {
  if (response.status === 204) {
    return null
  }

  const contentType = response.headers.get('content-type') || ''
  const isJson = contentType.includes('application/json')
  const data = isJson ? await response.json() : await response.text()

  if (!response.ok) {
    const message = typeof data === 'string'
      ? data
      : data?.detail || data?.message || 'Wystąpił błąd komunikacji z API.'

    throw new Error(message)
  }

  return data
}

export function getApiBaseUrl() {
  return API_BASE_URL
}

export function buildStaticFileUrl(path) {
  if (!path) {
    return ''
  }

  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }

  const normalizedPath = path.startsWith('/') ? path : `/${path}`

  return `${API_BASE_URL}${normalizedPath}`
}

export async function uploadCv(file) {
  const formData = new FormData()

  formData.append('file', file)

  const response = await fetch(`${API_BASE_URL}/api/v1/cv/upload/`, {
    method: 'POST',
    body: formData
  })

  return handleResponse(response)
}

export async function getCvList() {
  const response = await fetch(`${API_BASE_URL}/api/v1/cv/`)

  return handleResponse(response)
}

export async function getCvDetails(cvId) {
  const response = await fetch(`${API_BASE_URL}/api/v1/cv/${cvId}`)

  return handleResponse(response)
}

export async function updateCandidate(cvId, candidateData) {
  const response = await fetch(`${API_BASE_URL}/api/v1/cv/${cvId}/candidate`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(candidateData)
  })

  return handleResponse(response)
}

export async function deleteCv(cvId) {
  const response = await fetch(`${API_BASE_URL}/api/v1/cv/${cvId}`, {
    method: 'DELETE'
  })

  return handleResponse(response)
}