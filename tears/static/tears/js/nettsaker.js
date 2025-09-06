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
  const searchForm = document.getElementById('mainSearchForm');
  const searchInput = document.querySelector('input[name="q"]');
  const clearButton = document.getElementById('clearSearch');
  const articles = Array.from(listEl.children);

  // Sort dropdown value is now set via template, no need to set via JS

  // Search input clear button functionality
  function toggleClearButton() {
    if (searchInput && clearButton) {
      if (searchInput.value.trim()) {
        clearButton.style.display = 'block';
      } else {
        clearButton.style.display = 'none';
      }
    }
  }

  if (searchInput && clearButton) {
    searchInput.addEventListener('input', toggleClearButton);
    toggleClearButton(); // Initial check
    
    clearButton.addEventListener('click', () => {
      searchInput.value = '';
      searchInput.focus();
      toggleClearButton();
      // Optionally submit form to clear search results
      searchForm.submit();
    });
  }

  // Make radio buttons toggleable (click same = remove selection)
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

  // Function to update URL with all parameters including search and sort
  function updateURL() {
    const prog = getSelected('program');
    const kat = getSelected('kategori'); 
    const tema = getSelected('tema');
    const sort = sortEl ? sortEl.value : 'Ny';
    const search = searchInput ? searchInput.value.trim() : '';

    const params = new URLSearchParams();
    
    // Add search query if exists
    if (search) {
      params.set('q', search);
    }
    
    // Add filters only if they have values
    if (prog && prog.trim()) params.set('program', prog);
    if (kat && kat.trim()) params.set('kategori', kat);
    if (tema && tema.trim()) params.set('tema', tema);
    
    // Add sort if not default
    if (sort && sort !== 'Ny') {
      params.set('sort', sort);
    }

    // Update URL and reload page
    const newURL = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
    window.location.href = newURL;
  }

  // Client-side filtering (for current page only)
  function applyFilters() {
    const prog = getSelected('program');
    const kat = getSelected('kategori');
    const tema = getSelected('tema');

    let visible = 0;
    articles.forEach(a => {
      const okProg = !prog || a.dataset.program === prog;
      const okKat = !kat || a.dataset.kategori === kat;
      const okTema = !tema || a.dataset.tema === tema;

      const show = okProg && okKat && okTema;
      a.style.display = show ? '' : 'none';
      if (show) visible++;
    });

    if (resultCountEl) resultCountEl.textContent = `Viser ${visible} resultater`;
  }

  // Client-side sorting (for current page only)
  function applySort() {
    if (!sortEl) return;
    const val = sortEl.value;
    const collator = new Intl.Collator('nb', { sensitivity: 'base', numeric: true });

    const title = (el) => (el.dataset.title || '').trim();
    const time = (el) => Date.parse(el.dataset.date || '') || 0;

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

  function update() {
    applyFilters();
    applySort();
  }

  // Event listeners that trigger URL updates (server-side filtering)
  document.querySelectorAll(radioSel).forEach(r => r.addEventListener('change', updateURL));
  if (sortEl) sortEl.addEventListener('change', updateURL);

  // Search form submission
  if (searchForm) {
    searchForm.addEventListener('submit', function(e) {
      // Let the form submit naturally to include search query
      // The updateURL will be handled by the form action
    });
  }

  // Initialize client-side filtering for current page
  update();

  // Show active filters
  function showActiveFilters() {
    const params = new URLSearchParams(window.location.search);
    const activeFilters = document.getElementById('activeFilters');
    if (!activeFilters) return;
    
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
    
    if (params.get('tema')) {
      filtersHTML += `<span class="inline-flex items-center bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm mr-2 mb-2">
        Tema: ${params.get('tema')}
        <button onclick="removeFilter('tema')" class="ml-2">×</button>
      </span>`;
    }
    
    activeFilters.innerHTML = filtersHTML;
  }

  // Set radio button states based on URL parameters
  function setRadioStates() {
    const params = new URLSearchParams(window.location.search);
    
    // Set program radio
    const programValue = params.get('program');
    if (programValue) {
      const programRadio = document.querySelector(`input[name="program"][value="${programValue}"]`);
      if (programRadio) programRadio.checked = true;
    }
    
    // Set kategori radio
    const kategoriValue = params.get('kategori');
    if (kategoriValue) {
      const kategoriRadio = document.querySelector(`input[name="kategori"][value="${kategoriValue}"]`);
      if (kategoriRadio) kategoriRadio.checked = true;
    }
    
    // Set tema radio
    const temaValue = params.get('tema');
    if (temaValue) {
      const temaRadio = document.querySelector(`input[name="tema"][value="${temaValue}"]`);
      if (temaRadio) temaRadio.checked = true;
    }
  }

  // Initialize
  showActiveFilters();
  setRadioStates();
});

// Global functions for removing filters
function removeFilter(paramName) {
  const params = new URLSearchParams(window.location.search);
  params.delete(paramName);
  params.delete('page'); // Reset to first page
  window.location.href = window.location.pathname + '?' + params.toString();
}

function clearAllFilters() {
  window.location.href = window.location.pathname;
}