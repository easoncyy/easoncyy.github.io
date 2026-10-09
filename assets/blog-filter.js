document.addEventListener('DOMContentLoaded',()=>{
  const entries=[...document.querySelectorAll('.blog-entry')].map(el=>({el,...JSON.parse(el.dataset.record)}));
  let path=[],tag='',page=1;
  const search=document.querySelector('#blog-search');
  const button=(label,active,action)=>{const b=document.createElement('button');b.type='button';b.textContent=label;b.setAttribute('aria-pressed',String(active));b.addEventListener('click',action);return b;};
  const inside=e=>path.every((p,i)=>e.path[i]===p);
  function render(){
    const controls=document.querySelector('#blog-paths');controls.replaceChildren();
    const crumbs=document.createElement('div');crumbs.className='directory-buttons';
    crumbs.append(button('~/notes/blog',!path.length,()=>{path=[];page=1;render();}));
    path.forEach((p,i)=>crumbs.append(button('/ '+p,i===path.length-1,()=>{path=path.slice(0,i+1);page=1;render();})));
    controls.append(crumbs);
    const children=new Set(entries.filter(inside).map(e=>e.path[path.length]).filter(Boolean));
    if(!path.length) ['MATH','CS','AI','PHILOSOPHY','OTHER'].forEach(p=>children.add(p));
    const level=document.createElement('div');level.className='directory-buttons';
    [...children].sort().forEach(p=>level.append(button(p+'/ · '+entries.filter(e=>inside(e)&&e.path[path.length]===p).length,false,()=>{path=[...path,p];page=1;render();})));
    controls.append(level);
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
