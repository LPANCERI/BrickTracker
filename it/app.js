document.addEventListener("DOMContentLoaded", () => {

  Promise.all([
    fetch("../data.json"),
    fetch("../output.json")
  ])
    .then(([resData, resOutput]) => {

      if (!resData.ok) {
        throw new Error("Errore nel caricamento del data.json");
      }

      if (!resOutput.ok) {
        throw new Error("Errore nel caricamento del output.json");
      }

      return Promise.all([
        resData.json(),
        resOutput.json()
      ]);
    })
    .then(([data, output]) => {

      const container = document.getElementById("sets-container");

      // 🔥 mappa output: name -> oggetto
      const outputMap = Object.fromEntries(
        output.map(item => [item.name, item])
      );

      data.forEach(set => {

        const card = document.createElement("div");
        card.classList.add("set-card");

        const extra = outputMap[set.id]; // MATCH id ↔ name

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

            ${extra ? `
              <div class="set-price-extra">
                Prezzo disponibile: ${extra.price}
              </div>
            ` : ''}

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
