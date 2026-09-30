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
  3. Mở trace cùng `correlation_id` trên Langfuse, so sánh các span chính để xác định bước nào bất thường.
- Mitigation tạm thời: dựa trên evidence thực tế để rollback prompt, khôi phục cấu hình liên quan, tắt practice scenario hoặc giảm tải khi demo.
- Owner: `student-<MSSV>`

## Alert 1

- Tên: `HighLatencyP95`
- Severity: `warning`
- Duration: `5m`
- Kênh thông báo: Slack `#k4-l3b-alerts`
- SLI/SLO liên quan: SLO `fast_successful_requests` (99.5% request có `response_sent.latency_ms <= 3000`, cửa sổ 28 ngày) — panel **Latency percentiles and TTFT**
- Điều kiện và thời gian duy trì: `p95(response_sent.latency_ms) > 3000ms` liên tục trong 5 phút
- Ảnh hưởng tới người dùng: người dùng chờ lâu trước khi nhận câu trả lời; mỗi request chậm hơn 3000ms tiêu vào error budget 0.5%
- Ba bước kiểm tra đầu tiên:
  1. Mở dashboard panel Latency: xác nhận P95/P99 tăng từ lúc nào; so TTFT P95 với latency — TTFT bình thường mà latency cao nghĩa là chậm nằm ngoài bước sinh token đầu tiên.
  2. Lọc `data/logs.jsonl` trong khoảng đó lấy `response_sent` có `latency_ms` cao nhất và ghi lại `correlation_id`.
  3. Trên Langfuse, lọc trace theo metadata `correlation_id`, mở waterfall và so thời lượng `retrieve-context` với `generate-response` để xác định span chiếm phần lớn thời gian.
- Mitigation tạm thời: nếu span retrieval chậm thì tắt/khôi phục cấu hình retrieval (practice: `python scripts/inject_incident.py --scenario rag_slow --disable`); nếu generation chậm sau khi đổi prompt thì rollback label `production` về version trước; giảm concurrency khi demo.
- Owner: `student-2A202602781`

## Alert 2

- Tên: `HighErrorRateOrRetrievalFailing`
- Severity: `critical`
- Duration: `5m`
- Kênh thông báo: Slack `#k4-l3b-alerts`
- SLI/SLO liên quan: guardrail `error_rate_pct_max: 2` và `retrieval_success_rate_pct_min: 90` trong `config/slo.yaml`; request lỗi là bad event của SLO chính — panel **Error rate and retrieval success**
- Điều kiện và thời gian duy trì: `request_failed / request_received * 100 > 2%` **hoặc** `retrieval success < 90%` liên tục trong 5 phút
- Ảnh hưởng tới người dùng: người dùng nhận HTTP 500 thay vì câu trả lời, hoặc câu trả lời thiếu context; error budget bị tiêu rất nhanh
- Ba bước kiểm tra đầu tiên:
  1. Mở panel Errors: xem error rate, breakdown theo `error_type` và retrieval success giảm từ lúc nào.
  2. Lọc log `event == "request_failed"` trong khoảng đó, ghi lại `error_type`, `tool_name`, `payload.detail` và `correlation_id`.
  3. Mở trace cùng `correlation_id` trên Langfuse: tìm observation có level `ERROR` và đọc `statusMessage` để biết bước nào ném lỗi.
- Mitigation tạm thời: tắt nguồn lỗi đã xác định (practice: `python scripts/inject_incident.py --scenario tool_fail --disable`), khôi phục dependency/cấu hình retrieval, hoặc rollback thay đổi gần nhất; thông báo trên kênh Slack cho đến khi error rate về dưới 2%.
- Owner: `student-2A202602781`

## Alert 3

- Tên: `CostPerRequestSpike`
- Severity: `warning`
- Duration: `10m`
- Kênh thông báo: Slack `#k4-l3b-alerts`
- SLI/SLO liên quan: guardrail `daily_cost_usd_max: 2.5` trong `config/slo.yaml`; baseline `avg_cost_usd ≈ 0.0021` — panel **Cost over time** và **Input and output tokens**
- Điều kiện và thời gian duy trì: `avg(response_sent.cost_usd) > 0.005 USD/request` (≈ 2.4× baseline) liên tục 10 phút, **hoặc** tổng cost 24h > 2.5 USD
- Ảnh hưởng tới người dùng: câu trả lời dài bất thường (chậm hơn, khó đọc) và ngân sách bị đốt nhanh; nếu kéo dài sẽ phải hạ chất lượng/giới hạn dịch vụ
- Ba bước kiểm tra đầu tiên:
  1. Mở panel Cost và Tokens: xác định cost tăng do `tokens_in` (prompt/context dài) hay `tokens_out` (câu trả lời dài), và traffic có tăng không — cost tăng mà traffic không tăng nghĩa là cost/request tăng.
  2. Lọc `response_sent` có `cost_usd`/`tokens_out` cao nhất, ghi lại `correlation_id`.
  3. Mở trace tương ứng: xem usage/cost của generation `generate-response` và prompt version được link — so với trace baseline cùng input.
- Mitigation tạm thời: rollback label `production` về prompt version trước nếu version mới làm câu trả lời dài hơn; tắt nguồn gây tăng token (practice: `python scripts/inject_incident.py --scenario cost_spike --disable`); giới hạn độ dài output.
- Owner: `student-2A202602781`
