import { useEffect, useMemo, useRef, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { AdaptiveDpr, Grid, Sparkles } from '@react-three/drei'
import * as THREE from 'three'
import type { Priority } from '../../api/client'
import { priorityColor, scenePalette, type Theme } from '../../theme'
import { onPulse } from './pulse'

const BLOCKS = 13
const SPACING = 1.7
const MAX_PULSES = 10
const HALF = (BLOCKS - 1) / 2

type Building = { x: number; z: number; h: number; w: number; phase: number }
type Pulse = { x: number; z: number; born: number; life: number; speed: number; strength: number; color: THREE.Color }

/** A stable, seeded skyline: taller towers near the centre, parks scattered between. */
function makeSkyline(): Building[] {
  let seed = 11
  const random = () => {
    seed = (seed * 16807) % 2147483647
    return (seed - 1) / 2147483646
  }
  const buildings: Building[] = []
  const radius = HALF * SPACING
  for (let i = 0; i < BLOCKS; i++) {
    for (let j = 0; j < BLOCKS; j++) {
      const bx = (i - HALF) * SPACING
      const bz = (j - HALF) * SPACING
      const centre = Math.max(0, 1 - Math.hypot(bx, bz) / (radius * 1.05))
      for (const [ox, oz] of [[-0.36, -0.36], [0.36, -0.36], [-0.36, 0.36], [0.36, 0.36]]) {
        if (random() < 0.2) continue
        buildings.push({
          x: bx + ox,
          z: bz + oz,
          h: 0.2 + random() * (0.5 + centre * centre * 4.2),
          w: 0.5 + random() * 0.14,
          phase: random() * Math.PI * 2,
        })
      }
    }
  }
  return buildings
}

/** Street crossings lie half a block away from block centres. */
function randomCrossing(): [number, number] {
  const pick = () => (Math.floor(Math.random() * BLOCKS) - HALF + 0.5) * SPACING
  return [pick(), pick()]
}

function City({ theme }: { theme: Theme }) {
  const buildings = useMemo(makeSkyline, [])
  const mesh = useRef<THREE.InstancedMesh>(null)
  const rings = useRef<(THREE.Mesh | null)[]>([])
  const pulses = useRef<Pulse[]>([])
  const pending = useRef<Priority[]>([])
  const nextAmbient = useRef(0.4)
  const palette = scenePalette[theme]
  const colors = useMemo(() => ({
    base: new THREE.Color(palette.building),
    top: new THREE.Color(palette.buildingTop),
    glow: new THREE.Color(palette.glow),
  }), [palette])
  const dummy = useMemo(() => new THREE.Object3D(), [])
  const tint = useMemo(() => new THREE.Color(), [])

  useEffect(() => onPulse((priority) => { pending.current.push(priority) }), [])

  useFrame((state) => {
    const t = state.clock.elapsedTime
    const live = pulses.current
    if (t > nextAmbient.current) {
      const [x, z] = randomCrossing()
      live.push({ x, z, born: t, life: 3.2, speed: 2.4, strength: 0.75, color: colors.glow })
      nextAmbient.current = t + 0.9 + Math.random() * 1.4
    }
    for (const priority of pending.current.splice(0)) {
      const big = priority === 'high' ? 1.6 : 1.2
      live.push({ x: 0, z: 0, born: t, life: 5, speed: 4.2, strength: big,
        color: new THREE.Color(priorityColor[priority]) })
    }
    pulses.current = live.filter((pulse) => t - pulse.born < pulse.life).slice(-MAX_PULSES)

    const city = mesh.current
    if (city) {
      buildings.forEach((b, index) => {
        let glow = 0.06 * (0.5 + 0.5 * Math.sin(t * 0.7 + b.phase))
        let glowColor = colors.glow
        for (const p of pulses.current) {
          const age = t - p.born
          const front = age * p.speed
          const distance = Math.hypot(b.x - p.x, b.z - p.z)
          const band = Math.exp(-((distance - front) ** 2) / 0.45)
          const value = band * (1 - age / p.life) * p.strength
          if (value > glow) {
            glow = value
            glowColor = p.color
          }
        }
        const height = b.h * (1 + 0.28 * glow)
        dummy.position.set(b.x, height / 2, b.z)
        dummy.scale.set(b.w, height, b.w)
        dummy.updateMatrix()
        city.setMatrixAt(index, dummy.matrix)
        tint.copy(colors.base).lerp(colors.top, Math.min(1, b.h / 4))
          .lerp(glowColor, Math.min(1, glow)).multiplyScalar(1 + glow * 0.9)
        city.setColorAt(index, tint)
      })
      city.instanceMatrix.needsUpdate = true
      if (city.instanceColor) city.instanceColor.needsUpdate = true
    }

    rings.current.forEach((ring, index) => {
      if (!ring) return
      const p = pulses.current[index]
      ring.visible = Boolean(p)
      if (!p) return
      const age = t - p.born
      const radius = Math.max(0.01, age * p.speed)
      ring.position.set(p.x, 0.03, p.z)
      ring.scale.set(radius, radius, radius)
      const material = ring.material as THREE.MeshBasicMaterial
      material.color.copy(p.color)
      material.opacity = Math.max(0, (1 - age / p.life) * 0.7 * Math.min(1, p.strength))
    })
  })

  return (
    <>
      <instancedMesh ref={mesh} args={[undefined, undefined, buildings.length]}>
        <boxGeometry />
        <meshStandardMaterial roughness={0.5} metalness={0.15} toneMapped={false} />
      </instancedMesh>
      {Array.from({ length: MAX_PULSES }, (_, index) => (
        <mesh key={index} ref={(node) => { rings.current[index] = node }}
          rotation={[-Math.PI / 2, 0, 0]} visible={false}>
          <ringGeometry args={[0.94, 1, 96]} />
          <meshBasicMaterial transparent depthWrite={false} blending={THREE.AdditiveBlending}
            toneMapped={false} side={THREE.DoubleSide} />
        </mesh>
      ))}
    </>
  )
}

/** Slow orbit that leans gently toward the pointer. */
function CameraRig() {
  const pointer = useRef({ x: 0, y: 0 })
  const target = useMemo(() => new THREE.Vector3(), [])
  useEffect(() => {
    const move = (event: PointerEvent) => {
      pointer.current.x = (event.clientX / window.innerWidth) * 2 - 1
      pointer.current.y = (event.clientY / window.innerHeight) * 2 - 1
    }
    window.addEventListener('pointermove', move, { passive: true })
    return () => window.removeEventListener('pointermove', move)
  }, [])
  useFrame((state, delta) => {
    const angle = state.clock.elapsedTime * 0.035 + Math.PI / 4
    target.set(
      Math.cos(angle) * 21 + pointer.current.x * 2,
      17 - pointer.current.y * 1.5,
      Math.sin(angle) * 21,
    )
    state.camera.position.lerp(target, 1 - Math.exp(-delta * 1.5))
    state.camera.lookAt(0, -1.5, 0)
  })
  return null
}

export default function CityScene({ theme }: { theme: Theme }) {
  const [visible, setVisible] = useState(() => document.visibilityState !== 'hidden')
  useEffect(() => {
    const update = () => setVisible(document.visibilityState !== 'hidden')
    document.addEventListener('visibilitychange', update)
    return () => document.removeEventListener('visibilitychange', update)
  }, [])
  const palette = scenePalette[theme]
  return (
    <Canvas className="city-canvas" dpr={[1, 1.5]} frameloop={visible ? 'always' : 'never'}
      camera={{ position: [15, 17, 15], fov: 36, near: 0.1, far: 140 }}
      gl={{ antialias: true, alpha: true, powerPreference: 'low-power' }}>
      <fog attach="fog" args={[palette.fog, 24, 62]} />
      <ambientLight intensity={palette.ambient} />
      <hemisphereLight args={[palette.sky, palette.ground, 0.35]} />
      <directionalLight position={[10, 16, 6]} intensity={palette.sun} />
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.01, 0]}>
        <circleGeometry args={[120, 64]} />
        <meshStandardMaterial color={palette.ground} roughness={1} />
      </mesh>
      <Grid position={[0, 0.005, 0]} args={[60, 60]} cellSize={SPACING / 2} sectionSize={SPACING}
        cellColor={palette.grid} sectionColor={palette.grid} cellThickness={0.4} sectionThickness={0.9}
        fadeDistance={48} fadeStrength={1.4} infiniteGrid />
      <City theme={theme} />
      <Sparkles count={70} scale={[26, 7, 26]} position={[0, 3.5, 0]} size={2.2} speed={0.25}
        opacity={theme === 'dark' ? 0.8 : 0.45} color={palette.sparkle} />
      <CameraRig />
      <AdaptiveDpr pixelated={false} />
    </Canvas>
  )
}
