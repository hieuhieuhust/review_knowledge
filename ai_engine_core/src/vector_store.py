import torch
import torch.nn.functional as F
from typing import List
from src.schemas import searchresultschema
from src.decorates import logger

class pytorchvectorstorage:
    """kho lưu trữ và tìm kiếm bằng pytorch batching"""
    
    def __init__(self, num_docs: int = 50, dim: int = 768):
        self.dim = dim
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # tạo sẵn ma trận 50 tài liệu mẫu: shape [50,768]
        torch.manual_seed(100)
        raw_tensors = torch.randn(num_docs, self.dim, device = self.device)
        self.doc_matrix = F.normalize(raw_tensors, p=2,dim=1)
        
        self.doc_texts = [f"tài liệu nghiệp vụ số #{i}: hướng dẫn quy trình vận hành và chính sách công ty" for i in range(num_docs)]
        logger.success(f"pytorch vectorstore sẵn sàng với {num_docs}")
        
    def search_top_k(self, query_text: str, k: int = 3) -> list[searchresultschema]:
        """tạo vector câu hỏi và nhân ma trận pytroch tìm top k"""
        seed = abs(hash(query_text)) % (10**6)
        torch.manual_seed(seed)
        q_vec = F.normalize(torch.randn(1, self.dim, device= self.device), p=2,dim=1)
        # squeeze(0): tại dim có idx 0 thì nếu size =1 thì nó xóa cái dim đó đi
        
        # nhân ma trận siêu tốc: [1,768] @ [768,50] -> [1,50]
        score = torch.matmul(q_vec, self.doc_matrix.T).squeeze(0)
        top_scores, top_indices = torch.topk(score, k=k)
        # .T là cái chuyển từ hàng sang cột
        
        results= []
    
        for score, idx in zip(top_scores.tolist(), top_indices.tolist()):
            # zip kiểu đóng gói thành theo vị trí idx sau lưu vào results với 3 thuộc  tính 
            results.append(searchresultschema(
                doc_id = idx,
                score=round(score,4),
                summary=self.doc_texts[idx]
            ))
        return results

            