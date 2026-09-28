# Rubric Day 13 Monitoring & LLMOps

Điểm bắt buộc là 100: 60 điểm nhóm và 40 điểm cá nhân. Bonus tối đa 10 điểm, tổng tối đa 110. Mọi điểm phải có code chạy được và evidence thuộc đúng commit SHA đã nộp.

## A. Điểm nhóm — 60 điểm

### A1. Logging và correlation — 10 điểm

| Thành phần | Điểm | Bằng chứng |
|---|---:|---|
| Nhận `x-request-id` hoặc sinh ID hợp lệ, truyền và trả lại qua response header | 4 | middleware, response header và structured log |
| Log JSON có event, timestamp, `correlation_id` và metadata model/env/feature | 3 | `04-structured-log` và source liên quan |
| Log validator đạt tối thiểu 80/100, không rò context giữa request | 3 | `02-log-validator` và test |

Không đạt tối đa nếu chỉ hard-code output để vượt validator hoặc log không nối được với trace.

### A2. PII protection — 10 điểm

| Thành phần | Điểm | Bằng chứng |
|---|---:|---|
| Có rule cho email, điện thoại Việt Nam, CCCD và thẻ thanh toán | 4 | `app/pii.py` và tests |
| PII được scrub trước bước render/ghi file | 3 | logging processor/config và giải thích trong report |
| Log/trace thực tế không còn PII mẫu nguyên văn | 3 | `05-pii-redaction` |

Ảnh chỉ chụp regex hoặc code không thay thế evidence runtime.

### A3. Tracing và prompt version — 10 điểm

| Thành phần | Điểm | Bằng chứng |
|---|---:|---|
| Có tối thiểu 10 traces và liên kết được với log bằng `correlation_id` | 3 | `06-trace-list`, `08-trace-metadata` |
| Trace có root, retrieval và generation đúng quan hệ cha-con; có model, token và cost | 3 | `07-trace-waterfall` |
| Có prompt v1/v2 và trace gắn đúng name/version/label | 2 | `09-prompt-versions` và trace IDs trong report |
| Chứng minh promote/rollback label `production` | 2 | `10-prompt-rollback` |

Trace không có child observation hoặc chứa PII thô không đạt điểm tối đa.

### A4. Dashboard, SLO và alerts — 10 điểm

| Thành phần | Điểm | Bằng chứng |
|---|---:|---|
| Dashboard có dữ liệu và đủ 6 panel: latency/TTFT, traffic, errors/retrieval, cost, tokens, quality | 4 | `11-dashboard-overview` |
| Có đơn vị, time range và threshold/SLO line hợp lý | 2 | dashboard runtime |
| Một SLO và error budget được giải thích | 1 | `config/slo.yaml` và group report |
| Ba alert symptom-based có duration, severity, owner, Slack channel và runbook | 1 | `config/alert_rules.yaml`, `docs/alerts.md` |
| Dashboard validator đạt 6/6 | 2 | `03-dashboard-validator` |

Validator 6/6 nhưng không có dashboard runtime vẫn không đạt đủ điểm.

### A5. Incident investigation — 10 điểm

| Thành phần | Điểm | Bằng chứng |
|---|---:|---|
| Ghi đúng challenge ID, metric bất thường và khoảng thời gian | 2 | `12-incident-metric` |
| Tìm log line/`correlation_id` liên quan | 2 | `13-incident-log` |
| Tìm trace có cùng `correlation_id` và span gây ảnh hưởng | 2 | `14-incident-trace` |
| Root cause phù hợp với chuỗi evidence | 2 | group report và demo |
| Fix action và preventive measure khả thi | 2 | group report |

Metric, log và trace không cùng sự cố sẽ không được tính là một investigation hoàn chỉnh.

### A6. Integration và demo — 10 điểm

| Thành phần | Điểm | Bằng chứng |
|---|---:|---|
| Tests chạy trên commit cuối | 4 | `01-pytest` |
| Repo cài đặt và chạy lại được theo README | 2 | source, requirements và lệnh demo |
| Group report đầy đủ, link evidence mở được | 2 | `GROUP_REPORT.md` |
| Demo được luồng Metrics → Logs → Traces → Root cause | 2 | demo/Q&A |

