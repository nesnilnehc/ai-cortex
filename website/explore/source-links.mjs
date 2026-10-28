import manifest from './source-manifest.json?v=aic08-provenance-2' with {type:'json'};
if(!/^https:\/\/github\.com\/nesnilnehc\/ai-cortex$/.test(manifest.repositoryUrl)||!/^[a-f0-9]{40}$/.test(manifest.assetsRevision))throw Error('Invalid canonical source manifest');
export function sourceUrl(path,fragment=''){
 if(typeof path!=='string'||! /^(skills|specs|protocols|rules)\//.test(path)||path.split('/').some(part=>!part||part==='.'||part==='..')||/[\\%?#\u0000-\u001f]/u.test(path))throw Error(`Invalid source path: ${path}`);
 return `${manifest.repositoryUrl}/blob/${manifest.assetsRevision}/${path.split('/').map(encodeURIComponent).join('/')}${fragment?'#'+encodeURIComponent(fragment):''}`;
}
