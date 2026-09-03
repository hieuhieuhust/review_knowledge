from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pathlib import Path

router= APIRouter(prefix="/documents", tags=["Document Ingestion"])

UPLOAD_DIR= Path("storage/uploaded_docs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# uploadfile/ file
@router.post("/upload", summary="tải file tài liệu lên cho AI")
async def upload_document(file: UploadFile= File(...)):
    """
    endpoint nhận file từ người dùng (pdf, txt,docx), lưu vào đĩa cứng để chuẩn bị chuyển thành vector embedding cho rag
    """
    # 1. kiểm tra lại đuôi file hợp lệ
    allowed_extensions = [".txt", ".pdf", ".docx", ".md"]
    file_ext= Path(file.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= f"định dạng file {file_ext} không được hỗ trợ! chỉ nhận {allowed_extensions}"
        )
        
    # 2. đọc nội dung và lưu file 
    save_path= UPLOAD_DIR / file.filename
    content = await file.read()
    
    with open(save_path, "wb") as f:
        f.write(content)
        
    return {
        "status": "success",
        "filename": file.filename,
        "size_bytes": len(content),
        "saved_location": str(save_path.resolve()),
        "message": "đã nạp tài liệu thành công, sẵn sàng đưa vào pytorch vector store!"
    }