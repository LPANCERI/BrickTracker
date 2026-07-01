document.addEventListener("DOMContentLoaded", async () => {
  try {
    // Carico entrambi i JSON
    const [setsRes, pricesRes] = await Promise.all([
      fetch("../data.json"),
      fetch("/output.json") // <-- root del progetto
    ]);

    if (!setsRes.ok || !pricesRes.ok) {
      throw new Error("Errore nel caricamento dei JSON");
    }

    const sets = await setsRes.json();
    const prices = await pricesRes.json();

    const container = document.getElementById("sets-container");

    // Map per accesso veloce ai prezzi (più efficiente di find)
    const priceMap = new Map(prices.map(p => [p.id, p]));

    sets.forEach(set => {
      const priceData = priceMap.get(set.set); // match ID

      const card = document.createElement("div");
      card.classList.add("set-card");

      const buttons = [];

      if (set.lego) {
        buttons.push(`
          <a href="${set.lego}" target="_blank" class="btn btn-lego">
            LEGO
          </a>
        `);
      }

      if (set.amazon) {
        buttons.push(`
          <a href="${set.amazon}" target="_blank" class="btn btn-amazon">
            Amazon
          </a>
        `);
      }

      if (priceData?.url) {
        buttons.push(`
          <a href="${priceData.url}" target="_blank" class="btn btn-lcdm">
            La Città del Mattoncino
          </a>
        `);
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
            Prezzo di lancio: ${priceData?.price ?? "Non disponibile"}
          </div>

          <div class="set-buttons">
            ${buttons.join("")}
          </div>

        </div>
      `;

      container.appendChild(card);
    });

  } catch (err) {
    console.error("Errore nel caricamento dei dati:", err);
  }
});
