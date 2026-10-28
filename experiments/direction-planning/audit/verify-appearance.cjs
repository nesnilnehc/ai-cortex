const {chromium}=require('playwright');const fs=require('node:fs');const assert=require('node:assert/strict');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:1000}});const results=[];
try{await p.goto('http://127.0.0.1:8765/experiments/direction-planning/');for(const theme of ['light','dark']){await p.locator('#theme').selectOption(theme);await p.locator('[data-node="planning"]').click();for(const perspective of ['work','evidence']){await p.locator('#help-perspective').selectOption(perspective);
const data=await p.evaluate(()=>{
 const rgb=s=>{const n=s.match(/[\d.]+/g)?.map(Number)??[];return[n[0]??0,n[1]??0,n[2]??0,n[3]??1]};
 const lum=c=>c.slice(0,3).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
 const blend=(a,b)=>a.slice(0,3).map((v,i)=>v*a[3]+b[i]*(1-a[3])).concat(1);
 const bg=el=>{let chain=[];for(let x=el;x;x=x.parentElement)chain.unshift(x);let c=[255,255,255,1];for(const x of chain)c=blend(rgb(getComputedStyle(x).backgroundColor),c);return c};
 return [...document.querySelectorAll('body *')].filter(e=>e.getClientRects().length&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map(e=>{const st=getComputedStyle(e),back=bg(e),fg=blend(rgb(st.color),back),a=lum(fg),b=lum(back);return {text:e.textContent.trim().slice(0,45),ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)}});
});const failures=data.filter(x=>x.ratio<4.5);results.push({theme,perspective,minRatio:Math.min(...data.map(x=>x.ratio)),samples:data.length,failures});assert.deepEqual(failures,[]);}}
}finally{fs.writeFileSync(__dirname+'/req03-contrast.json',JSON.stringify(results,null,2)+'\n');await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
