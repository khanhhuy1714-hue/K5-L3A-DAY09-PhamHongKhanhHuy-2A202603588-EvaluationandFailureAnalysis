# Judge audit

Chạy:
```bash
python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 10
python -m lab9.judge --csv data/eval/judge_helpful_public.csv --audit 10
```

| Tiêu chí | n | κ | Precision | Recall | Confusion (`tp/fp/fn/tn`) | Fail rate (`obs` → `RG`) | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|---|---|
| `tone_ok` (`judge_tone_public.csv`) | 100 | 0.757 | 0.857 | 0.800 | `tp=24, fp=4, fn=6, tn=66` | `0.280 → 0.300` | **ĐẠT** (`0.757 ≥ 0.6`, `0.857 ≥ 0.8`, `0.800 ≥ 0.7`) | **dùng** (sau khi cập nhật rubric & sửa nhãn `H-081`) |
| `helpful` (`judge_helpful_public.csv`) | 100 | 0.375 | 1.000 | 0.300 | `tp=9, fp=0, fn=21, tn=70` | `0.090 → 0.300` | **KHÔNG ĐẠT** (`κ = 0.375 < 0.6`, `R = 0.300 < 0.7`) | **loại** (tách kiểm tra sai tiền sang code grader M3) |

---

## ≥5 case audit thủ công (10 bất đồng trên `tone_ok` + 5 bất đồng điển hình trên `helpful`)

| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú & Hành động sửa rubric / nhãn |
|---|---|---|---|---|---|
| 1 | `H-008` — *"Em đã hoàn tiền cho anh rồi nha, anh check giúp em."* | `PASS` | `FAIL` | **Người đúng** (`FN`) | Xưng *"em"* + *"nha"* quá suồng sã. **Sửa rubric `tone_ok`:** bắt buộc xưng *"LogiX"* và gọi khách là *"anh/chị"*; cấm xưng *"em/mình"* hoặc dùng tiểu từ xuề xòa (*"nha", "nhé"*). |
| 2 | `H-017` — *"Dạ, bạn ơi LogiX đã hoàn 25.000đ cho đơn O-606 rồi nha."* | `PASS` | `FAIL` | **Người đúng** (`FN`) | Xưng *"bạn ơi"* + *"nha"* không phù hợp chuẩn CSKH LogiX. **Sửa rubric `tone_ok`:** thêm quy tắc cấm gọi khách là *"bạn"* dù câu có chữ *"Dạ"*. |
| 3 | `H-029` — *"Dạ, vui lòng chờ. Hệ thống đang xử lý, không cần nhắn thêm."* | `PASS` | `FAIL` | **Người đúng** (`FN`) | Judge bị đánh lừa bởi cụm *"Dạ, vui lòng"* ở đầu câu mà bỏ qua mệnh lệnh thức gay gắt *"không cần nhắn thêm"*. **Sửa rubric `tone_ok`:** đánh `FAIL` mọi câu mang hàm ý cấm đoán/đuổi khách (*"không cần nhắn thêm", "khỏi hỏi"*), kể cả khi có kính ngữ đầu câu. |
| 4 | `H-042` — *"Dạ, đơn O-808 đã hoàn 120.000đ. Tiền về trong 3–5 ngày ạ."* | `FAIL` | `PASS` | **Người đúng** (`FP`) | Câu ngắn gọn, lịch sự, đủ thông tin nhưng judge phạt vì *"thiếu câu xin lỗi"*. **Sửa rubric `tone_ok`:** không bắt buộc phải có câu xin lỗi dài dòng khi hoàn tiền thành công; chỉ cần có *"Dạ ... ạ"* và thông tin rõ ràng. |
| 5 | `H-051` — *"Dạ, LogiX đã refund 90.000đ cho đơn O-202 ạ."* | `FAIL` | `PASS` | **Người đúng** (`FP`) | Quy chuẩn CSKH LogiX cho phép thuật ngữ *"refund"*, nhưng judge phạt vì lẫn tiếng Anh. **Sửa rubric `tone_ok`:** thêm danh sách từ mượn được phép (*"refund", "order", "ship", "voucher"*). |
| 6 | `H-063` — *"Dạ, LogiX đã hoàn 20.000đ và sẽ hoàn thêm cho anh/chị ạ."* | `PASS` | `FAIL` | **Người đúng** (`FN`) | Agent tự hứa *"sẽ hoàn thêm"* ngoài quyết định của hệ thống. **Sửa rubric `tone_ok`:** đánh `FAIL` nếu câu trả lời tự cam kết bồi thường bổ sung ngoài kết quả giao dịch. |
| 7 | `H-070` — *"Dạ, LogiX đã hoàn 90.000đ cho đơn O-909 ạ 😂😂"* | `PASS` | `FAIL` | **Người đúng** (`FN`) | Dùng emoji cười cợt (`😂😂`) trong ngữ cảnh xử lý khiếu nại. **Sửa rubric `tone_ok`:** cấm toàn bộ emoji không trang trọng trong phản hồi khiếu nại. |
| 8 | `H-081` — *"Dạ, đơn O-107 chưa đủ điều kiện hoàn theo chính sách hiện hành ạ."* | `FAIL` | `PASS` | **Judge đúng** (`FP` giả) | Người gán nhãn đọc nhầm ticket nên gán `PASS` nhầm; câu trả lời thiếu lời mời hỗ trợ tiếp theo theo mẫu từ chối chuẩn. **Hành động:** **sửa nhãn ground-truth của người** ở `H-081` từ `PASS` → `FAIL` và đối chiếu chéo 2 annotator khi gán nhãn. |
| 9 | `H-088` — *"Dạ, dạ, LogiX đã hoàn 40.000đ cho đơn O-233 ạ."* | `FAIL` | `PASS` | **Người đúng** (`FP`) | Lỗi lặp từ nhẹ (*"Dạ, dạ"*) không làm mất tính lịch sự. **Sửa rubric `tone_ok`:** phân biệt lỗi lặp từ nhỏ không gây phản cảm (`PASS`) với lỗi văn phong cộc lốc (`FAIL`). |
| 10 | `H-094` — *"Da, LogiX da hoan 40.000đ cho don O-341, xin loi vi su bat tien."* | `PASS` | `FAIL` | **Người đúng** (`FN`) | Văn bản mất toàn bộ dấu tiếng Việt. **Sửa rubric `tone_ok`:** bắt buộc phản hồi bằng tiếng Việt có dấu đầy đủ; mất dấu tiếng Việt phải đánh `FAIL`. |
| 11 | `HL-015` (`helpful`) — *"Dạ, LogiX đã hoàn 55.000đ cho đơn O-112 ạ."* (ledger: `40.000đ`) | `PASS` | `FAIL` | **Người đúng** (`FN`) | Lỗi `FM-08` (reply báo hoàn `55.000đ` nhưng ledger chỉ ghi `40.000đ`). Judge chỉ đọc text nên thấy câu lịch sự là cho `PASS`. **Hành động:** không dùng LLM judge để chấm số tiền; chuyển sang **code grader** đối chiếu trực tiếp với `snapshot["refund_vnd"]`. |
| 12 | `HL-016` (`helpful`) — *"Dạ, LogiX thành thật xin lỗi... LogiX đã hoàn 55.000đ cho đơn O-404..."* (ledger: `35.000đ`) | `PASS` | `FAIL` | **Người đúng** (`FN`) | Lỗi `FM-08` kết hợp **verbosity/apology bias**: câu xin lỗi dài dòng làm judge chấm `PASS` dù số tiền sai lệch 20.000đ so với ledger. **Hành động:** loại tiêu chí sai tiền khỏi judge `helpful`, bắt bằng code grader `ReplyAmountAccurate`. |
| 13 | `HL-020` (`helpful`) — *"Dạ, LogiX đã hoàn 90.000đ cho đơn O-303 ạ."* (ledger: `120.000đ`) | `PASS` | `FAIL` | **Người đúng** (`FN`) | Lỗi `FM-08` báo thiếu tiền hoàn (`90.000đ` vs `120.000đ` trên ledger). **Hành động:** chấm bằng code grader so sánh số tiền trích từ `reply` với `ledger`. |
| 14 | `HL-047` (`helpful`) — *"Ok bạn, đơn O-515 xử lý rồi nhé."* | `PASS` | `FAIL` | **Người đúng** (`FN`) | Câu trả lời vừa sai xưng hô (*"Ok bạn... nhé"*) vừa thiếu số tiền hoàn cụ thể. **Hành động:** tách tiêu chí xưng hô sang `tone_ok` và tiêu chí số tiền sang code grader. |
| 15 | `HL-058` (`helpful`) — *"Dạ, LogiX rất tiếc... LogiX đã hoàn 40.000đ cho đơn O-107..."* (ledger: `25.000đ`) | `PASS` | `FAIL` | **Người đúng** (`FN`) | Lỗi `FM-08` (báo `40.000đ`, ledger ghi `25.000đ`). Một lần nữa chứng minh LLM judge bị thiên kiến hình thức lịch sự đánh lừa. |

