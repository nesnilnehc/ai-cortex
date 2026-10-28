/* Selection/copy identity only; the textarea remains the single owner of edited text. */
export function createRequestState(){
 let node=null,version=0,pending=null;
 return {
  select(id){if(node===id)return false;node=id;version++;pending=null;return true;},
  edit(){version++;pending=null;},
  clear(){node=null;version++;pending=null;},
  begin(text){if(!node||pending)return null;pending=Object.freeze({node,version,text});return pending;},
  finish(token){if(pending!==token||token.version!==version||token.node!==node)return false;pending=null;return true;}
 };
}
