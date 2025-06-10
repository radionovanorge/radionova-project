
  const dagsliste = document.querySelector(".frame-11");
  const ukesoversikt = document.querySelector(".frame");
  const ukedager = document.querySelector(".frame-2")
  const dagsKnapp = document.querySelector(".component-2");
  const ukeKnapp = document.querySelector(".component-4");


  // ukedager knapper
  const dagKnappene = document.querySelectorAll("#mandag, #tirsdag, #onsdag, #torsdag, #fredag, #lordag, #sondag");
  const alleDager = document.querySelectorAll(".Mandager, .Tirsdager, .Onsdager, .Torsdager, .Fredager, .Lordager, .Sondager");
  
  // Start med å skjule ukesoversikt

  ukesoversikt.style.display = "none";

  // prøver å sette av den dagen det er og gjorde den knappen svart og vise bare den.
const dagene = ["Sondager", "Mandager", "Tirsdager", "Onsdager", "Torsdager", "Fredager", "Lordager"];
const dagIds = ["sondag", "mandag", "tirsdag", "onsdag", "torsdag", "fredag", "lordag"];
const currentDay = new Date().getDay(); // 0 = søndag

dagene.forEach((dagClass, index) => {
  const el = document.querySelector(`.${dagClass}`);
  const knapp = document.getElementById(dagIds[index]);
  const tekst = knapp.querySelector(".text-wrapper-4, .text-wrapper-6");

  if (el) {
    // Vis kun dagens programblokk
    el.style.display = index === currentDay ? "inline-flex" : "none";
  }

  if (knapp && tekst) {
    if (index === currentDay) {
      knapp.classList.remove("component-6");
      knapp.classList.add("component-5");
      tekst.classList.remove("text-wrapper-4");
      tekst.classList.add("text-wrapper-6");
    } else {
      knapp.classList.remove("component-5");
      knapp.classList.add("component-6");
      tekst.classList.remove("text-wrapper-6");
      tekst.classList.add("text-wrapper-4");
    }
  }
});


  //start med ukedageneknappene til å endre farge on click
dagKnappene.forEach(knapp => {
  knapp.addEventListener("click", () => {
    // 1. Bytt stil på knappene
    dagKnappene.forEach(k => {
      k.classList.remove("component-5");
      k.classList.add("component-6");
      const child = k.querySelector("div");
      child.classList.remove("text-wrapper-6");
      child.classList.add("text-wrapper-4");
    });

    knapp.classList.remove("component-6");
    knapp.classList.add("component-5");
    const child = knapp.querySelector("div");
    child.classList.remove("text-wrapper-4");
    child.classList.add("text-wrapper-6");

    // 2. Vis kun riktig dag-div
    const valgt = knapp.id.charAt(0).toUpperCase() + knapp.id.slice(1) + "er";
    const alleDager = document.querySelectorAll(".Mandager, .Tirsdager, .Onsdager, .Torsdager, .Fredager, .Lordager, .Sondager");

    alleDager.forEach(dag => {
      dag.style.display = dag.classList.contains(valgt) ? "flex" : "none";
    });
  });
});
