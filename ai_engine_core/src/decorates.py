import time
from functools import wraps
from loguru import logger

# cấu hình lưu log ra file 
logger.add("logs/engine.log", rotation="1 MB", level="INFO", encoding="utf-8")
# logger để lưu những sự kiện, thông tin mình cần theo dõi


def measure_async_latency(func):
    """decorator đo thời gian  chạy của hàm bất đồng bộ async def"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        logger.info(f"bắt đầu thực thi: [{func.__name__}]")
        
        result = await func(*args, **kwargs)
        
        duration = time.perf_counter() - start
        logger.info(f"hoàn  thành [{func.__name__}] trong {duration:.4f} giây")
        return result
    return wrapper