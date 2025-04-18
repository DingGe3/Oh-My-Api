<template>
  <div class="dashboard">
    <aside class="sidebar">
      <ul>
        <li @click="showContent('xiangdao')">项导文档</li>
        <li @click="showContent('shiyong')">使用 API</li>
        <li @click="showContent('chart')">本月统计</li>
        <li @click="showContent('demo1')">往月统计</li>
        <li @click="showContent('ip1')">IP 日统计</li>
        <li @click="showContent('ip2')">IP 月统计</li>
        <li @click="showContent('deepseek')">DS 统计</li>
      </ul>
    </aside>

    <main class="main-content">
      <div v-if="activeId === 'xiangdao'">
        <h2>项导文档</h2>
        <button @click="goTo('https://docs.pguide.studio/')">点击进入</button>
      </div>
      <div v-if="activeId === 'shiyong'">
        <h2>使用 API</h2>
        <button @click="goTo('https://docs.pguide.studio/public-service/GPT/')">GPT API 调用及部署</button>
      </div>

      <div
        v-for="id in chartIds"
        :key="id"
        :id="id"
        class="chart"
        v-show="activeId === id"
        ref="charts"
      ></div>
    </main>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import * as echarts from 'echarts'

const activeId = ref('')
const chartIds = ['chart', 'deepseek', 'demo1', 'ip1', 'ip2']
const chartInstances = new Map()

const chartRefs = ref([])

function goTo(url) {
  window.open(url, '_blank')
}

function showContent(id) {
  activeId.value = id
  nextTick(() => {
    setTimeout(() => {
      if (chartIds.includes(id)) {
        renderChart(id)
      }
    }, 300)
  })
}

async function renderChart(id) {
  const chartDom = document.getElementById(id)
  if (!chartDom || chartDom.clientWidth === 0 || chartDom.clientHeight === 0) {
    console.warn(`容器尺寸为0，跳过绘制`, chartDom)
    return
  }

  if (chartInstances.has(id)) {
    chartInstances.get(id).dispose()
  }

  const fileMap = {
    chart: 'apiperday.json',
    deepseek: 'deepseekday.json',
    demo1: 'apipermonth.json',
    ip1: 'ipperday.json',
    ip2: 'ippermonth.json',
  }

  const res = await fetch(`./data_processed/${fileMap[id]}`)
  const data = await res.json()

  const chart = echarts.init(chartDom)
  chart.setOption(generateOption(id, data))
  chartInstances.set(id, chart)
  chart.resize()
}

function formatDate(rawDate) {
  const d = new Date(rawDate)
  return `${d.getMonth() + 1}-${d.getDate()}`
}

function generateOption(id, data) {
  const dates = data.map(d => formatDate(d['时间'] || d['月份']))
  const keys = Object.keys(data[0]).filter(k => k !== '时间' && k !== '月份')
  const series = keys.map(name => ({
    name,
    type: 'line',
    data: data.map(d => d[name]),
  }))

  return {
    title: {
      text: {
        chart: '三月日访问量',
        deepseek: '四月 ds 日访问量',
        demo1: '往月访问量',
        ip1: '三月访问记录',
        ip2: '往月访问记录',
      }[id],
      textStyle: { fontSize: 18 },
    },
    tooltip: { trigger: 'axis' },
    legend: { data: keys, top: '5%' },
    grid: { top: '20%', left: '10%', right: '10%', bottom: '15%' },
    xAxis: { type: 'category', data: dates },
    yAxis: { type: 'value' },
    series,
  }
}

// 可选：监听容器 resize 自动刷新图表
onMounted(() => {
  const observer = new ResizeObserver(() => {
    const id = activeId.value
    if (chartIds.includes(id) && chartInstances.has(id)) {
      chartInstances.get(id).resize()
    }
  })

  chartIds.forEach(id => {
    const el = document.getElementById(id)
    if (el) observer.observe(el)
  })
})
</script>

<style scoped>
.dashboard {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 200px;
  background-color: #333;
  color: white;
  padding: 20px;
  overflow-y: auto;
  flex-shrink: 0;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow-y: auto;
  background-color: #fff;
}

.chart {
  flex: 1;
  width: 100%;
  height: 100%;
  min-height: 600px;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  font-size: 18px;           /* 放大字体 */
  margin-bottom: 15px;       /* 增加选项间距 */
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s, color 0.3s;
  cursor: pointer;           /* 鼠标悬浮变成手型 */
  left: 10px;
}

.sidebar li:hover {
  background-color: #555;    /* 悬停背景色变深 */
  color: #ffd700;            /* 悬停字体变金色，可自行调整 */
}

.sidebar li {
  position: relative;
  padding-left: 20px;
}

.sidebar li::before {
  content: '➤'; /* 或者 '➤'、'▸'、'►' 这些都可以 */
  position: absolute;
  left: 0;
  right: 20px;
  top: 12px;
  color: #ffd700;  /* 可改颜色 */
  font-size: 16px;
  line-height: 1;
}

.sidebar li:hover::before {
  color: #00ffff;  /* 悬停时变亮蓝色 */
}


</style>
