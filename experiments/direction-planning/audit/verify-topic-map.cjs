const {chromium}=require('playwright');const fs=require('node:fs');const path=require('node:path');const assert=require('node:assert/strict');const {createHash}=require('node:crypto');
const base=path.resolve(__dirname,'..'),catalog=JSON.parse(fs.readFileSync(path.join(base,'catalog.json'))),guides=JSON.parse(fs.readFileSync(path.join(base,'skill-guidance.json'))),edges=JSON.parse(fs.readFileSync(path.join(base,'skill-edges.json')));
(async()=>{const model=await import('../skill-graph.mjs');const baseline=[...new Set(model.getSkillGraph().groups.flatMap(group=>model.getSkillForest(group.id).connections.map(edge=>edge.id)))].sort();const browser=await chromium.launch();const report={date:new Date().toISOString(),browser:browser.version(),matrix:[],skills:[],errors:[]};try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}});page.on('pageerror',e=>report.errors.push(e.message));await page.goto('http://127.0.0.1:8765/experiments/direction-planning/');
 await page.locator('.topic-toggle').first().waitFor({state:'visible',timeout:1500});
 assert.equal(await page.locator('.skill-node:visible').count(),0);assert.equal(await page.locator('.topic-region').count(),5);assert.equal(await page.locator('.topic-connector').count(),3);assert.equal(await page.locator('.topic-loop').count(),2);
 await page.locator('[data-topic-relation="repair-feedback"]').click();assert.match(await page.locator('#skill-relations').textContent(),/停止条件/);assert.equal(await page.locator('.skill-group[data-topic-related="true"]').count(),2);await page.locator('#close-panel').click();
 for(const toggle of await page.locator('.topic-toggle').all())await toggle.click();

 assert.deepEqual((await page.locator('.skill-node').evaluateAll(elements=>elements.map(el=>el.dataset.skill))).sort(),catalog.map(x=>x.id).sort());
 assert.equal(await page.locator('#node-asset-select').count(),0);assert.equal(await page.locator('#help-perspective').count(),0);
 for(const {id,purpose} of catalog){
  const button=page.locator(`.skill-node[data-skill="${id}"]`);assert.equal(await button.isVisible(),true);assert.equal(await button.locator('code').isVisible(),true,`${id}: name must be visible`);assert.equal(await button.locator('code').innerText(),id);assert.equal(await button.locator('strong').innerText(),purpose);
  await button.click();assert.deepEqual(await checkRoutes(),[],`${id}: route occlusion`);assert.deepEqual(await page.locator('#selected-tool-guide dd').allTextContents(),['when','provide','use','result'].map(key=>guides[id][key]));
  const expected=edges.filter(edge=>edge.from===id||edge.to===id),related=[...new Set(expected.map(edge=>edge.from===id?edge.to:edge.from))].sort();
  assert.deepEqual((await page.locator('.skill-node[data-related="true"]').evaluateAll(els=>els.map(el=>el.dataset.skill))).sort(),related);
  assert.equal(await page.locator('#panel-relations-button').getAttribute('data-count'),String(expected.length));
  await page.locator('#panel-relations-button').click();assert.equal(await page.locator('#skill-relations [data-relation]').count(),expected.length);
  if(!expected.length)assert.match(await page.locator('#skill-relations').textContent(),/未标出|没有/);
  await page.locator('#close-panel').click();assert.equal(await button.evaluate(el=>el===document.activeElement),true);
  report.skills.push({id,visibleAfterExpansion:true,guide:true,relations:expected.length});
 }
 // Sample every actual SVG segment against every primary node interior.
 async function checkRoutes(){
  return page.evaluate(()=>{
   const box=document.querySelector('.skill-atlas').getBoundingClientRect();
   const nodes=[...document.querySelectorAll('.skill-node')].map(node=>{const r=node.getBoundingClientRect();return {id:node.dataset.skill,left:r.left-box.left+1,right:r.right-box.left-1,top:r.top-box.top+1,bottom:r.bottom-box.top-1};});
   const hits=[];
   for(const path of document.querySelectorAll('#skill-edge-paths path')){
    const length=path.getTotalLength();for(let i=1;i<Math.ceil(length);i+=3){const point=path.getPointAtLength(i);const hit=nodes.find(r=>point.x>r.left&&point.x<r.right&&point.y>r.top&&point.y<r.bottom);if(hit){hits.push({edge:path.dataset.skillEdge,node:hit.id});break;}}
   }
   const paths=[...document.querySelectorAll('#skill-edge-paths path')].map(path=>({id:path.dataset.skillEdge,points:[...path.getAttribute('d').matchAll(/[ML]([\d.-]+),([\d.-]+)/g)].map(m=>[+m[1],+m[2]])}));
   for(let a=0;a<paths.length;a++)for(let b=a+1;b<paths.length;b++)for(let i=1;i<paths[a].points.length;i++)for(let j=1;j<paths[b].points.length;j++){
    const p=paths[a].points[i-1],q=paths[a].points[i],r=paths[b].points[j-1],t=paths[b].points[j];
    const v=p[0]===q[0]?[p,q]:r[0]===t[0]?[r,t]:null,h=p[1]===q[1]?[p,q]:r[1]===t[1]?[r,t]:null;
    if(v&&h&&v[0][0]>Math.min(h[0][0],h[1][0])+.5&&v[0][0]<Math.max(h[0][0],h[1][0])-.5&&h[0][1]>Math.min(v[0][1],v[1][1])+.5&&h[0][1]<Math.max(v[0][1],v[1][1])-.5)hits.push({crossing:[paths[a].id,paths[b].id]});
   }
   return hits;
  });
 }
 for(const [width,height] of [[360,667],[390,844],[1024,768],[1280,800],[1440,1000]])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height});await page.locator('#theme').selectOption(theme);
  assert.equal(await page.locator('.skill-node:visible').count(),70);assert.equal(await page.locator('.skill-node code:visible').count(),70);
  const labelIssues=await page.locator('.skill-node').evaluateAll(nodes=>nodes.flatMap(node=>{const box=node.getBoundingClientRect(),name=node.querySelector('code'),description=node.querySelector('strong'),n=name.getBoundingClientRect(),d=description.getBoundingClientRect();return n.left<box.left||n.right>box.right+1||d.right>box.right+1||n.bottom>d.top+1||name.scrollWidth>name.clientWidth+1?[node.dataset.skill]:[];}));assert.deepEqual(labelIssues,[],`${width}: names/descriptions must fit without overlap`);assert.equal(await page.locator('.relations-canvas').count(),1);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  const button=page.locator('.skill-node[data-skill="prepare-release"]');await button.focus();await page.keyboard.press('Enter');
  assert.match(await page.locator('#selected-tool-purpose').textContent(),/发布/);assert.deepEqual(await checkRoutes(),[],`${width}/${theme}: node occlusion`);
  const sizes=await page.locator('.skill-node').evaluateAll(nodes=>nodes.map(node=>node.getBoundingClientRect().height));assert.ok(Math.max(...sizes)<=90,`${width}: oversized node`);await page.locator('#panel-relations-button').click();assert.equal(await page.locator('#skill-relations [data-relation]').count(),2);
  if(width<1200){const nodeBox=await button.boundingBox(),panelBox=await page.locator('#detail-panel').boundingBox();assert.ok(nodeBox.y>=0&&nodeBox.y+nodeBox.height<=panelBox.y,`${width}: selected node remains above sheet`);}
  await page.locator('#detail-panel').press('Escape');assert.equal(await button.evaluate(el=>el===document.activeElement),true);
  const hub=page.locator('.skill-node[data-skill="orchestrate-code-review"]');await hub.click();assert.deepEqual(await checkRoutes(),[],`${width}/${theme}: dense hub occlusion`);await page.locator('#close-panel').click();
  report.matrix.push({width,height,theme,allSkillsDisplayed:true,oneGraph:true,overflow:false,keyboardSelection:true,focusReturned:true,maxNodeHeight:Math.max(...sizes),routesClear:true});
 }
 await page.setViewportSize({width:1440,height:1000});await page.locator('.skill-node[data-skill="prepare-release"]').click();await page.locator('#panel-relations-button').click();await page.locator('[data-peer="publish-release"]').click();assert.equal(await page.locator('.skill-node[data-skill="publish-release"]').getAttribute('aria-pressed'),'true');assert.match(await page.locator('#selected-tool-purpose').textContent(),/正式发布/);await page.locator('#close-panel').click();
 await page.setViewportSize({width:1440,height:1000});await page.locator('.skill-node[data-skill="prepare-release"]').click();await page.locator('#panel-work-button').click();await page.locator('#edit-request').evaluate(el=>el.open=true);await page.locator('#request-text').fill('保留本次发布范围');await page.locator('.skill-node[data-skill="publish-release"]').click();await page.locator('#panel-work-button').click();assert.equal(await page.locator('#request-text').inputValue(),'保留本次发布范围');
 await page.locator('#close-panel').click();await page.locator('#find-tools').click();await page.locator('#tool-search').fill('review-roadmap');assert.equal(await page.locator('[data-tool="review-roadmap"]').evaluate(el=>el.closest('.tool-group').dataset.group),'planning');await page.locator('[data-tool="review-roadmap"]').click();assert.equal(await page.locator('.skill-node[data-skill="review-roadmap"]').getAttribute('aria-pressed'),'true');
 await page.locator('[data-node="direction"]').click();await page.setViewportSize({width:1280,height:800});await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));assert.deepEqual((await page.locator('#skill-edge-paths path').evaluateAll(els=>els.map(el=>el.dataset.skillEdge))).sort(),baseline);await page.locator('#panel-assets-button').click();assert.equal(await page.locator('.skill-node[data-skill="define-mission"]').getAttribute('aria-pressed'),'true');
 for(const width of [390,1440]){await page.locator('#close-panel').click();await page.setViewportSize({width,height:width===390?844:1000});await page.locator('#theme').selectOption('light');await page.locator('.skill-node[data-skill="prepare-release"]').click();await page.locator('#panel-relations-button').click();await page.screenshot({path:path.join(__dirname,`topic-map-${width}.png`)});}
 await page.locator('#close-panel').click();await page.locator('#collapse-topics').click();assert.equal(await page.locator('.skill-node:visible').count(),0);await page.locator('#find-tools').click();await page.locator('#tool-search').fill('publish-release');await page.locator('[data-tool="publish-release"]').click();assert.equal(await page.locator('[data-toggle="release"]').getAttribute('aria-expanded'),'true');assert.equal(await page.locator('.skill-node[data-skill="publish-release"]').isVisible(),true);await page.locator('#panel-relations-button').click();await page.locator('[data-peer="commit-work"]').click();assert.equal(await page.locator('[data-toggle="commit"]').getAttribute('aria-expanded'),'true');assert.equal(await page.locator('.skill-node[data-skill="commit-work"]').getAttribute('aria-pressed'),'true');await page.locator('#close-panel').click();await page.locator('[data-toggle="commit"]').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('[data-toggle="commit"]').getAttribute('aria-expanded'),'false');await page.locator('#collapse-topics').click();
 await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:path.join(__dirname,'topic-map-overview.png')});
 assert.deepEqual(report.errors,[]);report.status='passed';
 }catch(e){report.status='failed';report.error=e.stack;throw e;}finally{report.sourceHashes=Object.fromEntries(['index.html','story.mjs','workspace.css','skill-graph.mjs','panel-model.mjs','workflow.mjs','relations.mjs','story-model.mjs','skill-guidance.json','skill-edges.json','topic-map.mjs','audit/verify-topic-map.cjs'].map(file=>[file,createHash('sha256').update(fs.readFileSync(path.join(base,file))).digest('hex')]));fs.writeFileSync(path.join(__dirname,'topic-map-browser.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});
