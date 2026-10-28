const {chromium}=require('playwright');
const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');const {createHash}=require('node:crypto');
const base=path.resolve(__dirname,'..');const guides=JSON.parse(fs.readFileSync(path.join(base,'skill-guidance.json')));
const nodes=['direction','planning','design','build','quality','commit','release','research','foundation','collaboration'];
(async()=>{const browser=await chromium.launch();const report={date:new Date().toISOString(),browser:browser.version(),matrix:[],skills:[],errors:[]};
try{const page=await browser.newPage({viewport:{width:1440,height:1000}});page.on('pageerror',e=>report.errors.push(e.message));
await page.goto('http://127.0.0.1:8765/experiments/direction-planning/');
await page.locator('[data-node="quality"]').click();await page.locator('#node-asset-select').waitFor({state:'visible',timeout:1500});
for(const node of nodes){
 await page.locator(`[data-node="${node}"]`).click();
 for(const option of await page.locator('#node-asset-select option').all()){
  const id=await option.getAttribute('value');await page.locator('#node-asset-select').selectOption(id);
  assert.deepEqual(await page.locator('#selected-tool dd').allTextContents(),['when','provide','use','result'].map(k=>guides[id][k]));
  assert.equal(await page.locator('.panel-body').evaluate(el=>el.scrollTop),0);
  report.skills.push({id,node,fourFields:true});
 }
}
assert.deepEqual(report.skills.map(x=>x.id).sort(),Object.keys(guides).sort());
for(const [width,height] of [[360,667],[390,844],[1024,768],[1280,800],[1440,1000]])for(const theme of ['light','dark'])for(const lens of ['work','evidence']){
 await page.setViewportSize({width,height});await page.locator('#theme').selectOption(theme);await page.locator('#help-perspective').selectOption(lens);
 for(const node of nodes){
  if(await page.locator('#close-panel').isVisible())await page.locator('#close-panel').click();
  await page.locator(`[data-node="${node}"]`).click();
  const picker=page.locator('#node-asset-select');
  const box=await picker.boundingBox();assert.ok(box.y>=0&&box.y+box.height<=height,`${width}/${node}: picker visible without scroll`);
  assert.equal(await page.locator('.panel-body').evaluate(el=>el.scrollTop),0);
  await page.locator('.panel-body').evaluate(el=>el.scrollTop=el.scrollHeight);
  const after=await picker.boundingBox();assert.equal(after.y,box.y,'Picker must remain outside long instructions');
  assert.equal(await picker.evaluate(el=>!!el.checkVisibility()),true);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 }
 // Keyboard selection, context switch and perspective retain the chosen asset.
 await page.locator('#node-asset-select').focus();assert.equal(await page.locator('#node-asset-select').evaluate(el=>el===document.activeElement),true);
 const next=await page.locator('#node-asset-select option').nth(1).getAttribute('value');await page.locator('#node-asset-select').selectOption(next);
 const selected=await page.locator('#node-asset-select').inputValue();
 assert.equal(selected,next);await page.locator('#panel-work-button').focus();await page.keyboard.press('Enter');
 assert.equal(await page.locator('#node-asset-select').isVisible(),true);
 await page.locator('#help-perspective').selectOption(lens==='work'?'evidence':'work');
 assert.equal(await page.locator('#node-asset-select').inputValue(),selected);
 await page.locator('#panel-assets-button').focus();await page.keyboard.press('Enter');assert.equal(await page.locator('#selected-tool').isVisible(),true);
 await page.locator('#detail-panel').press('Escape');assert.equal(await page.locator('[data-node="collaboration"]').evaluate(el=>document.activeElement===el),true);
 report.matrix.push({width,height,theme,lens,allNodes:true,entryWithoutScroll:true,pickerPinned:true,keyboardModeSwitchAndClose:true,nativePopupSelection:'separate IAB check',selectionPreserved:true,overflow:false});
}
await page.setViewportSize({width:1440,height:1000});await page.locator('#find-tools').click();await page.locator('#tool-search').fill('commit-work');await page.locator('[data-tool="commit-work"]').click();assert.equal(await page.locator('#node-asset-select').inputValue(),'commit-work');
await page.locator('#panel-work-button').click();await page.locator('#edit-request').evaluate(el=>el.open=true);await page.locator('#request-text').fill('保留我的工作请求');await page.locator('#panel-assets-button').click();await page.locator('#node-asset-select').selectOption('deliver-feature');await page.locator('#panel-work-button').click();assert.equal(await page.locator('#request-text').inputValue(),'保留我的工作请求');
for(const width of [390,1440]){if(await page.locator('#close-panel').isVisible())await page.locator('#close-panel').click();await page.setViewportSize({width,height:width===390?844:1000});await page.locator('#theme').selectOption('light');await page.locator('[data-node="quality"]').click();await page.screenshot({path:path.join(__dirname,`asset-entry-${width}.png`)});}
assert.deepEqual(report.errors,[]);assert.equal(await page.locator('.relations-canvas').count(),1);report.status='passed';
}catch(e){report.status='failed';report.error=e.stack;throw e;}finally{report.sourceHashes=Object.fromEntries(['index.html','story.mjs','panel-model.mjs','workspace.css','skill-guidance.json','audit/verify-asset-entry.cjs'].map(file=>[file,createHash('sha256').update(fs.readFileSync(path.join(base,file))).digest('hex')]));fs.writeFileSync(path.join(__dirname,'asset-entry-browser.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
