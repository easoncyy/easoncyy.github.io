document.addEventListener('DOMContentLoaded', () => {
  const buttons = [...document.querySelectorAll('[data-library-category]')];
  const entries = [...document.querySelectorAll('.library-entry')];
  const subjects = document.getElementById('library-subjects');
  if (!subjects) return;
  const academic = ['教材', '习题', '参考书'];
  let category = 'all';
  let subject = 'all';
  const update = () => {
    let count = 0;
    entries.forEach(entry => {
      entry.hidden = !((category === 'all' || entry.dataset.category === category) &&
        (subject === 'all' || entry.dataset.subject === subject));
      if (!entry.hidden) count++;
    });
    document.getElementById('library-count').textContent = `${count} / ${entries.length} books`;
    const empty = document.getElementById('library-empty');
    empty.hidden = count !== 0;
    empty.textContent = entries.length ? '这个分类下暂时没有图书。' : '书架暂时为空，等待第一本书。';
  };
  const renderSubjects = () => {
    subjects.replaceChildren();
    subjects.hidden = !academic.includes(category);
    if (subjects.hidden) return;
    const label = document.createElement('span');
    label.className = 'library-subject-label';
    label.textContent = '学科 /';
    subjects.append(label);
    const available = [...new Set(entries.filter(entry => entry.dataset.category === category)
      .map(entry => entry.dataset.subject))].sort((a, b) => a.localeCompare(b, 'zh-CN'));
    ['all', ...available].forEach(value => {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = value === 'all' ? '全部学科' : value;
      button.setAttribute('aria-pressed', String(value === subject));
      button.addEventListener('click', () => {
        subject = value;
        renderSubjects();
        update();
      });
      subjects.append(button);
    });
  };
  buttons.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.libraryCategory;
    subject = 'all';
    buttons.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
    renderSubjects();
    update();
  }));
  update();
});
