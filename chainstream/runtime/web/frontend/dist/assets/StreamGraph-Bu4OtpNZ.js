import{s as p,_ as m,i as _,c as u,w as e,r as a,o as g,a as o,b as f,d as r}from"./index-DNdhB_e1.js";function y(t){return p({url:"/monitor/streamGraph",method:"get",params:t})}const v={data(){return{chartNode:[],chartEdge:[]}},mounted(){this.drawChart()},created(){this.getStreamGraphData()},methods:{drawChart(){var t=_(document.querySelector(".chart-content")),n={tooltip:{trigger:"item",triggerOn:"mousemove"},animation:!1,series:[{type:"sankey",bottom:"10%",emphasis:{focus:"adjacency"},data:this.chartNode,links:this.chartEdge,orient:"vertical",label:{position:"top"},lineStyle:{color:"source",curveness:.5}}]};t.setOption(n)},getStreamGraphData(){y().then(t=>{this.chartNode=t.data.node,this.chartEdge=t.data.edge,this.drawChart()})}}},x=r("div",{class:"chart-container",style:{height:"100%",width:"100%"}},[r("div",{class:"chart-content",style:{height:"100%",width:"100%"}})],-1),w=r("h1",null,"some tools or buttons",-1);function C(t,n,S,b,k,i){const c=a("el-main"),d=a("el-footer"),s=a("el-container"),h=a("el-button"),l=a("el-aside");return g(),u(s,{style:{height:"100%",margin:"0",padding:"0"}},{default:e(()=>[o(s,{style:{height:"100%",margin:"0",padding:"0"}},{default:e(()=>[o(c,{style:{height:"calc(100% - 100px)",margin:"0",padding:"0"}},{default:e(()=>[x]),_:1}),o(d,{height:"100px"},{default:e(()=>[w]),_:1})]),_:1}),o(l,{width:"200px",style:{display:"flex","justify-content":"center"}},{default:e(()=>[o(h,{type:"primary",onClick:i.getStreamGraphData},{default:e(()=>[f("Refresh")]),_:1},8,["onClick"])]),_:1})]),_:1})}const N=m(v,[["render",C]]);export{N as default};