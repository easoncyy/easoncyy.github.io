document.addEventListener('DOMContentLoaded', () => {
  const entries = [...document.querySelectorAll('.log-entry')];
  const search = document.getElementById('log-search');
  const buttons = [...document.querySelectorAll('[data-log-type]')];
  if (!search) return;
  let kind = 'all';
  const update = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    entries.forEach(entry => {
      entry.hidden = !((kind === 'all' || entry.dataset.logKind === kind) && entry.textContent.toLocaleLowerCase().includes(query));
      if (!entry.hidden) count++;
    });
    document.getElementById('log-count').textContent = `${count} / ${entries.length} entries · newest first`;
    document.getElementById('log-empty').hidden = count !== 0;
  };
  buttons.forEach(button => button.addEventListener('click', () => {
    kind = button.dataset.logType;
    buttons.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
    update();
  }));
  search.addEventListener('input', update);
  update();
});
