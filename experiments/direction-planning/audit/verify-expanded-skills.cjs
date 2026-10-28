const {chromium}=require('playwright');const fs=require('node:fs');const path=require('node:path');const assert=require('node:assert/strict');const {createHash}=require('node:crypto');
const base=path.resolve(__dirname,'..'),catalog=JSON.parse(fs.readFileSync(path.join(base,'catalog.json'))),guides=JSON.parse(fs.readFileSync(path.join(base,'skill-guidance.json'))),edges=JSON.parse(fs.readFileSync(path.join(base,'skill-edges.json')));
(async()=>{const browser=await chromium.launch();const report={date:new Date().toISOString(),browser:browser.version(),matrix:[],skills:[],errors:[]};try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}});page.on('pageerror',e=>report.errors.push(e.message));await page.goto('http://127.0.0.1:8765/experiments/direction-planning/');
 await page.locator('.skill-node').first().waitFor({state:'visible',timeout:1500});
 assert.deepEqual((await page.locator('.skill-node').evaluateAll(elements=>elements.map(el=>el.dataset.skill))).sort(),catalog.map(x=>x.id).sort());
 assert.equal(await page.locator('#node-asset-select').count(),0);assert.equal(await page.locator('#help-perspective').count(),0);
 for(const {id} of catalog){
  const button=page.locator(`.skill-node[data-skill="${id}"]`);assert.equal(await button.isVisible(),true);
  await button.click();assert.deepEqual(await page.locator('#selected-tool-guide dd').allTextContents(),['when','provide','use','result'].map(key=>guides[id][key]));
  const expected=edges.filter(edge=>edge.from===id||edge.to===id),related=[...new Set(expected.map(edge=>edge.from===id?edge.to:edge.from))].sort();
  assert.deepEqual((await page.locator('.skill-node[data-related="true"]').evaluateAll(els=>els.map(el=>el.dataset.skill))).sort(),related);
  assert.equal(await page.locator('#panel-relations-button').getAttribute('data-count'),String(expected.length));
  await page.locator('#panel-relations-button').click();assert.equal(await page.locator('#skill-relations [data-relation]').count(),expected.length);
  if(!expected.length)assert.match(await page.locator('#skill-relations').textContent(),/未标出|没有/);
  await page.locator('#close-panel').click();assert.equal(await button.evaluate(el=>el===document.activeElement),true);
  report.skills.push({id,visibleByDefault:true,guide:true,relations:expected.length});
 }
 for(const [width,height] of [[360,667],[390,844],[1024,768],[1280,800],[1440,1000]])for(const theme of ['light','dark']){
  await page.setViewportSize({width,height});await page.locator('#theme').selectOption(theme);
  assert.equal(await page.locator('.skill-node:visible').count(),70);assert.equal(await page.locator('.relations-canvas').count(),1);
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  const button=page.locator('.skill-node[data-skill="prepare-release"]');await button.focus();await page.keyboard.press('Enter');
  assert.match(await page.locator('#selected-tool-purpose').textContent(),/发布/);await page.locator('#panel-relations-button').click();assert.equal(await page.locator('#skill-relations [data-relation]').count(),2);
  if(width<1200){const nodeBox=await button.boundingBox(),panelBox=await page.locator('#detail-panel').boundingBox();assert.ok(nodeBox.y>=0&&nodeBox.y+nodeBox.height<=panelBox.y,`${width}: selected node remains above sheet`);}
  await page.locator('#detail-panel').press('Escape');assert.equal(await button.evaluate(el=>el===document.activeElement),true);
  report.matrix.push({width,height,theme,allSkillsDisplayed:true,oneGraph:true,overflow:false,keyboardSelection:true,focusReturned:true});
 }
 await page.setViewportSize({width:1440,height:1000});await page.locator('.skill-node[data-skill="prepare-release"]').click();await page.locator('#panel-relations-button').click();await page.locator('[data-peer="publish-release"]').click();assert.equal(await page.locator('.skill-node[data-skill="publish-release"]').getAttribute('aria-pressed'),'true');assert.match(await page.locator('#selected-tool-purpose').textContent(),/正式发布/);await page.locator('#close-panel').click();
 await page.setViewportSize({width:1440,height:1000});await page.locator('.skill-node[data-skill="prepare-release"]').click();await page.locator('#panel-work-button').click();await page.locator('#edit-request').evaluate(el=>el.open=true);await page.locator('#request-text').fill('保留本次发布范围');await page.locator('.skill-node[data-skill="publish-release"]').click();await page.locator('#panel-work-button').click();assert.equal(await page.locator('#request-text').inputValue(),'保留本次发布范围');
 await page.locator('#close-panel').click();await page.locator('#find-tools').click();await page.locator('#tool-search').fill('review-roadmap');assert.equal(await page.locator('[data-tool="review-roadmap"]').evaluate(el=>el.closest('.tool-group').dataset.group),'planning');await page.locator('[data-tool="review-roadmap"]').click();assert.equal(await page.locator('.skill-node[data-skill="review-roadmap"]').getAttribute('aria-pressed'),'true');
 for(const width of [390,1440]){await page.locator('#close-panel').click();await page.setViewportSize({width,height:width===390?844:1000});await page.locator('#theme').selectOption('light');await page.locator('.skill-node[data-skill="prepare-release"]').click();await page.locator('#panel-relations-button').click();await page.screenshot({path:path.join(__dirname,`expanded-skills-${width}.png`)});}
 await page.locator('#close-panel').click();await page.setViewportSize({width:1440,height:1000});await page.evaluate(()=>window.scrollTo(0,0));await page.screenshot({path:path.join(__dirname,'expanded-skills-overview.png')});
 assert.deepEqual(report.errors,[]);report.status='passed';
 }catch(e){report.status='failed';report.error=e.stack;throw e;}finally{report.sourceHashes=Object.fromEntries(['index.html','story.mjs','workspace.css','skill-graph.mjs','panel-model.mjs','workflow.mjs','relations.mjs','story-model.mjs','skill-guidance.json','skill-edges.json','audit/verify-expanded-skills.cjs'].map(file=>[file,createHash('sha256').update(fs.readFileSync(path.join(base,file))).digest('hex')]));fs.writeFileSync(path.join(__dirname,'expanded-skills-browser.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});
