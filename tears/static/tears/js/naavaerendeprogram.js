function parseTid(tid) {
    console.log("dette fungerer")
    const regex = /(\d{1,2})(?::?(\d{2}))?\s*(?:-|til)\s*(\d{1,2})(?::?(\d{2}))?/i;
    const match = tid.match(regex);
    if (!match) return null;
  
    const [sh, sm = 0, eh, em = 0] = [
      parseInt(match[1]),
      parseInt(match[2] || 0),
      parseInt(match[3]),
      parseInt(match[4] || 0),
    ];
  
    const now = new Date();
    const start = new Date(now);
    start.setHours(sh, sm, 0, 0);
  
    const end = new Date(now);
    end.setHours(eh, em, 0, 0);
    if (end < start) end.setDate(end.getDate() + 1);
  
    return { start, end };
  }
  
  function visAktivRedaksjon() {
    const currentDay = new Date().getDay(); // 0 = søndag
    const dagKlasser = ["Søndager", "Mandager", "Tirsdager", "Onsdager", "Torsdager", "Fredager", "Lørdager"];
    const dagensWrapper = document.querySelector(`.${dagKlasser[currentDay]}`);
    if (!dagensWrapper) return;
  
    const blocks = dagensWrapper.querySelectorAll(".frame-18");
  
    blocks.forEach(block => {
      const tidEl = block.querySelector(".text-wrapper-4");
      const overlay = block.querySelector(".overlap-group-wrapper");
      if (!tidEl || !overlay) return;
  
      const tider = parseTid(tidEl.textContent);
      if (!tider) return;
  
      const nå = new Date();
      const { start, end } = tider;
  
      if (nå >= start && nå <= end) {
        overlay.style.display = "block"; 
        block.style.position = "relative";
        block.style.flex = "0 0 auto";
        block.style.backgroundColor = "#ffe4fb";
        block.style.borderRight = "4px solid #511120";
      } else {
        block.style.position = "";
        block.style.flex = "";
        block.style.backgroundColor = "";
        block.style.borderRight = "";
      }
    });
  }
  
  visAktivRedaksjon();