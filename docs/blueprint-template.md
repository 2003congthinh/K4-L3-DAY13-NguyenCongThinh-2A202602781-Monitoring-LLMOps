# Khung thiết kế Observability

Dùng khung này trước khi triển khai, sau đó chuyển kết quả cuối sang `submission/REPORT.md`.

## Người dùng và luồng chính

- Ai gửi request?
- Request đi qua những thành phần nào?
- Correlation ID được tạo và truyền ở đâu?

## Tín hiệu quan sát

| Thành phần | Log cần có | Metric cần có | Span cần có |
|---|---|---|---|
| API | | | |
| Retrieval | | | |
| LLM | | | |

## SLO và alert

| SLI | Mục tiêu | Cửa sổ đo | Alert |
|---|---:|---|---|
| Latency P95 | | | |
| Error rate | | | |
| Cost | | | |
| Quality | | | |

## Rủi ro dữ liệu

- PII có thể xuất hiện ở đâu?
- Dữ liệu nào được phép ghi vào log?
- Redaction diễn ra trước bước nào?
