<script setup>

</script>

<template>
  <el-container style="height: 100%; margin: 0; padding: 0;">
<!--    <el-header>header</el-header>-->



    <el-container style="height: 100%; margin: 0; padding: 0;">
      <el-main style="height: calc(100% - 100px); margin: 0; padding: 0;">
        <div class="chart-container" style="height: 100%; width: 100%; ">
<!--          <div class="chart-title">Stream Graph</div>-->
          <div class="chart-content" style="height: 100%; width: 100%; "></div>
        </div>
      </el-main>

      <el-footer height="100px">
        <h1>some tools or buttons</h1>

      </el-footer>
    </el-container>

    <el-aside width="200px"><h1>some tools or buttons</h1></el-aside>

<!--    <el-footer>footer</el-footer>-->
  </el-container>
</template>

<script>
import * as echarts from 'echarts';
import { getStreamGraphData } from '@/api/monitor/streamGraph.js';

export default {
  data() {
    return {
      chartNode: [],
      chartEdge: []
    }
  },
  // created() {
  //   this.drawChart();
  // },
  mounted() {
    this.drawChart();
  },
  created() {
    this.getStreamGraphData();
  },
  methods: {
    drawChart() {
      // var chartDom = document.getElementById('chart');
      var myChart = echarts.init(document.querySelector('.chart-content'));

      var option = {
          tooltip: {
            trigger: 'item',
            triggerOn: 'mousemove'
          },
          animation: false,
          series: [
            {
              type: 'sankey',
              bottom: '10%',
              emphasis: {
                focus: 'adjacency'
              },
              data: this.chartNode,
              links: this.chartEdge,
              orient: 'vertical',
              label: {
                position: 'top'
              },
              lineStyle: {
                color: 'source',
                curveness: 0.5
              }
            }
          ]
        };
    myChart.setOption(option);
    // console.log(option);
    },
    getStreamGraphData() {
      getStreamGraphData().then(res => {
        // console.log(res.data);
        this.chartNode = res.data.node;
        this.chartEdge = res.data.edge;
        this.drawChart(); // 在数据更新后重新绘制图表
      })
    }
  }
}

</script>

<style>

.chart-container {

  background-color: #fff;
  border: 3px solid #4c4b4b;
}

el-aside {
  margin-right: 0;
}

router-view {
  padding: 0;
  margin: 0;
  height: 100%;
}

</style>