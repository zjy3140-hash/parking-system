const apiBase = "http://127.0.0.1:5000/api/parking/lot";

// 初始化停车场显示
window.onload = async function() {
    await loadParkingLotStatus();
    // 每隔 10 秒钟刷新一次停车场状态
    setInterval(loadParkingLotStatus, 10000);
}

// 加载停车场状态
async function loadParkingLotStatus() {
  const res = await fetch(apiBase);
  const data = await res.json();

  const parkingLotElement = document.getElementById('parking-lot');
  parkingLotElement.innerHTML = `
    <div>
      <h3>停车场总车位：${Object.keys(data).reduce((sum, level) => sum + Object.keys(data[level]).length, 0)}，空闲：${Object.keys(data).reduce((sum, level) => sum + Object.values(data[level]).flat().filter(space => !space.occupied).length, 0)}，已占用：${Object.keys(data).reduce((sum, level) => sum + Object.values(data[level]).flat().filter(space => space.occupied).length, 0)} </h3>
    </div>
    <div id="parking-layout">
      ${Object.keys(data).map(level => `
        <div class="level" id="${level}">
          <h4>${level}</h4>
          ${Object.keys(data[level]).map(area => `
            <div class="area" id="${level}-${area}">
              ${area}区: ${data[level][area].map(space => `
                <span class="status ${space.occupied ? 'occupied' : ''}">车位 ${space.space}</span>
              `).join(' ')}
            </div>
          `).join('')}
        </div>
      `).join('')}
    </div>
  `;
}

// 添加停车位
async function addParkingSpace() {
  const level = document.getElementById('add-level').value;
  const area = document.getElementById('add-area').value;
  const space = document.getElementById('add-space').value;

  if (!level || !area || !space) {
    alert('请填写完整的车位信息');
    return;
  }

  const res = await fetch("http://127.0.0.1:5000/api/parking/add_space", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ level, area, space })
  });
  const data = await res.json();
  alert(data.message || data.error);
  loadParkingLotStatus();  // 刷新状态
}

// 删除停车位
async function deleteParkingSpace() {
  const level = document.getElementById('delete-level').value;
  const area = document.getElementById('delete-area').value;
  const space = document.getElementById('delete-space').value;

  if (!level || !area || !space) {
    alert('请填写完整的车位信息');
    return;
  }

  const res = await fetch("http://127.0.0.1:5000/api/parking/delete_space", {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ level, area, space })
  });
  const data = await res.json();
  alert(data.message || data.error);
  loadParkingLotStatus();  // 刷新状态
}