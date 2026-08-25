from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ValidationError

# --- PHẦN 1: ĐỊNH NGHĨA SCHEMAS BẰNG PYDANTIC ---

# 1. Định nghĩa kiểu Role hợp lệ
RoleType = Literal["system", "user", "assistant", "tool"]

class MessageSchema(BaseModel):
    """Schema Pydantic đại diện cho một tin nhắn chuẩn."""
    role: RoleType = Field(description="Vai trò: system, user, assistant hoặc tool")
    content: str = Field(min_length=1, description="Nội dung tin nhắn, không được để trống")
    timestamp: datetime = Field(default_factory=datetime.now, description="Thời gian tạo tin nhắn")

    def count_words(self) -> int:
        """Đếm số lượng từ trong tin nhắn."""
        return len(self.content.split())

class AgentConfig(BaseModel):
    """Schema cấu hình cho một AI Agent."""
    name: str = Field(min_length=2, max_length=50, description="Tên của Agent")
    model_name: str = Field(default="gpt-4o-mini", description="Mô hình LLM sử dụng")
    temperature: float = Field(
        default=0.7, 
        ge=0.0, 
        le=2.0, 
        description="Độ sáng tạo của LLM, chỉ từ 0.0 đến 2.0"
    )
    system_prompt: str = Field(
        default="Bạn là trợ lý AI chuyên nghiệp.", 
        description="Chỉ thị hệ thống cho Agent"
    )


# --- PHẦN 2: LẬP TRÌNH HƯỚNG ĐỐI TƯỢNG (OOP) ---

class AIAgent:
    """Lớp quản lý logic hoạt động của AI Agent."""
    
    def __init__(self, config: AgentConfig):
        self.config: AgentConfig = config
        self.history: List[MessageSchema] = []
        
        # Khởi tạo tin nhắn System đầu tiên từ config
        self._init_system_message()

    def _init_system_message(self) -> None:
        """Phương thức nội bộ để nạp system prompt vào lịch sử."""
        system_msg = MessageSchema(role="system", content=self.config.system_prompt)
        self.history.append(system_msg)

    def add_message(self, role: RoleType, content: str) -> MessageSchema:
        """Tạo và thêm tin nhắn mới vào lịch sử sau khi đã validate qua Pydantic."""
        msg = MessageSchema(role=role, content=content)
        self.history.append(msg)
        return msg

    def chat(self, user_input: str) -> str:
        """Mô phỏng hàm chat với người dùng."""
        # 1. Lưu tin nhắn của User
        self.add_message(role="user", content=user_input)
        
        # 2. Giả lập câu trả lời từ AI (ở Chặng 3 ta sẽ nối API thật vào đây)
        bot_reply = f"[{self.config.name} - Model {self.config.model_name}] Đã tiếp nhận yêu cầu: '{user_input}'"
        
        # 3. Lưu câu trả lời của AI vào lịch sử
        self.add_message(role="assistant", content=bot_reply)
        return bot_reply

    def get_history_as_dict(self) -> List[dict]:
        """Xuất toàn bộ lịch sử thành danh sách Dict chuẩn JSON."""
        # model_dump() là hàm của Pydantic để biến object thành dict
        return [msg.model_dump(mode="json") for msg in self.history]