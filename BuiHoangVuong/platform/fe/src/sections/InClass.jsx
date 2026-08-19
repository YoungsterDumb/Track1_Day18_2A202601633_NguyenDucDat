import { useEffect, useState } from "react";
import { api } from "../api.js";

const CATEGORIES = ["All", "High Risk", "Medium Risk", "Low Risk"];

export default function InClass() {
  const [rows, setRows] = useState([]);
  const [category, setCategory] = useState("All");
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [openRow, setOpenRow] = useState(null);

  async function load(nextCategory = category) {
    try {
      setRows(await api.ranking(nextCategory === "All" ? null : nextCategory));
      setError("");
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function sync() {
    setStatus("Đang đồng bộ dữ liệu trường học...");
    try {
      const mix = await api.sync();
      setStatus(`Đã đồng bộ ${mix.students} học sinh (${mix.high} cao / ${mix.mid} trung bình / ${mix.low} thấp).`);
      await load();
    } catch (err) {
      setError(err.message);
      setStatus("");
    }
  }

  async function score() {
    setStatus("Đã xếp hàng đợi chấm điểm...");
    try {
      const job = await api.score();
      for (let attempt = 0; attempt < 40; attempt += 1) {
        // eslint-disable-next-line no-await-in-loop
        const current = await api.job(job.id);
        if (current.status === "done") {
          setStatus(`Chấm điểm xong: ${current.students_scored} học sinh (job #${current.id}).`);
          await load();
          return;
        }
        if (current.status === "failed") {
          setError(current.error || "Job chấm điểm thất bại.");
          setStatus("");
          return;
        }
        // eslint-disable-next-line no-await-in-loop
        await new Promise((resolve) => setTimeout(resolve, 500));
      }
      setStatus("Job vẫn đang chạy, thử tải lại sau.");
    } catch (err) {
      setError(err.message);
      setStatus("");
    }
  }

  const counts = rows.reduce((acc, row) => ({ ...acc, [row.risk_category]: (acc[row.risk_category] || 0) + 1 }), {});

  return (
    <section>
      <div className="toolbar">
        <button onClick={sync}>🔄 Sync School Data</button>
        <button onClick={score}>⚡ Calculate Risk Scores</button>
        <select value={category} onChange={(e) => { setCategory(e.target.value); load(e.target.value); }}>
          {CATEGORIES.map((item) => (
            <option key={item} value={item}>{item}</option>
          ))}
        </select>
      </div>
      {status && <p className="status">{status}</p>}
      {error && <p className="error" role="alert">{error}</p>}

      <div className="metrics">
        <div className="card metric high"><span>High Risk</span><strong>{counts["High Risk"] || 0}</strong></div>
        <div className="card metric medium"><span>Medium Risk</span><strong>{counts["Medium Risk"] || 0}</strong></div>
        <div className="card metric low"><span>Low Risk</span><strong>{counts["Low Risk"] || 0}</strong></div>
      </div>

      <table className="data-table" data-testid="ranking-table">
        <thead>
          <tr>
            <th>#</th><th>Học sinh</th><th>TB</th><th>Xu hướng</th><th>Rớt</th><th>Login 7d</th><th>Risk</th><th></th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={row.student_id} className={openRow === row.student_id ? "open" : ""}>
              <td>{index + 1}</td>
              <td>{row.name}</td>
              <td>{row.avg_score}</td>
              <td>{row.score_trend > 0 ? `+${row.score_trend}` : row.score_trend}</td>
              <td>{row.failed_count}</td>
              <td>{row.logins_7d}</td>
              <td><span className={`pill ${row.risk_category.split(" ")[0].toLowerCase()}`}>{row.risk_score}</span></td>
              <td>
                <button className="link" onClick={() => setOpenRow(openRow === row.student_id ? null : row.student_id)}>
                  Why?
                </button>
              </td>
            </tr>
          ))}
          {rows.length === 0 && (
            <tr><td colSpan={8} className="muted">Chưa có dữ liệu — bấm Sync rồi Calculate.</td></tr>
          )}
        </tbody>
      </table>

      {openRow && (
        <div className="card explanation" data-testid="explanation">
          {rows.find((row) => row.student_id === openRow)?.explanation}
        </div>
      )}
    </section>
  );
}