## B. Điểm cá nhân — 40 điểm

### B1. Ownership kỹ thuật — 15 điểm

| Thành phần | Điểm | Bằng chứng |
|---|---:|---|
| Có commit/PR riêng, khớp khai báo trong `TEAM.md` | 5 | lịch sử Git và report cá nhân |
| Có đóng góp kỹ thuật thực vào file/hàm/artifact được giao | 6 | code/config/test/dashboard/runbook |
| Tự chạy, kiểm chứng và giải thích được phần mình làm | 4 | evidence, lệnh kiểm tra và Q&A |

Chỉ sửa tên, format report hoặc thực hiện công việc hành chính không được tính là ownership kỹ thuật đầy đủ.

### B2. Hiểu luồng end-to-end — 15 điểm

| Thành phần | Điểm | Chuẩn cần giải thích |
|---|---:|---|
| Metrics | 4 | metric nào phát hiện triệu chứng và vì sao |
| Logs | 4 | cách khoanh vùng và lấy `correlation_id` |
| Traces | 4 | cách tìm span gây chậm/lỗi và kết luận root cause |
| LLMOps vận hành | 3 | vai trò của prompt version, token/cost, SLO hoặc rollback |

Điểm này được chấm bằng report cá nhân và Q&A; không chỉ dựa vào vai trò được phân công.

### B3. Báo cáo cá nhân — 10 điểm

| Thành phần | Điểm | Bằng chứng |
|---|---:|---|
| Nhiệm vụ, file/hàm, commit/PR và artifact được ghi rõ | 3 | report cá nhân |
| Có quyết định kỹ thuật, blocker và cách xử lý cụ thể | 3 | report cá nhân |
| Có evidence/lệnh kiểm tra mở được | 2 | link tương đối, commit hoặc PR |
| Nội dung khớp Git, `TEAM.md` và không sao chép | 2 | đối chiếu toàn repo |

## C. Bonus — tối đa 10 điểm

Chỉ chấm bonus khi phần bắt buộc chạy được end-to-end:

- Tối đa +5: cost optimization có before/after trên cùng workload.
- Tối đa +5: automation hữu ích như secret/PII scan, dashboard generation hoặc CI.
- Tối đa +5: audit log riêng có schema, retention và truy vấn minh họa.

Tổng bonus không vượt 10 điểm.

## D. Technical gates và vi phạm

- `validate_logs.py` và `validate_dashboard.py` là technical gates, không thay thế evidence runtime hoặc rubric.
- Screenshot không thay thế source/config; source/config không thay thế screenshot runtime.
- Chỉ chấm artifact có trong commit SHA đã nộp.

| Vi phạm | Mức xử lý |
|---|---:|
| Commit API key, secret hoặc PII | -20 điểm; có thể 0 điểm nếu rò rỉ nghiêm trọng |
| Sửa/tự tạo challenge chính thức hoặc dùng challenge sai lớp | 0 điểm phần incident; có thể hủy bài nếu làm giả evidence |
| Sao chép source, report, dashboard hoặc evidence | 0 điểm toàn bài |
| Làm giả trace, screenshot, log hoặc commit history | 0 điểm toàn bài |
| Repo không chạy được end-to-end | -15 điểm |
| Hard-code output chỉ để vượt validator | -15 điểm |
| Thiếu `TEAM.md`, group report hoặc evidence nhóm bắt buộc | -5 điểm mỗi hạng mục |
| Thiếu report cá nhân | Thành viên đó mất toàn bộ điểm B3 và không có căn cứ chấm các phần cá nhân liên quan |
| Tên repo hoặc nội dung nộp sai quy ước | Yêu cầu nộp lại; có thể trừ 5 điểm |
| Nộp muộn hoặc sửa bài sau deadline | Áp dụng theo [RULES.md](RULES.md) |

Danh sách và cách đặt evidence xem tại [SUBMISSION.md](SUBMISSION.md) và [grading-evidence.md](grading-evidence.md).
