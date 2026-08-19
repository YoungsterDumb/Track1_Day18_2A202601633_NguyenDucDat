# TEST SCRIPT — Chặng 5 · Chuẩn bị test

**Nhóm:** Mái Ấm Gia Đình · **Case C — AI Support Radar (VLearn)** · Day 18

---

## 1. Relevant context — một câu hỏi, tối đa 2 phút

> *"Trong hai tuần gần đây, bạn có buổi nào ngồi tự xem lại bài một mình sau giờ học mà gặp một chỗ không hiểu ngay không? Buổi gần nhất rơi vào khoảng ngày nào?"*

- **Có + có mốc thời gian** → relevant context đạt.
- **Không** → vẫn test được để tìm interaction breakdown, nhưng **ghi rõ vào Feedback Note** và **không** dùng người này để đưa ra value claim.

---

## 2. Opening — đọc gần nguyên văn

> *"Chúng mình đang thử ba cách thiết kế, không kiểm tra bạn. Không có câu trả lời đúng hoặc sai. Bạn hãy tự thao tác và nói to điều mình đang nghĩ; mình sẽ cố gắng không hướng dẫn. Nếu bạn hỏi mình một câu, nhiều khả năng mình sẽ hỏi ngược lại bạn — đấy không phải là mình né, mà là điều mình cần biết."*

Rồi đưa **màn hình chung** của app và để tester tự đọc bối cảnh.

---

## 3. Outcome task — dùng đúng một câu này cho cả A, B và C

> **"Bạn đang xem lại slide này một mình lúc gần 10 giờ tối, và có một đoạn bạn chưa hiểu. Hãy dùng phương án này để bạn không phải bỏ qua đoạn đó, và để chỗ bạn đang mắc đến được người có thể giúp bạn."**

Task nói **kết quả cần đạt**, không nói nút cần bấm. Không đổi câu chữ giữa ba option.

---

## 4. Observation focus — tối đa 5 thứ

| # | Quan sát | Vì sao chọn |
|---|---|---|
| **1** | **First action** — trong 20 giây đầu tester chạm vào cái gì trước | Cho biết cơ chế nào tự lộ ra được, cơ chế nào cần giải thích (Gate 4) |
| **2** | **Evidence được đọc hay bỏ qua** — có đọc "Trợ lý dựa vào" (B) và danh sách tín hiệu (C) không | Đây là câu hỏi Human–AI cốt lõi: user có kiểm chứng được điều máy nói không |
| **3** | **Correction / recovery** — tester làm gì khi thấy thứ sai về mình, và mất bao lâu để tìm ra đường sửa | Kiểm trực tiếp Gate 3 |
| **4** | **Hesitation** — chỗ tester dừng, cuộn lên cuộn xuống, hoặc đọc lại | Chỉ ra chỗ mô hình tinh thần bị gãy |
| **5** | **Option được chọn + trade-off** — chọn cái nào, **đánh đổi điều gì** để chọn nó | "Thích B" không tính; phải có cái giá đi kèm |

**Hai câu hỏi neo về Hypothesis Problem — hỏi ở phần so sánh:**
- *"Ở phương án bạn chọn, bạn có phải mở lời với ai không? Cảm giác lúc đó thế nào?"*
- *"Có phương án nào khiến bạn thấy không thoải mái khi người khác biết bạn đang gặp khó không?"*

---

## 5. Luật facilitation

**Phải:**
- Tester tự điều khiển. Không cầm chuột hộ.
- Dùng **cùng một task** cho A/B/C.
- Đảo thứ tự giữa ba tester (xem `prototype/annotations.md`).
- Ghi **hành vi trước**, diễn giải sau. Ghi cả những chỗ tester im lặng.
- Prototype là Streamlit: mỗi thao tác gây một lần vẽ lại trang. Nếu tester dừng vì **đang đợi trang**, đó là độ trễ công cụ — **không** ghi thành hesitation.

**Không:**
- Không narrate, không giải thích icon, không nói "bạn bấm vào đây này".
- Không lấp im lặng — đếm thầm 5 giây.
- Không hỏi *"Bạn có thích không?"*.
- Không đính chính khi tester hiểu sai — đó chính là dữ liệu.

**Ba câu cứu hộ:**
1. *"Bạn cứ nói to suy nghĩ của mình nhé."*
2. *"Bạn sẽ làm gì tiếp theo?"*
3. *"Theo bạn, nó nên hoạt động như thế nào?"*

> **Nhắc riêng cho nhóm này** — Day 17 buổi luyện của Đạt dính đúng ba lỗi: nói nhiều hơn user (53/47), đính chính sản phẩm giữa buổi (01:12), và bỏ trôi tín hiệu *"khó quá thì bỏ qua"* mà không đào hậu quả. Cả ba lỗi đều **rất dễ tái phát trong buổi test prototype**. Hễ tester nói *"cái này chắc là…"* mà nói sai → **im lặng và ghi lại**, đừng sửa.

---

## 6. Timeline 20 phút

| Thời gian | Hoạt động |
|---|---|
| *trước buổi* | **Chạy sẵn app** (`cd prototype && streamlit run app.py`) hoặc mở sẵn link đã deploy, và bấm `↺ Về màn hình chung` để state sạch |
| 0–2 | Làm quen + relevant context + opening + xin phép ghi chú/ghi âm |
| 2–14 | Tester dùng A/B/C — **~4 phút mỗi option**, quay về màn hình chung giữa các lần |
| 14–18 | So sánh: chọn cái nào, vì sao, đánh đổi gì, muốn tự làm phần nào và giao AI phần nào |
| 18–20 | Facilitator hoàn thành Feedback Note ngay khi còn nhớ |

**Ba câu so sánh cuối:**
1. *"Trong tình huống này, bạn chọn A, B hay C? Vì sao?"*
2. *"Bạn muốn tự làm phần nào và giao cho AI phần nào?"*
3. *"Điều gì ở phương án đã chọn khiến bạn chưa thoải mái?"*
