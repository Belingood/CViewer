import { useRef, useState } from 'react'
import { UploadCloud } from 'lucide-react'

const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'webp']

function isAllowedFile(file) {
  const extension = file.name.split('.').pop()?.toLowerCase()

  return ALLOWED_EXTENSIONS.includes(extension)
}

export default function UploadBox({ onUpload, isUploading }) {
  const inputRef = useRef(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [localError, setLocalError] = useState('')

  function handleFileChange(event) {
    const file = event.target.files?.[0]

    setLocalError('')

    if (!file) {
      setSelectedFile(null)
      return
    }

    if (!isAllowedFile(file)) {
      setSelectedFile(null)
      setLocalError('API aktualnie przyjmuje tylko pliki JPG, JPEG, PNG i WEBP. PDF nie jest jeszcze obsługiwany przez backend.')
      event.target.value = ''
      return
    }

    setSelectedFile(file)
  }

  function handleSubmit(event) {
    event.preventDefault()

    if (!selectedFile) {
      setLocalError('Najpierw wybierz obraz CV.')
      return
    }

    onUpload(selectedFile)
  }

  return (
    <form className="upload-box" onSubmit={handleSubmit}>
      <div className="upload-dropzone" onClick={() => inputRef.current?.click()}>
        <UploadCloud size={46} />
        <h2>Prześlij obraz CV do analizy OCR</h2>
        <p>Obsługiwane formaty: JPG, JPEG, PNG, WEBP.</p>
        <input
          ref={inputRef}
          type="file"
          accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp"
          onChange={handleFileChange}
          hidden
        />
      </div>

      {selectedFile && (
        <div className="selected-file">
          <strong>Wybrany plik:</strong> {selectedFile.name}
        </div>
      )}

      {localError && <div className="form-error">{localError}</div>}

      <button className="primary-button" type="submit" disabled={isUploading}>
        {isUploading ? 'Analizowanie dokumentu...' : 'Prześlij i analizuj'}
      </button>
    </form>
  )
}
