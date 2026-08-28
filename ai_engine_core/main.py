from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.api.v1.chat import router as chat_router
from src.api.v1.search import router as search_router

app = FastAPI(
    title="Enterprise AI Backend Platform",
    description="Hệ thống Backend AI Streaming & Vector Search chuẩn Microservices",
    version="2.0.0"
)

# 1. GẮN CÁC ROUTER VÀO VỚI TIỀN TỐ /api/v1
app.include_router(chat_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")


# 2. TRANG CHỦ GIAO DIỆN WEB CHAT
@app.get("/", response_class=HTMLResponse, tags=["UI"])
async def root_ui():
    return """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>Enterprise AI Streaming</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; background: #f4f6f9; }
            .chat-container { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h2 { color: #2c3e50; text-align: center; }
            .input-group { display: flex; gap: 10px; margin-top: 20px; }
            input { flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; }
            button { padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; }
            #response-box { margin-top: 25px; padding: 15px; min-height: 100px; background: #f8f9fa; border-left: 4px solid #007bff; border-radius: 4px; font-size: 16px; line-height: 1.6; white-space: pre-wrap; }
            .context-badge { background: #e2e8f0; color: #475569; padding: 6px 10px; border-radius: 6px; font-size: 13px; margin-bottom: 10px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h2>Enterprise AI Platform (Clean Architecture)</h2>
            <div class="input-group">
                <input type="text" id="queryInput" placeholder="Nhập câu hỏi..." value="Quy định nghỉ phép năm">
                <button onclick="startStreaming()">Gửi câu hỏi</button>
            </div>
            <div id="response-box">Câu trả lời sẽ chạy từng từ ở đây...</div>
        </div>

        <script>
            function startStreaming() {
                const query = document.getElementById('queryInput').value.trim();
                const box = document.getElementById('response-box');
                if (!query) return;

                box.innerHTML = "Đang tìm kiếm tài liệu từ PyTorch VectorStore...<br><br>";
                
                // Kết nối vào đúng route chuẩn: /api/v1/chat/stream
                const eventSource = new EventSource(`/api/v1/chat/stream?prompt=${encodeURIComponent(query)}`);

                eventSource.addEventListener('context', function(e) {
                    box.innerHTML = `<div class="context-badge">${e.data}</div><br><br><b>AI Phản hồi:</b> `;
                });

                eventSource.addEventListener('token', function(e) {
                    box.innerHTML += e.data;
                });

                eventSource.addEventListener('done', function(e) {
                    eventSource.close();
                });

                eventSource.onerror = function() {
                    eventSource.close();
                };
            }
        </script>
    </body>
    </html>
    """