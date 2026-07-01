document.addEventListener("DOMContentLoaded", () => {

  Promise.all([
    fetch("../data.json").then(res => res.json()),
    fetch("../output.json").then(res => res.json())
  ])
  .then(([data, output]) => {

    // crea mappa id -> price
    const priceMap = new Map(
      output.map(item => [item.id, item.price])
    );

    const container = document.getElementById("sets-container");

    data.forEach(set => {

      const price = priceMap.get(set.set) || set.prezzo;

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
            Prezzo di lancio: ${price ?? "N/D"}
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
