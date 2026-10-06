document.addEventListener("DOMContentLoaded", () => {
  const isArticle = window.location.pathname.startsWith("/posts/");
  if (!isArticle) return;
  const header = document.getElementById("title-block-header");
  if (!header) return;
  const slug = window.location.pathname.split("/")[2];
  if (!slug) return;
  const breadcrumb = document.createElement("nav");
  breadcrumb.className = "article-path";
  breadcrumb.setAttribute("aria-label", "文章路径");
  const home = document.createElement("a");
  home.href = "/";
  home.textContent = "~/notes";
  const blog = document.createElement("a");
  blog.href = "/blog.html";
  blog.textContent = "blog";
  const current = document.createElement("span");
  current.textContent = decodeURIComponent(slug) + "/";
  current.setAttribute("aria-current", "page");
  breadcrumb.append(home, document.createTextNode(" / "), blog,
    document.createTextNode(" / "), current);
  header.prepend(breadcrumb);
  const blogLink = document.querySelector('.navbar a[href$="blog.html"]');
  if (blogLink) {
    blogLink.classList.add("active");
    blogLink.setAttribute("aria-current", "location");
  }
});
