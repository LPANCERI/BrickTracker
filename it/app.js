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

        // container bottoni
        let buttonsHTML = "";

        if (set.lego) {
          buttonsHTML += `<a href="${set.lego}" target="_blank" class="btn">LEGO</a>`;
        }

        if (set.amazon) {
          buttonsHTML += `<a href="${set.amazon}" target="_blank" class="btn">Amazon</a>`;
        }

        if (set.lacitadelmattoncino) {
          buttonsHTML += `<a href="${set.lacitadelmattoncino}" target="_blank" class="btn">La Città del Mattoncino</a>`;
        }

        card.innerHTML = `
          <img src="${set.img}" alt="${set.nome}">

          <div class="set-info">

            <div>${set.nome} - #${set.set}</div>

            <div class="price">Prezzo di lancio: ${set.prezzo}</div>

            <div class="btn-container">
              ${buttonsHTML}
            </div>

          </div>
        `;

        container.appendChild(card);
      });
    })
    .catch(err => {
      console.error("Errore nel caricamento dei dati:", err);
    });

});
