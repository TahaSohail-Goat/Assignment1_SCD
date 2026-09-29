import { useLayoutEffect, useRef, useState } from 'react'
import { Canvas, useFrame, useThree } from '@react-three/fiber'
import { ContactShadows, Html, RoundedBox } from '@react-three/drei'
import * as THREE from 'three'
import type { Theme } from '../../theme'

export type ChartDatum = { name: string; value: number; color: string }

const BAR_GAP = 1.6
const MAX_HEIGHT = 3.6

function Bar({ datum, index, x, max }: { datum: ChartDatum; index: number; x: number; max: number }) {
  const bar = useRef<THREE.Group>(null)
  const born = useRef<number | null>(null)
  const [hovered, setHovered] = useState(false)
  const height = Math.max(0.06, (datum.value / max) * MAX_HEIGHT)

  useFrame((state, delta) => {
    const group = bar.current
    if (!group) return
    born.current ??= state.clock.elapsedTime
    const started = state.clock.elapsedTime - born.current > index * 0.09
    const goal = started ? height : 0.001
    group.scale.y = THREE.MathUtils.damp(group.scale.y, goal, 4.5, delta)
    group.position.y = THREE.MathUtils.damp(group.position.y, hovered ? 0.18 : 0, 8, delta)
  })

  return (
    <group position={[x, 0, 0]}>
      <group ref={bar} scale={[1, 0.001, 1]}>
        <RoundedBox args={[0.82, 1, 0.82]} radius={0.08} smoothness={3} position={[0, 0.5, 0]}
          onPointerOver={(event) => { event.stopPropagation(); setHovered(true) }}
          onPointerOut={() => setHovered(false)}>
          <meshStandardMaterial color={datum.color} emissive={datum.color}
            emissiveIntensity={hovered ? 0.6 : 0.16} roughness={0.32} metalness={0.2} />
        </RoundedBox>
      </group>
      <Html position={[0, height + 0.42, 0]} center className="bar-value"
        style={{ animationDelay: `${0.35 + index * 0.09}s` }}>
        {datum.value}
      </Html>
      <Html position={[0, -0.02, 0.78]} center className="bar-name">
        {datum.name.charAt(0).toUpperCase() + datum.name.slice(1)}
      </Html>
    </group>
  )
}

function Bars({ data }: { data: ChartDatum[] }) {
  const group = useRef<THREE.Group>(null)
  const max = Math.max(1, ...data.map((datum) => datum.value))
  const offset = ((data.length - 1) * BAR_GAP) / 2
  useFrame((state, delta) => {
    if (!group.current) return
    const sway = Math.sin(state.clock.elapsedTime * 0.35) * 0.06 + state.pointer.x * 0.1
    group.current.rotation.y = THREE.MathUtils.damp(group.current.rotation.y, sway, 3, delta)
  })
  return (
    <group ref={group}>
      {data.map((datum, index) => (
        <Bar key={datum.name} datum={datum} index={index} x={index * BAR_GAP - offset} max={max} />
      ))}
    </group>
  )
}

/** Keeps the whole chart in view: wide cards show it large, narrow phones pull the camera back. */
function FitCamera({ span }: { span: number }) {
  const camera = useThree((state) => state.camera) as THREE.PerspectiveCamera
  const aspect = useThree((state) => state.size.width / Math.max(1, state.size.height))
  useLayoutEffect(() => {
    const visible = 2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2))
    const fitWidth = (span + 1.6) / (visible * aspect)
    const fitHeight = (MAX_HEIGHT + 2) / visible
    const distance = Math.max(fitWidth, fitHeight)
    camera.position.set(0, distance * 0.36 + 0.6, distance)
    camera.lookAt(0, 1.55, 0)
    camera.updateProjectionMatrix()
  }, [aspect, camera, span])
  return null
}

/** Decorative 3D bar chart. The accessible numbers are rendered separately as a list. */
export default function StatsChart3D({ data, theme }: { data: ChartDatum[]; theme: Theme }) {
  const span = Math.max(4, data.length * BAR_GAP)
  return (
    <Canvas className="chart-canvas" dpr={[1, 1.75]}
      camera={{ position: [0, 3.4, 9], fov: 34, near: 0.1, far: 80 }}
      gl={{ antialias: true, alpha: true }}>
      <FitCamera span={span} />
      <ambientLight intensity={theme === 'dark' ? 0.55 : 0.85} />
      <directionalLight position={[4, 8, 6]} intensity={1.2} />
      <pointLight position={[-5, 4, 3]} intensity={theme === 'dark' ? 18 : 10} color="#7de3d6" />
      <Bars data={data} />
      <ContactShadows position={[0, 0, 0]} scale={span + 4} blur={2.4} far={4.5}
        opacity={theme === 'dark' ? 0.6 : 0.35} />
    </Canvas>
  )
}
