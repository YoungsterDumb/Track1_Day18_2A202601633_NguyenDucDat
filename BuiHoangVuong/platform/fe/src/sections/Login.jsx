import { useState } from "react";
import { api, setToken } from "../api.js";

export default function Login({ onSignedIn }) {
  const [username, setUsername] = useState("teacher");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const data = await api.login(username, password);
      setToken(data.access_token);
      onSignedIn(data.username);
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-page">
      <form className="card login-card" onSubmit={submit}>
        <h1>Student Support Platform</h1>
        <p className="muted">Đăng nhập để xem cảnh báo trong lớp và tiến độ toàn khoá.</p>
        <label htmlFor="username">Tài khoản</label>
        <input id="username" value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" />
        <label htmlFor="password">Mật khẩu</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
        />
        {error && <p className="error" role="alert">{error}</p>}
        <button type="submit" disabled={busy || !password}>
          {busy ? "Đang đăng nhập..." : "Đăng nhập"}
        </button>
        <p className="hint">Demo: teacher / teacher123</p>
      </form>
    </div>
  );
}
