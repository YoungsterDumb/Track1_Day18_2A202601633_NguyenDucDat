import { useEffect, useState } from "react";
import { api, clearToken, getToken } from "./api.js";
import Login from "./sections/Login.jsx";
import InClass from "./sections/InClass.jsx";
import CourseLong from "./sections/CourseLong.jsx";

export default function App() {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(true);
  const [section, setSection] = useState("in-class");

  useEffect(() => {
    if (!getToken()) {
      setChecking(false);
      return;
    }
    api
      .me()
      .then((data) => setUser(data.username))
      .catch(() => clearToken())
      .finally(() => setChecking(false));
  }, []);

  if (checking) return <p className="muted center">Đang tải...</p>;
  if (!user) return <Login onSignedIn={setUser} />;

  return (
    <div className="app">
      <header>
        <h1>Student Support Platform</h1>
        <nav>
          <button className={section === "in-class" ? "active" : ""} onClick={() => setSection("in-class")}>
            In-Class
          </button>
          <button className={section === "course-long" ? "active" : ""} onClick={() => setSection("course-long")}>
            Course-Long
          </button>
        </nav>
        <div className="user">
          <span>{user}</span>
          <button className="link" onClick={() => { clearToken(); setUser(null); }}>Đăng xuất</button>
        </div>
      </header>
      <main>{section === "in-class" ? <InClass /> : <CourseLong />}</main>
    </div>
  );
}
