import { useState, type FormEvent } from 'react'
import { motion, type Variants } from 'motion/react'
import { ApiError, createComplaint, type Complaint } from '../api/client'
import { emitPulse } from '../components/three/pulse'

const stagger: Variants = { show: { transition: { staggerChildren: 0.07, delayChildren: 0.1 } } }
const rise: Variants = {
  hidden: { opacity: 0, y: 14 },
  show: { opacity: 1, y: 0, transition: { duration: 0.45, ease: [0.16, 1, 0.3, 1] } },
}
const steps = [
  { title: 'Read', body: 'Your words are read as written. No dropdown to get wrong.' },
  { title: 'Triage', body: 'A category, a priority and a short summary are assigned.' },
  { title: 'Route', body: 'Operators see urgent issues first on the dashboard.' },
]

type Field = 'text' | 'location' | 'reporter_contact'
type FieldErrors = Partial<Record<Field, string>>

function validate(text: string, location: string, contact: string): FieldErrors {
  const errors: FieldErrors = {}
  // Python/Pydantic measures Unicode code points, not JavaScript UTF-16 units.
  const textLength = [...text.trim()].length
  const locationLength = [...location.trim()].length
  if (textLength < 10 || textLength > 2000)
    errors.text = 'Complaint must be 10–2000 characters.'
  if (locationLength < 3 || locationLength > 200)
    errors.location = 'Location must be 3–200 characters.'
  if ([...contact.trim()].length > 200)
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
      emitPulse(complaint.priority)
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

  const textLength = [...text.trim()].length
  return (
    <section aria-labelledby="submit-heading" className="panel submit-panel">
      <div className="submit-layout">
        <div>
          <h2 id="submit-heading">Report a civic issue</h2>
          <p className="lead">Tell us what happened and where. Contact details are optional.</p>
          <motion.form onSubmit={submit} noValidate variants={stagger} initial="hidden" animate="show">
            <motion.div className="field" variants={rise}>
              <div className="field-head">
                <label htmlFor="complaint-text">Complaint</label>
                <span className="counter" aria-hidden="true">{textLength}/2000</span>
              </div>
              <textarea id="complaint-text" value={text} onChange={(event) => setText(event.target.value)}
                aria-invalid={Boolean(errors.text)} aria-describedby={errors.text ? 'text-error' : undefined}
                placeholder="e.g. Burst water main flooding Street 12 since fajr, water entering ground floors"
                rows={5} required />
              {errors.text && <p id="text-error" role="alert" className="field-error">{errors.text}</p>}
            </motion.div>

            <motion.div className="field-row" variants={rise}>
              <div className="field">
                <label htmlFor="complaint-location">Location</label>
                <input id="complaint-location" value={location}
                  onChange={(event) => setLocation(event.target.value)}
                  aria-invalid={Boolean(errors.location)}
                  aria-describedby={errors.location ? 'location-error' : undefined}
                  placeholder="Street, ward or landmark"
                  required />
                {errors.location && <p id="location-error" role="alert" className="field-error">{errors.location}</p>}
              </div>

              <div className="field">
                <label htmlFor="complaint-contact">Contact (optional)</label>
                <input id="complaint-contact" value={contact}
                  onChange={(event) => setContact(event.target.value)}
                  aria-invalid={Boolean(errors.reporter_contact)}
                  aria-describedby={errors.reporter_contact ? 'contact-error' : undefined}
                  placeholder="Phone or email" />
                {errors.reporter_contact && <p id="contact-error" role="alert" className="field-error">{errors.reporter_contact}</p>}
              </div>
            </motion.div>

            <motion.div variants={rise}>
              <motion.button type="submit" className="primary" disabled={pending}
                whileHover={pending ? undefined : { y: -2, scale: 1.02 }} whileTap={{ scale: 0.97 }}>
                {pending && <span className="spinner" aria-hidden="true" />}
                {pending ? 'Submitting…' : 'Submit complaint'}
              </motion.button>
            </motion.div>
          </motion.form>

          {pending && (
            <motion.div className="classifying" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
              <div className="scan" aria-hidden="true"><span /></div>
              <p role="status">Submitting and classifying your complaint. This can take a few seconds.</p>
            </motion.div>
          )}
          {failure && (
            <motion.p role="alert" className="banner-error" initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: [0, -6, 6, -3, 0] }} transition={{ duration: 0.4 }}>
              {failure}
            </motion.p>
          )}
        </div>

        <motion.aside className="how-it-works" aria-label="How triage works"
          initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.25, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
          <h3>How it works</h3>
          <ol>
            {steps.map((step, index) => (
              <motion.li key={step.title} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 + index * 0.12 }}>
                <span className="step-number" aria-hidden="true">{index + 1}</span>
                <div><strong>{step.title}</strong><p>{step.body}</p></div>
              </motion.li>
            ))}
          </ol>
        </motion.aside>
      </div>

      {created && (
        <motion.section aria-label="Triage result" className={`result priority-${created.priority}`}
          initial={{ opacity: 0, y: 24, scale: 0.97 }} animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ type: 'spring', stiffness: 220, damping: 22 }}>
          <div className="result-head">
            <motion.span className="result-check" aria-hidden="true" initial={{ scale: 0 }}
              animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 400, damping: 14, delay: 0.15 }}>✓</motion.span>
            <div>
              <h3>Complaint submitted</h3>
              <p className="reference">Reference: {created.id}</p>
            </div>
          </div>
          <dl>
            <dt>Category</dt><dd><span className={`badge cat-${created.category}`}>{created.category}</span></dd>
            <dt>Priority</dt><dd><span className={`badge prio-${created.priority}`}>{created.priority}</span></dd>
            <dt>AI summary</dt><dd>{created.ai_summary ?? 'No summary available'}</dd>
            <dt>Provider</dt><dd><span className="chip">{created.triaged_by}</span></dd>
          </dl>
        </motion.section>
      )}
    </section>
  )
}
