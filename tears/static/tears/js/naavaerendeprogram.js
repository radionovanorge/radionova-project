// Rotating text for sendetid
// This script rotates the text inside the element with id 'sendetid-current'
// It cycles through the text content of elements with class 'rot-item' inside the 'sendetid-rotator' box
document.addEventListener('DOMContentLoaded', function () {
  const box = document.getElementById('sendetid-rotator');
  if (!box) return;

  const current = document.getElementById('sendetid-current');
  const items = Array.from(box.querySelectorAll('.rot-item')).map(el => el.textContent.trim());
  if (items.length === 0) return;

  let i = 0, fadeMs = 250, holdMs = 3000;
  current.textContent = items[0];
  current.style.opacity = 1;

  if (items.length === 1) return; // nothing to rotate

  setInterval(() => {
    current.style.opacity = 0;
    setTimeout(() => {
      i = (i + 1) % items.length;
      current.textContent = items[i];
      current.style.opacity = 1;
    }, fadeMs);
  }, holdMs);
});
