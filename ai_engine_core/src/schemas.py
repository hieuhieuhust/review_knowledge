from datetime import datetime
from typing import Literal, List, Optional
from pydantic import BaseModel, Field

roletype = Literal["system", "user", "assistant"]

class messageschema(BaseModel):
    role: roletype # chỉ có 3 cái là system, user hoặc là assistant
    content: str = Field(min_length=1) # cái field có tác dụng để liệt kê thêm rule cho giá trị
    timestamp: datetime = Field(default_factory=datetime.now) # cái anyf đọc giờ
    
class agentconfig(BaseModel):
    agent_name: str = Field(default="enterprise assistant")
    model_name: str = Field(default="qwen-2.5-7b")
    temperature: float = Field(default=0.7, ge=0.0, le =2.0)
    system_prompt: str = Field(default="bạn là trợ lý AI chuyên nghiệp")
    embedding_dim: int = Field(default=768)
    # mấy cái field nó có tác dụng thêm cho biến 1 số rule
    
class searchresultschema(BaseModel):
    doc_id: int
    score: float
    summary: str
    
