# Student Early Warning System — Bùi Hoàng Vương

Dashboard Streamlit cảnh báo sớm học sinh có nguy cơ, dùng bộ luật (rule-based), chạy hoàn toàn cục bộ với SQLite.
Prototype cá nhân cho Case C — AI Support Radar (VLearn), nhóm Mái Ấm Gia Đình.

## Chạy bằng Docker (khuyến nghị)

```bash
cd BuiHoangVuong && docker compose up
```

Mở http://localhost:8501

**Tài khoản demo:** `teacher` / `teacher123` (hoặc `admin` / `admin123`)

## Luồng sử dụng

1. **Đăng nhập** bằng tài khoản demo ở trên.
2. Bấm **🔄 Sync School Data** — mô phỏng đồng bộ từ hệ thống nhà trường: sinh 50 học sinh với 3 nhóm nguy cơ (10 cao / 15 trung bình / 25 thấp), dữ liệu tất định (seed cố định).
3. Xem **bảng xếp hạng** theo điểm rủi ro 0–100 (High ≥70 · Medium 40–69 · Low <40), tải CSV nếu cần.
4. Mở **Why this rank?** để đọc giải thích tiếng Việt 1–2 câu cho từng học sinh, kèm gợi ý bước tiếp theo.

## Cấu trúc

| File | Vai trò |
| --- | --- |
| `app.py` | Giao diện Streamlit: đăng nhập → sync → xếp hạng → giải thích |
| `auth.py` | Xác thực đơn giản theo session (sha256, không có bảng user) |
| `sync.py` | Mô phỏng đồng bộ dữ liệu trường học (3 hồ sơ nguy cơ) |
| `scoring.py` | Trích xuất đặc trưng + tính điểm rủi ro theo luật |
| `explain.py` | Sinh câu giải thích tiếng Việt từ chính các luật chấm điểm |
| `database.py` | Khởi tạo SQLite (`students`, `assessments`, `logins`) |

## Cách chấm điểm

| Tín hiệu | Điều kiện | Điểm |
| --- | --- | --- |
| Điểm trung bình | `<5` / `<7` | 20 / 10 |
| Xu hướng điểm | `<-0.15` / `<-0.05` mỗi bài | 25 / 12 |
| Bài dưới 5 điểm | `>=2` / `=1` | 15 / 7 |
| Đăng nhập 7 ngày | `<3` / `<5` | 15 / 7 |

Tổng tối đa là **75**, nên ngưỡng High Risk (≥70) chỉ đạt khi cả 4 tín hiệu đều xấu nhất.

## Chạy trực tiếp (không Docker)

```bash
cd BuiHoangVuong
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Kiểm tra

```bash
curl -sf http://localhost:8501/_stcore/health   # -> ok
```

Dữ liệu SQLite nằm trong Docker volume `sqlite-data` (mount tại `/data`), không commit vào repo.
Xoá dữ liệu: `docker compose down -v`.

> Lưu ý: tài khoản đăng nhập là hard-code cho mục đích demo, không dùng cho môi trường thật.
