import { useEffect, useState } from 'react'
import { animate, motion, useMotionValue, useTransform } from 'motion/react'
import { canRender3D } from './three/capabilities'

/** A number that counts up in rich mode and is shown as-is everywhere else. */
export default function CountUp({ value }: { value: number }) {
  const [rich] = useState(canRender3D)
  const current = useMotionValue(rich ? 0 : value)
  const text = useTransform(current, (latest) => String(Math.round(latest)))
  useEffect(() => {
    if (!rich) {
      current.set(value)
      return
    }
    const controls = animate(current, value, { duration: 1.2, ease: [0.16, 1, 0.3, 1] })
    return () => controls.stop()
  }, [current, rich, value])
  return <motion.span>{text}</motion.span>
}
