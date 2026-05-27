<template>
  <section class="details-page">
    <router-link class="back-link" to="/">← Назад к списку</router-link>

    <header class="details-header">
      <h1>{{ ip }}</h1>
      <span :class="['status', connected ? 'online' : 'offline']">
        {{ connected ? 'WS connected' : 'WS disconnected' }}
      </span>
    </header>

    <div class="actions">
      <button :disabled="!connected" @click="sendCommand('start')">Start</button>
      <button :disabled="!connected" @click="sendCommand('stop')">Stop</button>
      <button :disabled="!connected" @click="sendCommand('restart')">Restart</button>
    </div>

    <p v-if="lastError" class="error">{{ lastError }}</p>

    <section class="cfg-editor">
      <div class="cfg-header">
        <h2>JSON конфиги</h2>
        <div class="cfg-actions">
          <button :disabled="!connected || cfgLoading" @click="loadCfgFiles">Обновить список</button>
          <button :disabled="!connected || !selectedCfgFile || cfgLoading" @click="loadSelectedFile">
            Открыть
          </button>
          <button :disabled="!connected || !selectedCfgFile || cfgLoading" @click="saveSelectedFile">
            Сохранить
          </button>
        </div>
      </div>

      <div class="cfg-picker">
        <label for="cfg-file">Файл</label>
        <select id="cfg-file" v-model="selectedCfgFile" :disabled="!connected || cfgLoading || !cfgFiles.length">
          <option disabled value="">Выберите JSON файл</option>
          <option v-for="file in cfgFiles" :key="file" :value="file">{{ file }}</option>
        </select>
      </div>

      <div class="cfg-picker">
        <label for="cfg-encoding">Кодировка</label>
        <select id="cfg-encoding" v-model="selectedEncoding" :disabled="!connected || !selectedCfgFile">
          <option value="utf-8">utf-8</option>
          <option value="utf-16le">utf-16le</option>
          <option value="utf-16be">utf-16be</option>
        </select>
      </div>

      <p v-if="cfgMessage" class="cfg-message">{{ cfgMessage }}</p>
      <textarea
        v-model="cfgContent"
        :disabled="!connected || !selectedCfgFile"
        class="cfg-textarea"
        spellcheck="false"
      />
    </section>

    <section class="logs">
      <h2>Логи сервера</h2>
      <pre>{{ logText }}</pre>
    </section>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const wsPort = import.meta.env.VITE_SERVER_WS_PORT ?? '8765'

const ip = computed(() => String(route.params.ip ?? 'unknown'))
const wsUrl = computed(() => `ws://${ip.value}:${wsPort}`)

const connected = ref(false)
const lastError = ref('')
const logs = ref<string[]>([])
const cfgFiles = ref<string[]>([])
const selectedCfgFile = ref('')
const cfgContent = ref('')
const cfgLoading = ref(false)
const cfgMessage = ref('')
const selectedEncoding = ref<'utf-8' | 'utf-16le' | 'utf-16be'>('utf-8')
const keepBom = ref(false)

let socket: WebSocket | null = null
let rpcCounter = 0

const logText = computed(() => logs.value.join('\n'))

function pushLog(message: string) {
  const now = new Date().toLocaleTimeString()
  logs.value = [...logs.value.slice(-250), `[${now}] ${message}`]
}

function connect() {
  if (!ip.value || ip.value === 'unknown') {
    lastError.value = 'Не найден IP сервера'
    return
  }

  lastError.value = ''
  pushLog(`Connecting to ${wsUrl.value}`)
  socket = new WebSocket(wsUrl.value)

  socket.onopen = () => {
    connected.value = true
    pushLog('WebSocket connected')
    loadCfgFiles()
  }

  socket.onclose = () => {
    connected.value = false
    pushLog('WebSocket disconnected')
  }

  socket.onerror = () => {
    lastError.value = 'Ошибка подключения к WebSocket'
    pushLog('WebSocket error')
  }

  socket.onmessage = (event: MessageEvent) => {
    const data = String(event.data)
    if (handleWsJsonMessage(data)) {
      return
    }
    pushLog(data)
  }
}

function sendRpc(action: string, extra: Record<string, unknown> = {}) {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    throw new Error('WebSocket не подключен')
  }
  rpcCounter += 1
  socket.send(
    JSON.stringify({
      request_id: `req-${Date.now()}-${rpcCounter}`,
      action,
      ...extra,
    }),
  )
}

