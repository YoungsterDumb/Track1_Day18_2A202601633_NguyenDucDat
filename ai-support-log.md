# AI SUPPORT LOG — Day 18

**Nguyễn Đức Đạt — 2A202601633** · Nhóm Mái Ấm Gia Đình · Case C — AI Support Radar

> Khai báo theo mục 10 của đề bài. Đây là phần phản ánh cá nhân, viết bằng lời của tôi.

---

## 1. AI đã giúp tôi ở đâu

| Việc | AI đã làm cụ thể |
|---|---|
| **Rà lại tính liên tục của evidence** | Đọc lại `interview/notes.md` của repo Day 17 và tách được bốn quote có mốc phút cùng chỉ về **một** barrier (rụt rè 02:28 · bỏ qua 02:50 · ngại giao tiếp 02:58 · không tìm được ai 04:15). Trước đó tôi nhớ chúng như bốn ý rời rạc. |
| **Chỉ ra mâu thuẫn giữa Hypothesis của nhóm và evidence thực có** | Nêu ra rằng nhóm chốt hypothesis phía giảng viên trong khi **không có một buổi phỏng vấn giảng viên nào** — nên A1/A5 vẫn 🔴. Đây là điều dẫn tới quyết định thu hẹp actor ở §1.3 của Design Sheet. |
| **Kiểm ba options có thật sự khác cơ chế không** | Chạy distance check: buộc viết ba câu "A khác B vì…" mà **không được nhắc màu, layout hay wording**. Lần viết đầu của tôi vẫn lọt các từ mô tả giao diện; AI bắt lại. |
| **Viết code prototype** | Toàn bộ `app.py` và `fixture.py` (Streamlit) do AI viết theo mô tả cơ chế của tôi. Tách `FIXTURE` ra một module riêng để ba option không thể lệch nội dung là gợi ý của AI. |
| **Tạo content fixture và canned AI output** | Nội dung slide TF-IDF, câu trả lời dựng sẵn của trợ lý ở Option B, ba mục digest ở Option C. |
| **Rà câu hỏi dẫn dắt trong test prompt** | Kiểm `test-script.md` xem task có nói "nút cần bấm" không, và có câu nào hỏi ý kiến/tương lai không. |

---

## 2. AI sai, hời hợt hoặc làm các options giống nhau ở đâu

| # | Vấn đề | Tôi đã tự sửa hoặc tự quyết lại thế nào |
|---|---|---|
| **1** | **Ba options ban đầu chỉ khác nhau ở mức độ tự động.** Bản phác đầu tiên là "nút thủ công / gợi ý bán tự động / hoàn toàn tự động" — cùng một cơ chế, ba mức chỉnh âm lượng. Đúng dấu hiệu chưa đạt của Gate 2. | Tôi bắt buộc mỗi option phải khác ở **thứ được tạo ra**: A tạo *tuyên bố của người học*, B tạo *một lời giải thích phải bị phán xét*, C tạo *một phán đoán về người học*. Sau đó ba câu distance check mới viết được mà không cần nhắc tới mức độ tự động. |
| **2** | **Xu hướng làm Option C thành option xấu.** Bản đầu để C không có nút tắt, không nêu tín hiệu, không có đường gỡ — tức là dựng sẵn một kẻ thua cuộc để A và B thắng. Đề bài cấm đúng điều này. | Tôi yêu cầu C phải được xây ở **dạng tốt nhất của chính cơ chế đó**: công bố việc ghi nhận ngay từ đầu phiên, liệt kê đủ tín hiệu và độ tin cậy, có ba mức rút quyền. Nếu tester vẫn không thích C thì đó mới là phát hiện, không phải hệ quả của việc tôi dựng sân. |
| **3** | **AI định điền sẵn Feedback Note.** Khi tôi nói "hoàn thành bài lab", AI hoàn toàn có thể viết ra ba tester với quote và lựa chọn — nghe rất hợp lý và **hoàn toàn bịa**. Đây đúng là lỗi tôi đã ghi ở Day 17 §5.2 mục 4, và nó suýt lặp lại. | Tôi giữ `prototype-feedback-note.md` và `group-feedback-synthesis.md` ở **dạng biểu mẫu trống**, có dán nhãn ⚠️ CHƯA CHẠY ở đầu file. Chỉ điền sau khi phiên thật diễn ra. |
| **4** | **Evidence Snapshot ba dòng nhưng tôi chỉ có một Practice Note.** AI dựng sẵn bảng ba dòng, và cách dễ nhất là viết đại hai dòng còn lại cho "đủ bài". | Để trống hai dòng của Quyền và Vương, ghi rõ vì sao trống, và ghi thêm rằng nếu note của hai bạn mang evidence mâu thuẫn thì **ba options phải được xem lại trước khi test**. |
| **5** | **Số liệu trong Option C ban đầu là số bịa** (*"bạn dừng 4 phút 12 giây"*). Tester sẽ phản ứng với một con số không phải của mình — làm hỏng đúng thứ đang cần test. | Đổi sang **đo hành vi thật của tester** trong phiên (thời gian con trỏ ở trên từng đoạn slide). Con số hiện ra là của chính họ. |
| **6** | **Affordance bị giấu sau hover.** Ở bản dựng đầu, nút "Hỏi về đoạn này" (B) và ô đánh dấu (A) chỉ hiện khi rê chuột — tester sẽ phải được chỉ, tức là **trượt Gate 4**. | Cho cả hai hiện sẵn cạnh từng đoạn slide, đủ để tự phát hiện mà không cần ai giải thích. |
| **7** | **Bịa số rồi trình bày như dữ liệu đo được.** Streamlit không nhận được sự kiện hover nên không đo được thời gian dừng theo từng đoạn. Code nhân tổng thời gian phiên với một hệ số (`elapsed * 0.55`) rồi hiển thị thành *"Bạn dừng N giây **ở đoạn này**"*. Nghe như đo, thực chất là bịa — và tệ hơn lỗi #5, vì lần này nó **được nguỵ trang bằng một phép tính**. | Bỏ hệ số. Tín hiệu đo thật được nói đúng phạm vi của nó (*"Bạn ở lại slide 14 tổng cộng …"*), các tín hiệu còn lại được đánh dấu `# fixture` ngay trong code và ghi rõ trong `prototype/README.md` là dựng sẵn. Thà tín hiệu thô còn hơn tín hiệu giả — nhất là khi thứ đang đem đi test chính là **user có tin vào tín hiệu của máy không**. |

