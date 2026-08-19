import numpy as np

def mse_loss(p, t):
    p = np.array(p)
    t = np.array(t)
    a = p -t 
    loss = 0
    for i in range(len(a)):
        loss += a[i]**2
    return loss/len(a)

# vì như thế thì thì sai số ở mức khá nhỏ và làm việc biến thiên chậm dẫn đến là việc học chậm hơn và bởi vì |x| biến thiên không niên tục lên gradient khó khăn khi tính toán nên người ta có nghĩ đến việc phạt nặng hơn vào việc loss cao nên để bình phương và bình phương nó cũng dễ dàng tính gradient hơn , nhưng ko phải cứ loss quá cao thì tốt, mũ 4, mũ 6 thì sẽ làm cho gradient biến thiên quá lớn dẫn đến việc học khó hội tụ hơn

# dự đoán 1 email spam thì nó là classification vì nó là dùng mô hình machine learning để học các đặc điểm của những email spam để đưa ra phán quyết là ko hoặc có 
# dự đoán nhiệt độ ngay mai thì có thể là hồi quy vừa có thể là classification: 
    # hồi quy: có thể dựa vào nhiệt độ, độ ẩm, để phác thảo lại biên độ biến đổi của nhiệt độ theo các đặc điểm đó 
    # classification: đưa ra 1 số mốc nhiệt độ riêng với từng đặc điểm của nó, dựa theo đặc điểm của thời tiết để dự đoán khả năng nhiệt độ nằm trong khả năng nào
# dự đoán khách hàng có rời bỏ dịch vụ không  thì nó là classification: dựa theo dữ liệu trước đó về khác hàng, có thể là về giá cả, sở thích, đặc điểm về đánh giá để đưa vào mô hình phân tích, so sánh xem đánh giá của khách hàng gần đây là như thế nào rồi dựa vào các đặc điểm đó để đưa ra tỉ lệ bỏ hoặc không bỏ

