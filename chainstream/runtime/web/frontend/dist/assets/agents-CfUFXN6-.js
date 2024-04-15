import{$ as m}from"./jquery-C13ZeFGA.js";import{s as h,e as S,c as d,w as s,r as i,o as g,a as n,d as p,b as o,t as c,f as b,g as T}from"./index-DNdhB_e1.js";function L(){return h({url:"/monitor/agents",method:"get"})}function x(t){return h({url:"/monitor/agents/start/"+t,method:"post"})}function H(t){return h({url:"/monitor/agents/stop/"+t,method:"post"})}function N(){return h({url:"/monitor/agents/getRunningAgents",method:"get"})}const $={style:{height:"40px",margin:"0",padding:"0"}},z={class:"custom-tree-node",style:{flex:"1",display:"flex","align-items":"center","justify-content":"space-between","font-size":"14px","padding-right":"8px"}},D={data(){return{path_loading:!0,running_loading:!1,agents_path:[],checkedNodes:[],defaultProps:{children:"children",label:"label",disabled:"disabled",is_running:"is_running"},agents_running:[{agent_id:"123456",agent_path:"C:\\Program Files\\Agent\\agent.exe",description:"This is a moke agent",version:"1.0.0",type:"user",status:"running",running_time:"2021-11-11 11:11:11",is_running:!0}],elTableHeight:m(".el-scrollbar").height()}},created(){this.getAgentsList(),window.addEventListener("resize",this.handleHightChange)},destroyed(){window.removeEventListener("resize",this.handleHightChange)},methods:{handleCheck(t){this.checkedNodes=checkedNodes},getRunningAgentsList(){this.running_loading=!0,N().then(t=>{this.agents_running=t.data,this.running_loading=!1})},getAgentsList(){this.path_loading=!0,L().then(t=>{this.agents_path=t.data,this.path_loading=!1}),this.getRunningAgentsList()},handleTreeStart(t){x(t.label).then(e=>{e.data.res==="ok"?(this.$message.success("Agent started successfully"),this.getAgentsList()):(this.$message.error("Agent start failed"),this.getAgentsList())})},handleTreeStop(t){H(t.label).then(e=>{e.data.res==="ok"?(this.$message.success("Agent stopped successfully"),this.getAgentsList()):(this.$message.error("Agent stop failed"),this.getAgentsList())})},handleStart(t,e){},handleStop(t,e){},filterType(t,e){return e.type===t},filterStatus(t,e){return e.status===t},handleHightChange(){this.elTableHeight=m(".el-scrollbar").height()}}},B=Object.assign(D,{__name:"agents",setup(t){return(e,P)=>{const u=i("el-button"),y=i("el-tree"),_=i("el-scrollbar"),w=i("el-aside"),a=i("el-table-column"),f=i("el-tag"),A=i("el-table"),v=i("el-container"),k=S("loading");return g(),d(v,{style:{height:"100%",margin:"0",padding:"0"}},{default:s(()=>[n(w,{height:e.elTableHeight,width:"20%",style:{margin:"0 1% 0 0",padding:"0"}},{default:s(()=>[p("div",$,[n(u,{type:"primary",onClick:e.getAgentsList},{default:s(()=>[o("Refresh")]),_:1},8,["onClick"])]),n(_,{style:{height:"calc(100% - 40px)",width:"100%",margin:"0",padding:"0"}},{default:s(()=>[n(y,{data:e.agents_path,props:e.defaultProps,"default-expand-all":""},{default:s(({node:l,data:r})=>[p("span",z,[p("span",null,c(l.label),1),!r.disabled&&!r.is_running?(g(),d(u,{key:0,size:"small",type:"success",onClick:C=>e.handleTreeStart(r)},{default:s(()=>[o("Start")]),_:2},1032,["onClick"])):b("",!0),r.is_running?(g(),d(u,{key:1,size:"small",type:"warning",onClick:C=>e.handleTreeStop(r)},{default:s(()=>[o("Stop")]),_:2},1032,["onClick"])):b("",!0)])]),_:1},8,["data","props"])]),_:1})]),_:1},8,["height"]),n(_,{style:{height:"100%",width:"100%",margin:"0",padding:"0"}},{default:s(()=>[T((g(),d(A,{data:e.agents_running,height:e.elTableHeight,style:{width:"100%",margin:"0",padding:"0"},"table-layout":"auto"},{default:s(()=>[n(a,{type:"index",label:"#",width:"50"}),n(a,{prop:"agent_id",label:"Agent ID",width:"180"}),n(a,{label:"Info"},{default:s(()=>[n(a,{prop:"agent_file_path",label:"Path",width:"180"}),n(a,{prop:"description",label:"Description",width:"180"}),n(a,{prop:"version",label:"Version",width:"120"}),n(a,{prop:"type",label:"Type",width:"120",filters:[{text:"system",value:"system"},{text:"user",value:"user"}],"filter-method":e.filterType},{default:s(l=>[n(f,null,{default:s(()=>[o(c(l.row.type),1)]),_:2},1024)]),_:1},8,["filter-method"])]),_:1}),n(a,{label:"Status"},{default:s(()=>[n(a,{prop:"status",label:"Status",width:"120",filters:[{text:"Stopped",value:"stopped"},{text:"Error",value:"error"}],"filter-method":e.filterStatus},{default:s(l=>[n(f,{type:"warning"},{default:s(()=>[o(c(l.row.status),1)]),_:2},1024)]),_:1},8,["filter-method"]),n(a,{prop:"created_at",label:"Created Time"})]),_:1})]),_:1},8,["data","height"])),[[k,e.running_loading]])]),_:1})]),_:1})}}});export{B as default};