# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert mẫu để tham khảo

Ví dụ dưới đây minh họa mức độ cụ thể cần có. Học viên không cần copy nguyên, nhưng ba alert trong bài nộp nên rõ ràng tương tự: điều kiện là gì, kéo dài bao lâu, ảnh hưởng tới user ra sao và người trực cần kiểm tra gì trước.

- Tên: `HighLatencyP95`
- Severity: `warning`
- Duration: `5m`
- Kênh thông báo: Slack `#k4-l3b-alerts`
- SLI/SLO liên quan: latency P95 của `response_sent.latency_ms`
- Điều kiện và thời gian duy trì: `p95(latency_ms) > 3000ms` trong 5 phút
- Ảnh hưởng tới người dùng: người dùng phải chờ lâu hơn trước khi nhận câu trả lời
- Ba bước kiểm tra đầu tiên:
  1. Mở dashboard latency để xác nhận P95/P99 và khoảng thời gian tăng.
  2. Lọc `data/logs.jsonl` trong khoảng đó, lấy một `correlation_id` có `latency_ms` cao.
  3. Mở trace cùng `correlation_id` trên Langfuse, so sánh thời gian span retrieval và generation.
- Mitigation tạm thời: nếu prompt version mới làm token tăng, rollback `production`; nếu retrieval chậm, tắt incident/practice scenario hoặc giảm concurrency khi demo.
- Owner: `student-<MSSV>`

## Alert 1

- Tên:
- Severity:
- Duration:
- Kênh thông báo: Slack
- SLI/SLO liên quan:
- Điều kiện và thời gian duy trì:
- Ảnh hưởng tới người dùng:
- Ba bước kiểm tra đầu tiên:
- Mitigation tạm thời:
- Owner:

## Alert 2

- Tên:
- Severity:
- Duration:
- Kênh thông báo: Slack
- SLI/SLO liên quan:
- Điều kiện và thời gian duy trì:
- Ảnh hưởng tới người dùng:
- Ba bước kiểm tra đầu tiên:
- Mitigation tạm thời:
- Owner:

## Alert 3

- Tên:
- Severity:
- Duration:
- Kênh thông báo: Slack
- SLI/SLO liên quan:
- Điều kiện và thời gian duy trì:
- Ảnh hưởng tới người dùng:
- Ba bước kiểm tra đầu tiên:
- Mitigation tạm thời:
- Owner:
