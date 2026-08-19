# Prototype A/B/C — Streamlit

Nhóm **Mái Ấm Gia Đình** · Case C — AI Support Radar (VLearn) · Track 1 Day 18

Ba micro-prototype cho ba Solution Options. Cùng user, cùng situation, cùng task,
cùng content fixture — chỉ critical interaction khác. Xem
[`../three-option-design-sheet.md`](../three-option-design-sheet.md) §2.2.

---

## Yêu cầu

**Python 3.9+** (đã chạy thử trên 3.11 và 3.12) · `streamlit`. Không cần gì khác.

## Chạy

```bash
cd prototype
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Trình duyệt tự mở ở `http://localhost:8501`.

**Tester ngồi máy khác, cùng Wi-Fi:**

```bash
streamlit run app.py --server.address 0.0.0.0
```
rồi đưa họ dòng **Network URL** mà Streamlit in ra.

**Tester ở xa:** đẩy repo lên GitHub → [share.streamlit.io](https://share.streamlit.io) →
chọn repo, main file `prototype/app.py`. Được một link công khai, tester không cần cài gì.
Nên deploy **trước buổi test** và tự mở thử link một lần.

---

## File

| File | Vai trò |
|---|---|
| `fixture.py` | **Dùng chung** — `FIXTURE` (context · nội dung slide 14 · task), CSS, `shell()`, `render_slide()`. Ba option đọc từ đúng module này nên **không thể lệch nội dung**. |
| `app.py` | Màn hình chung + ba option. Mỗi option là một hàm `screen_a/b/c()`, mỗi hàm đúng 3 trạng thái. |
| `annotations.md` | ⛔ **Chỉ dành cho facilitator** — annotation ngoài frame. Không mở trước mặt tester. |
| `requirements.txt` | Chỉ cần `streamlit`. Không model, không API thật. |

---

## Ba trạng thái mỗi option

```
MÀN HÌNH CHUNG  (bối cảnh · task · slide 14 — giống hệt nhau)
        ↓
CRITICAL INTERACTION  (chỗ ba option khác nhau)
        ↓
RESULT / USER DECISION  (+ đường lấy lại control)
```

Nút **↺ Về màn hình chung** có ở cả ba option và **xoá sạch state** — tester tiếp theo
bắt đầu từ đúng cùng một điểm.

---

## Ba điều cần biết khi facilitate

**1. Mỗi thao tác là một lần rerun.** Trang được vẽ lại sau mỗi lần bấm, có độ trễ nhẹ.
Nếu tester dừng lại vì đang đợi trang, **đó là độ trễ của công cụ, không phải hesitation**
— đừng ghi nhầm vào Feedback Note.

**2. Ô nhập chỉ được đọc khi bấm nút.** Nội dung tester gõ chưa được lưu cho tới khi họ
bấm nút kế tiếp. Đây là hành vi chuẩn của Streamlit, không phải lỗi.

**3. Option C — con số nào là thật, con số nào là fixture.**
Streamlit không nhận được sự kiện hover nên **không đo được** thời gian dừng trên từng đoạn.

| Tín hiệu hiển thị | Nguồn |
|---|---|
| *"Bạn ở lại slide 14 tổng cộng …"* | **Đo thật** — từ lúc mở Option C tới lúc bấm "Kết thúc phiên xem lại" |
| *"Bạn quay lại đoạn này 2 lần"* · *"4 học viên khác cũng dừng lâu"* · *"đọc chậm hơn tốc độ trung bình"* · *"rời slide trước khi đọc tới cuối"* | **Fixture dựng sẵn**, đánh dấu bằng comment trong `_c_items()` |

Prototype **cố tình không** suy ra số per-đoạn từ tổng thời gian — làm vậy là bịa số và
trình bày nó như dữ liệu đo được. Cơ chế đang được test (AI suy luận từ hành vi thụ động rồi
hành động trước khi hỏi) vẫn nguyên vẹn; chỉ độ chi tiết của một con số là thô hơn.

**Mục 2 trong digest ("Định nghĩa tf, df và n") là false positive có chủ ý** — hiện thân của
rủi ro **A2** ghi từ Day 17. Để tester tự phát hiện. **Không gợi ý.**

---

## Đã kiểm

Chạy thử trên **Python 3.11 và 3.12**. Toàn bộ đường đi của cả ba option chạy tự động bằng
`streamlit.testing.v1.AppTest` — 27 bước:
mở option → critical interaction → result → đường recovery → reset về màn hình chung.
**Không có exception nào.** Bao gồm: A gợi-ý-AI/bỏ-gợi-ý + gỡ đánh dấu · B hai lượt hỏi tới
khoảnh khắc "Không chắc" + bỏ mục khỏi nội dung gửi + thu hồi · C mở bảng dữ liệu được ghi +
gỡ mục + xem Support Queue + gỡ khỏi danh sách. Thêm một test riêng cho nhánh "Bạn nhắn thêm"
của Option B với nội dung **có chứa dấu ngoặc kép**.
