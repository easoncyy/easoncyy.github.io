// Quarto's listing filter listens for keyup. Also support paste and IME input.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".quarto-listing-filter input.search").forEach((input) => {
    input.addEventListener("input", () => {
      input.dispatchEvent(new KeyboardEvent("keyup", { bubbles: true }));
    });
  });
});