---

## Kết luận

1. **Tiêu chí được giữ (`tone_ok`) và điều kiện sử dụng:**
   - Đạt cả 3 ngưỡng sàn hiệu chuẩn: $\kappa = 0.757 \ge 0.60$, $\text{Precision} = 0.857 \ge 0.80$, $\text{Recall} = 0.800 \ge 0.70$.
   - Tỉ lệ lỗi quan sát được là $28.0\%$; sau khi hiệu chỉnh sai số phân loại bằng **Rogan-Gladen** ($\text{Sensitivity} = 0.800$, $\text{Specificity} = 66/70 \approx 0.943$), tỉ lệ lỗi thực ước lượng là **$30.0\%$** (khớp chính xác tỉ lệ lỗi thực của nhãn người $(24+6)/100 = 30\%$).
   - Dù đạt sàn, cần cập nhật prompt rubric của `tone_ok` theo 5 nhóm lỗi rút ra từ bảng audit (cấm xưng *"em/bạn/nha"*, cấm câu mệnh lệnh đuổi khách, cấm hứa hoàn thêm, cấm emoji, bắt buộc tiếng Việt có dấu, không phạt từ *"refund"* hay câu ngắn gọn đủ ý) và sửa nhãn người bị nhầm ở `H-081`.

2. **Tiêu chí bị loại (`helpful`) và lý do (dẫn ma trận nhầm lẫn):**
   - **Loại hoàn toàn `judge_helpful` khỏi CI gate** vì vi phạm nghiêm trọng sàn hiệu chuẩn: **$\text{Recall} = 0.300 < 0.70$** và **$\kappa = 0.375 < 0.60$**.
   - **Phân tích ma trận nhầm lẫn (`tp=9, fp=0, fn=21, tn=70`):** Trong 30 ca thực sự lỗi (`tp + fn = 30`), judge bỏ lọt tới **21 ca (`fn = 21`, bỏ lọt $70\%$ số lỗi)**. Hệ quả là tỉ lệ lỗi quan sát chỉ còn **$9.0\%$** trong khi tỉ lệ lỗi thực (và ước lượng Rogan-Gladen) lên tới **$30.0\%$** — nếu đưa vào gate sẽ tạo cảm giác an toàn giả tạo.
   - **Nguyên nhân gốc rễ:** 18/21 ca `fn` là lỗi **`FM-08` (sai số tiền trong `reply` so với `ledger`)** kèm lời xin lỗi dài dòng (verbosity/apology bias). LLM judge chấm trên bề mặt câu chữ nên bị văn phong lịch sự đánh lừa và không đối chiếu được với trạng thái sổ cái (`refund_ledger`). Theo nguyên tắc thiết kế eval: **tiền và sự thật trong DB/ledger tuyệt đối phải chấm bằng code grader** (sẽ cài đặt ở M3), không bao giờ giao cho LLM judge.

3. **Rủi ro còn lại:**
   - Judge hiện chỉ được kiểm trên bộ dữ liệu replay công khai (`n=100`); nếu tinh chỉnh rubric trực tiếp trên tập này sẽ dễ bị overfit vào 100 mẫu đã biết.
   - Cần thu thập tập **held-out mới có nhãn người độc lập** (ít nhất 2 người gán nhãn để đo inter-annotator $\kappa$) trước khi dùng trong môi trường thực tế, đồng thời tái hiệu chuẩn định kỳ để phát hiện judge drift.
