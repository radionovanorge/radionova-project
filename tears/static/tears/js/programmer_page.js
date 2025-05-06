document.querySelectorAll('.filter-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
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
    } else {
        grid.style.display = "none"; // Hide grid
        list.style.display = "block"; // Show list
        toggleBtn.querySelector("span").textContent = "Vis som rutenett";
    }
});

