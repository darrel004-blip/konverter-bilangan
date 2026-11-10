const baseConfig = {
  decimal: {
    label: "Masukkan angka desimal",
    hint: "0 sampai 255 per oktet",
    suffix: "DEC",
    placeholder: "Contoh: 192.168.1.1",
    example: "192.168.1.1"
  },
  binary: {
    label: "Masukkan angka biner",
    hint: "Tepat 8 bit per oktet",
    suffix: "BIN",
    placeholder: "Contoh: 11000000.10101000.00000001.00000001",
    example: "11000000.10101000.00000001.00000001"
  },
  octal: {
    label: "Masukkan angka oktal",
    hint: "0 sampai 377 per oktet",
    suffix: "OCT",
    placeholder: "Contoh: 300.250.1.1",
    example: "300.250.1.1"
  },
  hexadecimal: {
    label: "Masukkan angka heksadesimal",
    hint: "00 sampai FF per oktet",
    suffix: "HEX",
    placeholder: "Contoh: C0.A8.01.01",
    example: "C0.A8.01.01"
  }
};

let selectedBase = "decimal";
const form = document.getElementById("converterForm");
const sourceInput = document.getElementById("sourceInput");
const convertButton = document.getElementById("convertButton");
const errorMessage = document.getElementById("errorMessage");
const errorText = document.getElementById("errorText");
const resultsSection = document.getElementById("resultsSection");
const resultGrid = document.getElementById("resultGrid");

function selectBase(base) {
  selectedBase = base;
  document.querySelectorAll(".base-option").forEach((button) => {
    const active = button.dataset.base === base;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });

  const config = baseConfig[base];
  document.getElementById("inputLabel").textContent = config.label;
  document.getElementById("inputHint").textContent = config.hint;
  document.getElementById("inputSuffix").textContent = config.suffix;
  sourceInput.placeholder = config.placeholder;
  sourceInput.value = "";
  hideFeedback();
  sourceInput.focus();
}

function hideFeedback() {
  errorMessage.hidden = true;
  resultsSection.hidden = true;
  resultGrid.innerHTML = "";
}

function showError(message) {
  resultsSection.hidden = true;
  errorText.textContent = message;
  errorMessage.hidden = false;
}

function renderResults(results) {
  resultGrid.innerHTML = "";
  results.forEach((item, index) => {
    const card = document.createElement("article");
    card.className = "result-card";

    const top = document.createElement("div");
    top.className = "result-card-top";
    const name = document.createElement("span");
    name.className = "result-name";
    name.textContent = item.basis;
    const number = document.createElement("span");
    number.className = "result-index";
    number.textContent = `0${index + 1}`;
    top.append(name, number);

    const value = document.createElement("div");
    value.className = "result-value";
    value.textContent = item.hasil;

    const copy = document.createElement("button");
    copy.className = "copy-button";
    copy.type = "button";
    copy.textContent = "▢ Salin hasil";
    copy.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(item.hasil);
        copy.textContent = "✓ Tersalin";
        copy.classList.add("copied");
      } catch {
        copy.textContent = "Gagal menyalin";
      }
    });

    card.append(top, value, copy);
    resultGrid.append(card);
  });
  resultsSection.hidden = false;
  errorMessage.hidden = true;
}

document.querySelectorAll(".base-option").forEach((button) => {
  button.addEventListener("click", () => selectBase(button.dataset.base));
});

document.getElementById("exampleButton").addEventListener("click", () => {
  sourceInput.value = baseConfig[selectedBase].example;
  hideFeedback();
  sourceInput.focus();
});

document.getElementById("resetButton").addEventListener("click", () => {
  sourceInput.value = "";
  hideFeedback();
  sourceInput.focus();
});

sourceInput.addEventListener("input", () => {
  if (selectedBase === "hexadecimal") {
    const cursor = sourceInput.selectionStart;
    sourceInput.value = sourceInput.value.toUpperCase();
    sourceInput.setSelectionRange(cursor, cursor);
  }
  if (!errorMessage.hidden || !resultsSection.hidden) hideFeedback();
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const value = sourceInput.value;
  if (value.length === 0) {
    showError("Masukkan angka terlebih dahulu.");
    sourceInput.focus();
    return;
  }

  convertButton.disabled = true;
  convertButton.querySelector("span:first-child").textContent = "Mengonversi...";
  errorMessage.hidden = true;

  try {
    const response = await fetch("/api/convert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ base: selectedBase, value })
    });
    const data = await response.json();
    if (!response.ok || !data.success) {
      showError(data.error || "Input tidak sesuai dengan aturan basis yang dipilih.");
      return;
    }
    renderResults(data.results);
  } catch {
    showError("Tidak dapat terhubung ke server Python. Pastikan app.py sedang berjalan.");
  } finally {
    convertButton.disabled = false;
    convertButton.querySelector("span:first-child").textContent = "Konversi sekarang";
  }
});
