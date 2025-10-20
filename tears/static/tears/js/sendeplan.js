// sendeplan.js
document.addEventListener('DOMContentLoaded', () => {
  // --- Elements -------------------------------------------------------------
  const dagsliste     = document.querySelector('.frame-11');   // dagsoversikt container
  const ukesoversikt  = document.querySelector('.frame-123');  // ukesoversikt container
  const ukedager      = document.querySelector('.frame-2');    // weekday pills row

  // Tabs: Dagsoversikt (active) & Ukesoversikt (inactive)
  const dagsKnapp = document.querySelector('.component-2'); // active tab by default
  const ukeKnapp  = document.querySelector('.component-4'); // inactive tab by default

  // Weekday pills (buttons) + day content blocks
  const dagKnappene = document.querySelectorAll('#mandag, #tirsdag, #onsdag, #torsdag, #fredag, #lordag, #sondag');
  const alleDager   = document.querySelectorAll('.Mandager, .Tirsdager, .Onsdager, .Torsdager, .Fredager, .Lordager, .Sondager');

  if (!dagsliste || !ukesoversikt || !ukedager || !dagsKnapp || !ukeKnapp) return; // safety

  // --- Helpers --------------------------------------------------------------
  function setTabsActive(activeBtn, inactiveBtn) {
  activeBtn.classList.remove('component-4');  
  activeBtn.classList.add('component-2');
  inactiveBtn.classList.remove('component-2'); 
  inactiveBtn.classList.add('component-4');

  // Only change SVG colors, not text
  activeBtn.querySelectorAll('.color_logo').forEach(svg => {
    svg.classList.add('text-white');
    svg.classList.remove('text-[#511120]', 'text-[#4B0C1B]');
  });
  inactiveBtn.querySelectorAll('.color_logo').forEach(svg => {
    svg.classList.remove('text-white');
    svg.classList.add('text-[#4B0C1B]');
  });
  
  // Keep text color consistent
  activeBtn.querySelectorAll('.text-wrapper-4, .text-wrapper-6').forEach(t => t.style.color = '#ffffff');
  inactiveBtn.querySelectorAll('.text-wrapper-4, .text-wrapper-6').forEach(t => t.style.color = '#511120');
}

  function resetAllDays() {
    dagKnappene.forEach(k => {
      // inactive style
      k.classList.remove('component-5'); // active
      k.classList.add('component-6');    // inactive
      // bg: pink-ish
      k.classList.remove('bg-white');
      k.classList.add('bg-[#F2E7EB]');
      // text wrapper class flip (if you use these for styling)
      const child = k.querySelector('.text-wrapper-4, .text-wrapper-6');
      if (child) { child.classList.remove('text-wrapper-6'); child.classList.add('text-wrapper-4'); }
    });
  }

  const weekMap = {
    mandag:  'Mandager',
    tirsdag: 'Tirsdager',
    onsdag:  'Onsdager',
    torsdag: 'Torsdager',
    fredag:  'Fredager',
    lordag:  'Lordager',
    sondag:  'Sondager',
  };

  function showOnlyDayById(dayId) {
    const klass = weekMap[dayId];
    alleDager.forEach(el => {
      el.style.display = el.classList.contains(klass) ? 'flex' : 'none';
    });
  }

  function activateDayButton(btn) {
    btn.classList.remove('component-6');
    btn.classList.add('component-5');
    // bg: white for active
    btn.classList.add('bg-white');
    btn.classList.remove('bg-[#F2E7EB]');
    const child = btn.querySelector('.text-wrapper-4, .text-wrapper-6');
    if (child) { child.classList.remove('text-wrapper-4'); child.classList.add('text-wrapper-6'); }
    
    
    
  }

  // --- Initial state --------------------------------------------------------
  // Start in Dagsoversikt
  dagsliste.style.display    = 'block';
  ukesoversikt.style.display = 'none';
  ukedager.style.display     = 'block';
  setTabsActive(dagsKnapp, ukeKnapp);

  // Highlight today's day & show only that day's list
  (function initToday() {
    const jsDay = new Date().getDay(); // 0=Sun..6=Sat
    const idOrder = ['sondag','mandag','tirsdag','onsdag','torsdag','fredag','lordag'];
    const todayId = idOrder[jsDay];
    const todayBtn = document.getElementById(todayId);
    if (todayBtn) {
      resetAllDays();
      activateDayButton(todayBtn);
      showOnlyDayById(todayId);
    } else {
      // fallback: show Monday
      const fallbackBtn = document.getElementById('mandag');
      if (fallbackBtn) {
        resetAllDays();
        activateDayButton(fallbackBtn);
        showOnlyDayById('mandag');
      }
    }
  })();

  // --- Listeners ------------------------------------------------------------
  // Weekday pill clicks
  dagKnappene.forEach(knapp => {
    knapp.addEventListener('click', () => {
      resetAllDays();
      activateDayButton(knapp);
      showOnlyDayById(knapp.id);
    });
  });

  // Tabs
  dagsKnapp.addEventListener('click', () => {
    dagsliste.style.display    = 'block';
    ukesoversikt.style.display = 'none';
    ukedager.style.visibility = 'visible';
  ukedager.style.opacity = '1';
  ukedager.style.pointerEvents = '';
    
    setTabsActive(dagsKnapp, ukeKnapp);
  });

  ukeKnapp.addEventListener('click', () => {
    dagsliste.style.display    = 'none';
    ukesoversikt.style.display = 'block';
    ukedager.style.visibility     = 'hidden';
    ukedager.style.opacity = '0';
  ukedager.style.pointerEvents = 'none';
    setTabsActive(ukeKnapp, dagsKnapp);
  });

  // --- (Optional) utility for table-based schedule -------------------------
  // If you still use the addProgram helper elsewhere, keep it available:
  window.addProgram = function addProgram(day, time, title, endTime) {
    const rows = document.querySelectorAll('tbody tr');
    const idx = ['mandag','tirsdag','onsdag','torsdag','fredag','lørdag','søndag'].indexOf(day.toLowerCase()) + 1;
    rows.forEach(row => {
      const timeCell = row.querySelector('.time-cell');
      if (timeCell && timeCell.textContent === time) {
        const cell = row.cells[idx];
        if (cell) {
          cell.innerHTML = `
            <div class="program">${title}</div>
            <div class="program-time">${time} - ${endTime}</div>
          `;
        }
      }
    });
  };
});
(function(){
  const wrap  = document.getElementById('wrap');
  const ifrm  = document.getElementById('sheet');
  const hBar  = document.getElementById('hBar');
  const hSpace= document.getElementById('hSpace');

  
  

  function syncSizes(){
    // set spacer sizes to the wrapper's scroll sizes
    hSpace.style.width  = wrap.scrollWidth + 'px';

    // auto-hide bars if no scroll needed
    const needH = wrap.scrollWidth  > wrap.clientWidth;
    const needV = wrap.scrollHeight > wrap.clientHeight;
    hBar.classList.toggle('hidden', !needH);
  }

  // top bar <-> wrapper (horizontal)
  hBar.addEventListener('scroll', () => { wrap.scrollLeft = hBar.scrollLeft; });
  wrap.addEventListener('scroll', () => {
    hBar.scrollLeft = wrap.scrollLeft;
  });

  // right bar <-> wrapper (vertical)

  // update when iframe loads (dimension known) + on resize
  window.addEventListener('load', syncSizes);
  
  window.addEventListener('resize', syncSizes);

  // also observe wrapper for changes
  new ResizeObserver(syncSizes).observe(wrap);
})();