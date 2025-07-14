// backend/index.js
const express = require('express')
const jwt = require('jsonwebtoken')
const cors = require('cors')
const bodyParser = require('body-parser')

const app = express()
const SECRET_KEY = 'your-secret-key'
const mysql = require('mysql');
app.use(cors())
app.use(bodyParser.json())

const connection = mysql.createConnection({
  host:'localhost',
  user:'root',
  password:'123456',
  database:'ohmyapi'
})
connection.connect(function(err){
  if(err){
    console.error('error connecting:'+err.stack);
    return;
  }
  console.log('connected as id '+ connection.threadId)
});


// 登录接口
app.post('/api/login',(req,res)=>{
  const {username,password}=req.body
  connection.query('select * from user where username = ? and password  = ?',[username,password],(err,results)=>{
    if(err){
      console.error(err)
      return res.status(500).json({message:'服务器错误'})
    }
    if(results.length>0){
      const token = jwt.sign({username},SECRET_KEY,{expiresIn:'1h'})
      res.json({token})
    }else{
      res.status(401).json({message:用户名或密码错误})
    }
  })
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
