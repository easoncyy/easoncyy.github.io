document.addEventListener('DOMContentLoaded',()=>{
  const inputs=[...document.querySelectorAll('[data-reading-key]')],defaults=inputs.map(i=>i.checked);
  inputs.forEach(input=>{
    const key='notes-reading-v1:'+input.dataset.readingKey;
    try{const saved=localStorage.getItem(key);if(saved!==null)input.checked=saved==='true';}catch(_){}
    input.addEventListener('change',()=>{try{localStorage.setItem(key,String(input.checked));}catch(_){}});
  });
  document.querySelector('#reading-reset')?.addEventListener('click',()=>inputs.forEach((input,i)=>{input.checked=defaults[i];try{localStorage.removeItem('notes-reading-v1:'+input.dataset.readingKey);}catch(_){}}));
});
