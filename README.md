# Track1 · Day 18 — Ba Solution Options & ba Human–AI micro-prototype

**Case C — AI Support Radar (VLearn)** · Nhóm **Mái Ấm Gia Đình**

---

## 1. Thông tin cá nhân và nhóm

| | |
|---|---|
| **Họ tên** | Nguyễn Đức Đạt |
| **MHV** | 2A202601633 |
| **Track / Day** | Track 1 — Day 18 |
| **Nhóm** | **Mái Ấm Gia Đình** |
| **Case** | **Case C — AI Support Radar** (tiếp tục đúng case của Day 17) |

| # | Họ tên | MHV | Option chịu trách nhiệm chính |
|---|---|---|---|
| 1 | **Nguyễn Đức Đạt** | 2A202601633 | **Option A** + shared context / content fixture / shared components |
| 2 | La Thế Quyền | 2A202601699 | **Option B** |
| 3 | Bùi Hoàng Vương | 2A202601553 | **Option C** |

**Cấu trúc repo**

```
Track1_Day18_2A202601633_NguyenDucDat/
├── README.md                        ← file này
├── three-option-design-sheet.md     ← Chặng 1–3 (artifact chung của nhóm)
├── prototype-link.md                ← cách mở A/B/C + tự kiểm Gate 4
├── test-script.md                   ← Chặng 5: test prompt + observation focus
├── prototype-feedback-note.md       ← phiên do chính tôi facilitate  
├── group-feedback-synthesis.md      ← tổng hợp ba feedback           
├── ai-support-log.md
└── prototype/                    ← Streamlit app: màn hình chung + ba option
    ├── app.py            ← hub + screen_a/b/c(), mỗi option 3 trạng thái
    ├── fixture.py        ← FIXTURE + components dùng chung cho cả ba option
    ├── annotations.md    ← ⛔ chỉ dành cho facilitator, không mở trước mặt tester
    ├── requirements.txt · README.md
```

---

## 2. Hypothesis Problem

> **Khi tự xem lại bài một mình sau buổi live và gặp một đoạn không hiểu, học viên VLearn gặp khó khăn trong việc lấy được trợ giúp đúng chỗ, vì đường duy nhất còn lại là chủ động mở lời với một người thật — việc có chi phí xã hội cao với người ngại giao tiếp — dẫn đến họ bỏ qua đoạn đó và không ai biết là họ đã bỏ qua.**

**Nối về Day 17 bằng bốn quote nguyên văn, có mốc phút** — repo Day 17, `interview/notes.md`:

| Mốc | Lời của `L01` |
|---|---|
| 02:28 | *"tần suất mình hỏi giảng viên **khá là ít**, tại vì mình **khá là rụt rè**"* |
| 02:50 | *"Nếu mà khó khăn quá thì mình sẽ **bỏ qua**"* |
| 02:58 | *"mình khá là **ngại giao tiếp**, nhưng nếu có cách gì đấy khiến mình giao tiếp với giảng viên **mà không cần phải nói chuyện** thì mình có thể sử dụng"* |
| 04:15 | *"Khi mà **xem lại bài** thì mình cũng rất cần được hỗ trợ, nhưng mà mình **không tìm được ai** để hỗ trợ cho mình cả"* |

**Một quyết định của nhóm phải nói rõ:** Day 17 nhóm chốt hypothesis ở **phía giảng viên**, nhưng **không phỏng vấn được giảng viên nào** — A1 (mandate/thời gian) và A5 (trần năng lực) vẫn 🔴 chưa ai kiểm. Day 18 nhóm **giữ nguyên Case C** và **thu hẹp actor về phía học viên**, nơi evidence thật đang có. Cơ chế Support Queue gốc **không bị bỏ** — nó sống thành **Option C**, lần này chính học viên nhìn thấy mình bị xếp vào queue. Lý do đầy đủ và **cái giá phải trả** ghi ở [three-option-design-sheet.md §1.3](three-option-design-sheet.md).

