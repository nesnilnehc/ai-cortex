// Covers: AIC-REQ-04 A13-A15; native navigation, support and Chinese identity presentation.
const {chromium}=require('playwright'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
(async()=>{const browser=await chromium.launch(),report={localOnly:true,date:new Date().toISOString(),browser:browser.version(),matrix:[],errors:[]};try{
 for(const locale of ['zh','en'])for(const width of [360,390,1024,1280,1440])for(const theme of ['light','dark']){
  const p=await browser.newPage({viewport:{width,height:width<768?844:1000}});p.on('pageerror',e=>report.errors.push(e.message));
  const home=locale==='zh'?'/zh.html?lang=zh':'/?lang=en';await p.goto('http://127.0.0.1:4174'+home+'#skills');await p.locator('#theme').selectOption(theme);
  assert.equal(await p.locator('[data-site-destination=directory]').getAttribute('aria-current'),'location');
  await p.locator('[data-alternate-language]').click();assert.match(p.url(),/#skills$/);await p.locator('[data-alternate-language]').click();assert.match(p.url(),/#skills$/);
  await p.locator('[data-site-destination=start]').click();assert.equal(await p.locator('[data-site-destination=start]').getAttribute('aria-current'),'location');await p.goBack();assert.equal(await p.locator('[data-site-destination=directory]').getAttribute('aria-current'),'location');
  await p.locator('[data-site-destination=overview]').focus();await p.keyboard.press('Enter');await p.locator('.topic-toggle').first().waitFor();assert.equal(await p.locator('[data-site-destination=overview]').getAttribute('aria-current'),'page');assert.equal(await p.locator('[data-support-scope]').count(),2);
  await p.locator('[data-support-scope=foundation]').click();assert.ok(await p.locator('[data-support-target]').count()>2);await p.locator('[data-support-target=build]').click();assert.equal(await p.locator('[data-node=build]').getAttribute('aria-pressed'),'true');await p.locator('#close-panel').click();
  await p.locator('#find-tools').click();await p.locator('#tool-search').fill(locale==='zh'?'审查需求':'review-requirements');await p.locator('[data-tool=review-requirements]').click();assert.match(await p.locator('#detail-title').textContent(),/review-requirements/);if(locale==='zh'){assert.match(await p.locator('#detail-title').textContent(),/审查需求/);assert.equal(await p.locator('[data-skill=review-requirements] .skill-display-name').textContent(),'审查需求');}
  assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);await p.locator('#close-panel').focus();await p.keyboard.press('Enter');assert.equal(await p.locator('#detail-panel').getAttribute('data-open'),'false');
  await p.screenshot({path:path.join(__dirname,`evidence/revision/${locale}-${width}-${theme}.png`)});report.matrix.push({locale,width,theme,navigation:true,history:true,languageTypeAnchor:true,support:true,localizedName:true,noOverflow:true,keyboard:true});await p.close();
 }
 for(const locale of ['en','zh']){
  const p=await browser.newPage({javaScriptEnabled:false});const file=locale==='zh'?'zh.html':'';await p.goto(`http://127.0.0.1:4174/explore/${file}?lang=${locale}`);assert.equal(await p.locator('[data-site-destination]').count(),4);await p.locator('[data-site-destination=directory]').click();assert.match(p.url(),/#capabilities$/);assert.equal(await p.locator('#skills').count(),1);assert.equal(await p.locator('[aria-current]').count(),0);await p.close();
 }
 assert.deepEqual(report.errors,[]);report.status='passed';
}catch(e){report.status='failed';report.error=e.stack;throw e;}finally{fs.writeFileSync(path.join(__dirname,'evidence/revision/site-revision-browser.json'),JSON.stringify(report,null,2)+'\n');await browser.close();}})().catch(e=>{console.error(e);process.exitCode=1});
