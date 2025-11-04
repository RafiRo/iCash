const API_BASE = "http://localhost:8000";

async function loadInitData() {
  const res = await fetch(`${API_BASE}/init`);
  const data = await res.json();

  // Supermarkets
  const smSelect = document.getElementById("supermarket");
  data.supermarkets.forEach(s => {
    const opt = document.createElement("option");
    opt.value = s;
    opt.textContent = s;
    smSelect.appendChild(opt);
  });

// Users
const userSelect = document.getElementById("user");

// Add an empty option at the top
const newUserOpt = document.createElement("option");
newUserOpt.value = "";
newUserOpt.textContent = "Create new user";
userSelect.appendChild(newUserOpt);

// Add existing users
data.users.forEach(u => {
  const opt = document.createElement("option");
  opt.value = u;
  opt.textContent = u;
  userSelect.appendChild(opt);
});

  // Products
  const productSelect = document.getElementById("products");
  data.products.forEach(p => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = `${p.name} ($${p.price})`;
    productSelect.appendChild(opt);
  });
}

async function addPurchase() {
  const supermarket_id = document.getElementById("supermarket").value;
  const user_id = document.getElementById("user").value || null;
  const products = Array.from(document.getElementById("products").selectedOptions).map(o => parseInt(o.value));

  if (!supermarket_id || products.length === 0) {
    alert("Please select a supermarket and at least one product.");
    return;
  }

  const body = { supermarket_id, user_id, items: products };
  console.log("Sending:", body);

  const res = await fetch(`${API_BASE}/add_item`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  const result = await res.json();
  document.getElementById("result").innerHTML = `
    ✅ Purchase saved!<br/>
    <strong>User ID:</strong> ${result.user_id}<br/>
    <strong>Items:</strong> ${result.items.join(", ")}<br/>
    <strong>Total:</strong> $${result.total_amount.toFixed(2)}<br/>
    <strong>Timestamp:</strong> ${result.timestamp}
  `;
}


function openAnalytics() {
  window.open("stats.html", "_blank");
}

document.getElementById("submitBtn").addEventListener("click", addPurchase);
document.getElementById("analyticsBtn").addEventListener("click", openAnalytics);

loadInitData();
