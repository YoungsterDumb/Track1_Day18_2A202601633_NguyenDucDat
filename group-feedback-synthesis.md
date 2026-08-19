# GROUP FEEDBACK SYNTHESIS

**Nhóm:** Mái Ấm Gia Đình · Case C — AI Support Radar (VLearn) · Day 18
**Ba phiên:** Trọng Nam × Tester 1 · Hoài Nam × Tester 2 · Thị Nga × Tester 3

---

## 1. Bảng đối chiếu ba phiên

| Nội dung | Feedback 1 (Đạt) | Feedback 2 (Quyền) | Feedback 3 (Vương) | **Pattern hoặc khác biệt** |
|---|---|---|---|---|
| **Relevant context** — có/không |  |  |  |  |
| **Thứ tự A/B/C đã dùng** |  |  |  | *(để loại trừ hiệu ứng thứ tự)* |
| **First action** |  |  |  |  |
| **Breakdown chính** |  |  |  |  |
| **Evidence đọc hay bỏ qua** |  |  |  |  |
| **Cách lấy lại control** |  |  |  |  |
| **Option được chọn** | **B** | **B** | **B** | **3/3 — nhất trí.** Ba người facilitate khác nhau cùng ra một kết quả → giả thuyết "thiên vị người build option" bị làm yếu. Nhưng nhất trí ở n=3 là **dấu hiệu cần kiểm, không phải xác nhận**: không còn tester nào chọn khác để đối chiếu |
| **Trade-off** |  |  |  |  |
| **Điều chưa thoải mái ở option đã chọn** |  |  |  |  |

> **Đã biết:** 3/3 chọn B.
> **Chưa biết và phải lấy từ ghi chú phiên:** B được chọn **sau khi tester làm gì**, tester **bỏ qua
> hay đọc** khối *"Trợ lý dựa vào"* và nhãn độ chắc, và tester **đánh đổi cái gì** để chọn B.
> Không có ba thứ đó thì hàng "Option được chọn" không dùng được cho §3 — và với kết quả nhất trí
> thì càng cần, vì **không có phiên nào chọn khác để làm đối chứng**.

---

## 2. Pattern và khác biệt

> Viết bằng **hành vi**, không bằng số phiếu. *"Ba tester thích B"* không đạt Gate 5.

**Xuất hiện ở cả ba phiên:**

```

```

**Chỉ xuất hiện ở một phiên — và vì sao đáng chú ý:**

```

```

**Ba tester phản ứng khác nhau ở đâu, và điều gì có thể giải thích khác biệt đó:**

```

```

---

## 3. NEXT CHANGE — đúng một thay đổi

> Chọn **một** trong bốn dạng:
> ☐ Giữ một option và sửa interaction
> ☐ Kết hợp hai options nhưng **giữ một cơ chế chính rõ ràng**
> ☐ Bỏ một option vì tester không hiểu hoặc nó không tạo khác biệt
> ☐ Sửa cả ba rồi test người tiếp theo

> Với kết quả 3/3 nghiêng về B, dạng 1 (*giữ B và sửa interaction*) và dạng 2 (*kết hợp, giữ B
> làm cơ chế chính*) là hai dạng khả dĩ nhất. **Nhưng chọn dạng nào phải do hành vi quyết định,
> không do số phiếu** — nếu ba tester chọn B vì ba lý do khác nhau thì "sửa interaction nào" cũng
> là ba chỗ khác nhau. Và kết quả nhất trí làm câu hỏi *"vì sao"* quan trọng hơn chứ không nhẹ đi:
> ba người khác nhau hội tụ về một cơ chế thì lý do hội tụ chính là finding.

**Next Change của nhóm:**

```

```

**Evidence nào dẫn tới quyết định này** — dẫn lại hành vi cụ thể của tester, không dẫn ý kiến:

```

```

**Iteration tiếp theo sẽ kiểm điều gì:**

```

```

---

## 4. STILL UNPROVEN sau ba feedback


| # | Điều chưa được chứng minh | Vì sao ba feedback không giải quyết được |
|---|---|---|
| 1 | **Consequence của việc "bỏ qua"** — bỏ qua một đoạn dẫn tới hậu quả gì | Day 17 không đào được; Day 18 test prototype, không phải test hậu quả học tập theo thời gian |
| 2 | **A1 — mandate và thời gian của giảng viên** | Không phỏng vấn giảng viên nào ở cả Day 17 lẫn Day 18 |
| 3 | **A5 — trần năng lực xử lý của giảng viên** | Cần dữ liệu vận hành thật, không lấy được từ prototype |
| 4 | **A2 — tín hiệu hành vi có phân biệt được "không hiểu" với việc khác không** | Option C mô phỏng tín hiệu bằng canned logic; chỉ test được **phản ứng** của user với tín hiệu, không test được **độ chính xác** của tín hiệu |
| 5 | **Vì sao cả ba chọn B** — lựa chọn đó đến từ hành vi nào, và tester chấp nhận đánh đổi gì | Mới có kết quả đếm phiếu. Số phiếu không nói được lý do; Gate 5 yêu cầu hành vi + trade-off đi kèm mỗi lựa chọn. Ba người có thể chọn cùng một option vì **ba lý do khác nhau** — chưa phân biệt được |
| 6 | **B có chống được lỗi lớn nhất của chính nó không** — tester có phát hiện ra khi AI trả lời **sai mà nghe thuyết phục** | Prototype B chỉ có hai câu trả lời canned (`prototype/app.py:256–268`): một câu *"Khá chắc"* đúng, một câu *"Không chắc"* tự nhận không biết. **Không tester nào từng gặp một câu trả lời sai.** Rủi ro "đi tiếp với hiểu sai" — trade-off chính của B ở §2.3 design sheet — vẫn nguyên vẹn chưa kiểm |
| 7 | **Hiệu ứng thứ tự** — chọn B vì cơ chế hay vì vị trí trong chuỗi A/B/C | Chỉ loại trừ được khi ba phiên chạy **ba thứ tự khác nhau** và ô *"Thứ tự A/B/C đã dùng"* ở §1 được điền. Với kết quả **nhất trí**, thứ tự là lời giải thích cạnh tranh mạnh nhất còn lại |
| 8 | **B có thật sự hạ được chi phí xã hội không** — hay chỉ hoãn nó lại | B vẫn kết thúc bằng việc gửi cho một người thật; chỉ khác là AI mở lời hộ. Design sheet §2.3 đã ghi *"chi phí xã hội chỉ giảm chứ chưa bằng 0"*. Prototype dừng ở màn "đã gửi" — không phiên nào đi tới lúc giảng viên trả lời |

---
