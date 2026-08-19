# PROTOTYPE ANNOTATION — CHỈ DÀNH CHO FACILITATOR

> ⛔ **Không mở file này trước mặt tester.** Đây là annotation "ngoài frame" theo Chặng 4.
> Không giải thích icon, không narrate, không xác nhận tester "làm đúng".

---

## OPTION A — "Tôi đang mắc ở đây"

```
We expect the tester to: tự tìm ra ô đánh dấu ở lề đoạn slide, chọn đúng đoạn mình
                          không hiểu, và DỪNG LẠI ở câu hỏi "ai được nhìn thấy?"
Watch for:                — tester có tự thấy ô ⚑ ở lề không, hay phải quét mắt tìm?
                          — tester chọn phạm vi hiển thị nào, và có do dự trước
                            "Giảng viên và lab coach" không?
                          — tester có bấm "Nhờ AI gợi ý cách diễn đạt" không?
                            Nếu có: dùng nguyên văn, sửa, hay bỏ?
                          — tester có gửi khi để trống ô ghi chú không, hay nghĩ
                            rằng bắt buộc phải viết?
                          — tester có nhận ra "chưa ai xem" nghĩa là gì không?
Do not explain:           ⚑ là gì · sự khác nhau giữa ba mức hiển thị ·
                          rằng có thể gửi khi để trống · nút "Gỡ đánh dấu" nằm ở đâu
```

---

## OPTION B — Hỏi tại chỗ, AI tự đề nghị chuyển cho người thật

```
We expect the tester to: hỏi ít nhất một câu, ĐỌC hoặc BỎ QUA khối "Trợ lý dựa vào",
                          rồi gặp lúc AI nói "không chắc" và phải quyết định có
                          chuyển cho giảng viên hay không.
Watch for:                — tester có đọc khối "Trợ lý dựa vào" không, hay chỉ đọc
                            phần trả lời? (đây là câu hỏi evidence quan trọng nhất)
                          — phản ứng khi nhãn đổi từ "Khá chắc" sang "Không chắc":
                            thấy yên tâm hơn hay mất tin tưởng?
                          — tester chọn "Xem trước rồi chuyển giúp tôi",
                            "Để tôi tự hỏi", hay "Không, tôi thử tiếp"?
                          — ở màn duyệt: tester có bỏ mục nào không?
                            Đặc biệt: có bỏ "Tên và lớp của bạn" không?
                          — tester có tự gõ câu hỏi riêng không, hay chỉ bấm hai
                            câu gợi ý sẵn?
Do not explain:           rằng chỉ có hai lượt trả lời dựng sẵn ·
                          ý nghĩa của nhãn độ chắc · rằng có nút thu hồi
```

---

## OPTION C — Radar tự tổng hợp, user review sau

```
We expect the tester to: cứ đọc slide bình thường, bấm "Kết thúc phiên xem lại",
                          rồi PHẢN ỨNG với việc một mục đã được gửi cho giảng viên
                          TRƯỚC KHI họ được hỏi.
Watch for:                — tester có đọc banner "đang ghi nhận hoạt động" ở đầu
                            phiên không, hay cuộn thẳng qua?
                          — có ai bấm "Ghi nhận những gì?" hoặc "Tắt" không?
                          — phản ứng khi thấy nhãn "đã gửi cho giảng viên":
                            có nhận ra là đã gửi rồi không? bao lâu mới nhận ra?
                          — tester có phát hiện mục nào SAI về mình không?
                            (mục 2 "Định nghĩa tf, df và n" nhiều khả năng là
                            false positive — hãy để tester tự nói ra)
                          — tester bấm "Xem giảng viên đang nhìn thấy gì về tôi"
                            hay bỏ qua? Phản ứng với dòng "Gợi ý hành động:
                            nhắn riêng cho học viên này"?
                          — tester dùng đường recovery nào: gỡ từng mục / không gửi
                            gì / gỡ khỏi danh sách / xoá dữ liệu / tắt hẳn?
Do not explain:           rằng "Bạn ở lại slide 14 tổng cộng …" là thời gian thật của họ ·
                          rằng các tín hiệu khác là fixture dựng sẵn ·
                          rằng mục 2 có thể sai · ý nghĩa của "Ưu tiên: CAO"
```

---

## Ghi chú vận hành

- **Đảo thứ tự A/B/C giữa ba tester** để triệt tiêu hiệu ứng thứ tự:
  Tester 1 → A, B, C · Tester 2 → B, C, A · Tester 3 → C, A, B.
  Ghi thứ tự đã dùng vào đầu Feedback Note.
- **Reset:** nút `↺ Về màn hình chung` có ở cả ba option và **xoá sạch state** — tester tiếp theo bắt đầu từ đúng cùng một điểm.
- Prototype là Streamlit app: `cd prototype && streamlit run app.py`. Không có model hay API thật; mọi output của AI là canned.
- **Mỗi thao tác là một lần rerun.** Nếu tester dừng vì đang đợi trang vẽ lại, đó là **độ trễ của công cụ, không phải hesitation** — đừng ghi nhầm vào Feedback Note.
- **Ô nhập chỉ được đọc khi bấm nút** — hành vi chuẩn của Streamlit, không phải lỗi.
- Nếu tester hỏi "cái này hoạt động thế nào?" → hỏi lại: **"Theo bạn, nó nên hoạt động như thế nào?"**
