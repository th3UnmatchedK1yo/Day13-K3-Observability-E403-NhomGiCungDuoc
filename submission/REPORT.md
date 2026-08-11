# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: NhomGiCungDuoc
- Repository URL: [Sinh viên chèn link repo]
- Commit SHA cuối: [Sinh viên chèn mã SHA]
- Thành viên và vai trò:
  - Võ Hà Minh Huy (2A202601373) - Dashboard, SLO & Alert
  - Đỗ Duy Đông (2a202601657) - Logging & PII
  - Nguyễn Minh Thái (2A202601619) - Tracing & Prompt Version, Incident & Demo

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100
- Tổng số traces: >10
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: Sử dụng Langfuse Dashboard

## 3. Logging và tracing

- Evidence correlation ID: evidence/correlation_id.png
- Evidence PII redaction: evidence/pii_redaction.png
- Evidence trace waterfall: evidence/trace_waterfall.png
- Giải thích một span đáng chú ý: Dựa trên Trace Waterfall của request bị chậm (lúc làm CP3), span `retrieve` thuộc mock_rag tốn nhiều thời gian nhất (>2s), kéo theo tổng thời gian xử lý của cả request tăng lên. Điều này chứng tỏ sự cần thiết của sub-component trace trong việc phát hiện nút thắt cổ chai.

## 4. Prompt versioning

- Prompt name: day13-chat
- Version/label baseline: v1 / production
- Version/label candidate: v2 / staging
- Trace ID của mỗi version: [Sinh viên tự điền sau khi test]
- Bằng chứng đổi label hoặc rollback: evidence/prompt_versioning.png

## 5. Dashboard, SLO và alerts

- Kết quả `validate_dashboard.py`: 6/6
- Evidence dashboard: evidence/dashboard.png
- SLO đã chọn và lý do: Sử dụng bộ thông số mặc định (Latency P95 < 3s, Error Rate < 2%, Cost < 2.5USD, Quality >= 0.75). Lý do: Đây là các thông số thực tế, đảm bảo trải nghiệm người dùng không bị gián đoạn và giới hạn ngân sách rõ ràng.
- Alert rules và runbook: Đã cấu hình thành công 3 cảnh báo (high_latency_p95, elevated_error_rate, cost_budget_exceeded) trong file `config/alert_rules.yaml` và viết tài liệu xử lý tại `docs/alerts.md`.

## 6. Điều tra challenge

- Challenge ID: day13-k3-observability-v1
- Triệu chứng từ metrics: Đỉnh độ trễ (latency spike) tăng mạnh đột biến. Chỉ số P95 Latency vượt xa mức 2 giây đối với tính năng `refund`.
- Trace ID liên quan: req-252f0f66
- Log line/correlation ID liên quan: req-252f0f66
- Root cause: Hệ thống RAG (Retrieval-Augmented Generation) phản hồi rất chậm. Hàm `retrieve` bên trong `app/mock_rag.py` tốn quá nhiều thời gian gây nghẽn toàn bộ luồng xử lý (Do kịch bản sự cố `rag_slow`).
- Fix action: Khởi động lại service, tối ưu hoá vector database hoặc thêm timeout giới hạn thời gian chờ cho RAG retrieval. (Trong Lab: Tắt incident bằng cờ `--disable`).
- Preventive measure: Thiết lập Alert tự động cho chỉ số `latency_p95` (rule `high_latency_p95`). Áp dụng cơ chế Caching (bộ nhớ đệm) để trả về ngay kết quả cho các câu hỏi trùng lặp mà không cần gọi RAG. Lắp Circuit Breaker để ngắt mạch khi vector store phản hồi chậm.
## 7. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc | Commit/PR | Điều đã học |
|---|---|---|---|
| Võ Hà Minh Huy | Dashboard, SLO & Alert | (chèn link commit) | Hiểu cách setup metrics và xây dựng Runbook |
| Đỗ Duy Đông | Logging & PII | (chèn link commit) | Cấu hình log struct và redact PII Regex |
| Nguyễn Minh Thái | Tracing & Prompt, Incident & Demo | (chèn link commit) | Cách điều tra root cause bằng traces và logs |
