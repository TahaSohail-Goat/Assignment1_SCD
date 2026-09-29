/**
 * Capability checks for the decorative animation layer. They never throw: a blocked or
 * missing browser API simply means the plain CSS presentation is used.
 */
export function prefersReducedMotion(): boolean {
  try {
    return window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches === true
  } catch {
    return false
  }
}

const softwareRenderer = /swiftshader|llvmpipe|softpipe|software|basic render/i

/** True when the renderer string names a CPU rasteriser, which would make the scene sluggish. */
export function isSoftwareRenderer(gl: WebGLRenderingContext | WebGL2RenderingContext): boolean {
  const info = gl.getExtension?.('WEBGL_debug_renderer_info')
  const renderer = info ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL) : gl.getParameter?.(gl.RENDERER)
  return typeof renderer === 'string' && softwareRenderer.test(renderer)
}

/** Hardware-accelerated WebGL only: software rendering falls back to the static presentation. */
export function supportsWebGL(): boolean {
  try {
    if (typeof window.WebGLRenderingContext === 'undefined') return false
    const canvas = document.createElement('canvas')
    const gl = (canvas.getContext('webgl2') ?? canvas.getContext('webgl')) as
      WebGLRenderingContext | WebGL2RenderingContext | null
    if (!gl) return false
    const software = isSoftwareRenderer(gl)
    gl.getExtension?.('WEBGL_lose_context')?.loseContext()
    return !software
  } catch {
    return false
  }
}

/** Rich mode: 3D scenes and counting numbers. Off without WebGL or when less motion is requested. */
export function canRender3D(): boolean {
  return !prefersReducedMotion() && supportsWebGL()
}