function handleWsJsonMessage(raw: string): boolean {
  try {
    const payload = JSON.parse(raw) as {
      type?: string
      ok?: boolean
      files?: string[]
      filename?: string
      content_base64?: string
      error?: string
      message?: string
    }
    if (!payload || typeof payload !== 'object' || !payload.type) {
      return false
    }

    if (payload.type === 'cfg_list') {
      if (!payload.ok) {
        cfgMessage.value = payload.error ?? 'Ошибка загрузки списка файлов'
        return true
      }
      cfgFiles.value = Array.isArray(payload.files) ? payload.files : []
      if (!cfgFiles.value.includes(selectedCfgFile.value)) {
        selectedCfgFile.value = cfgFiles.value[0] ?? ''
      }
      cfgMessage.value = `Найдено файлов: ${cfgFiles.value.length}`
      return true
    }

    if (payload.type === 'cfg_read') {
      if (!payload.ok) {
        cfgMessage.value = payload.error ?? 'Ошибка чтения файла'
        return true
      }
      const rawBytes = base64ToBytes(payload.content_base64 ?? '')
      const sniffed = sniffEncoding(rawBytes)
      selectedEncoding.value = sniffed.encoding
      keepBom.value = sniffed.hasBom
      cfgContent.value = decodeBytes(rawBytes, sniffed.encoding)
      cfgMessage.value = `Файл ${payload.filename ?? ''} загружен`
      return true
    }

    if (payload.type === 'cfg_write') {
      cfgMessage.value = payload.ok ? payload.message ?? 'Сохранено' : payload.error ?? 'Ошибка сохранения файла'
      return true
    }
    return false
  } catch {
    return false
  }
}

function loadCfgFiles() {
  cfgLoading.value = true
  cfgMessage.value = ''
  try {
    sendRpc('cfg_list')
  } catch (err) {
    cfgMessage.value = (err as Error).message
  } finally {
    cfgLoading.value = false
  }
}

function loadSelectedFile() {
  if (!selectedCfgFile.value) {
    cfgMessage.value = 'Сначала выберите файл'
    return
  }
  cfgLoading.value = true
  cfgMessage.value = ''
  try {
    sendRpc('cfg_read', { filename: selectedCfgFile.value })
  } catch (err) {
    cfgMessage.value = (err as Error).message
  } finally {
    cfgLoading.value = false
  }
}

function saveSelectedFile() {
  if (!selectedCfgFile.value) {
    cfgMessage.value = 'Сначала выберите файл'
    return
  }
  cfgLoading.value = true
  cfgMessage.value = ''
  try {
    JSON.parse(cfgContent.value)
    const rawBytes = encodeText(cfgContent.value, selectedEncoding.value, keepBom.value)
    sendRpc('cfg_write', { filename: selectedCfgFile.value, content_base64: bytesToBase64(rawBytes) })
  } catch (err) {
    cfgMessage.value = `Некорректный JSON: ${(err as Error).message}`
  } finally {
    cfgLoading.value = false
  }
}

function bytesToBase64(bytes: Uint8Array): string {
  let binary = ''
  const chunkSize = 0x8000
  for (let i = 0; i < bytes.length; i += chunkSize) {
    const chunk = bytes.subarray(i, i + chunkSize)
    binary += String.fromCharCode(...chunk)
  }
  return btoa(binary)
}

function base64ToBytes(base64: string): Uint8Array {
  const binary = atob(base64)
  const bytes = new Uint8Array(binary.length)
  for (let i = 0; i < binary.length; i += 1) {
    bytes[i] = binary.charCodeAt(i)
  }
  return bytes
}

function sniffEncoding(bytes: Uint8Array): { encoding: 'utf-8' | 'utf-16le' | 'utf-16be'; hasBom: boolean } {
  if (bytes.length >= 2 && bytes[0] === 0xff && bytes[1] === 0xfe) {
    return { encoding: 'utf-16le', hasBom: true }
  }
  if (bytes.length >= 2 && bytes[0] === 0xfe && bytes[1] === 0xff) {
    return { encoding: 'utf-16be', hasBom: true }
  }
  if (bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
    return { encoding: 'utf-8', hasBom: true }
  }

  let evenZero = 0
  let oddZero = 0
  for (let i = 0; i < bytes.length; i += 1) {
    if (bytes[i] === 0) {
      if (i % 2 === 0) evenZero += 1
      else oddZero += 1
    }
  }
  if (oddZero > evenZero * 2) {
    return { encoding: 'utf-16le', hasBom: false }
  }
  if (evenZero > oddZero * 2) {
    return { encoding: 'utf-16be', hasBom: false }
  }
  return { encoding: 'utf-8', hasBom: false }
}

