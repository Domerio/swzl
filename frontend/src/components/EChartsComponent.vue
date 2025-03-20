<template>
  <div ref="echartsContainer" :style="{ width: width, height: height }"></div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: 'EChartsComponent',
  props: {
    // 图表的宽度
    width: {
      type: String,
      default: '100%',
    },
    // 图表的高度
    height: {
      type: String,
      default: '400px',
    },
    // 图表的类型
    chartType: {
      type: String,
      required: true,
      validator(value) {
        return ['line', 'bar', 'pie', 'radar'].includes(value);
      },
    },
    // 图表的配置数据
    chartData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      chart: null,
    };
  },
  mounted() {
    this.initChart();
  },
  watch: {
    chartData: 'updateChart',
    chartType: 'updateChart',
  },
  methods: {
    // 初始化图表
    initChart() {
      this.chart = echarts.init(this.$refs.echartsContainer);
      this.updateChart();
    },
    // 更新图表
    updateChart() {
      if (!this.chart) return;

      let option = {};
      const { chartType, chartData } = this;

      // 根据 chartType 渲染不同的图表
      switch (chartType) {
        case 'line':
          option = this.getLineChartOptions(chartData);
          break;
        case 'bar':
          option = this.getBarChartOptions(chartData);
          break;
        case 'pie':
          option = this.getPieChartOptions(chartData);
          break;
        case 'radar':
          option = this.getRadarChartOptions(chartData);
          break;
        default:
          option = {};
      }

      this.chart.setOption(option);
    },
    // 获取折线图的配置
    getLineChartOptions(data) {
      return {
        title: {
          text: '折线图示例',
        },
        tooltip: {
          trigger: 'axis',
        },
        xAxis: {
          type: 'category',
          data: data.categories,
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            data: data.values,
            type: 'line',
          },
        ],
      };
    },
    // 获取柱状图的配置
    getBarChartOptions(data) {
      return {
        title: {
          text: '柱状图示例',
        },
        xAxis: {
          type: 'category',
          data: data.categories,
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            data: data.values,
            type: 'bar',
          },
        ],
      };
    },
    // 获取饼图的配置
    getPieChartOptions(data) {
      return {
        title: {
          text: '饼图示例',
        },
        series: [
          {
            name: '水果分布',
            type: 'pie',
            data: data.map(item => ({ value: item.value, name: item.name })),
          },
        ],
      };
    },
    // 获取雷达图的配置
    getRadarChartOptions(data) {
      return {
        title: {
          text: '雷达图示例',
        },
        radar: {
          indicator: data.indicators,
        },
        series: [
          {
            name: '评分',
            type: 'radar',
            data: [
              {
                value: data.values,
              },
            ],
          },
        ],
      };
    },
  },
};
</script>

<style scoped>
</style>
