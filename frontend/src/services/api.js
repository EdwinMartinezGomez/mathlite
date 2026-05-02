/**
 * Servicio API — Comunicación con el backend MathLite.
 */
import axios from 'axios'

const API = '/api'

/**
 * Ejecuta un programa MathLite en el backend.
 * @param {string} code - Código fuente MathLite
 * @returns {Promise<object>} Resultado con tokens, AST, símbolos, output y errores
 */
export async function runProgram(code) {
  const { data } = await axios.post(`${API}/run`, { code })
  return data
}

/**
 * Verifica que el backend esté activo.
 * @returns {Promise<object>} Estado del servicio
 */
export async function healthCheck() {
  const { data } = await axios.get(`${API}/health`)
  return data
}
