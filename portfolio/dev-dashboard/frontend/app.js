const API = "/api/dashboard";
let langsChart = null;

const $ = (id) => document.getElementById(id);

function setLoading(v) {
  $("loader").classList.toggle("hidden", !v);
}

function showError(msg) {
  const el = $("error");
  el.textContent = msg;
  el.classList.remove("hidden");
}

function clearError() {
  $("error").classList.add("hidden");
}

function heatColor(count) {
  if (!count) return "#161b22";       // нет активности
  if (count < 2) return "#0e4429";    // 1 коммит
  if (count < 5) return "#006d32";    // 2–4
  if (count < 10) return "#26a641";   // 5–9
  if (count < 20) return "#39d353";   // 10–19
  return "#7ee787";                    // 20+ (ярко-зелёный)
}

function renderHeatmap(days) {
  const container = $("heatmap");
  container.innerHTML = "";
  days.forEach((d) => {
    const cell = document.createElement("div");
    cell.className = "cell";
    cell.style.background = heatColor(d.contributionCount);
    cell.title = `${d.date}: ${d.contributionCount}`;
    container.appendChild(cell);
  });
}

function renderLanguages(langs) {
  const labels = Object.keys(langs);
  const data = Object.values(langs);
  const palette = ["#58a6ff", "#3fb950", "#d29922", "#f85149", "#a371f7", "#39c5cf", "#db6d28"];

  if (langsChart) langsChart.destroy();

  langsChart = new Chart($("langs-chart"), {
    type: "doughnut",
    data: {
      labels,
      datasets: [{ data, backgroundColor: palette, borderWidth: 0 }],
    },
    options: {
      plugins: {
        legend: { labels: { color: "#e6edf3", font: { size: 12 } } },
      },
    },
  });
}

function renderTopRepos(repos) {
  const ul = $("top-repos");
  ul.innerHTML = "";
  repos.forEach((r) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <a href="${r.url}" target="_blank" rel="noopener">${r.name}</a>
      <p>${r.description || "—"}</p>
      <div class="repo-meta">
        <span>⭐ ${r.stars}</span>
        <span>🍴 ${r.forks}</span>
        <span>${r.language || ""}</span>
      </div>
    `;
    ul.appendChild(li);
  });
}

function renderDashboard(data) {
  $("avatar").src = data.user.avatar_url;
  $("name").textContent = data.user.name || data.user.login;
  $("login").textContent = "@" + data.user.login;
  $("bio").textContent = data.user.bio || "—";
  $("followers").textContent = data.user.followers;
  $("repos").textContent = data.user.public_repos;

  $("stars").textContent = data.stats.total_stars;
  $("commits").textContent = data.stats.total_commits;
  $("langs-count").textContent = Object.keys(data.stats.languages).length;
  $("followers-2").textContent = data.user.followers;

  const badge = $("cache-badge");
  badge.textContent = data.cached ? "из кэша" : "свежие данные";
  badge.classList.toggle("fresh", !data.cached);

  renderLanguages(data.stats.languages);
  renderHeatmap(data.contributions);
  renderTopRepos(data.top_repos);

  $("app").classList.remove("hidden");
}

async function load(username) {
  setLoading(true);
  clearError();
  try {
    const url = username ? `${API}?username=${encodeURIComponent(username)}` : API;
    const r = await fetch(url);
    if (!r.ok) {
      const err = await r.json().catch(() => ({}));
      throw new Error(err.detail || `HTTP ${r.status}`);
    }
    renderDashboard(await r.json());
  } catch (e) {
    showError("Ошибка: " + e.message);
  } finally {
    setLoading(false);
  }
}

$("search-form").addEventListener("submit", (e) => {
  e.preventDefault();
  const u = $("username").value.trim();
  load(u);
});

load();