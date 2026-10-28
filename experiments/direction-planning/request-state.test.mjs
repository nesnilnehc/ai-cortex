import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRequestState} from './request-state.mjs';
test('same node selection retains the edited request; different selection invalidates copies',()=>{
 const state=createRequestState();assert.equal(state.select('planning'),true);
 const copy=state.begin('my edited request');assert.equal(state.begin('duplicate'),null);
 assert.equal(state.select('planning'),false);assert.equal(state.finish(copy),true);
 const stale=state.begin('old request');assert.equal(state.select('direction'),true);
 const current=state.begin('new request');assert.equal(state.finish(stale),false);
 assert.equal(state.begin('duplicate'),null);assert.equal(state.finish(current),true);
});
test('close and reopen invalidate a late copy of the same node',()=>{
 const state=createRequestState();state.select('planning');const old=state.begin('old');
 state.clear();state.select('planning');assert.equal(state.finish(old),false);
 const fresh=state.begin('fresh');assert.equal(fresh.text,'fresh');assert.equal(state.finish(fresh),true);
});
test('editing the same context invalidates a pending copy without changing selection',()=>{
 const state=createRequestState();state.select('planning');const old=state.begin('before edit');
 state.edit();assert.equal(state.finish(old),false);assert.equal(state.select('planning'),false);
 const fresh=state.begin('after edit');assert.equal(state.finish(fresh),true);
});
