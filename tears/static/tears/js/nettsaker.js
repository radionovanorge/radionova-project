const resultCountEl = document.getElementById('resultCount');
const totalAll = resultCountEl ? Number(resultCountEl.dataset.total || 0) : 0;

function setResultCount(n) {
  if (resultCountEl) {
    resultCountEl.textContent = `Viser ${n} av ${totalAll} resultater`;
  }
}


const radioSel = 'input[type="radio"][name="program"], input[type="radio"][name="kategori"], input[type="radio"][name="tema"]';

document.addEventListener('DOMContentLoaded', () => {
  const listEl = document.getElementById('articleList');
  if (!listEl) return;

  const resultCountEl = document.querySelector('#resultCount');
  const sortEl = document.getElementById('sortSelect');
  const articles = Array.from(listEl.children);

  // gjør radioer "togglebare" (klikk på samme => fjern valg)
  document.querySelectorAll(radioSel).forEach(r => {
    r.addEventListener('mousedown', function () {
      this.dataset.wasChecked = this.checked ? 'true' : 'false';
    });
    r.addEventListener('click', function () {
      if (this.dataset.wasChecked === 'true') {
        this.checked = false;
        this.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
  });

  const getSelected = (name) => {
    const el = document.querySelector(`input[type="radio"][name="${name}"]:checked`);
    return el ? (el.value || null) : null;
  };

  function applyFilters() {
    const prog = getSelected('program');
    const kat  = getSelected('kategori');
    const tema = getSelected('tema');

    let visible = 0;
    articles.forEach(a => {
      const okProg = !prog || a.dataset.program === prog;
      const okKat  = !kat  || a.dataset.kategori === kat;
      const okTema = !tema || a.dataset.tema === tema;

      const show = okProg && okKat && okTema;
      a.style.display = show ? '' : 'none';
      if (show) visible++;
    });

    if (resultCountEl) resultCountEl.textContent = `Viser ${visible} resultater`;
  }

  function applySort() {
    if (!sortEl) return;
    const val = sortEl.value;
    const collator = new Intl.Collator('nb', { sensitivity: 'base', numeric: true });

    const title = (el) => (el.dataset.title || '').trim();
    const time  = (el) => Date.parse(el.dataset.date || '') || 0;

    const visible = articles.filter(a => a.style.display !== 'none');

    if (val === 'Ny' || val === 'Gammel') {
      visible.sort((a, b) => time(b) - time(a));
      if (val === 'Gammel') visible.reverse();
    } else if (val === 'asc' || val === 'desc') {
      visible.sort((a, b) => collator.compare(title(a), title(b)));
      if (val === 'desc') visible.reverse();
    }

    const frag = document.createDocumentFragment();
    const hidden = articles.filter(a => a.style.display === 'none');
    visible.forEach(a => frag.appendChild(a));
    hidden.forEach(a => frag.appendChild(a));
    listEl.appendChild(frag);
  }

  // Funksjon for å oppdatere URL og laste siden på nytt med filtre
  function updateURL() {
    const prog = getSelected('program');
    const kat = getSelected('kategori'); 
    const tema = getSelected('tema');
    const sort = sortEl ? sortEl.value : 'Ny';

    const params = new URLSearchParams();
    if (prog) params.set('program', prog);
    if (kat) params.set('kategori', kat);
    if (tema) params.set('tema', tema);
    if (sort && sort !== 'Ny') params.set('sort', sort);

    // Oppdater URL og last siden på nytt
    const newURL = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
    window.location.href = newURL;
  }

  function update() {
    applyFilters();
    applySort();
  }

  // Bruk updateURL for å sende filtre til serveren
  document.querySelectorAll(radioSel).forEach(r => r.addEventListener('change', updateURL));
  if (sortEl) sortEl.addEventListener('change', updateURL);

  // init for klient-side filtrering av gjeldende side
  update();
});
   const searchInput = document.querySelector('input[name="q"]');
        const clearButton = document.getElementById('clearSearch');
        
        function toggleClearButton() {
            if (searchInput.value.trim()) {
                clearButton.style.display = 'block';
            } else {
                clearButton.style.display = 'none';
            }
        }
        
        searchInput.addEventListener('input', toggleClearButton);
        toggleClearButton(); // Initial check
        
        clearButton.addEventListener('click', () => {
            searchInput.value = '';
            searchInput.focus();
            toggleClearButton();
        });

        // Vis aktive filtre
        function showActiveFilters() {
            const params = new URLSearchParams(window.location.search);
            const activeFilters = document.getElementById('activeFilters');
            let filtersHTML = '';
            
            if (params.get('q')) {
                filtersHTML += `<span class="inline-flex items-center bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm mr-2 mb-2">
                    Søk: "${params.get('q')}"
                    <button onclick="removeFilter('q')" class="ml-2">×</button>
                </span>`;
            }
            
            if (params.get('program')) {
                filtersHTML += `<span class="inline-flex items-center bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm mr-2 mb-2">
                    Program: ${params.get('program')}
                    <button onclick="removeFilter('program')" class="ml-2">×</button>
                </span>`;
            }
            
            if (params.get('kategori')) {
                filtersHTML += `<span class="inline-flex items-center bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm mr-2 mb-2">
                    Kategori: ${params.get('kategori')}
                    <button onclick="removeFilter('kategori')" class="ml-2">×</button>
                </span>`;
            }
            
            activeFilters.innerHTML = filtersHTML;
        }

        // Fjern spesifikk filter
        function removeFilter(paramName) {
            const params = new URLSearchParams(window.location.search);
            params.delete(paramName);
            params.delete('page'); // Reset til første side
            window.location.href = window.location.pathname + '?' + params.toString();
        }

        // Fjern alle filtre
        function clearAllFilters() {
            window.location.href = window.location.pathname;
        }

        // Sett checked status på radio buttons basert på URL
        function setRadioStates() {
            const params = new URLSearchParams(window.location.search);
            
            // Sett program radio
            const programValue = params.get('program');
            if (programValue) {
                const programRadio = document.querySelector(`input[name="program"][value="${programValue}"]`);
                if (programRadio) programRadio.checked = true;
            }
            
            // Sett kategori radio
            const kategoriValue = params.get('kategori');
            if (kategoriValue) {
                const kategoriRadio = document.querySelector(`input[name="kategori"][value="${kategoriValue}"]`);
                if (kategoriRadio) kategoriRadio.checked = true;
            }
        }

        // Initialize på page load
        document.addEventListener('DOMContentLoaded', () => {
            showActiveFilters();
            setRadioStates();
        });