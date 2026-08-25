import asyncio
import time
from typing import List, AsyncGenerator
import torch
import torch.nn.functional as F
from pydantic import BaseModel, Field
from loguru import logger

# 1. pydantic schemas
class searchrequest(BaseModel):
    user_id: str
    query_text: str
    top_k: int = Field(default=2, ge=1, le=10)
    # ge >= 1 và le <= (greater, less than or equal)
    
class searchresult(BaseModel):
    user_id: str
    doc_index: int
    similarity_score: float
    
# 2. async pytorch vector engine
class asynpytorchengine:
    """hệ thống tìm kiếm vector bất đồng bộ tối ưu hóa bằng pytorch"""
    
    def __init__(self, num_docs: int = 100, dim: int=768):
        self.dim = dim
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # tạo sẵn một "kho dữ liệu" gồm num_docs tài liệu dưới dạng ma trận batch tensor 2 chiều [num_docs, dim]
        torch.manual_seed(42)
        raw_docs = torch.randn(num_docs, self.dim, device=self.device)
        
        # chuẩn hóa ma trận theo chiều ngang (dim =1)
        self.doc_matrix: torch.Tensor = F.normalize(raw_docs, p=2, dim=1)
        
        logger.success(f"khởi tạo kho dữ liệu pytorch: {num_docs} docs, {dim} chiều trên [{self.device}]")
        
    def _get_query_vector(self, query_text: str) -> torch.Tensor:
        """tạo vector giả lập cho câu hỏi của user (shape: [1,768])"""
        # dùng hash của chuỗi làm seed để cùng câu hỏi ra cùng vector
        seed = abs(hash(query_text)) % (10**6)
        torch.manual_seed(seed)
        q_vec = torch.randn(1, self.dim, device=self.device)
        return F.normalize(q_vec, p=2, dim=1)
    
    async def search_single_query(self, req: searchrequest) -> List[searchresult]:
        """
        xử lý mô hình bất đồng bộ
        Mô phỏng gọi API LLM/Embedding mất 0.5s nhưng không làm nghẽn CPU
        """
        logger.info(f"[User {req.user_id}] bắt đầu xử lý câu hỏi: '{req.query_text}'")
        await asyncio.sleep(0.5)
        
        # 1. lấy vector câu hỏi
        q_vec = self._get_query_vector(req.query_text)
        
        # 2. pytorch batch multiplication
        # nhân ma trận [1,768] với ma trận chuyển vị [768, num_docs] -> ra mảng điểm [1, num_docs]
        scores = torch.matmul(q_vec, self.doc_matrix.T).squeeze(0)
        # squeeze(n) thì nó là xóa dim size có kích thước = 1 ở vị trí có index n, ko thêm n thì nó xóa hết mọi vị trí dim size = 1
        # unsqueeze(n) thì nó là thêm dim có size =1 vào vị trí n 
        
        # 3. lấy top-k tài liệu có điểm cao nhất bằng torch.topk
        top_score, top_indices = torch.topk(scores, k = req.top_k)
        
        results = []
        for score, idx in zip(top_score.tolist(), top_indices.tolist()):
            results.append(searchresult(
                user_id=req.user_id,
                doc_index=idx,
                similarity_score=round(score,4)
            ))
            
        logger.success(f"[user {req.user_id}] hoàn thành tìm kiếm")
        return results
    
    async def stream_token(self, text: str) -> AsyncGenerator[str, None]:
        """async generator: bắn token bất đồng bộ về phía clients"""
        for word in text.split(" "):
            await asyncio.sleep(0.05)
            yield word + " "
    
    