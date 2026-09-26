import { useState, type FormEvent } from 'react'
import { ApiError, createComplaint, type Complaint } from '../api/client'

type Field = 'text' | 'location' | 'reporter_contact'
type FieldErrors = Partial<Record<Field, string>>

function validate(text: string, location: string, contact: string): FieldErrors {
  const errors: FieldErrors = {}
  if (text.trim().length < 10 || text.trim().length > 2000)
    errors.text = 'Complaint must be 10–2000 characters.'
  if (location.trim().length < 3 || location.trim().length > 200)
    errors.location = 'Location must be 3–200 characters.'
  if (contact.trim().length > 200)
    errors.reporter_contact = 'Contact must be at most 200 characters.'
  return errors
}

function serverFieldErrors(error: ApiError): FieldErrors {
  const fields: FieldErrors = {}
  for (const detail of error.body?.error.details ?? []) {
    const field = detail.field
    if (
      (field === 'text' || field === 'location' || field === 'reporter_contact') &&
      typeof detail.message === 'string'
    ) {
      fields[field] = detail.message
    }
  }
  return fields
}

export default function Submit() {
  const [text, setText] = useState('')
  const [location, setLocation] = useState('')
  const [contact, setContact] = useState('')
  const [errors, setErrors] = useState<FieldErrors>({})
  const [pending, setPending] = useState(false)
  const [failure, setFailure] = useState('')
  const [created, setCreated] = useState<Complaint | null>(null)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const nextErrors = validate(text, location, contact)
    setErrors(nextErrors)
    setCreated(null)
    setFailure('')
    if (Object.keys(nextErrors).length) return

    setPending(true)
    try {
      const complaint = await createComplaint({
        text: text.trim(),
        location: location.trim(),
        reporter_contact: contact.trim() || null,
      })
      setCreated(complaint)
    } catch (error) {
      if (error instanceof ApiError) {
        setErrors(serverFieldErrors(error))
        const retryAfter = error.retryAfter?.trim()
        setFailure(error.status === 429 && retryAfter && /^\d+$/.test(retryAfter)
          ? `${error.message} Retry after ${retryAfter} seconds.`
          : error.message)
      } else {
        setFailure('Could not reach the service. Please try again.')
      }
    } finally {
      setPending(false)
    }
  }

  return (
    <section aria-labelledby="submit-heading">
      <h2 id="submit-heading">Report a civic issue</h2>
      <p>Tell us what happened and where. Contact details are optional.</p>
      <form onSubmit={submit} noValidate>
        <label htmlFor="complaint-text">Complaint</label>
        <textarea id="complaint-text" value={text} onChange={(event) => setText(event.target.value)}
          aria-invalid={Boolean(errors.text)} aria-describedby={errors.text ? 'text-error' : undefined}
          maxLength={2001} rows={5} required />
        {errors.text && <p id="text-error" role="alert">{errors.text}</p>}

        <label htmlFor="complaint-location">Location</label>
        <input id="complaint-location" value={location}
          onChange={(event) => setLocation(event.target.value)}
          aria-invalid={Boolean(errors.location)}
          aria-describedby={errors.location ? 'location-error' : undefined}
          maxLength={201} required />
        {errors.location && <p id="location-error" role="alert">{errors.location}</p>}

        <label htmlFor="complaint-contact">Contact (optional)</label>
        <input id="complaint-contact" value={contact}
          onChange={(event) => setContact(event.target.value)}
          aria-invalid={Boolean(errors.reporter_contact)}
          aria-describedby={errors.reporter_contact ? 'contact-error' : undefined}
          maxLength={201} />
        {errors.reporter_contact && <p id="contact-error" role="alert">{errors.reporter_contact}</p>}

        <button type="submit" disabled={pending}>{pending ? 'Submitting…' : 'Submit complaint'}</button>
      </form>
      {pending && <p role="status">Submitting and classifying your complaint. This can take a few seconds.</p>}
      {failure && <p role="alert">{failure}</p>}
      {created && (
        <section aria-label="Triage result">
          <h3>Complaint submitted</h3>
          <p>Reference: {created.id}</p>
          <dl>
            <dt>Category</dt><dd>{created.category}</dd>
            <dt>Priority</dt><dd>{created.priority}</dd>
            <dt>AI summary</dt><dd>{created.ai_summary ?? 'No summary available'}</dd>
            <dt>Provider</dt><dd>{created.triaged_by}</dd>
          </dl>
        </section>
      )}
    </section>
  )
}
