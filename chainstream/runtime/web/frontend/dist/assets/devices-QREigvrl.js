import{_ as b,r as n,o as a,k as _,a as t,w as e,d as i,t as v,b as c,F as u,l as w,c as C}from"./index-DNdhB_e1.js";const j={class:"card-header"},V={style:{flex:"auto"}},D={data(){return{statisticalData:[{title:"Total Usage",value:268500},{title:"Agent Count",value:100},{title:"User Count",value:1e3},{title:"Device Count",value:1e4}],drawer2:!1}},methods:{cancelClick(){this.drawer2=!1},confirmClick(){this.drawer2=!1}}},R=Object.assign(D,{__name:"device_card",props:{model_name:{type:String,default:"LLM Card",required:!0}},setup(m){return(l,o)=>{const f=n("el-statistic"),p=n("el-col"),s=n("el-row"),h=n("el-container"),y=n("RefreshRight"),g=n("el-icon"),d=n("el-button"),k=n("el-card"),x=n("el-drawer");return a(),_(u,null,[t(k,{style:{"max-width":"480px"},shadow:"hover"},{header:e(()=>[i("div",j,[i("span",null,v(m.model_name),1)])]),footer:e(()=>[t(s,{justify:"end"},{default:e(()=>[t(d,{type:"primary",size:"default"},{default:e(()=>[t(g,null,{default:e(()=>[t(y)]),_:1}),c(" Refresh ")]),_:1}),t(d,{type:"primary",size:"default",onClick:o[0]||(o[0]=r=>l.drawer2=!0)},{default:e(()=>[c("More")]),_:1})]),_:1})]),default:e(()=>[t(h,null,{default:e(()=>[t(s,{style:{width:"100%"}},{default:e(()=>[(a(!0),_(u,null,w(l.statisticalData,(r,z)=>(a(),C(p,{span:24,style:{"align-content":"center","justify-content":"center","text-align":"center"}},{default:e(()=>[t(f,{title:r.title,value:r.value},null,8,["title","value"])]),_:2},1024))),256))]),_:1})]),_:1})]),_:1}),t(x,{modelValue:l.drawer2,"onUpdate:modelValue":o[1]||(o[1]=r=>l.drawer2=r),direction:"rtl"},{header:e(()=>[i("h1",null,v(m.model_name),1)]),default:e(()=>[]),footer:e(()=>[i("div",V,[t(d,{onClick:l.cancelClick},{default:e(()=>[c("cancel")]),_:1},8,["onClick"]),t(d,{type:"primary",onClick:l.confirmClick},{default:e(()=>[c("confirm")]),_:1},8,["onClick"])])]),_:1},8,["modelValue"])],64)}}}),B=b(R,[["__scopeId","data-v-cad41bd9"]]),S={data(){return{cards:[{model_name:"Phone",content:"Content of card"},{model_name:"Watch",content:"Content of card"},{model_name:"ChainStreamSensor",content:"Content of card"}]}}},N=Object.assign(S,{__name:"devices",setup(m){return(l,o)=>{const f=n("el-text"),p=n("el-col"),s=n("el-row"),h=n("el-container");return a(),_(u,null,[t(f,{style:{"font-size":"24px","text-align":"center","margin-top":"50px","font-weight":"bold"},type:"primary"},{default:e(()=>[c("Devices")]),_:1}),t(h,null,{default:e(()=>[t(s,{style:{height:"40vh",width:"100%",margin:"0",padding:"0"},align:"middle",justify:"start"},{default:e(()=>[(a(!0),_(u,null,w(l.cards,(y,g)=>(a(),C(p,{key:g,span:6,style:{"align-content":"center","justify-content":"center"}},{default:e(()=>[t(B,{model_name:y.model_name},null,8,["model_name"])]),_:2},1024))),128))]),_:1})]),_:1})],64)}}});export{N as default};
