const link=document.querySelector('#legacy-capability-link'),target=new URL(link.href),current=new URL(location.href);
for(const [key,value]of current.searchParams)if(!['lang','view'].includes(key))target.searchParams.set(key,value);
location.replace(target.href);
