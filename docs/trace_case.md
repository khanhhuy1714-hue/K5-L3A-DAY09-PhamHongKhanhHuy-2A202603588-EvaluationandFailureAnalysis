# Trace case: từ trace tới quyết định sai đầu tiên

Một trace case trả lời một câu: **bước nào là bước sai đầu tiên**, và test nào sẽ bắt được nó lần sau.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-014 --seed 11
python -m lab9.trace_case --shape fixed --claim C-014 --seed 11   # đối chứng
```

Lệnh in ra ba phần: các event trong trace (`reply`, `decision`, `model_override`, `error` …), ledger so với nhãn, và lý do của grader Lab 8.

## Case phân tích: `seeded_regression C-014@11` (FM-05 dẫn tới FM-08)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-014@11` (run ID trace: `R-seeded_regression-C-014-s11`, trong report `eval_seeded_regression.json`) |
| Triệu chứng | `TrialPass` (`pass_rate`) FAIL vì `proposal_mismatch` (`proposal_amount=120000 != label=150000`); `RefundAmountCorrect` FAIL vì ledger chỉ ghi `refund_vnd=90000` khác với nhãn `120000`; `ReplyAmountAccurate` (FM-08) FAIL vì `reply` nói *"Dạ, LogiX đã hoàn 120.000đ cho đơn O-515."* trong khi ledger thực tế chỉ ghi `90000`. |
| Bước sai đầu tiên | **Step 5 `proposal`**: `{"amount_vnd": 120000}` (sau khi Step 4 `refund_history` đọc thấy `{"refund_count": 1, "refunded_vnd": 30000}`). |
| Vì sao là bước *đầu tiên* | Các bước trước đó đều đúng: **Step 1 `handoff`** tạo yêu cầu hợp lệ (`allowed_tools: ["lookup_order", "lookup_policy", "compute_compensation"]`); **Step 2 `investigator`** đọc đúng đơn `O-515` (`status="delivered_late", delay_days=5, damage_verified=true`); **Step 3 `quote`** tính đúng mức bồi thường tối đa `amount_vnd=150000` (`max(30000, 150000)` từ `SHIP-LATE-03` và `DMG-04`); **Step 4 `refund_history`** chỉ là bước đọc lịch sử hoàn tiền (`30000`). Sai lầm bắt đầu ở **Step 5 `proposal`** khi agent tự lấy `150000 - 30000 = 120000` trước khi gọi host `issue_refund`, làm host trừ trần đơn `O-515` thêm một lần nữa (`120000 - 30000 = 90000`) và kéo theo **Step 6 `reply`** báo sai số tiền (`120.000đ` vs ledger `90000`). |
| Failure mode | `FM-05` (`pre_deducted — trừ trước khi được duyệt`), kéo theo `FM-08` (`misreport — reply nói số tiền khác ledger`) ở Step 6. |
| Đối chứng | Trên `fixed C-014@11` (`R-fixed-C-014-s11`): sau **Step 3 `quote`** (`amount_vnd=150000`), agent **không** tự trừ tiền trước mà truyền thẳng `proposal=150000` xuống host `issue_refund`. Host tự áp trần đơn hàng (trừ khoản hoàn trước `30000` một lần duy nhất) và ghi ledger `refund_vnd=120000`, đồng thời **Step 4 `reply`** báo đúng *"Dạ, LogiX đã hoàn 120.000đ cho đơn O-515."* (`PASS`). |
| Regression test | `tests/test_lab9_trace_case.py::test_c014_first_wrong_step_is_pre_deducted_proposal` và `test_c014_graders_flag_regression_and_pass_fixed` — kiểm tra trực tiếp sự kiện `proposal` ở Step 5 và xác nhận cả 3 grader (`RefundAmountCorrect`, `ReplyAmountAccurate`, `QuoteProposalConsistent`) đều đánh `False` trên `seeded_regression C-014@11` và `True` trên `fixed C-014@11`. |
| Chưa chắc chắn | Trace chỉ cho thấy agent đã gọi `lookup_refund_history` rồi giảm `proposal` xuống `120000`, nhưng không chứng minh được nguyên nhân xuất phát từ prompt hướng dẫn sai cho agent hay logic code cứng trong bước hậu xử lý báo giá nếu không đọc mã nguồn của shape. |

## Quy tắc

- Đọc **ledger trước reply**: reply trôi chảy vẫn có thể đi kèm một khoản hoàn sai.
- "Bước sai đầu tiên" phải dẫn số event cụ thể, không phải "agent bị nhầm".
- Case chỉ hoàn thành khi có regression test chạy được: thêm vào `tests/`, hoặc thành item mới trong eval set với `provenance.from_trace`.
