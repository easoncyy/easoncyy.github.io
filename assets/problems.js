document.addEventListener('DOMContentLoaded',()=>{
  const index=JSON.parse(document.querySelector('#problem-index').textContent);
  const days=[...document.querySelectorAll('.problem-day')];
  const questions=[...document.querySelectorAll('.problem-entry')].map(el=>({el,...JSON.parse(el.dataset.problem)}));
  const category=document.querySelector('#problem-category'),tag=document.querySelector('#problem-tag');
  let categoryPath=[];
  const today=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  const query=new URLSearchParams(location.search);
  const valid=d=>/^\d{4}-\d{2}-\d{2}$/.test(d)&&!Number.isNaN(Date.parse(d+'T00:00:00Z'));
  let selected=valid(query.get('date')||'')?query.get('date'):(index.dates[today]?today:Object.keys(index.dates).sort().at(-1)||today);
  let [year,month]=selected.split('-').map(Number);
  const option=(select,value,label)=>{const o=document.createElement('option');o.value=value;o.textContent=label;select.append(o);};
  [...new Set(questions.flatMap(q=>q.tags))].sort().forEach(t=>option(tag,t,t));
  function drawCategories(){
    category.replaceChildren();
    document.querySelector('#problem-category-label').textContent=categoryPath.join(' / ')||'全部';
    const button=(label,active,action)=>{const b=document.createElement('button');b.type='button';b.textContent=label;b.setAttribute('aria-pressed',String(active));b.addEventListener('click',action);return b;};
    category.append(button('全部分类',!categoryPath.length,()=>{categoryPath=[];drawCategories();showDay();}));
    function branch(parent,prefix){
      const members=questions.filter(q=>prefix.every((p,i)=>q.path[i]===p));
      const names=[...new Set(members.map(q=>q.path[prefix.length]).filter(Boolean))].sort();
      names.forEach(name=>{
        const current=[...prefix,name];const active=current.every((p,i)=>categoryPath[i]===p);
        const children=members.filter(q=>q.path[prefix.length]===name);
        const expandable=children.some(q=>q.path.length>current.length);
        const node=document.createElement('div');node.className='problem-category-node';
        const control=button(name+'/',active,()=>{categoryPath=active&&categoryPath.length===current.length?prefix:current;drawCategories();showDay();});
        if(expandable)control.setAttribute('aria-expanded',String(active));node.append(control);
        if(active&&expandable){const nested=document.createElement('div');nested.className='directory-children';branch(nested,current);node.append(nested);}
        parent.append(node);
      });
    }
    const roots=document.createElement('div');roots.className='directory-root-list';branch(roots,[]);category.append(roots);
  }
  function showDay(resetAnswers=false){
    days.forEach(el=>el.hidden=el.dataset.date!==selected);
    if(resetAnswers)document.querySelectorAll('.problem-answer').forEach(el=>el.open=false);
    let count=0;
    questions.forEach(q=>{
      const prefix=categoryPath;
      q.el.hidden=!prefix.every((p,i)=>q.path[i]===p)||Boolean(tag.value&&!q.tags.includes(tag.value));
      if(!q.el.hidden&&q.el.closest('.problem-day').dataset.date===selected)count++;
    });
    document.querySelector('#problem-empty').hidden=count>0;
    document.querySelector('.problem-initial-empty')?.setAttribute('hidden','');
    document.querySelector('#problem-status').textContent=selected+' · '+count+' 道题';
  }
  function calendar(){
    document.querySelector('#calendar-month').textContent=`${year} / ${String(month).padStart(2,'0')}`;
    const grid=document.querySelector('#calendar-grid');grid.replaceChildren();
    const offset=(new Date(Date.UTC(year,month-1,1)).getUTCDay()+6)%7;
    for(let i=0;i<offset;i++){const blank=document.createElement('span');blank.setAttribute('aria-hidden','true');grid.append(blank);}
    const total=new Date(Date.UTC(year,month,0)).getUTCDate();
    for(let d=1;d<=total;d++){
      const date=`${year}-${String(month).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
      const b=document.createElement('button');b.type='button';b.className='calendar-day';
      const label=document.createElement('span');label.textContent=d;b.append(label);
      const count=index.dates[date]||0;
      if(count){const n=document.createElement('small');n.textContent=count+' 题';b.append(n);b.classList.add('has-problems');}
      b.setAttribute('aria-label',date+'，'+count+' 道题');b.setAttribute('aria-pressed',String(date===selected));
      if(date===today)b.setAttribute('aria-current','date');
      b.disabled=date>today;
      b.addEventListener('click',()=>{selected=date;const url=new URL(location.href);url.searchParams.set('date',date);history.replaceState(null,'',url);showDay(true);calendar();});
      grid.append(b);
    }
  }
  for(const id of ['prev','next'])document.querySelector('#calendar-'+id).addEventListener('click',()=>{const date=new Date(Date.UTC(year,month-1+(id==='prev'?-1:1),1));year=date.getUTCFullYear();month=date.getUTCMonth()+1;calendar();});
  document.querySelector('#calendar-today').addEventListener('click',()=>{selected=today;[year,month]=today.split('-').map(Number);const url=new URL(location.href);url.searchParams.set('date',today);history.replaceState(null,'',url);showDay(true);calendar();});
  tag.addEventListener('change',()=>showDay());
  document.querySelector('#problem-filter-reset').addEventListener('click',()=>{categoryPath=[];tag.value='';drawCategories();showDay();});
  drawCategories();showDay();calendar();
});
