/* Run with NODE_PATH pointing at an existing local Playwright installation. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const out=__dirname;
const url='http://127.0.0.1:8765/experiments/direction-planning/';
(async()=>{
 const browser=await chromium.launch({headless:true});
 const report={date:new Date().toISOString(),browser:await browser.version(),matrix:[],checks:[],consoleErrors:[],remoteRequests:[]};
 try{
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 await context.grantPermissions(['clipboard-read','clipboard-write']);
 const page=await context.newPage();page.on('pageerror',e=>report.consoleErrors.push(e.message));
 page.on('request',r=>{if(!r.url().startsWith('http://127.0.0.1:8765/'))report.remoteRequests.push(r.url())});
 await page.goto(url);await page.locator('#catalog-count').filter({hasText:'全部'}).waitFor({state:'attached'});
 for(const width of [360,390,1024,1280,1440])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height:1000});await page.locator('#theme').selectOption(theme);
  await page.locator('[data-node="planning"]').click();
  await page.locator('#edit-request summary').click();await page.locator('#request-text').fill('matrix draft');
  await page.locator('#copy-request').click();await page.locator('#copy-feedback').filter({hasText:'已复制，可以'}).waitFor();
  assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),'matrix draft');
  const result=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,panel:document.querySelector('#detail-panel').getBoundingClientRect().toJSON(),copy:document.querySelector('#copy-request').getBoundingClientRect().toJSON(),close:document.querySelector('#close-panel').getBoundingClientRect().toJSON(),title:document.querySelector('#detail-title').textContent}));
  assert.equal(result.overflow,false,`${width}/${theme}: overflow`);
  assert.ok(result.copy.y>=0&&result.copy.bottom<=1000,`${width}/${theme}: copy outside viewport`);
  assert.ok(result.close.y>=0&&result.close.bottom<=1000,`${width}/${theme}: close outside viewport`);
  await page.locator('#detail-panel').press('Escape');assert.equal(await page.locator('[data-node="planning"]').evaluate(el=>el===document.activeElement),true);
  for(const node of ['direction','planning','design','build','quality','commit','release','research','foundation','collaboration']){
   await page.locator(`[data-node="${node}"]`).click();assert.equal(await page.locator('#detail-panel').getAttribute('data-open'),'true');
   if(['planning','design','build','quality','release'].includes(node)){await page.locator('#try-example').click();assert.equal(await page.locator('#try-example').getAttribute('aria-pressed'),'true');await page.locator('#try-example').click();}
   await page.locator('#detail-panel').press('Escape');
   await page.locator(`[data-node="${node}"]`).focus();await page.keyboard.press('Enter');assert.equal(await page.locator('#detail-panel').getAttribute('data-open'),'true');
   await page.locator('#close-panel').click();assert.equal(await page.locator(`[data-node="${node}"]`).evaluate(el=>el===document.activeElement),true);
  }
  // Keyboard-driven search and empty/result recovery in the actual modal.
  await page.locator('[data-node="planning"]').click();await page.locator('#find-tools').click();
  await page.locator('#tool-search').fill('not-a-real-skill-xyz');await page.locator('#no-tools').waitFor({state:'visible'});
  await page.locator('#clear-tools').click();await page.locator('#tool-search').fill('commit-work');
  await page.locator('[data-tool="commit-work"]').focus();await page.keyboard.press('Enter');
  assert.equal(await page.locator('#detail-title').textContent(),'保存与整合');
  await page.locator('#find-tools').click();await page.locator('#tool-search').fill('Python');await page.keyboard.press('Escape');
  assert.equal(await page.locator('#tools').evaluate(el=>el.open),false);assert.equal(await page.locator('#detail-title').textContent(),'保存与整合');
  assert.equal(await page.locator('#find-tools').evaluate(el=>el===document.activeElement),true);
  await page.keyboard.press('Escape');await page.locator('[data-node="planning"]').click();
  await page.screenshot({path:path.join(out,`req03-${width}-${theme}.png`),fullPage:true});
  report.matrix.push({width,theme,overflow:false,allNodesPointerAndKeyboard:true,examplesToggle:true,copyRoundTrip:true,copyAndCloseVisible:true,searchEmptyResultEscape:true});
  await page.locator('#detail-panel').press('Escape');
 }
 await page.setViewportSize({width:1440,height:1000});await page.locator('[data-node="planning"]').click();
 await page.locator('#edit-request summary').click();await page.locator('#request-text').fill('custom edited text');
 await page.locator('[data-node="planning"]').click();assert.equal(await page.locator('#request-text').inputValue(),'custom edited text');
 await page.locator('[data-node="direction"]').click();assert.notEqual(await page.locator('#request-text').inputValue(),'custom edited text');
 assert.match(await page.locator('#copy-feedback').textContent(),/默认请求已更新/);
 report.checks.push('same-node preserves edited text; different-node replacement announces context');
 for(const mode of ['absent','reject','deferred']){
  const copyPage=await context.newPage();await copyPage.goto(url);await copyPage.locator('[data-node="planning"]').click();
  await copyPage.locator('#edit-request summary').click();await copyPage.locator('#request-text').fill('selected request');
  await copyPage.evaluate(mode=>{window.copyCalls=0;Object.defineProperty(navigator,'clipboard',{configurable:true,value:mode==='absent'?undefined:{writeText:text=>{window.copyCalls++;window.copiedText=text;return mode==='reject'?Promise.reject(Error('denied')):new Promise((resolve,reject)=>{window.resolveCopy=resolve;window.rejectCopy=reject})}}})},mode);
  await copyPage.locator('#copy-request').click();
  if(mode!=='deferred'){
   await copyPage.locator('#copy-feedback').filter({hasText:'未能自动复制'}).waitFor();
   assert.equal(await copyPage.locator('#request-text').inputValue(),'selected request');
   assert.equal(await copyPage.locator('#request-text').evaluate(el=>el.selectionStart===0&&el.selectionEnd===el.value.length),true);
   assert.equal(await copyPage.locator('#copy-request').isEnabled(),true);
  }else{
   assert.equal(await copyPage.locator('#copy-request').isDisabled(),true);
   await copyPage.locator('#copy-request').dispatchEvent('click');assert.equal(await copyPage.evaluate(()=>window.copyCalls),1);
   await copyPage.locator('[data-node="direction"]').click();const fresh=await copyPage.locator('#request-text').inputValue();
   await copyPage.evaluate(()=>window.resolveCopy());assert.equal(await copyPage.locator('#request-text').inputValue(),fresh);
   assert.doesNotMatch(await copyPage.locator('#copy-feedback').textContent(),/已复制，可以/);
   // A text edit also invalidates an earlier copy of the same work context.
   await copyPage.locator('#edit-request summary').click();await copyPage.locator('#copy-request').click();
   await copyPage.locator('#request-text').fill('edited while copying');await copyPage.evaluate(()=>window.resolveCopy());
   assert.equal(await copyPage.locator('#request-text').inputValue(),'edited while copying');assert.doesNotMatch(await copyPage.locator('#copy-feedback').textContent(),/已复制，可以/);
   // A late rejection also must not open/edit the newly selected request.
   await copyPage.locator('#copy-request').click();await copyPage.locator('[data-node="planning"]').click();
   await copyPage.evaluate(()=>window.rejectCopy(Error('late')));assert.equal(await copyPage.locator('#edit-request').evaluate(el=>el.open),false);
  }
  report.checks.push(`clipboard ${mode}: recovery / selection isolation passed`);await copyPage.close();
 }
 await context.grantPermissions(['clipboard-read','clipboard-write']);
 await page.locator('#edit-request').evaluate(el=>el.open=true);await page.locator('#request-text').fill('REQ03 browser clipboard success');await page.locator('#copy-request').click();
 await page.locator('#copy-feedback').filter({hasText:'已复制，可以'}).waitFor();assert.equal(await page.evaluate(()=>navigator.clipboard.readText()),'REQ03 browser clipboard success');
 report.checks.push('real Chromium clipboard write/read success');
 await page.emulateMedia({reducedMotion:'reduce'});await page.locator('#detail-panel').press('Escape');
 await page.locator('[data-node="quality"]').focus();await page.keyboard.press('Enter');await page.locator('#quality-details summary').click();
 for(const state of ['pass','fail','missing']){await page.locator(`[data-result="${state}"]`).click();assert.equal(await page.locator('#detail-title').textContent(),'检查与修复')}
 await page.locator('#detail-panel').press('Escape');
 const focus=await page.locator('[data-node="quality"]').evaluate(el=>({active:el===document.activeElement,outline:getComputedStyle(el).outlineStyle}));assert.equal(focus.active,true);assert.notEqual(focus.outline,'none');
 await page.setViewportSize({width:720,height:500});await page.locator('[data-node="planning"]').click();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 const zoomCopy=await page.locator('#copy-request').boundingBox();assert.ok(zoomCopy.y>=0&&zoomCopy.y+zoomCopy.height<=500);
 report.checks.push('keyboard Enter/Escape, selected focus outline, reduced motion; 200% desktop zoom-equivalent 720x500 CSS viewport (not native browser zoom)');
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}});const fallback=await nojs.newPage();await fallback.goto(url);
 assert.equal(await fallback.locator('noscript a').getAttribute('href'),'../../skills/INDEX.md');assert.ok(await fallback.locator('noscript a').isVisible());
 assert.equal(await fallback.locator('[data-node="direction"]').innerText().then(x=>x.includes('方向与目标')),true);
 await fallback.screenshot({path:path.join(out,'req03-nojs.png'),fullPage:true});await nojs.close();report.checks.push('script-free readable labels and canonical catalogue fallback');
 const noArt=await context.newPage();await noArt.route('**/assets/work-stories.png',r=>r.abort());await noArt.goto(url);await noArt.locator('[data-node="direction"]').click();assert.equal(await noArt.locator('#detail-title').textContent(),'方向与目标');await noArt.close();report.checks.push('missing illustration retains selectable labels and contextual explanation');
 assert.deepEqual(report.consoleErrors,[]);assert.deepEqual(report.remoteRequests,[]);
 report.limitations=['Safari native automation and real mobile hardware not exercised','Screen-reader spoken output and human comprehension require owner/reviewer participation; no pass claimed'];
 report.status='passed';
 }catch(error){report.status='failed';report.error=error.stack;throw error}
 finally{fs.writeFileSync(path.join(out,'req03-browser.json'),JSON.stringify(report,null,2)+'\n');await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
