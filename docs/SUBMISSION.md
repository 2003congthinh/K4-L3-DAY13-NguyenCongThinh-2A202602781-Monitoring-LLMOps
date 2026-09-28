# Hướng dẫn nộp bài cá nhân Day 13

## 1. Hình thức và tên repository

Đây là **bài lab cá nhân**. Mỗi học viên làm và nộp một repository riêng theo mẫu:

```text
K4-L3-DAY13-HoVaTen-MSSV-Monitoring-LLMOps
```

Ví dụ:

```text
K4-L3-DAY13-NguyenVanAn-123456-Monitoring-LLMOps
```

Tên viết không dấu, không khoảng trắng và ngăn cách bằng dấu `-`. Không dùng tên nhóm và không nộp chung repository với học viên khác.

## 2. Nộp ở đâu và nộp thông tin gì?

Mỗi học viên tự nộp trên VLearn LMS/Codelabs:

1. URL repository cá nhân.
2. Commit SHA cuối dùng để chấm.

Deadline mặc định là 23:59:59 ngày diễn ra lab theo múi giờ Asia/Ho_Chi_Minh. Nếu có thông báo khác, dùng mốc chính thức mới nhất của Lab Coach/Key Coach.

Commit SHA phải tồn tại trên remote và chứa đầy đủ source, config, `submission/REPORT.md` và evidence. Các thay đổi sau deadline không được dùng để chấm nếu không có thông báo gia hạn.

## 3. Cấu trúc bắt buộc

```text
K4-L3-DAY13-HoVaTen-MSSV-Monitoring-LLMOps/
├── app/                         # source đã hoàn thiện
├── config/                      # dashboard, SLO, alert và challenge gốc
├── data/                        # input mẫu; không commit log chứa PII
├── docs/
│   └── alerts.md                # runbook cho ba alert
├── scripts/                     # load test, incident và validators
├── tests/                       # public tests và test bổ sung
├── submission/
│   ├── REPORT.md                # báo cáo cá nhân duy nhất
│   └── evidence/
│       ├── README.md
│       └── các file evidence
├── README.md
├── requirements.txt
└── .env.example
```

Không tạo `TEAM.md`, group report hoặc báo cáo thành viên riêng. Toàn bộ kết quả và phần giải thích của học viên nằm trong `submission/REPORT.md`.

## 4. Quy tắc chung cho evidence

Evidence phải chứng minh kết quả chạy trên đúng commit SHA được nộp:

- Ảnh phải đọc được tên màn hình/panel, giá trị, time range và ID liên quan.
- Không cắt mất thông tin cần đối chiếu, nhưng phải che secret và PII.
- Dùng dữ liệu test của repo; không dùng dữ liệu thật của người dùng.
- Test/validator có thể lưu dạng ảnh `.png` hoặc output text `.txt`.
- Source, YAML, runbook và commit được dẫn bằng đường dẫn/link; không cần chụp toàn bộ code.
- Mọi đường dẫn trong report phải là đường dẫn tương đối và mở được trên GitHub.
- Không dùng source, report, trace ID hoặc evidence của học viên khác/lớp khác.

Từ `submission/REPORT.md`, dẫn ảnh như sau:

```markdown
![Dashboard overview](evidence/11-dashboard-overview.png)
```

Không dùng đường dẫn cục bộ như `C:\Users\...` hoặc `/home/student/...`.

## 5. Checklist evidence bắt buộc

Tên file dưới đây là gợi ý; có thể dùng tên khác nếu `REPORT.md` dẫn đúng.

| Evidence | Nội dung phải nhìn thấy hoặc kiểm chứng được | File gợi ý |
|---|---|---|
| Test cuối | Lệnh `python -m pytest -q`, số test pass/fail | `01-pytest.png` hoặc `.txt` |
| Log validator | Kết quả cuối của `validate_logs.py`, điểm tối thiểu 80/100 | `02-log-validator.png` |
| Dashboard validator | Kết quả `validate_dashboard.py`, đủ 6/6 | `03-dashboard-validator.png` |
| Structured log | Log JSON có timestamp, event, `correlation_id`, model, env, feature và latency | `04-structured-log.png` |
| PII redaction | Input test chứa PII giả và log đầu ra đã che email/điện thoại/CCCD/thẻ | `05-pii-redaction.png` |
| Trace list | Danh sách tối thiểu 10 traces do chính học viên tạo | `06-trace-list.png` |
| Trace waterfall | Một trace có root observation, retrieval và generation theo đúng quan hệ cha-con | `07-trace-waterfall.png` |
| Trace metadata | `correlation_id`, model, prompt name/version/label, token và cost; không có PII thô | `08-trace-metadata.png` |
| Prompt versions | Prompt v1/v2 và các label `baseline`, `candidate`, `production` | `09-prompt-versions.png` |
| Prompt rollback | Trạng thái trước/sau khi promote hoặc rollback `production`; kèm trace ID của hai version trong report | `10-prompt-rollback.png` |
| Dashboard runtime | Đủ 6 panel, có dữ liệu, time range, đơn vị và threshold/SLO line | `11-dashboard-overview.png` |
| Incident metric | Metric bất thường và khoảng thời gian xảy ra challenge | `12-incident-metric.png` |
| Incident log | Log line bất thường có `correlation_id` | `13-incident-log.png` |
| Incident trace | Trace có cùng `correlation_id`, thấy span gây chậm/lỗi | `14-incident-trace.png` |

