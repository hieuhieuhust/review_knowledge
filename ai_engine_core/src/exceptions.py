class baseaiexceptions(Exception):
    """lớp lỗi cha của hệ thống"""
    pass

class emptyqueryerror(baseaiexceptions):
    """lỗi khi user gửi câu hỏi rỗng"""
    pass

class sesionnotfounderror(baseaiexceptions):
    """lỗi khi không tìm thấy phiên hội thoại"""
    pass

