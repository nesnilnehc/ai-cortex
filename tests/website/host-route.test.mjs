// Covers: AIC-REQ-04 A13/QAS-06; observed static-host clean-URL compatibility.
import {test} from 'node:test';
import assert from 'node:assert/strict';
import {getActiveDestination,getAlternateDestination} from '../../website/site-navigation.mjs';
test('provider-normalized home and legacy paths preserve existing section contracts',()=>{
 for(const [alias,canonical]of[['/zh','/zh.html'],['/index','/index.html'],['/explore/zh','/explore/zh.html'],['/explore/index','/explore/index.html']]){
  for(const hash of ['','#capabilities','#asset-directory','#skills','#start'])assert.equal(getActiveDestination(alias,hash),getActiveDestination(canonical,hash));
  assert.equal(getAlternateDestination(alias,'#capabilities','en','relations'),getAlternateDestination(canonical,'#capabilities','en','relations'));
 }
});
test('unknown paths are still rejected rather than treated as a homepage',()=>{
 for(const path of ['/unknown','/zh-unrelated','/explore-other','/__proto__'])assert.throws(()=>getActiveDestination(path,'#capabilities'));
});
