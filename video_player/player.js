document.addEventListener("DOMContentLoaded", () => {
  fetch("/timestamps/eminem_live")
    .then((res) => res.json())
    .then((data) => {
      console.log("Timestamps:", data.timestamps);
    });
});
