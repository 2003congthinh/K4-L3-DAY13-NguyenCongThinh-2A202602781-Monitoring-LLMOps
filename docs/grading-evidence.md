# Danh sách evidence cần thu thập

## Bắt buộc

- Kết quả cuối của `validate_logs.py`.
- Danh sách có tối thiểu 10 traces.
- Một trace waterfall đầy đủ, có span retrieval và LLM tách riêng.
- Hai prompt version và trace hiển thị đúng name/label/version.
- Một bằng chứng đổi label hoặc rollback prompt.
- Log JSON có correlation ID và metadata.
- Log chứng minh PII đã được redact.
- Kết quả `python scripts/validate_dashboard.py` hợp lệ.
- Dashboard đủ 6 nhóm chỉ số.
- Alert rules và runbook đã hoàn thiện.
- Evidence điều tra challenge: metric, log line/correlation ID và trace ID liên quan.

## Không bắt buộc

- So sánh trước/sau khi tối ưu chi phí.
- Audit log tách riêng.
- Custom metric hoặc automation do nhóm tự xây.

Ảnh phải đặt trong `submission/evidence/` và được dẫn lại bằng đường dẫn tương đối trong `submission/reports/GROUP_REPORT.md` hoặc báo cáo cá nhân liên quan.
