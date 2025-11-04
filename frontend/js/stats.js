const ANALYTICS_URL = "http://localhost:8001";
const BACKEND_URL = "http://localhost:8000";

async function loadSupermarkets() {
  const res = await fetch(`${BACKEND_URL}/init`);
  const data = await res.json();
  const select = document.getElementById("supermarket");
  data.supermarkets.forEach(s => {
    const opt = document.createElement("option");
    opt.value = s;
    opt.textContent = s;
    select.appendChild(opt);
  });
}

async function loadStats() {
  const supermarket_id = document.getElementById("supermarket").value;
  if (!supermarket_id) {
    alert("Please select a supermarket first.");
    return;
  }

  const res = await fetch(`${ANALYTICS_URL}/${supermarket_id}`);
  if (!res.ok) {
    alert("Error loading analytics");
    return;
  }

  const data = await res.json();
  document.getElementById("result").innerHTML = `
    <strong>🧾 Unique Buyers:</strong> ${data.unique_buyers}<br/><br/>
    <strong>👥 Special Users:</strong><br/>
    <ul>${data.special_users.map(u => `<li>${u.user_id} (${u.purchase_count} purchases)</li>`).join("") || "<li>None</li>"}</ul>
    <strong>🥇 Top Items:</strong><br/>
    <ul>${data.top_items.map(i => `<li>${i.item_name} (${i.count})</li>`).join("")}</ul>
  `;
}

document.getElementById("loadStatsBtn").addEventListener("click", loadStats);
window.onload = loadSupermarkets;
