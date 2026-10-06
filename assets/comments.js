(() => {
  "use strict";
  const config = window.SITE_COMMENTS;
  const status = document.getElementById("comments-status");
  if (!status || !config) return;
  const script = document.createElement("script");
  script.src = "https://giscus.app/client.js";
  script.async = true;
  script.crossOrigin = "anonymous";
  // Directory URLs and index.html must share the same discussion.
  const articlePath = window.location.pathname.replace(/\/index\.html$/, "/").replace(/\/$/, "") + "/";
  const options = {
    repo: config.repo,
    "repo-id": config.repoId,
    category: config.category,
    "category-id": config.categoryId,
    mapping: "specific",
    term: articlePath,
    strict: "1",
    "reactions-enabled": "1",
    "emit-metadata": "1",
    "input-position": "top",
    theme: "light",
    lang: "zh-CN",
    loading: "lazy"
  };
  for (const [key, value] of Object.entries(options)) {
    script.setAttribute(`data-${key}`, value);
  }
  status.textContent = "使用 GitHub 账号参与讨论。若评论未显示，可刷新页面后重试。";
  window.addEventListener("message", (event) => {
    if (event.origin !== "https://giscus.app" || !event.data || typeof event.data !== "object") return;
    const message = event.data.giscus;
    if (!message || typeof message.error !== "string") return;
    if (message.error.includes("Discussion not found")) return;
    status.textContent = message.error.includes("not installed")
      ? "评论正在配置中，暂未开放。"
      : "评论暂时无法加载。你也可以在 GitHub 中参与讨论。";
  });
  script.addEventListener("error", () => {
    status.textContent = "评论暂时无法加载。你也可以在 GitHub 中参与讨论。";
  });
  const link = document.createElement("a");
  link.href = `https://github.com/${config.repo}/discussions`;
  link.textContent = "前往 GitHub 讨论 ↗";
  link.className = "comments-fallback";
  document.querySelector("#comments .giscus").before(link);
  document.querySelector("#comments .giscus").append(script);
})();

