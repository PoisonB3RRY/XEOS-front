import { spawn } from 'child_process'

console.log('正在同时启动 运营门户 (3000) 与 运维门户 (3001)...')

const isWin = process.platform === 'win32'
const npxCmd = isWin ? 'npx.cmd' : 'npx'

const tenant = spawn(npxCmd, ['vite', '--port', '3000'], { stdio: 'inherit', shell: true })
const ops = spawn(npxCmd, ['vite', '--config', 'vite.config.ops.js'], { stdio: 'inherit', shell: true })

process.on('SIGINT', () => {
  tenant.kill()
  ops.kill()
  process.exit()
})
