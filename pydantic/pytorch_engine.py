import time
from pathlib import Path
from typing import List, Dict, Any, Generator
from functools import wraps

import torch
import torch.nn.functional as F
from pydantic import BaseModel, Field
from loguru import logger

# 1. cấu hình logging
# lưu lại lịch sử hoạt động vào file để sau xem lại chương trình chạy như nào
# lưu log vào file , khi log đạt 500kb thì lưu vào file mới, chỉ ghi log > info
logger.add("logs/pytorch_app.log", rotation="500 KB", level ="INFO")

# 2. decorator đo thời gian ra đời và thông tin thiết bị 
def benchmarch_pytorch(func):
    """vừa đo thời gian, vừa ghi lại thiết bị phần cứng đang xử lý"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        
        # kiểm tra thiết bị là gpu hay cpu
        device_name = "NVIDIA GPU (CUDA)"  if torch.cuda.is_available() else "CPU"
        logger.info(f"bắt đầu hàm {func.__name__} trên thiết bị: {device_name}")
        
        result = func(*args, **kwargs)
        
        elapsed = time.perf_counter() - start_time
        logger.info(f"hàm {func.__name__} hoàn thành trong {elapsed:.6f} giây")
        
        return result
    return wrapper

# 3. pydantic model kiểm soát vecto tài liệu
class DocumentChunk(BaseModel):
    """Schema đại diện cho một đoạn văn bản kèm Vector Embedding"""
    doc_id: str = Field(description = "Mã định danh tài liệu")
    text: str = Field(min_length =1, description = "nội dung văn bản")
    # vecto nhúng thường có 768 chiều ( chuẩn của mô hình BERT / BGE tiếng việt)
    vector_dim: int =Field(default=768, description="số chiều của vector")
    
# 4. class quản lý tìm kiếm bằng pytorch (oop + pytorch)
class pytorchvectormatcher:
    """lớp xử lý tính toán độ tương đồng ngữ nghĩa bằng pytorch"""
    
    def __init__(self, embedding_dim: int = 768):
        self.dim = embedding_dim
        # chọn thiết bị tối ưu nhất 
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        logger.success(f"khỏi tạo pytorch engine thành công trên: {self.device}")
        
    def create_fake_embedding(self, seed_number: int) -> torch.tensor:
        """
        tạo vector ngẫu nhiên giả lập (đại diện cho văn bản sau khi qua model AI)
         
        vector được chuẩn hóa (L2 Normalize) về độ dài = 1 theo chuẩn RAG.
        """
        torch.manual_seed(seed_number) # cố định số ngẫu nhiên để test
        
        # tạo vecto/tensor số thực 1 hàng (high) và 768 cột(widgth)
        raw_vector = torch.randn(1, self.dim, dtype =torch.float32, device=self.device)
        
        # chuẩn hóa vector bằng pytorch F.normalize
        normalize_vector = F.normalize(raw_vector, p=2, dim =1)
        return normalize_vector
    
    @benchmarch_pytorch
    def compute_similarity(self, query_vec: torch.Tensor, doc_vec: torch.Tensor) -> float:
        """
        tính độ tương đồng cosine giữa câu hỏi và tài liệu pytorch
        điểm số từ -1.0 đến 1.0(cầng gần 1.0 nghĩa là càng khớp)
        """
        
        # pytorch cosine similarity
        score = F.cosine_similarity(query_vec, doc_vec)
        return score.item() # chuyển từ pytorch tensor về số float python thông thường
    
    def stream_matched_result(self, text: str, score:float) -> Generator[str, None, None]:
        """Generator streaming kết quả tìm kiếm điểm số tương đồng"""
        
        header = f"[Độ tương đồng: {score * 100:.2f}%]"
        for char in header:
            time.sleep(0.02)
            yield char
        
        for word in text.split(" "):
            time.sleep(0.05)
            yield word + " "