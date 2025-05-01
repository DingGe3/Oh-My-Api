# Project BG

An Echart.js interface for displaying the usage of OpenAI-HK agents. The backend uses MySQL8 for persistent storage, and the communication layer uses Ajax to asynchronously request data.

## Develop Routine

1. API usage date and month distribution (line chart)
2. Simple classification based on IP and API used, use slider component or drop-down box to switch views
3. Backend verification login and persistent storage in MySQL


## Project Setup

Recommended IDE: VSCode, the tutorial of it refers to: [PGuide Docs](https://docs.pguide.studio/campus-wiki/common-software/IDE/VSCode/)

### Install packages

Refer to [CQMU Mirror Wiki#PYPI](https://docs.pguide.studio/public-service/cqmu-mirror/wiki/#pypi) to make build faster!

Operational: use conda to do env management

```python

pip install -r requirements.txt

```
vue版本项目运行方法：
1.安装环境
确保安装了node.js，并添加到环境变量中
在终端中frontend目录下安装echarts和vite（运行npm install和npm install echarts）
2.启动后端和前端
在backend目录下运行node index.js
在frontend目录下运行npm run dev
（在这一步若报错为SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
    则运行代码Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
然后重试）
3.进入返回的local地址