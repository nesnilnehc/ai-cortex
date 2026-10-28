const {chromium}=require('playwright');const fs=require('node:fs');const assert=require('node:assert/strict');
(async()=>{const browser=await chromium.launch();const report={date:new Date().toISOString(),matrix:[],errors:[]};
try{const page=await browser.newPage();page.on('pageerror',e=>report.errors.push(e.message));await page.goto('http://127.0.0.1:8765/experiments/direction-planning/');
await page.locator('#help-perspective').selectOption('evidence');assert.match(await page.locator('#perspective-preview').textContent(),/成果/);assert.equal(await page.locator('#detail-panel').getAttribute('data-open'),'false');
for(const width of [360,390,1024,1280,1440])for(const theme of ['light','dark']){
 await page.setViewportSize({width,height:1000});await page.locator('#theme').selectOption(theme);await page.locator('[data-node="design"]').click();
 await page.locator('#edit-request').evaluate(el=>el.open=true);await page.locator('#request-text').fill('preserve this edited request');const skills=await page.locator('#node-tools').textContent();
 for(const lens of ['work','evidence']){
  await page.locator('#help-perspective').selectOption(lens);
  assert.equal(await page.locator('.panel-body').evaluate(el=>el.scrollTop),0,'Changed explanation must be visible');
  assert.equal(await page.locator('#detail-title').textContent(),lens==='work'?'把事情说清楚':'需求、设计与任务');
  assert.equal(await page.locator('.relations-canvas').getAttribute('data-perspective'),lens);
  assert.equal(await page.locator('[data-node="design"] strong').textContent(),lens==='work'?'把事情说清楚':'需求、设计与任务');
  assert.equal(await page.locator('[data-edge="build-quality"] text').textContent(),lens==='work'?'修复后复核':'实现与检查依据');
  const endMarker=await page.locator('[data-edge="build-quality"] path').evaluate(el=>getComputedStyle(el).markerEnd);assert.ok(endMarker.includes(lens==='work'?'loop-arrow':'reference-end'));
  const boundary=await page.locator('.work-boundary').evaluate(el=>getComputedStyle(el).borderTopStyle);assert.equal(boundary,lens==='work'?'solid':'dashed');
  assert.doesNotMatch(await page.locator('#work-help').textContent(),/[点线面]：/);
assert.equal(await page.locator('[data-node="design"]').getAttribute('aria-pressed'),'true');assert.equal(await page.locator('#request-text').inputValue(),'preserve this edited request');assert.equal(await page.locator('#node-tools').textContent(),skills);
  assert.match(await page.locator('#work-help').textContent(),lens==='work'?/审查一份已有需求/:/需求文档/);
  assert.equal(await page.locator('.relations-canvas').count(),1);assert.equal(await page.locator('#detail-panel').count(),1);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  const copy=await page.locator('#copy-request').boundingBox();assert.ok(copy.y>=0&&copy.y+copy.height<=1000,`${width}/${lens}: copy visibility`);
 }
 await page.screenshot({path:__dirname+`/lenses-${width}-${theme}.png`,fullPage:true});
 await page.locator('#detail-panel').press('Escape');assert.equal(await page.locator('[data-node="design"]').evaluate(el=>document.activeElement===el),true);
 report.matrix.push({width,theme,bothLenses:true,requestPreserved:true,skillScopePreserved:true,oneMap:true,overflow:false,copyVisible:true});
}
await page.setViewportSize({width:1440,height:1000});await page.locator('#help-perspective').focus();assert.equal(await page.locator('#help-perspective').evaluate(el=>document.activeElement===el),true);await page.locator('#help-perspective').selectOption('work');
await page.locator('[data-node="design"]').click();await page.locator('.scenario-boundary>summary').click();assert.match(await page.locator('#ordinary-help').innerText(),/直接补充需求文档/);await page.locator('.scenario-boundary>details>summary').click();assert.equal(await page.locator('#asset-help dt').count(),4);
await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:text=>new Promise(resolve=>{window.resolveCopy=resolve;window.captured=text})}}));
await page.locator('#copy-request').click();await page.locator('#help-perspective').selectOption('evidence');await page.evaluate(()=>window.resolveCopy());await page.locator('#copy-feedback').filter({hasText:'已复制，可以'}).waitFor();
await page.locator('[data-node="planning"]').click();assert.match(await page.locator('#work-help').textContent(),/修订依据/);
assert.deepEqual(report.errors,[]);report.limitations=['Native select popup arrow-key selection could not be exercised by this headless runtime; no native-popup keyboard pass claimed.'];report.status='passed';report.extra=['Empty selection keeps the map unselected','Perspective selector exposes its label and accepts focus','Scenario boundary and four asset types remain disclosed','Changing perspective preserves the in-flight copy and request context','Perspective persists across work selection'];
}catch(e){report.status='failed';report.error=e.stack;throw e}finally{fs.writeFileSync(__dirname+'/lenses-browser.json',JSON.stringify(report,null,2)+'\n');await browser.close()}})().catch(e=>{console.error(e);process.exitCode=1});
