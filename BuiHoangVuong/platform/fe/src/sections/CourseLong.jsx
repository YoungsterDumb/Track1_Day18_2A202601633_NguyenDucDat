import { useEffect, useState } from "react";
import { api } from "../api.js";

export default function CourseLong() {
  const [summary, setSummary] = useState(null);
  const [progress, setProgress] = useState([]);
  const [interventions, setInterventions] = useState([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ student_id: "", kind: "tutoring", owner: "teacher", note: "" });

  async function loadAll() {
    try {
      const [nextSummary, nextProgress, nextInterventions] = await Promise.all([
        api.analytics(),
        api.progress(),
        api.interventions(),
      ]);
      setSummary(nextSummary);
      setProgress(nextProgress);
      setInterventions(nextInterventions);
      setError("");
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadAll();
  }, []);

  async function createIntervention(event) {
    event.preventDefault();
    try {
      await api.createIntervention({ ...form, student_id: Number(form.student_id) });
      setForm({ ...form, student_id: "", note: "" });
      await loadAll();
    } catch (err) {
      setError(err.message);
    }
  }

  async function resolve(id) {
    try {
      await api.resolveIntervention(id);
      await loadAll();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <section>
      {error && <p className="error" role="alert">{error}</p>}
      {summary && (
        <div className="metrics" data-testid="analytics">
          <div className="card metric"><span>Học sinh</span><strong>{summary.students}</strong></div>
          <div className="card metric"><span>Hoàn thành TB</span><strong>{Math.round(summary.avg_completion_rate * 100)}%</strong></div>
          <div className="card metric"><span>Tổng giờ học</span><strong>{summary.total_hours}</strong></div>
          <div className="card metric"><span>Can thiệp mở</span><strong>{summary.open_interventions}</strong></div>
        </div>
      )}

      {summary && (
        <div className="card">
          <h3>Tiến độ theo tuần</h3>
          <div className="sparkline">
            {summary.weekly_completion.map((week) => (
              <div key={week.week} className="bar" title={`Tuần ${week.week}: ${Math.round(week.completion_rate * 100)}%`}>
                <div style={{ height: `${Math.max(4, week.completion_rate * 100)}%` }} />
                <span>T{week.week}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <h3>Tiến độ từng học sinh</h3>
      <table className="data-table" data-testid="progress-table">
        <thead>
          <tr><th>ID</th><th>Học sinh</th><th>Lớp</th><th>Tuần</th><th>Hoàn thành</th><th>Giờ học</th></tr>
        </thead>
        <tbody>
          {progress.slice(0, 20).map((row) => (
            <tr key={row.student_id}>
              <td>{row.student_id}</td>
              <td>{row.name}</td>
              <td>{row.cohort}</td>
              <td>{row.weeks_tracked}</td>
              <td>
                <div className="progress-bar"><div style={{ width: `${row.completion_rate * 100}%` }} /></div>
                {Math.round(row.completion_rate * 100)}%
              </td>
              <td>{row.hours_spent}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Can thiệp hỗ trợ</h3>
      <form className="toolbar" onSubmit={createIntervention}>
        <input
          placeholder="Student ID"
          value={form.student_id}
          onChange={(e) => setForm({ ...form, student_id: e.target.value })}
          required
        />
        <select value={form.kind} onChange={(e) => setForm({ ...form, kind: e.target.value })}>
          <option value="tutoring">tutoring</option>
          <option value="mentor call">mentor call</option>
          <option value="parent contact">parent contact</option>
        </select>
        <input placeholder="Ghi chú" value={form.note} onChange={(e) => setForm({ ...form, note: e.target.value })} />
        <button type="submit">+ Tạo can thiệp</button>
      </form>
      <table className="data-table" data-testid="interventions-table">
        <thead>
          <tr><th>#</th><th>Học sinh</th><th>Loại</th><th>Phụ trách</th><th>Trạng thái</th><th></th></tr>
        </thead>
        <tbody>
          {interventions.slice(0, 20).map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.student_name}</td>
              <td>{item.kind}</td>
              <td>{item.owner}</td>
              <td><span className={`pill ${item.status === "open" ? "high" : "low"}`}>{item.status}</span></td>
              <td>
                {item.status === "open" && (
                  <button className="link" onClick={() => resolve(item.id)}>Đóng</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
