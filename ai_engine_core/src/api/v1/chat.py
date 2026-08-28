import asyncio 
from typing import AsyncGenerator
from fastapi import APIRouter, Query
from sse_starlette.sse import EventSourceResponse

# import các thành phần từ tầng logic
from src.schemas import agentconfig
from src.engine import asyncAIChatengine

# khởi tạo apirouter riêng cho module chat
router = APIRouter(prefix="/chat", tags=["chat & streaming"])

# khởi tạo engine
config= agentconfig(
    agent_name="VN-Enterprise-Bot",
    model_name="qwen-2.5-7b",
    system_prompt= "bạn là trợ lý AI chuyên nghiệp hỗ trợ về tra cứu thông tin"
)

engine= asyncAIChatengine(config=config)

async def generate_ai_stream(user_query:str) -> AsyncGenerator[dict, None]:
    """hàm sinh luồng streaming"""
    docs= await engine.ask_with_context(user_query)
    best_doc= docs[0]
    
    yield{
        "event": "context",
        "data": f"[tài liệu khớp #{best_doc.doc_id} | điểm: {best_doc.score*100:1.f}%]: {best_doc.summary}"
    }
    full_answer= f"dựa trên {best_doc.summary}, hệ thống xác nhận yêu cầu '{user_query} của bạn đã được tiếp nhận và xử lý hoàn tất"
    
    for word in full_answer.split(" "):
        await asyncio.sleep(0.06)
        yield {
            "event": "token",
            "data": word + " "
        }
        
    yield{
        "event": "done",
        "data": "hoàn thành"
    }

# đường dẫn lúc này sẽ tự động là /api/v1/chat/stream
@router.get("/stream")
async def stream_chat(promt: str = Query(..., example="quy định nghỉ phép năm")):
    """endpoint streaming sse cho chatbot"""
    return EventSourceResponse(generate_ai_stream(promt))
