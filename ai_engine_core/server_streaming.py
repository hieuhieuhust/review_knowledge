import asyncio 
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
from typing import AsyncGenerator

# 1. Import đúng chuẩn hoa thường từ Chặng 1
from src.schemas import agentconfig
from src.engine import asyncAIChatengine

app = FastAPI(title="ai streaming server (module 2.2)")

# 2. Khởi tạo cấu hình với đúng tham số system_prompt
config = agentconfig(
    agent_name="VN-Enterprise-Bot",
    model_name="qwen-2.5-7b",
    system_prompt="bạn là trợ lý AI chuyên nghiệp hỗ trợ tra cứu thông tin"
)
engine = asyncAIChatengine(config=config)


# --- GIAO DIỆN WEB CHAT TẠI TRANG CHỦ (/) ---
@app.get("/", response_class=HTMLResponse)
async def chat_ui():
    """Giao diện Web Chat kết nối trực tiếp vào endpoint của bạn."""
    return """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <title>Demo AI Streaming SSE</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; background: #f4f6f9; }
            .chat-container { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
            h2 { color: #2c3e50; text-align: center; }
            .input-group { display: flex; gap: 10px; margin-top: 20px; }
            input { flex: 1; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-size: 15px; }
            button { padding: 12px 24px; background: #007bff; color: white; border: none; border-radius: 8px; font-size: 15px; cursor: pointer; }
            button:hover { background: #0056b3; }
            #response-box { margin-top: 25px; padding: 15px; min-height: 100px; background: #f8f9fa; border-left: 4px solid #007bff; border-radius: 4px; font-size: 16px; line-height: 1.6; white-space: pre-wrap; }
            .context-badge { background: #e2e8f0; color: #475569; padding: 6px 10px; border-radius: 6px; font-size: 13px; margin-bottom: 10px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h2>Trợ lý AI Streaming (Module 2.2)</h2>
            <div class="input-group">
                <input type="text" id="queryInput" placeholder="Nhập câu hỏi của bạn..." value="quy định nghỉ phép năm">
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
                
                // Kết nối chính xác vào route /app/v1/chat/stream?promt=... của bạn
                const eventSource = new EventSource(`/app/v1/chat/stream?promt=${encodeURIComponent(query)}`);

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


# --- HÀM TẠO LUỒNG TOKEN STREAMING (GENERATOR) ---
async def generate_ai_stream(user_query: str) -> AsyncGenerator[dict, None]:
    """
    1. tìm tài liệu liên quan bằng pytorch
    2. streaming từng token về phía client qua server-sent event (sse)
    """
    # 1. tìm tài liệu khớp nhất với pytorch
    docs = await engine.ask_with_context(user_query)
    best_docs = docs[0]
    
    # bắn sự kiện đầu tiên: thông báo tài liệu tìm thấy
    yield {
        "event": "context",
        "data": f"[tài liệu khớp # {best_docs.doc_id} | độ tương đồng: {best_docs.score*100:.1f}%]: {best_docs.summary} "
    }
    
    # 2. giả lập câu trả lời hoàn chỉnh từ AI
    full_answer = f"dựa trên {best_docs.summary}, tôi xin phản hồi câu hỏi '{user_query}' của bạn như sau: quy trình đã được phê duyệt và bạn có thể thực hiện đúng theo hướng dẫn trên cổng nội bộ."
    
    # 3. bắn từng từ ra ngoài theo thời gian thực (streaming)
    for word in full_answer.split(" "):
        await asyncio.sleep(0.06)
        yield {
            "event": "token",
            "data": word + " "
        }
        
    # 4. bắn sự kiện kết thúc
    yield {
        "event": "done",
        "data": "[Hoàn thành]"
    }
    

# --- ENDPOINT STREAMING SSE ---
@app.get("/app/v1/chat/stream", tags=["streaming"])
async def stream_chat_endpoint(promt: str = Query(..., example="quy định nghỉ phép năm")):
    """
    client (web/app) gọi vào link này sẽ nhận luồng text chạy liên tục
    """
    return EventSourceResponse(generate_ai_stream(promt))