
  const dagsliste = document.querySelector(".frame-11");
  const ukesoversikt = document.querySelector(".frame-123");
  const ukedager = document.querySelector(".frame-2")
  const dagsKnapp = document.querySelector(".component-2");
  const ukeKnapp = document.querySelector(".component-4");


  // ukedager knapper
  const dagKnappene = document.querySelectorAll("#mandag, #tirsdag, #onsdag, #torsdag, #fredag, #lordag, #sondag");
  const alleDager = document.querySelectorAll(".Mandager, .Tirsdager, .Onsdager, .Torsdager, .Fredager, .Lordager, .Sondager");
  
  // skjule ukesoveriskt
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

dagsKnapp.addEventListener("click", () => {
  dagsliste.style.display = "block";
  ukesoversikt.style.display = "none";
  ukedager.style.display = "block";
  console.log("Dagsliste er nå synlig");
  dagsKnapp.classList.remove("component-4");
    dagsKnapp.classList.add("component-2");
    ukeKnapp.classList.remove("component-2");
    ukeKnapp.classList.add("component-4");
  
    // Endre tekstfarge direkte
    dagsKnapp.querySelector(".text-wrapper-4, .text-wrapper-6").style.color = "#ffffff";
    ukeKnapp.querySelector(".text-wrapper-4, .text-wrapper-6").style.color = "#511120";
  
    // Endre rektangel-farge
    dagsKnapp.querySelectorAll(".rectangle, .rectangle-2, .rectangle-3").forEach(r => r.style.backgroundColor = "#ffffff");
    ukeKnapp.querySelectorAll(".rectangle-4, .rectangle-5, .rectangle-6").forEach(r => r.style.backgroundColor = "#511120");


});

ukeKnapp.addEventListener("click", () => {
  dagsliste.style.display = "none";
  ukesoversikt.style.display = "block";
  ukedager.style.display = "none";
  console.log("Ukesoversikt er nå synlig");

  ukeKnapp.classList.remove("component-4");
    ukeKnapp.classList.add("component-2");
    dagsKnapp.classList.remove("component-2");
    dagsKnapp.classList.add("component-4");
  
    ukeKnapp.querySelector(".text-wrapper-4, .text-wrapper-6").style.color = "#ffffff";
    dagsKnapp.querySelector(".text-wrapper-4, .text-wrapper-6").style.color = "#511120";
  
    ukeKnapp.querySelectorAll(".rectangle-4, .rectangle-5, .rectangle-6").forEach(r => r.style.backgroundColor = "#ffffff");
    dagsKnapp.querySelectorAll(".rectangle, .rectangle-2, .rectangle-3").forEach(r => r.style.backgroundColor = "#511120");
});
// addProgram function to add a program to the schedule
// This function will add a program to the schedule based on the day, time, title, and end time
 function addProgram(day, time, title, endTime) {
            const rows = document.querySelectorAll('tbody tr');
            const dayIndex = ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag', 'søndag'].indexOf(day.toLowerCase()) + 1;
            
            rows.forEach(row => {
                const timeCell = row.querySelector('.time-cell');
                if (timeCell && timeCell.textContent === time) {
                    const cell = row.cells[dayIndex];
                    if (cell) {
                        cell.innerHTML = `
                            <div class="program">${title}</div>
                            <div class="program-time">${time} - ${endTime}</div>
                        `;
                    }
                }
            });
        }
