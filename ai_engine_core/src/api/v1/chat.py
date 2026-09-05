import asyncio 
from typing import AsyncGenerator, Optional
from fastapi import APIRouter, Query, Depends, Header, HTTPException, status
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.ext.asyncio import AsyncSession

# import các thành phần từ tầng logic
from src.schemas import agentconfig
from src.engine import asyncAIChatengine
from src.api.v1.auth import get_current_user

# import các thành phần trong database
from src.db.session import get_db
from src.db.models import UserModel, ConversationModel, MessageModel

# khởi tạo apirouter riêng cho module chat
router = APIRouter(prefix="/chat", tags=["chat & streaming"])

# khởi tạo engine
config= agentconfig(
    agent_name="VN-Enterprise-Bot",
    model_name="qwen-2.5-7b",
    system_prompt= "bạn là trợ lý AI chuyên nghiệp hỗ trợ về tra cứu thông tin"
)

engine= asyncAIChatengine(config=config)

# dependency injection với depend(): kiểm tra quyền truy cập qua api key
async def  verify_api_key(x_api_key: str=Header(default="my-secret-key-123")):
    """hàm bảo vệ: chỉ có ai có API key mới được dùng"""
    if x_api_key != "my-secret-api-key-123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="api key không hợp lệ! vui lòng kiểm tra lại"
        )
    return x_api_key

async def generate_ai_stream_and_save(
    conversation_id: Optional[int],
    user_query:str,
    db: AsyncSession,
    user_id: int
    ) -> AsyncGenerator[dict, None]:
    
    # 1. nếu chưa có cuộc trò chuyện -> tạo mới và gắn đúng user_id của người này
    if not conversation_id or conversation_id <= 0:
        new_conv = ConversationModel(
            user_id= user_id,
            title= user_query[30]
        )
        db.add(new_conv)
        await db.commit
        await db.commit
        conversation_id=new_conv.id
        
    # 2. lưu câu hỏi của user và database
    user_msg = MessageModel(conversation_id= conversation_id, role="user", content= user_query)
    db.add(user_msg)
    await db.commit()
    
    # 3. tìm tài liệu từ pytorch vectorstore
    docs = await engine.ask_with_context(user_query)
    best_doc = docs[0]
    
    """hàm sinh luồng streaming"""
    docs= await engine.ask_with_context(user_query)
    best_doc= docs[0]
    
    yield{ # thông báo cho người đọc qua frontend qua event context
        "event": "context",
        "data": f"[tài liệu khớp #{best_doc.doc_id} | điểm: {best_doc.score*100:1.f}%]: {best_doc.summary}"
    }
    
    # 4. stream từng từ ra ngoài
    full_answer= f"dựa trên {best_doc.summary}, hệ thống xác nhận yêu cầu '{user_query} của bạn đã được tiếp nhận và xử lý hoàn tất"
    accumulated = []
    
    for word in full_answer.split(" "):
        await asyncio.sleep(0.06)
        accumulated.append(word)
        yield { # stream nội dung AI qua event token
            "event": "token",
            "data": word + " "
        }
    
    # 5. lưu câu trả lời của ai vào database
    ai_msg = MessageModel(
        conversation_id= conversation_id,
        role = "assistant",
        content= " ".join(accumulated)
    )
    
    yield{ # báo cho frontend biết là đã done qua event
        "event": "done",
        "data": "hoàn thành"
    }

# đường dẫn lúc này sẽ tự động là /api/v1/chat/stream
@router.get("/stream")
async def stream_chat(
    promt: str = Query(..., example="quy định nghỉ phép năm"),
    conversation_id: Optional[int] = Query(default=None), 
    db: AsyncSession = Depends(get_db),
    current_user: UserModel= Depends(get_current_user)
):
    """endpoint streaming sse cho chatbot"""
    return EventSourceResponse(
        generate_ai_stream_and_save(
            conversation_id=conversation_id,
            user_query= promt,
            db= db,
            user_id=current_user.id
        )
    )