Nếu dashboard không thể đọc rõ trong một ảnh, tách thành `11a-dashboard-latency-errors.png` và `11b-dashboard-cost-token-quality.png`.

## 6. Evidence nào không cần chụp ảnh?

Không cần screenshot các file sau vì giảng viên kiểm tra trực tiếp trên commit:

- `config/slo.yaml`;
- `config/alert_rules.yaml`;
- `docs/alerts.md`;
- source code và tests;
- commit history.

Trong `submission/REPORT.md`, hãy dẫn đúng file, section hoặc commit liên quan.

## 7. Yêu cầu riêng cho incident

Evidence incident chỉ hợp lệ khi ba tín hiệu cùng chỉ về một request hoặc cùng khoảng sự cố:

```text
Metric bất thường
        ↓
Log có correlation_id
        ↓
Trace có cùng correlation_id
        ↓
Span gây ảnh hưởng
        ↓
Root cause và hành động xử lý
```

`REPORT.md` phải ghi challenge ID, khoảng thời gian, metric cụ thể, log line/`correlation_id`, trace ID, span gây ảnh hưởng, root cause, fix action và preventive measure.

Không sửa, tự tạo hoặc lấy `config/challenge.json` từ lớp khác.

## 8. Nội dung báo cáo cá nhân

Hoàn thiện trực tiếp `submission/REPORT.md`. Báo cáo phải có:

- họ tên, MSSV, lớp, repository URL và commit SHA;
- kết quả baseline và kết quả cuối;
- cách triển khai logging, PII, tracing và prompt version;
- dashboard, SLO, error budget và alerts;
- chuỗi điều tra incident;
- một quyết định kỹ thuật và lý do;
- một lỗi/blocker cùng cách xử lý;
- giải thích luồng Metrics → Logs → Traces;
- vai trò của prompt version, token/cost, SLO hoặc rollback;
- điều học được và hạn chế còn lại;
- đường dẫn tới toàn bộ evidence bắt buộc.

Nội dung phải do chính học viên thực hiện và khớp với source, evidence cùng lịch sử Git của repository cá nhân.

## 9. Không được nộp

- `.env`, Langfuse secret, API key hoặc token.
- PII nguyên văn trong log, trace, screenshot hoặc report.
- `.venv/`, cache, dependency đã cài hoặc file sinh ra không phục vụ chấm.
- Source, report, trace ID hoặc evidence của học viên/lớp khác.
- Evidence giả hoặc ảnh đã chỉnh sửa làm sai lệch kết quả.
- `config/challenge.json` đã bị tự ý sửa.
- Ảnh dashboard trống hoặc ảnh không đọc được thông tin cần chấm.

## 10. Kiểm tra trước khi push

Chạy trên commit cuối:

```bash
python -m pytest -q
python scripts/validate_logs.py
python scripts/validate_dashboard.py
git status --short
git log -1 --oneline
```

Checklist cuối:

- [ ] Source và TODO bắt buộc đã hoàn thành bằng repository cá nhân.
- [ ] Test, log validator và dashboard validator có evidence.
- [ ] Có tối thiểu 10 traces, waterfall, metadata và prompt rollback.
- [ ] Dashboard đủ 6 panel; SLO/error budget và 3 alert/runbook đã hoàn thiện.
- [ ] Incident evidence nối đúng metric → log → trace.
- [ ] `submission/REPORT.md` đã điền đầy đủ.
- [ ] Không có secret, PII thô hoặc nội dung sao chép từ người khác/lớp khác.
- [ ] Tất cả link/ảnh mở được trực tiếp trên GitHub.
- [ ] URL repo cá nhân và commit SHA cuối đã được nộp.
