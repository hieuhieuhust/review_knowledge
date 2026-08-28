from fastapi import APIRouter
from typing import List
from src.schemas import searchresultschema
from src.vector_store import pytorchvectorstorage

# khởi tạo apirouter riêng cho module search
router= APIRouter(prefix="/search", tags= ["Vector Search"])
vector_store= pytorchvectorstorage()

# đường dẫn lúc này sẽ tự động là /api/v1/search
@router.get("", response_model=list[searchresultschema])
async def search_vector(query:str, top_k: int =3):
    """endpoint tìm kiếm tài liệu tương đồng bằng pytorch"""
    return vector_store.search_top_k(query_text=query,k=top_k)