const input = document.getElementById("sch-input");
const spinner = document.getElementById("sch-spinner");
const grid = document.getElementById("sch-grid");
const errorBox = document.getElementById("sch-error");
const sectionLabel = document.getElementById("sch-section-label");
const countBadge = document.getElementById("sch-count-badge");
const filterChips = document.querySelectorAll(".filter-chip");


// ── Typing search ──
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    const q = input.value.trim();
    if (!q) {
      resetToPopular();
      return;
    }
    doSearch(q);
  }
});

// ── Filter chips ──
filterChips.forEach(chip => {
  chip.addEventListener("click", () => {
    filterChips.forEach(c => c.classList.remove("active"));
    chip.classList.add("active");
    const q = chip.dataset.q;
    if (!q) {
      input.value = "";
      resetToPopular();
    } else {
      input.value = q;
      doSearch(q);
    }
  });
});

// ── Search ──
async function doSearch(query) {
  showSpinner(true);
  hideError();
  grid.style.opacity = "0.4";

  try {
    const res = await fetch(`/scholarships/api/search/?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "خطا در جستجو");
    renderCards(data.results);
    sectionLabel.textContent = `نتایج: ${query}`;
    countBadge.textContent = data.results.length;
  } catch (err) {
    showError(err.message);
  } finally {
    showSpinner(false);
    grid.style.opacity = "1";
  }
}

// ── Render cards ──
function renderCards(results) {
  if (!results.length) {
    grid.innerHTML = `<p class="text-center text-muted w-100 py-4">نتیجه‌ای یافت نشد</p>`;
    return;
  }

  grid.innerHTML = results.map(s => `
    <div class="col-12 col-md-6 col-xl-4">
      <div class="sch-card card border h-100 p-3">
        <div class="d-flex gap-2 flex-wrap mb-2">
          ${s.country ? `<span class="tag-country">${s.country}</span>` : ""}
          ${s.level ? `<span class="tag-level">${s.level}</span>` : ""}
        </div>
        <h3 class="sch-card__title mb-2">${s.title}</h3>
        <p class="sch-card__desc flex-grow-1 mb-3">${s.description}</p>
        <a href="${s.link}" target="_blank" rel="noopener"
           class="sch-card__link d-inline-flex align-items-center gap-1 mb-3">
          <i class="bi bi-arrow-left"></i> مشاهده وب‌سایت
        </a>
        <div class="sch-card__footer d-flex justify-content-between align-items-center">
          <span class="sch-card__source">${s.source}</span>
          ${s.deadline ? `<span class="sch-card__deadline"><i class="bi bi-clock"></i> ${s.deadline}</span>` : ""}
        </div>
      </div>
    </div>
  `).join("");
}

// ── Reset to popular (reload page) ──
function resetToPopular() {
  location.reload();
}

function showSpinner(show) {
  spinner.style.display = show ? "block" : "none";
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("d-none");
}

function hideError() {
  errorBox.classList.add("d-none");
}