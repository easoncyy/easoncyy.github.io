document.addEventListener('DOMContentLoaded', () => {
  const entries = [...document.querySelectorAll('.log-entry')];
  const search = document.getElementById('log-search');
  if (!search) return;
  const update = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    entries.forEach(entry => {
      entry.hidden = !entry.textContent.toLocaleLowerCase().includes(query);
      if (!entry.hidden) count++;
    });
    document.getElementById('log-count').textContent = `${count} / ${entries.length} entries · newest first`;
    document.getElementById('log-empty').hidden = count !== 0;
  };
  search.addEventListener('input', update);
  update();
});