**Điều vẫn chưa được chứng minh:** consequence của việc "bỏ qua" (Day 17 không đào được) · pattern (mới một người, chưa có mốc thời gian cụ thể nào) · toàn bộ phía giảng viên (A1, A5) · phản chứng *"thầy cô rất hay hỗ trợ"* (03:53) chưa được đào thành sự kiện · barrier là **chi phí xã hội** hay thật ra là **discoverability** (01:14) thì chưa tách được.

---

## 3. Three Solution Options

Cả ba cùng một user, một situation, một task, một desired outcome và **một content fixture** (slide 14/22 "Chuẩn hoá trọng số TF-IDF"). Chỉ critical interaction khác.

| | Cơ chế | User làm gì | AI làm gì | Agency | Trade-off chính |
|---|---|---|---|---|---|
| **A**<br>*Tôi đang mắc ở đây*<br><sub>`screen_a()`</sub> | Học viên **tự tuyên bố** chỗ mắc; hệ thống chỉ vận chuyển tín hiệu | Chọn đoạn · chọn loại khó khăn · **chọn ai được nhìn thấy** · viết hoặc bỏ trống | Gần như không. Một việc tuỳ chọn: gợi ý cách diễn đạt | **Don't Act** — 100% quyền ở học viên | Đòi hỏi học viên **tự nhận ra và tự tuyên bố** mình đang mắc — đúng thứ `L01` nói là ngại làm |
| **B**<br>*Hỏi tại chỗ, AI tự đề nghị chuyển*<br><sub>`screen_b()`</sub> | AI giải thích ngay tại đoạn slide, có trích nguồn; hết khả năng thì **đề nghị** chuyển cho người thật | Hỏi bằng lời của mình · phán xét câu trả lời · **duyệt trước** nội dung gửi đi | Sinh câu trả lời + trích nguồn · **tự đánh giá độ chắc** · đề xuất escalate | **Act rồi Ask** — Ask ở bước không thu hồi được | Nếu AI **sai mà nghe thuyết phục**, học viên đi tiếp với hiểu sai và không ai biết |
| **C**<br>*Radar tự tổng hợp*<br><sub>`screen_c()`</sub> | AI **suy ra từ hành vi thụ động** rồi tự sinh danh sách và **tự đẩy** mục tin cậy cao vào Support Queue | **Không làm gì lúc học.** Sau đó review và **gỡ** mục sai | Đo hành vi · phán đoán · xếp độ tin cậy · **hành động trước khi hỏi** | **Act** — học viên chỉ được phủ quyết sau | Chi phí cho học viên bằng 0, nhưng đọc sai hành vi thì báo nhầm (rủi ro **A2**), và bị đưa vào danh sách **trước khi** được hỏi |

**Distance check** — viết không nhắc màu, layout hay wording:
- **A khác B vì** ở A thứ được tạo ra là *tuyên bố của chính học viên* và không có câu trả lời nào được sinh ra; ở B thứ được tạo ra là *một lời giải thích do máy sinh* mà học viên phải phán xét, và việc chuyển sang người thật là do máy đề nghị.
- **B khác C vì** B **chỉ tồn tại khi học viên mở lời hỏi**; C **hoạt động từ sự im lặng** — học viên không hỏi gì mà tín hiệu vẫn được tạo và vẫn được gửi đi.
- **A khác C vì** ở A học viên quyết định *cái gì trở thành tín hiệu và ai được nhìn thấy nó*; ở C hệ thống quyết định cả hai điều đó trước, học viên chỉ còn quyền gỡ ra sau.

**Prototype (Streamlit):**

```bash
cd prototype && pip install -r requirements.txt && streamlit run app.py
```

