// backend/index.js
const express = require('express')
const jwt = require('jsonwebtoken')
const cors = require('cors')
const bodyParser = require('body-parser')

const app = express()
const SECRET_KEY = 'your-secret-key'

app.use(cors())
app.use(bodyParser.json())

// 模拟的用户数据
const USERS = [
  { username: 'admin', password: '123456' }
]

// 登录接口
app.post('/api/login', (req, res) => {
  const { username, password } = req.body
  const user = USERS.find(u => u.username === username && u.password === password)
  if (user) {
    const token = jwt.sign({ username }, SECRET_KEY, { expiresIn: '1h' })
    res.json({ token })
  } else {
    res.status(401).json({ message: 'Invalid credentials' })
  }
})

// 需要授权的接口
app.get('/api/protected', (req, res) => {
  const authHeader = req.headers.authorization
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ message: 'Missing token' })
  }

  const token = authHeader.split(' ')[1]
  try {
    const decoded = jwt.verify(token, SECRET_KEY)
    res.json({ message: `Hello ${decoded.username}, you have access!` })
  } catch (err) {
    res.status(401).json({ message: 'Invalid token' })
  }
})

app.listen(3000, () => {
  console.log('Backend running at http://localhost:3000')
})
