import { useEffect, useState } from 'react'

const EMPTY_FORM = {
  first_name: '',
  last_name: '',
  email: '',
  phone: ''
}

export default function CandidateForm({ candidate, onSave, isSaving }) {
  const [formData, setFormData] = useState(EMPTY_FORM)

  useEffect(() => {
    setFormData({
      first_name: candidate?.first_name || '',
      last_name: candidate?.last_name || '',
      email: candidate?.email || '',
      phone: candidate?.phone || ''
    })
  }, [candidate])

  function handleChange(event) {
    const { name, value } = event.target

    setFormData((current) => ({
      ...current,
      [name]: value
    }))
  }

  function handleSubmit(event) {
    event.preventDefault()

    onSave(formData)
  }

  return (
    <form className="candidate-form" onSubmit={handleSubmit}>
      <div className="form-grid">
        <label>
          Imię
          <input name="first_name" value={formData.first_name} onChange={handleChange} placeholder="np. Jan" />
        </label>

        <label>
          Nazwisko
          <input name="last_name" value={formData.last_name} onChange={handleChange} placeholder="np. Kowalski" />
        </label>

        <label>
          E-mail
          <input name="email" type="email" value={formData.email} onChange={handleChange} placeholder="np. jan@example.com" />
        </label>

        <label>
          Telefon
          <input name="phone" value={formData.phone} onChange={handleChange} placeholder="np. +48 123 456 789" />
        </label>
      </div>

      <button className="primary-button" type="submit" disabled={isSaving}>
        {isSaving ? 'Zapisywanie...' : 'Zapisz korektę OCR'}
      </button>
    </form>
  )
}