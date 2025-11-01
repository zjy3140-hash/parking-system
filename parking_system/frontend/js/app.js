const apiBase = "http://127.0.0.1:5000/api/parking";

async function parkIn() {
  const plate = document.getElementById("plateIn").value;
  const res = await fetch(`${apiBase}/in`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ plate_number: plate })
  });
  const data = await res.json();
  alert(data.message || data.error);
}

async function parkOut() {
  const plate = document.getElementById("plateOut").value;
  const res = await fetch(`${apiBase}/out`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ plate_number: plate })
  });
  const data = await res.json();
  alert(data.message ? `出库成功，收费${data.cost}元` : data.error);
}

async function getStatus() {
  const res = await fetch(`${apiBase}/status`);
  const data = await res.json();
  document.getElementById("status").innerText =
    `总车位：${data.total} | 已占用：${data.occupied} | 空闲：${data.free}`;
}