document.addEventListener("DOMContentLoaded", () => {

  fetch("../data.json")
    .then(res => {
      if (!res.ok) {
        throw new Error("Errore nel caricamento del JSON");
      }
      return res.json();
    })
    .then(data => {
      const container = document.getElementById("sets-container");

      data.forEach(set => {
        const card = document.createElement("div");
        card.classList.add("set-card");

        let buttonsHTML = "";

        if (set.lego) {
          buttonsHTML += `<a href="${set.lego}" target="_blank" class="btn btn-lego">LEGO</a>`;
        }

        if (set.amazon) {
          buttonsHTML += `<a href="${set.amazon}" target="_blank" class="btn btn-amazon">Amazon</a>`;
        }

        let lcdmHTML = "";

        if (set.lacittadelmattoncino) {
          lcdmHTML = `
            <div class="lcdm-container">
              <a href="${set.lacittadelmattoncino}" target="_blank" class="btn btn-lcdm">
                La Città del Mattoncino
              </a>
            </div>
          `;
        }

        card.innerHTML = `
          <div class="set-media">
            <img src="${set.img}" alt="${set.nome}">
          </div>

          <div class="set-info">

            <div class="set-title">
              ${set.nome} - #${set.set}
            </div>

            <div class="set-price">
              Prezzo di lancio: ${set.prezzo}
            </div>

            <div class="set-buttons">
              ${buttonsHTML}
            </div>

            ${lcdmHTML}

          </div>
        `;

        container.appendChild(card);
      });
    })
    .catch(err => {
      console.error("Errore nel caricamento dei dati:", err);
    });

});
