# Báo cáo Day 13 Observability

## 1. Thông tin nhóm

- Tên nhóm: NhomGiCungDuoc
- Repository URL: https://github.com/th3UnmatchedK1yo/Day13-K3-Observability-E403-NhomGiCungDuoc
- Commit SHA cuối: 09135074c7610912b9e4fe3dc125cd8a3f836cec
- Thành viên và vai trò:
  - Võ Hà Minh Huy (2A202601373) - Dashboard, SLO & Alert
  - Đỗ Duy Đông (2a202601657) - Logging & PII
  - Nguyễn Minh Thái (2A202601619) - Tracing & Prompt Version, Incident & Demo

## 2. Kết quả kỹ thuật

- Điểm `validate_logs.py`: 100/100 (Xem ảnh: evidence/validate_logs.png)
- Tổng số traces: >10 (Xem ảnh: evidence/traces_list.png)
- Số PII leak còn lại: 0
- Link/đường dẫn dashboard: Sử dụng Langfuse Dashboard

## 3. Logging và tracing

- Evidence correlation ID: evidence/logs_metadata.png
- Evidence PII redaction: evidence/logs_pii.png
- Evidence trace waterfall: evidence/trace_waterfall_rag_slow.png
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

## 7. Bonus: Cost Optimization & Audit Log
- Đã cấu hình giới hạn token đầu ra (max 250) để chống vọt xà chi phí (Cost Spike). Bằng chứng: evidence/cost_spike_bonus.png

## 8. Đóng góp cá nhân

Với mỗi thành viên, ghi rõ nhiệm vụ và link commit/PR tương ứng.

| Thành viên | Phần việc (Nhiệm vụ & File phụ trách) | Commit/PR | Điều đã học |
|---|---|---|---|
| **Đỗ Duy Đông** (Tech Lead) | **CP1:** Thiết lập Structured Logging, Middleware (Correlation ID) và bảo vệ dữ liệu (PII).<br>*(File: `app/logging_config.py`, `app/middleware.py`, `app/pii.py`, `app/main.py`)* | [Sinh viên chèn link commit của Đông] | Hiểu cách setup logs tập trung, truy vết request qua hệ thống vi dịch vụ. |
| **Võ Hà Minh Huy** (SRE) | **CP2 & Bonus:** Cấu hình Dashboard Spec, đo lường SLO, Alert Rules, Runbook xử lý sự cố và tính năng Cost Optimization.<br>*(File: `config/slo.yaml`, `config/alert_rules.yaml`, `docs/alerts.md`, `docs/dashboard-spec.md`, `app/incidents.py`, `app/mock_llm.py`)* | [Sinh viên chèn link commit của Huy] | Biết cách định lượng độ tin cậy, lên kịch bản on-call thực chiến và kiểm soát chi phí LLM. |
| **Nguyễn Minh Thái** (QA) | **CP3 & Report:** Tích hợp Langfuse Tracing (Sub-components), Fetch Prompt, tính năng Anomaly Detection và chịu trách nhiệm toàn bộ hồ sơ Báo cáo.<br>*(File: `app/tracing.py`, `app/agent.py`, `app/mock_rag.py`, `scripts/detect_anomalies.py`, `submission/REPORT.md`, `evidence/*`)* | [Sinh viên chèn link commit của Thái] | Nắm vững kỹ thuật dùng Trace Waterfall để xác định gốc rễ của độ trễ (latency spikes). |