function decodeBytes(bytes: Uint8Array, encoding: 'utf-8' | 'utf-16le' | 'utf-16be'): string {
  if (encoding === 'utf-8') {
    const bomStripped =
      bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf ? bytes.subarray(3) : bytes
    return new TextDecoder('utf-8').decode(bomStripped)
  }
  if (encoding === 'utf-16le') {
    const bomStripped = bytes.length >= 2 && bytes[0] === 0xff && bytes[1] === 0xfe ? bytes.subarray(2) : bytes
    return new TextDecoder('utf-16le').decode(bomStripped)
  }
  const bomStripped = bytes.length >= 2 && bytes[0] === 0xfe && bytes[1] === 0xff ? bytes.subarray(2) : bytes
  return new TextDecoder('utf-16be').decode(bomStripped)
}

function encodeText(
  text: string,
  encoding: 'utf-8' | 'utf-16le' | 'utf-16be',
  withBom: boolean,
): Uint8Array {
  if (encoding === 'utf-8') {
    const utf8 = new TextEncoder().encode(text)
    if (!withBom) return utf8
    const out = new Uint8Array(utf8.length + 3)
    out.set([0xef, 0xbb, 0xbf], 0)
    out.set(utf8, 3)
    return out
  }

  const bomLength = withBom ? 2 : 0
  const out = new Uint8Array(bomLength + text.length * 2)
  if (withBom) {
    if (encoding === 'utf-16le') {
      out[0] = 0xff
      out[1] = 0xfe
    } else {
      out[0] = 0xfe
      out[1] = 0xff
    }
  }
  let offset = bomLength
  for (let i = 0; i < text.length; i += 1) {
    const code = text.charCodeAt(i)
    const low = code & 0xff
    const high = (code >> 8) & 0xff
    if (encoding === 'utf-16le') {
      out[offset] = low
      out[offset + 1] = high
    } else {
      out[offset] = high
      out[offset + 1] = low
    }
    offset += 2
  }
  return out
}

function sendCommand(command: 'start' | 'stop' | 'restart') {
  if (!socket || socket.readyState !== WebSocket.OPEN) {
    lastError.value = 'WebSocket не подключен'
    return
  }

  socket.send(command)
  pushLog(`Command sent: ${command}`)
}

onMounted(() => {
  connect()
})

onUnmounted(() => {
  if (socket) {
    socket.close()
    socket = null
  }
})
</script>

<style scoped>
.details-page {
  display: grid;
  gap: 14px;
}

.back-link {
  width: fit-content;
  color: #93c5fd;
  text-decoration: none;
}

.details-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

h1 {
  color: #f8fafc;
  font-size: clamp(1.4rem, 3vw, 2rem);
}

.status {
  font-size: 0.9rem;
  border-radius: 999px;
  padding: 6px 12px;
  border: 1px solid;
}

.status.online {
  color: #86efac;
  border-color: #14532d;
  background: #052e16;
}

.status.offline {
  color: #fca5a5;
  border-color: #7f1d1d;
  background: #450a0a;
}

.actions {
  display: flex;
  gap: 10px;
}

button {
  border: 1px solid #334155;
  background: #0f172a;
  color: #f8fafc;
  padding: 10px 18px;
  border-radius: 12px;
  cursor: pointer;
  font-weight: 600;
}

button:hover:enabled {
  border-color: #38bdf8;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error {
  color: #fda4af;
}

.logs {
  border: 1px solid #1e293b;
  border-radius: 14px;
  background: #020617;
  padding: 12px;
}

h2 {
  color: #cbd5e1;
  margin-bottom: 10px;
}

pre {
  min-height: 220px;
  max-height: 420px;
  overflow: auto;
  color: #e2e8f0;
  white-space: pre-wrap;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New',
    monospace;
  font-size: 0.86rem;
}

.cfg-editor {
  border: 1px solid #1e293b;
  border-radius: 14px;
  background: #020617;
  padding: 12px;
  display: grid;
  gap: 10px;
}

.cfg-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.cfg-actions {
  display: flex;
  gap: 8px;
}

.cfg-picker {
  display: grid;
  gap: 6px;
}

label {
  color: #cbd5e1;
  font-size: 0.9rem;
}

select {
  border: 1px solid #334155;
  background: #0f172a;
  color: #f8fafc;
  padding: 8px 10px;
  border-radius: 10px;
}

.cfg-message {
  color: #a5b4fc;
  font-size: 0.9rem;
}

.cfg-textarea {
  width: 100%;
  min-height: 240px;
  max-height: 420px;
  border: 1px solid #334155;
  border-radius: 10px;
  padding: 10px;
  background: #020617;
  color: #e2e8f0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New',
    monospace;
  resize: vertical;
}
</style>
