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

# Branches

## main

pure html,css,js realization.

## vue-component-dev

use modern vue3 composable syntax and apis to develop oh-my-api