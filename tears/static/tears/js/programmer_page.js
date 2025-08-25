console.log("Programmer page script loaded.");
document.querySelectorAll('.filter-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        console.log(`Checkbox ${checkbox.value} changed to ${checkbox.checked}`);
        // Deselect all checkboxes except the one that was just clicked
        document.querySelectorAll('.filter-checkbox').forEach(cb => {
            if (cb !== checkbox) cb.checked = false;
        });

        const selectedCategory = document.querySelector('.filter-checkbox:checked')?.value || null;

        const cards = document.querySelectorAll('#programGrid > div');

        cards.forEach(card => {
            const cardCategory = card.getAttribute('data-category');

            if (!selectedCategory || cardCategory === selectedCategory) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });

        // Update the count of visible programs. 
        const nonvisibleCards = document.querySelectorAll('#programGrid > div[style="display: none;"]').length;
        const totalCards = document.querySelectorAll('#programGrid > div').length
        const showcards = (totalCards - nonvisibleCards) / 2
        document.querySelector('#resultCount').textContent = `Viser ${showcards} treff`;
    });
    
});
// vis som liste eller rutenett knapp
const toggleBtn = document.getElementById("toggleViewBtn");
const grid = document.querySelector(".program-rutenett");
const list = document.querySelector(".program-list");

let showingGrid = true;

toggleBtn.addEventListener("click", () => {
    showingGrid = !showingGrid;

    if (showingGrid) {
        grid.style.display = "grid"; // Show grid
        list.style.display = "none"; // Hide list
        toggleBtn.querySelector("span").textContent = "Vis som liste";
        document.getElementById('listIcon').classList.remove('hidden');
        document.getElementById('gridIcon').classList.add('hidden');
    } else {
        grid.style.display = "none"; // Hide grid
        list.style.display = "block"; // Show list
        toggleBtn.querySelector("span").textContent = "Vis som rutenett";
        document.getElementById('gridIcon').classList.remove('hidden');
        document.getElementById('listIcon').classList.add('hidden');
    }
});
// asc/desc sorting (locale-aware for nb)
document.getElementById("sortSelect").addEventListener("change", function () {
  const asc = this.value === "asc";
  const container = showingGrid ? grid : list; // use your existing refs
  if (!container) return;

  const collator = new Intl.Collator("nb", { sensitivity: "base", numeric: true });
  const titleOf = el => (el.querySelector("h3")?.textContent || "").trim().toLowerCase();

  const cards = Array.from(container.querySelectorAll(":scope > div"));

  cards.sort((a, b) => collator.compare(titleOf(a), titleOf(b)));
  if (!asc) cards.reverse();

  // reattach in new order
  const frag = document.createDocumentFragment();
  cards.forEach(c => frag.appendChild(c));
  container.appendChild(frag);

  console.log(`Sorted programs ${asc ? "A–Å" : "Å–A"} in the ${showingGrid ? "grid" : "list"} view.`);
  
});
