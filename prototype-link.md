# PROTOTYPE A/B/C — cách mở

**Nhóm:** Mái Ấm Gia Đình · Case C — AI Support Radar (VLearn)

Prototype dựng bằng **Streamlit**. Không có model hay API thật; mọi output của AI là canned.

---

## Mở prototype

```bash
cd prototype
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Trình duyệt tự mở ở `http://localhost:8501`.

**Tester ngồi máy khác, cùng Wi-Fi:** `streamlit run app.py --server.address 0.0.0.0`
rồi đưa họ dòng **Network URL**.

**Tester ở xa:** đẩy repo lên GitHub → [share.streamlit.io](https://share.streamlit.io) →
main file `prototype/app.py` → được một link công khai, tester không cần cài gì.
**Deploy trước buổi test** và tự mở thử link một lần.

| Màn hình | Nội dung |
|---|---|
| **Màn hình chung** | Bối cảnh · task · slide fixture · ba nút vào A/B/C |
| **Option A** | "Tôi đang mắc ở đây" — user tự tuyên bố, AI không suy đoán gì |
| **Option B** | Hỏi tại chỗ, AI trả lời có trích nguồn, tự đề nghị chuyển cho người thật khi không chắc |
| **Option C** | Radar tự tổng hợp từ hành vi, tự gửi mục tin cậy cao, user review sau |

**Dùng chung:** `prototype/fixture.py` chứa `FIXTURE` — toàn bộ nội dung slide, bối cảnh và task.
**Cả ba option đọc từ đúng object này**, nên không option nào có thể lệch nội dung so với hai
option kia.

⛔ `prototype/annotations.md` là annotation ngoài frame — **không mở trước mặt tester**.

---

## Definition of testable — tự kiểm theo Gate 4

| Điều kiện | Trạng thái | Ở đâu |
|---|---|---|
| Tester tự mở và thao tác được cả A/B/C | ✅ | Màn hình chung có ba nút; mỗi option có `↺ Về màn hình chung` |
| Cả ba bắt đầu từ **cùng một context và task** | ✅ | `shell()` dựng dải context giống hệt nhau; task nằm trong `FIXTURE["task"]` |
| Option hiểu được **không cần facilitator narrate** | ✅ | Affordance là nút hiện sẵn cạnh từng đoạn slide, không ẩn |
| Nội dung đủ thật để tester ra quyết định | ✅ | Slide 14 TF-IDF là nội dung kỹ thuật thật, có một đoạn khó thật (chuẩn hoá L2 sau khi nhân) |
| Mỗi option có điểm user **lấy lại control** | ✅ | A: gỡ đánh dấu · B: duyệt trước khi gửi + thu hồi · C: gỡ mục / không gửi gì / xoá dữ liệu / tắt hẳn |
| Có đường **reset** về common context | ✅ | `↺ Về màn hình chung` **xoá sạch state** — tester tiếp theo bắt đầu từ đúng cùng một điểm |

**Đã kiểm bằng cách nào:** chạy tự động toàn bộ đường đi của cả ba option bằng
`streamlit.testing.v1.AppTest` — **27 bước**, gồm cả đường recovery và đường reset.
Không có exception nào.

---

## Quy mô — cố tình giữ nhỏ

Mỗi option chỉ có **3 trạng thái**, đúng scope của Chặng 4:

```
COMMON CONTEXT (slide 14, giống hệt nhau)
        ↓
CRITICAL INTERACTION (chỗ ba option khác nhau)
        ↓
RESULT / USER DECISION (+ đường lấy lại control)
```

**Không build:** onboarding · dashboard · đăng nhập · responsive nhiều thiết bị · model thật ·
failure catalog đầy đủ.

---

## Ba điều facilitator phải biết trước buổi test

1. **Mỗi thao tác là một lần rerun.** Nếu tester dừng vì đang đợi trang vẽ lại, **đó là độ trễ
   của công cụ, không phải hesitation** — đừng ghi nhầm vào Feedback Note.
2. **Ô nhập chỉ được đọc khi bấm nút** — hành vi chuẩn của Streamlit, không phải lỗi.
3. **Ở Option C, chỉ một con số là đo thật:** *"Bạn ở lại slide 14 tổng cộng …"*, đo từ lúc mở
   option tới lúc bấm "Kết thúc phiên xem lại". Các tín hiệu còn lại là fixture dựng sẵn.
   Streamlit không nhận được sự kiện hover nên không đo được dwell theo từng đoạn, và prototype
   **cố tình không** suy ra số per-đoạn từ tổng thời gian — làm vậy là bịa số rồi trình bày nó
   như dữ liệu đo được. Chi tiết ở [prototype/README.md](prototype/README.md).