Deploy được lên [share.streamlit.io](https://share.streamlit.io) (main file `prototype/app.py`) để tester mở bằng link, không cần cài gì. Chi tiết ở [prototype-link.md](prototype-link.md).

---

## 4. Đóng góp của tôi trong nhóm

| Việc | Cụ thể |
|---|---|
| **Evidence Snapshot & Hypothesis Problem** | Bóc lại bốn quote có mốc phút từ bản ghi Day 17 của chính tôi; phát hiện cả bốn cùng chỉ về một barrier. Nêu vấn đề rằng hypothesis phía giảng viên chưa có một buổi phỏng vấn nào chống lưng, dẫn tới quyết định thu hẹp actor ở §1.3. |
| **Comparison Contract** | Chốt năm thứ phải giữ nguyên ở A/B/C (user · situation · task · desired outcome · content fixture) và viết task ở dạng **outcome**, không nói nút. |
| **Shared context & content fixture** | Viết nội dung slide 14 TF-IDF dùng chung cho cả ba option, chọn đúng một đoạn khó thật (chuẩn hoá L2 diễn ra sau khi nhân). Đưa toàn bộ vào `fixture.py → FIXTURE` để **ba option không thể lệch nội dung**. |
| **Shared components** | `fixture.py`: CSS, `shell()`, `render_slide()`, dải context, nút reset — dùng chung, không option nào được sửa riêng. |
| **Option A — chịu trách nhiệm chính** | Cơ chế no-inference; ba mức phạm vi hiển thị (riêng tư / giảng viên + coach / cả lớp ẩn danh) là cách trả lời trực tiếp quote 02:58 *"giao tiếp mà không cần phải nói chuyện"*; giữ AI ở mức **Ask** và tuyên bố giới hạn ngay cạnh nút. |
| **Human–AI decisions** | Lập bảng bốn quyết định cho cả ba option; lập luận vì sao A phải **Don't Act** (gán nhãn sai cho người không hề nói vậy là tổn hại, rủi ro A2), vì sao B **Ask** đúng ở bước gửi cho người thật, và vì sao C **Act** — có chủ ý, để đem chính điều đó đi test. |
| **Chuẩn hoá A/B/C** | Kiểm cả ba option chạy được từ cùng context, cùng task, cùng đường reset (reset xoá sạch state để tester sau bắt đầu từ đúng một điểm); bỏ đoạn code suy ra thời gian dừng per-đoạn từ tổng thời gian phiên ở Option C, vì đó là bịa số rồi trình bày như dữ liệu đo được. |
| **Test script & annotations** | Viết `test-script.md` (relevant context · outcome task · 5 observation focus · luật facilitation) và `prototype/annotations.md` cho cả ba option, kèm quy tắc **đảo thứ tự A/B/C** giữa ba tester và ba điều facilitator phải biết về độ trễ rerun của Streamlit. |
| **Facilitation** | ** Phiên với Tester 1 do tôi facilitate — xem mục 5. |

---

## 5. Prototype Feedback

**Điều đã chắc chắn nằm trong Still Unproven ngay từ bây giờ** — vì Day 18 về mặt thiết kế không thể trả lời:

| # | Chưa được chứng minh | Vì sao ba feedback không giải quyết được |
|---|---|---|
| 1 | Consequence của việc "bỏ qua" một đoạn | Day 17 không đào được; Day 18 test prototype, không test hậu quả học tập theo thời gian |
| 2 | **A1** — mandate và thời gian của giảng viên | Chưa phỏng vấn giảng viên nào ở cả hai ngày |
| 3 | **A5** — trần năng lực xử lý của giảng viên | Cần dữ liệu vận hành thật |
| 4 | **A2** — tín hiệu hành vi có phân biệt được "không hiểu" với việc khác không | Option C mô phỏng tín hiệu bằng canned logic → chỉ test được **phản ứng** của user, không test được **độ chính xác** của tín hiệu |

**Nhóm sẽ được phép kết luận:** *"Với Hypothesis Problem này, chúng tôi đã thử ba cách giải. Tester đã ___, vì vậy iteration tiếp theo chúng tôi sẽ ___."*
**Nhóm sẽ không được kết luận:** *"User đã xác nhận solution này đúng."*

---

## 6. AI Support Log

Bản đầy đủ ở [ai-support-log.md](ai-support-log.md). Tóm tắt:

**AI đã giúp:** rà lại tính liên tục của evidence từ bản ghi Day 17 · chỉ ra mâu thuẫn giữa hypothesis của nhóm và evidence thực có · chạy distance check cho ba options · viết toàn bộ code prototype · tạo content fixture và canned output · rà `test-script.md`.

**AI sai hoặc hời hợt ở đâu, và tôi tự sửa gì:**

| Vấn đề | Tôi đã sửa |
|---|---|
| **Ba options ban đầu chỉ là một cơ chế chỉnh ở ba mức tự động** — đúng dấu hiệu trượt Gate 2 | Bắt mỗi option phải khác ở **thứ được tạo ra**: *tuyên bố của người học* / *lời giải thích phải bị phán xét* / *phán đoán về người học* |
| **Xu hướng dựng Option C thành kẻ thua cuộc** (không nút tắt, không nêu tín hiệu, không đường gỡ) | Xây C ở **dạng tốt nhất của chính cơ chế đó**: công bố ngay đầu phiên · liệt kê đủ tín hiệu và độ tin cậy · ba mức rút quyền |
| **Định điền sẵn Feedback Note** — nghe hợp lý và hoàn toàn bịa | Giữ hai file ở dạng biểu mẫu trống, dán nhãn ⚠️ ở đầu file |
| **Evidence Snapshot ba dòng nhưng tôi chỉ có một Practice Note** | Để trống hai dòng của Quyền và Vương, ghi rõ vì sao, và ghi thêm rằng note của hai bạn có thể buộc xem lại ba options **trước** khi test |
| **Số liệu trong Option C là số bịa** | Đổi sang đo **hành vi thật của tester** trong phiên |
| **Affordance bị giấu sau hover** → sẽ buộc facilitator phải chỉ, trượt Gate 4 | Cho hiện sẵn ở mức mờ, đủ tự phát hiện |

---

## Trạng thái theo năm gate

| Gate | Trạng thái | Ở đâu |
|---|---|---|
| **1. Evidence Continuity** | ✅ Hypothesis đủ user · situation · job · barrier · consequence; nối về **bốn** quote có mốc phút của Day 17; nêu **năm** điều chưa biết | Design Sheet §1 · README §2 |
| **2. Meaningful Options** | ✅ Cùng user/situation/task/outcome/content fixture; khác cơ chế **và** khác cách chia quyền quyết định; ba câu distance check không nhắc giao diện | Design Sheet §2 · README §3 |
| **3. Human Control** | ✅ Bảng bốn quyết định × ba option; agency tương xứng hậu quả khi sai; mỗi option có ít nhất một đường lấy lại control và một đường về task ban đầu | Design Sheet §3 |
| **4. Test-ready** | ✅ Ba option chạy được, cùng context, cùng task, có reset xoá sạch state; 27 bước của cả ba option chạy tự động qua `AppTest`, không exception | `prototype/` · prototype-link.md |
| **5. Learning** | ⬜ **Chưa đạt — cần ba phiên test thật** | prototype-feedback-note.md · group-feedback-synthesis.md |

## Kiểm tra trước khi nộp

- [x] Repo đúng tên `Track1_Day18_2A202601633_NguyenDucDat`
- [x] README đủ sáu phần và ghi rõ **Đóng góp của tôi trong nhóm**
- [x] Ba prototype cùng user, situation, task, content và desired outcome
- [x] AI Support Log là phần phản ánh của chính tôi
- [x] **Chạy phiên test của tôi với Tester 1** và điền `prototype-feedback-note.md`
- [x] Đủ ba Feedback Note → điền `group-feedback-synthesis.md` (pattern · Next Change · Still Unproven)
- [x] Xác nhận Quyền và Vương đồng ý với phân công Option B / Option C ghi ở mục 1
