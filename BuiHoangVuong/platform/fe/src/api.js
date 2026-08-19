const TOKEN_KEY = "ews.token";

export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const setToken = (token) => localStorage.setItem(TOKEN_KEY, token);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);

async function request(path, options = {}) {
  // Only an *authenticated* call getting 401 means the session lapsed; a 401 on
  // /auth/login is simply a wrong password and must surface the API's message.
  const hadToken = Boolean(getToken());
  const response = await fetch(`/api${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(getToken() ? { Authorization: `Bearer ${getToken()}` } : {}),
      ...(options.headers || {}),
    },
  });
  if (response.status === 401 && hadToken) {
    clearToken();
    throw new Error("Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại.");
  }
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || `Yêu cầu thất bại (${response.status})`);
  }
  return response.status === 204 ? null : response.json();
}

export const api = {
  login: (username, password) =>
    request("/auth/login", { method: "POST", body: JSON.stringify({ username, password }) }),
  me: () => request("/auth/me"),
  sync: () => request("/in-class/sync", { method: "POST" }),
  score: () => request("/in-class/score", { method: "POST" }),
  job: (id) => request(`/in-class/jobs/${id}`),
  ranking: (category) => request(`/in-class/ranking${category ? `?category=${encodeURIComponent(category)}` : ""}`),
  progress: () => request("/course-long/progress"),
  analytics: () => request("/course-long/analytics/summary"),
  interventions: (status) => request(`/course-long/interventions${status ? `?status=${status}` : ""}`),
  createIntervention: (payload) =>
    request("/course-long/interventions", { method: "POST", body: JSON.stringify(payload) }),
  resolveIntervention: (id) => request(`/course-long/interventions/${id}`, { method: "PATCH" }),
};
