document.addEventListener('DOMContentLoaded',()=>{
  const entries=[...document.querySelectorAll('.blog-entry')].map(el=>({el,...JSON.parse(el.dataset.record)}));
  let path=[],tag='',page=1;
  const search=document.querySelector('#blog-search');
  const sidebar=document.querySelector('.blog-directory');
  const desktopSlot=document.querySelector('.blog-layout');
  const mobileSlot=document.querySelector('#blog-mobile-directory');
  const mobile=window.matchMedia('(max-width: 800px)');
  const searchBlock=document.querySelector('.blog-search-block');
  const titleBlock=document.querySelector('#title-block-header');
  const tools=document.querySelector('.blog-tools');
  const positionDirectory=()=>{
    (mobile.matches?mobileSlot:desktopSlot).append(sidebar);
    if(mobile.matches)tools.insertBefore(searchBlock,mobileSlot);
    else titleBlock.append(searchBlock);
  };
  mobile.addEventListener('change',positionDirectory);positionDirectory();
  const button=(label,active,action)=>{const b=document.createElement('button');b.type='button';b.textContent=label;b.setAttribute('aria-pressed',String(active));b.addEventListener('click',action);return b;};
  const inside=e=>path.every((p,i)=>e.path[i]===p);
  function render(){
    const controls=document.querySelector('#blog-paths');controls.replaceChildren();
    const crumbs=document.createElement('div');crumbs.className='directory-buttons';
    crumbs.append(button('全部文章',!path.length,()=>{path=[];page=1;render();}));
    controls.append(crumbs);
    const roots=['MATH','CS','AI','PHILOSOPHY','OTHER'];
    entries.forEach(e=>{if(!roots.includes(e.path[0]))roots.push(e.path[0]);});
    const rootList=document.createElement('div');rootList.className='directory-root-list';
    function addBranch(parent, prefix, names){
      names.forEach(name=>{
        const current=[...prefix,name];
        const members=entries.filter(e=>current.every((part,i)=>e.path[i]===part));
        const children=[...new Set(members.map(e=>e.path[current.length]).filter(Boolean))].sort();
        const selected=current.every((part,i)=>path[i]===part);
        const node=document.createElement('div');node.className='directory-node';
        const control=button(name+'/ · '+members.length,selected,()=>{
          path=selected&&path.length===current.length?prefix:current;
          page=1;render();
        });
        if(children.length)control.setAttribute('aria-expanded',String(selected));
        node.append(control);
        if(selected&&children.length){
          const nested=document.createElement('div');nested.className='directory-children';
          addBranch(nested,current,children);node.append(nested);
        }
        parent.append(node);
      });
    }
    addBranch(rootList,[],roots);
    controls.append(rootList);
    const tags=document.querySelector('#blog-tags');tags.replaceChildren();
    tags.append(button('全部标签',!tag,()=>{tag='';page=1;render();}));
    [...new Set(entries.flatMap(e=>e.tags))].sort().forEach(t=>tags.append(button('#'+t,tag===t,()=>{tag=tag===t?'':t;page=1;render();})));
    const query=search.value.trim().toLocaleLowerCase();
    const matches=entries.filter(e=>inside(e)&&(!tag||e.tags.includes(tag))&&[e.title,e.description,...e.tags,...e.path].join(' ').toLocaleLowerCase().includes(query));
    const pages=Math.max(1,Math.ceil(matches.length/10));page=Math.min(page,pages);
    entries.forEach(e=>e.el.hidden=true);matches.slice((page-1)*10,page*10).forEach(e=>e.el.hidden=false);
    document.querySelector('#blog-count').textContent=matches.length+' entries / 篇文章';document.querySelector('#blog-empty').hidden=matches.length>0;
    const pager=document.querySelector('#blog-pages');pager.replaceChildren();if(pages>1)for(let i=1;i<=pages;i++)pager.append(button(String(i),i===page,()=>{page=i;render();}));
  }
  search.addEventListener('input',()=>{page=1;render();});render();
});
