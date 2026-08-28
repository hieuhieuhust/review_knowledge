import asyncio
import json
from pathlib import Path
from typing import List, AsyncGenerator
from src.schemas import agentconfig,  messageschema, searchresultschema
from src.exceptions import emptyqueryerror
from src.decorates import measure_async_latency, logger
from src.vector_store import pytorchvectorstorage

class asyncAIengine:
    """bộ não AI chat engine kết hợp tìm kiếm pytorch và asyncio"""
    
    def __init__(self, config: agentconfig):
        self.config = config
        self.history: list[messageschema] = [
            messageschema(role="system", content= config.system_promt)
        ]
        self.vector_store = pytorchvectorstorage(dim=config.embedding_dim)
        
    @measure_async_latency
    async def ask_with_context(self, query:str):
        cleaned_query = query.strip()
        # dọn dẹp khoảng trắng đầu cuối
        if not cleaned_query: # nếu rỗng
            raise emptyqueryerror("câu hỏi của bạn không được để trống")
        
        # thêm câu hỏi vào lịch sử chat
        self.history.append(messageschema(
            role="user",
            content=cleaned_query
        ))
        
        # giả lập độ trễ i/o bất đồng bộ
        await asyncio.sleep(0.3)
        
        # tìm kiếm top 2 tài liệu khớp nhất từ pytorch
        matched_docs= self.vector_store.search_top_k(cleaned_query, k=2)
        return matched_docs
        
    async def stream_response(self, text: str) -> AsyncGenerator[str, None]:
        """sreaming câu trả lời bất đồng bộ từng chữ"""
        for word in text.split(" "):
            await asyncio.sleep(0.04)
            yield word + " "
            
    def save_session_to_json(self, file_path_str: str ="storage/session.json") -> None:
        """ lưu toàn bộ lịch sử hội thoại ra file json"""
        path= Path(file_path_str)
        path.parent.mkdir(parent=True, exist_ok=True)
        
        data = {
            "config": self.config.model_dump(),
            "history": [msg.model_dump(mode="json") for msg in self.history]
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logger.success(f"đã lưu phiên chat thành công tại: {path.resolve()}")
        