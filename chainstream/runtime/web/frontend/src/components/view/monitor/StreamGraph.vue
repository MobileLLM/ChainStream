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

export default {
  data() {

  },
  // created() {
  //   this.drawChart();
  // },
  mounted() {
    this.drawChart();
  },
  methods: {
    drawChart() {
      // var chartDom = document.getElementById('chart');
      var myChart = echarts.init(document.querySelector('.chart-content'));
      // var option = {
      //   tooltip: {
      //     trigger: 'item',
      //     triggerOn:'mousemove'
      //   },
      //   data: [
      //     { name: 'a' },
      //     { name: 'b' },
      //     { name: 'a1' },
      //     { name: 'b1' },
      //     { name: 'c' },
      //     { name: 'e' }
      //   ],
      //   links: [
      //     { source: 'a', target: 'a1', value: 5 },
      //     { source: 'e', target: 'b', value: 3 },
      //     { source: 'a', target: 'b1', value: 3 },
      //     { source: 'b1', target: 'a1', value: 1 },
      //     { source: 'b1', target: 'c', value: 2 },
      //     { source: 'b', target: 'c', value: 1 }
      //   ],
      //   animation: false,
      //   series: [
      //     {
      //       type: 'sankey',
      //       bottom: '10%',
      //       emphasis: {
      //         focus: 'adjacency'
      //       },
      //       orient: 'vertical',
      //       label: {
      //         position: 'top',
      //       },
      //       lineStyle: {
      //         color: 'source',
      //         curveness: 0.5
      //       },
      //
      //     }
      //   ]
      // }
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
              data: [
                { name: 'a' },
                { name: 'b' },
                { name: 'a1' },
                { name: 'b1' },
                { name: 'c' },
                { name: 'e' }
              ],
              links: [
                { source: 'a', target: 'a1', value: 5 },
                { source: 'e', target: 'b', value: 3 },
                { source: 'a', target: 'b1', value: 3 },
                { source: 'b1', target: 'a1', value: 1 },
                { source: 'b1', target: 'c', value: 2 },
                { source: 'b', target: 'c', value: 1 }
              ],
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