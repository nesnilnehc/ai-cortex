const {chromium}=require('playwright');
const fs=require('node:fs');
const assert=require('node:assert/strict');
const path=require('node:path');
const {createHash}=require('node:crypto');
const base=path.resolve(__dirname,'..');
const catalog=JSON.parse(fs.readFileSync(path.join(base,'catalog.json')));
const guidance=JSON.parse(fs.readFileSync(path.join(base,'skill-guidance.json')));
(async()=>{
 const browser=await chromium.launch();
 const report={date:new Date().toISOString(),skills:[],matrix:[],errors:[],browser:browser.version()};
 try{
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  page.on('pageerror',e=>report.errors.push(e.message));
  await page.goto('http://127.0.0.1:8765/experiments/direction-planning/');
  await page.locator('[data-node="planning"]').click();
  await page.locator('#recommended-tools details[data-skill="orchestrate-roadmap-planning"] > summary').click({timeout:1500});
  assert.equal(await page.locator('#recommended-tools [data-skill="orchestrate-roadmap-planning"] dl dt').count(),4);
  await page.locator('#help-perspective').selectOption('evidence');
  assert.equal(await page.locator('#recommended-tools [data-skill="orchestrate-roadmap-planning"]').evaluate(el=>el.open),true);
  // Exercise every skill from its actual graph context, not a parallel catalogue view.
  const seen=new Set();
  for(const node of ['direction','planning','design','build','quality','commit','release','research','foundation','collaboration']){
   await page.locator(`[data-node="${node}"]`).click();
   await page.locator('#all-node-tools > summary').click();
   for(const entry of await page.locator('#node-tools details[data-skill]').all()){
    const id=await entry.getAttribute('data-skill');
    await entry.locator(':scope > summary').click();
    const fields=await entry.locator('dl dd').allTextContents();
    assert.deepEqual(fields,['when','provide','use','result'].map(key=>guidance[id][key]));
    assert.equal(await entry.locator('dl').isVisible(),true);
    const source=entry.locator('.skill-source');
    const response=await page.request.get(new URL(await source.getAttribute('href'),page.url()).href);
    assert.equal(response.status(),200);
    assert.equal(createHash('sha256').update(await response.body()).digest('hex'),guidance[id].sourceHash);
    seen.add(id);report.skills.push({id,node,fourFieldsVisible:true,sourceVerified:true});
    await entry.locator(':scope > summary').click();
   }
  }
  assert.deepEqual([...seen].sort(),catalog.map(x=>x.id).sort());
  // Search is an optional entrance to the same panel and guidance.
  await page.locator('#close-panel').click();
  await page.locator('#find-tools').click();await page.locator('#tool-search').fill('commit-work');
  await page.locator('[data-tool="commit-work"]').click();
  assert.equal(await page.locator('#selected-tool dd').count(),4);
  assert.match(await page.locator('#selected-tool').innerText(),/不自动推送/);
  await page.locator('#edit-request').evaluate(el=>el.open=true);
  await page.locator('#request-text').fill('保留这段自定义请求');
  await page.locator('#help-perspective').selectOption('evidence');
  assert.equal(await page.locator('#request-text').inputValue(),'保留这段自定义请求');
  assert.equal(await page.locator('#selected-tool dd').count(),4);
  for(const width of [360,390,1024,1280,1440])for(const theme of ['light','dark']){
   await page.setViewportSize({width,height:1000});
   await page.locator('#theme').selectOption(theme);
   if(await page.locator('#close-panel').isVisible())await page.locator('#close-panel').click();
   await page.locator('[data-node="quality"]').focus();await page.keyboard.press('Enter');
   const summary=page.locator('#recommended-tools details[data-skill="orchestrate-code-review"] > summary');
   await summary.focus();await page.keyboard.press('Enter');
   assert.equal(await summary.evaluate(el=>el.parentElement.open),true);
   assert.equal(await page.locator('#recommended-tools [data-skill="orchestrate-code-review"] dd').count(),4);
   await page.locator('.panel-body').evaluate(el=>el.scrollTop=el.scrollHeight);
   const overflow=await page.evaluate(()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,offenders:[...document.querySelectorAll('body *')].map(el=>({tag:el.tagName,id:el.id,right:el.getBoundingClientRect().right,width:el.getBoundingClientRect().width})).filter(el=>el.right>innerWidth+1&&el.width>0).slice(-12)}));
   if(overflow.scroll>overflow.width){console.log(overflow);await page.screenshot({path:path.join(__dirname,'skill-guidance-overflow.png')});}
   assert.equal(overflow.scroll>overflow.width,false,`${width}/${theme}: overflow`);
   assert.equal(await page.locator('.relations-canvas').count(),1);
   const close=await page.locator('#close-panel').boundingBox();assert.ok(close.y>=0&&close.y+close.height<=1000);
   await page.keyboard.press('Escape');assert.equal(await page.locator('[data-node="quality"]').evaluate(el=>el===document.activeElement),true);
   report.matrix.push({width,theme,keyboardDisclosure:true,oneMap:true,overflow:false,closeReachable:true,focusReturned:true});
  }
  for(const width of [390,1440]){
   await page.setViewportSize({width,height:1000});await page.locator('#theme').selectOption('light');
   await page.locator('#find-tools').click();await page.locator('#tool-search').fill('prioritize-backlog');await page.locator('[data-tool="prioritize-backlog"]').click();
   assert.equal(await page.locator('.panel-body').evaluate(el=>el.scrollTop),0,'Selected usage starts at the panel top');
   await page.screenshot({path:path.join(__dirname,`skill-guidance-${width}.png`),fullPage:width>=1200});
  }
  assert.deepEqual(report.errors,[]);report.status='passed';
 }catch(error){report.status='failed';report.error=error.stack;throw error;}
 finally{
  const files=['index.html','story.mjs','workspace.css','skill-guidance.json','skill-guidance.mjs','skill-guidance.test.mjs','audit/verify-skill-guidance.cjs'];
  report.sourceHashes=Object.fromEntries(files.map(file=>[file,createHash('sha256').update(fs.readFileSync(path.join(base,file))).digest('hex')]));
  fs.writeFileSync(path.join(__dirname,'skill-guidance-browser.json'),JSON.stringify(report,null,2)+'\n');await browser.close();
 }
})().catch(error=>{console.error(error);process.exitCode=1;});
