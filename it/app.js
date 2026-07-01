document.addEventListener("DOMContentLoaded", async () => {
  try {
    const [setsRes, pricesRes] = await Promise.all([
      fetch("../data.json"),
      fetch("../../output.json")
    ]);

    if (!setsRes.ok || !pricesRes.ok) {
      throw new Error("Errore nel caricamento dei JSON");
    }

    const sets = await setsRes.json();
    const prices = await pricesRes.json();

    const container = document.getElementById("sets-container");

    // mappa output.json (id → prezzo)
    const priceMap = new Map(
      prices.map(p => [String(p.id), p])
    );

    // =========================
    // 🔥 RENDER SET PRINCIPALI
    // =========================
    sets.forEach(set => {
      const priceData = priceMap.get(String(set.set));

      const prezzoBase = set.prezzo ?? "Non disponibile";

      let lcdmPrice = "";
      if (priceData?.price) {
        const raw = String(priceData.price).trim();
        lcdmPrice = raw.startsWith("€") ? raw : `€${raw}`;
      }

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

      if (set.lacittadelmattoncino) {
        buttons.push(`
          <a href="${set.lacittadelmattoncino}" target="_blank" class="btn btn-lcdm">
            La Città del Mattoncino${lcdmPrice ? ` ${lcdmPrice}` : ""}
          </a>
        `);
      }

      const card = document.createElement("div");
      card.classList.add("set-card");

      card.innerHTML = `
        <div class="set-media">
          <img src="${set.img}" alt="${set.nome}">
        </div>

        <div class="set-info">

          <div class="set-title">
            ${set.nome} - #${set.set}
          </div>

          <div class="set-price">
            Prezzo di lancio: ${prezzoBase}
          </div>

          <div class="set-buttons">
            ${buttons.join("")}
          </div>

        </div>
      `;

      container.appendChild(card);
    });

    // =========================
    // 🔥 NUOVA SEZIONE > 50€
    // =========================
    const highPriceContainer = document.getElementById("high-price-container");

    if (highPriceContainer) {
      const highPriceSets = sets.filter(set => {
        const prezzo = parseFloat(set.prezzo);
        return !isNaN(prezzo) && prezzo > 50;
      });

      const sectionTitle = document.createElement("h2");
      sectionTitle.textContent = "🔥 Set sopra i 50€";

      const wrapper = document.createElement("div");
      wrapper.classList.add("offers");

      highPriceSets.forEach(set => {
        const item = document.createElement("div");
        item.classList.add("offer-item");

        item.innerHTML = `
          <strong>${set.nome} - #${set.set}</strong><br>
          <span class="price">${set.prezzo}</span>
        `;

        wrapper.appendChild(item);
      });

      if (highPriceSets.length === 0) {
        wrapper.innerHTML = "<p>Nessun set sopra i 50€.</p>";
      }

      highPriceContainer.appendChild(sectionTitle);
      highPriceContainer.appendChild(wrapper);
    }

  } catch (err) {
    console.error("Errore nel caricamento dei dati:", err);
  }
});
