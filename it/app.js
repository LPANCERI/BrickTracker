document.addEventListener("DOMContentLoaded", () => {

  const container = document.getElementById("sets-container");

  const tema = document.body.dataset.tema;

  // 🔥 carichiamo entrambi i JSON
  Promise.all([
    fetch("../data.json").then(res => res.json()),
    fetch("../prezzi.json").then(res => res.json())
  ])
  .then(([data, prezzi]) => {

    const filtered = data.filter(set => set.tema === tema);

    filtered.forEach(set => {

      const prezzoAmazon = prezzi?.[set.id]?.amazon ?? "non disponibile";

      const card = document.createElement("div");
      card.classList.add("set-card");

      card.innerHTML = `
        <img src="${set.img}" alt="${set.nome}">

        <div class="set-info">

          <div>${set.nome} - #${set.set}</div>

          <div class="price">
            Prezzo di lancio: ${set.prezzo} <br>
            Prezzo Amazon: ${prezzoAmazon}
          </div>

          <div class="btn-container">
            <a href="${set.lego}" target="_blank" class="btn">LEGO</a>
            <a href="${set.amazon}" target="_blank" class="btn">Amazon</a>
          </div>

        </div>
      `;

      container.appendChild(card);
    });

  })
  .catch(err => {
    console.error("Errore:", err);
  });

});