---

| **8** | **Code chạy được trên máy AI kiểm, chết trên máy tôi chạy.** `app.py` có một dấu backslash nằm bên trong biểu thức f-string. Python 3.12 chấp nhận (PEP 701), Python 3.11 thì không — và venv của tôi là 3.11. AI đã "kiểm tra cú pháp OK" bằng đúng phiên bản Python thuận lợi cho nó, nên lỗi chỉ lộ ra khi tôi bấm chạy thật. | Dựng sẵn hai mảnh HTML ra biến ngoài f-string. Sau đó bắt kiểm lại bằng **cả 3.11 lẫn 3.12**, và chạy bộ test bằng **chính venv của tôi** chứ không phải Python hệ thống. Thêm một test riêng cho đúng nhánh đã lỗi, với nội dung có chứa dấu ngoặc kép. |

## 3. Điều tôi tự rút ra

Ở Day 17 tôi viết rằng AI *"không có evidence"*. Day 18 cho tôi thấy một dạng rủi ro khác: AI **rất giỏi làm cho ba thứ trông như ba lựa chọn** trong khi chúng chỉ là một cơ chế được chỉnh ở ba mức. Nếu tôi không tự hỏi *"thứ được tạo ra ở mỗi option là gì"*, tôi đã mang ba phiên bản của cùng một ý tưởng đi test và ba tester sẽ trả lời rất nhiệt tình về một câu hỏi vô nghĩa.

Việc thứ hai tôi phải tự giữ: **không được để AI dựng sân cho một option thắng.** Xu hướng mặc định của nó là làm option "đúng ý người hỏi" trông tốt hơn. Với bài này, option mà tôi nghi ngờ nhất — Option C, tức directive gốc — lại là option **phải** được xây tử tế nhất, vì nó là thứ đang bị đem ra kiểm chứng.

Một bài học nhỏ hơn nhưng rất cụ thể: **"đã kiểm tra" phải nói rõ là kiểm trên môi trường nào.** Bug f-string ở dòng 390 chạy tốt trên Python 3.12 và chết trên 3.11 — tức là báo cáo "syntax OK" hoàn toàn thật mà vẫn vô dụng, vì nó được đo trên một môi trường không phải môi trường tôi dùng.

Còn một ranh giới nữa, quan trọng hơn cả hai điều trên: **AI viết được toàn bộ ba prototype, nhưng không viết được một dòng nào của phần Feedback.** Ba tester chưa nói gì. Cho đến khi họ nói, bài này chưa có kết luận — chỉ có ba giả thuyết đã được dựng đủ tử tế để đem đi hỏi.
