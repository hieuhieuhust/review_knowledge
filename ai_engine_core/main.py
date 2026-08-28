import asyncio 
from src.schemas import agentconfig
from src.engine import asyncAIengine
from src.exceptions import emptyqueryerror
from src.decorates import logger 

async def run_demo():
    print("khỏi động async enterprise ai engine chặng 1")
    
    # 1. khởi tạo cấu hình và engine
    config = agentconfig(
        agent_name="VN=legal-Assistant",
        model_name= "qwen-1.5-14b",
        temperature=0.3,
        system_promt="bạn là trợ lý tư vấn hoạt động doanh nghiệp VN"
    )
    
    engine = asyncAIengine(config =config)
    
    # 2. câu hỏi người dùng
    user_query="quy định về thời hạn báo trước khi đơn phương chấm dứt hợp đồng lao động"
    
    try:
        # 3. tìm kiếm tài liệu liên quan
        docs = await engine.ask_with_context(user_query)
        print (f"user: {user_query}")
        print ("tài liệu khớp nhất từ pytorch vector store")
        for d in docs:
            print(f"[Doc #{d.doc_id} | điểm tương đồng: {d.score*100:.2f}%]: {d.summary}")
            
            print("AI phản hồi (streaming)")
            ai_reply_text = f"căn cứ vào {docs[0].summary}, người lao động cần báo trước ít nhất 30 ngày đối với hợp đồng xác định thời hạn"
            
            async for token in engine.stream_response(ai_reply_text):
                print(token, end="", flush =True)
            print("\n")
        # 5. lưu phiên chat ra json
        engine.save_session_to_json("storage/chat_history.json")
    except emptyqueryerror as e:
        logger.error(f"lỗi: {e}")
        
if __name__ == "__main__":
    asyncio.run(run_demo())