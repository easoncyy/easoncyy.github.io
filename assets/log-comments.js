// Each journal entry owns an independent giscus iframe, loaded on expansion.
document.addEventListener('DOMContentLoaded', () => {
  const config = window.SITE_COMMENTS;
  const panels = [...document.querySelectorAll('.log-comments')];
  if (!config || !panels.length) return;
  const origin = 'https://giscus.app';
  const page = new URL(location.href);
  let session = page.searchParams.get('giscus') || '';
  try {
    if (session) localStorage.setItem('giscus-session', JSON.stringify(session));
    else session = JSON.parse(localStorage.getItem('giscus-session') || '""');
  } catch { session = session || ''; }
  if (page.searchParams.has('giscus')) {
    page.searchParams.delete('giscus');
    history.replaceState(null, '', page.href);
  }
  const widgets = new Map();
  const makeSource = panel => {
    const backlink = new URL(page.href);
    backlink.hash = panel.id;
    const params = new URLSearchParams({
      origin: backlink.href, backLink: backlink.href, session,
      repo: config.repo, repoId: config.repoId,
      category: config.category, categoryId: config.categoryId,
      term: panel.dataset.commentTerm, strict: '1',
      reactionsEnabled: '1', emitMetadata: '0', inputPosition: 'top',
      theme: 'light', description: panel.closest('.log-entry').querySelector('.log-entry-title')?.textContent || '日志评论'
    });
    return `${origin}/zh-CN/widget?${params}`;
  };
  const mount = panel => {
    if (widgets.has(panel)) return;
    const status = panel.querySelector('.log-comments-status');
    const container = panel.querySelector('.log-comments-widget');
    const iframe = document.createElement('iframe');
    iframe.className = 'log-comments-frame';
    iframe.title = `${panel.closest('.log-entry').querySelector('.log-entry-title')?.textContent || '日志'}的评论`;
    iframe.setAttribute('allow', 'clipboard-write');
    iframe.src = makeSource(panel);
    status.textContent = '正在加载评论…';
    iframe.addEventListener('load', () => {
      status.textContent = '使用 GitHub 账号参与讨论。';
    });
    const fallback = document.createElement('a');
    fallback.href = `https://github.com/${config.repo}/discussions`;
    fallback.textContent = '无法加载？前往 GitHub 讨论 ↗';
    fallback.className = 'log-comments-fallback';
    fallback.target = '_blank';
    fallback.rel = 'noopener';
    container.append(iframe, fallback);
    widgets.set(panel, iframe);
  };
  panels.forEach(panel => panel.addEventListener('toggle', () => {
    if (panel.open) mount(panel);
  }));
  window.addEventListener('message', event => {
    if (event.origin !== origin || !event.data || typeof event.data !== 'object') return;
    const message = event.data.giscus;
    if (!message || typeof message !== 'object') return;
    const widget = [...widgets.entries()].find(([, iframe]) => iframe.contentWindow === event.source);
    if (!widget) return;
    const [panel, iframe] = widget;
    const height = Number(message.resizeHeight);
    if (Number.isFinite(height) && height > 0) iframe.style.height = `${Math.ceil(height)}px`;
    if (message.signOut || (typeof message.error === 'string' && /Bad credentials|Invalid state|State has expired/.test(message.error))) {
      session = '';
      try { localStorage.removeItem('giscus-session'); } catch { /* Storage may be unavailable. */ }
      widgets.forEach((frame, owner) => { frame.src = makeSource(owner); });
    }
    if (typeof message.error === 'string' && !message.error.includes('Discussion not found')) {
      panel.querySelector('.log-comments-status').textContent = '评论暂时无法加载，可以稍后刷新或前往 GitHub 讨论。';
    }
  });
  // Restore the right entry after returning from GitHub sign-in.
  let anchor;
  try { anchor = document.getElementById(decodeURIComponent(page.hash.slice(1))); } catch { /* Invalid URL fragment. */ }
  if (anchor?.classList.contains('log-comments')) {
    anchor.open = true;
    mount(anchor);
  }
});
