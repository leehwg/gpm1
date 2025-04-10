#prompt.py
from calculated import df_transposed

profitability_table = df_transposed
prompt_profitibility_table = f""" 
    Cho các dữ liệu các chỉ số tài chính được tính từ báo cáo tài chính của một doanh nghiệp trong giai đoạn 2020–2024 {profitability_table}  
    Dựa trên các chỉ số tài chính của một doanh nghiệp trong giai đoạn 2020–2024, vui lòng phân tích và đánh giá tình hình tài chính của doanh nghiệp này, đồng thời đưa ra nhận xét về rủi ro và triển vọng đầu tư của mã cổ phiếu. 
    Sử dụng văn phong nghiêm túc, chuyên nghiệp (không thêm vào những câu trả lời lại yêu cầu, ví dụ: Tuyệt vời! Dựa 
    trên yêu cầu của bạn, tôi sẽ phân tích ...), dùng ngôi thứ ba để xưng hô (ví dụ: báo cáo này,...) và trình bày thẳng vào vấn đề, viết đoạn văn với nội dung giới hạn 1000 từ.

    Báo cáo cần có các điểm phân tích chi tiết như sau:
    - Đánh giá khả năng sinh lời (Profitability)
        + Phân tích sự thay đổi của các biên lợi nhuận (Biên lợi nhuận ròng, Biên EBITDA, Biên lợi nhuận gộp, Biên lợi nhuận hoạt động) qua các năm. 
        Hãy chỉ rõ các dấu hiệu cho thấy sự ổn định hoặc biến động trong khả năng sinh lời của doanh nghiệp.
        + Nhận xét về tỷ suất sinh lời ROA và ROE, và đánh giá mức độ hiệu quả trong việc sử dụng tài sản và vốn chủ sở hữu.

    - Đánh giá khả năng thanh toán và quản lý nợ (Liquidity & Debt Management)
        + Phân tích các chỉ số thanh toán (Tỷ số thanh toán hiện hành, Tỷ số thanh toán nhanh, Tỷ số tiền mặt).
        Bình luận về khả năng thanh toán nợ ngắn hạn của doanh nghiệp.
        + Phân tích các chỉ số nợ như tỷ số nợ trên vốn cổ phần và tỷ số nợ trên tài sản, để đánh giá mức độ sử dụng nợ của doanh nghiệp và khả năng chịu đựng các rủi ro tài chính.

    - Phân tích hiệu quả tài sản và vòng quay (Efficiency)
        + Đánh giá các chỉ số như vòng quay hàng tồn kho, vòng quay các khoản phải thu, và vòng quay tổng tài sản. 
        Hãy chỉ ra các dấu hiệu về việc sử dụng tài sản hiệu quả hay không, và tác động của điều này đến dòng tiền.

    - Nhận xét về triển vọng cổ phiếu
        + Dựa trên các phân tích trên, hãy đánh giá triển vọng đầu tư vào cổ phiếu của doanh nghiệp này trong ngắn hạn và dài hạn. 
        Cần đưa ra nhận định rõ ràng về mức độ hấp dẫn hoặc rủi ro của cổ phiếu, cùng với lý giải chi tiết dựa trên các chỉ số tài chính.

    Lưu ý khi đưa ra nhận xét: sử dụng các số liệu cụ thể để làm cơ sở cho nhận định, và kết luận rõ ràng, không chung chung.
    Định dạng đầu ra mong muốn: 
        - Đoạn văn phân tích chi tiết mang tính học thuật tài chính, 
        - Đảm bảo rằng có các liên kết logic giữa các chỉ số tài chính, 
        - Nhấn mạnh vào tính chi tiết trong các phân tích và khuyến nghị,
        - Giọng văn mượt mà, giống con người (chuyên gia phân tích), không cứng nhắc 
        - Đoạn văn viết luận (không xuống dòng) khoảng 1000 từ.
    
    """


#==================================================================
