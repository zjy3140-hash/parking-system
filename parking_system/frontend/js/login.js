async function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  if (!username || !password) {
    document.getElementById('error-message').innerText = '请输入用户名和密码';
    return;
  }

  const res = await fetch("http://127.0.0.1:5000/api/admin/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });
  const data = await res.json();

  if (res.ok) {
    window.location.href = "admin.html";
  } else {
    document.getElementById('error-message').innerText = data.error || '登录失败';
  }
}