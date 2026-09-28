# Rubric Day 13 AI Observability

Điểm bắt buộc là 100. Bonus tối đa 10 điểm; tổng điểm tối đa 110. Mọi điểm đều cần code chạy được và evidence có thể kiểm chứng.

## A Điểm nhóm 60 điểm

| Tiêu chí | Điểm | Bằng chứng bắt buộc | Chuẩn đạt tối đa |
|---|---:|---|---|
| Logging và correlation | 10 | `app/middleware.py`, log JSON, response headers | ID hợp lệ, không rò context, metadata đầy đủ |
| PII protection | 10 | `app/pii.py`, processor, tests, log đã scrub | Redact trước khi ghi; không leak sample PII |
| Tracing và prompt version | 10 | ≥10 trace IDs, waterfall, prompt v1/v2, rollback | Trace gắn đúng name, label, version và metadata |
| Dashboard SLO alert | 10 | validator, dashboard 6 panel, SLO/error budget, alert/runbook | Đúng source, TTFT/tool success, đơn vị và threshold |
| Incident investigation | 10 | metric, correlation ID/log line, trace ID | Chuỗi Metrics → Logs → Traces xác định đúng root cause và fix |
| Integration và demo | 10 | lệnh chạy, tests, demo đúng evidence | Hệ thống chạy end-to-end trên commit đã nộp |

## B Điểm cá nhân 40 điểm

| Tiêu chí | Điểm | Bằng chứng bắt buộc | Chuẩn đạt tối đa |
|---|---:|---|---|
| Ownership kỹ thuật | 15 | commit/PR, file/hàm và artifact | Đóng góp thực, có thể tái hiện và giải thích |
| Hiểu luồng end-to-end | 15 | Q&A và mục cá nhân trong TEAM/report | Giải thích được logging, tracing, metrics và incident |
| Báo cáo cá nhân | 10 | nhiệm vụ, quyết định, lỗi đã xử lý, điều học được | Nội dung khớp Git và evidence, không sao chép |

## Bonus tối đa 10 điểm

Chỉ chấm bonus khi phần bắt buộc chạy được end-to-end.

- Tối đa +5: cost optimization có before/after và cùng workload.
- Tối đa +5: automation hữu ích như secret/PII scan, dashboard generation hoặc CI.
- Tối đa +5: audit log riêng có schema, retention và truy vấn minh họa.

Tổng bonus không vượt 10 điểm.

## Điều kiện trừ điểm hoặc bài không hợp lệ

| Vi phạm | Mức xử lý |
|---|---:|
| Commit API key, secret hoặc PII | -20 điểm; có thể 0 điểm nếu gây rò rỉ nghiêm trọng |
| Sửa/tự tạo challenge chính thức | 0 điểm phần incident; xem xét hủy bài nếu làm giả evidence |
| Sao chép source, report, dashboard hoặc evidence | 0 điểm toàn bài |
| Làm giả trace, screenshot, log hoặc commit history | 0 điểm toàn bài |
| Repo không chạy được end-to-end | -15 điểm |
| Hard-code output chỉ để vượt validator | -15 điểm |
| Thiếu `TEAM.md`, `REPORT.md` hoặc evidence bắt buộc | -5 điểm mỗi hạng mục |
| Tên repo/nội dung nộp sai quy ước | Yêu cầu nộp lại; có thể trừ 5 điểm |
| Nộp muộn hoặc sửa bài sau deadline | Áp dụng theo [RULES.md](RULES.md) |

`validate_logs.py` và `validate_dashboard.py` là technical gates. Điểm script không thay thế rubric.
