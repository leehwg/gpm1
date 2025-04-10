# sab.py
import pandas as pd
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

import os
import google.generativeai as genai
import requests
from dotenv import load_dotenv

from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY

# ============================================================== Đọc dữ liệu tài chính từ file Excel
info_df = pd.read_excel("info.xlsx", sheet_name="Phan_loai_nganh")
cdkt_df = pd.read_excel("BCTC.xlsx", sheet_name="CDKT")
kqkd_df = pd.read_excel("BCTC.xlsx", sheet_name="KQKD")
lctt_df = pd.read_excel("BCTC.xlsx", sheet_name="LCTT")
tm_df = pd.read_excel("BCTC.xlsx", sheet_name="TM")

# Lấy thông tin công ty
company_name = info_df["Tên công ty"].iloc[0]
company_symbol = info_df["Mã"].iloc[0]
company_exchange = info_df["Sàn"].iloc[0]
company_sector = info_df["Ngành ICB - cấp 2"].iloc[0]

# Đăng ký font TTF
font_path_regular = "DejaVuSans.ttf"  # Đường dẫn đến font TTF DejaVuSans (regular)
font_path_bold = "DejaVuSans-Bold.ttf"  # Đường dẫn đến font TTF DejaVuSans-Bold

pdfmetrics.registerFont(TTFont('DejaVuSans', font_path_regular))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path_bold))

# Khởi tạo PDF và đăng ký font hỗ trợ tiếng Việt
pdf_filename = "financial_report.pdf"
c = canvas.Canvas(pdf_filename, pagesize=A4)

fonts.addMapping('DejaVuSans', 0, 0, 'DejaVuSans.ttf')
fonts.addMapping('DejaVuSans-Bold', 0, 0, 'DejaVuSans-Bold.ttf')

# Đặt màu xanh #003366, đỏ #8B0000
blue_color = HexColor('#003366')
red_color = HexColor('#B22222')

# Cài đặt font DejaVuSans
c.setFont("DejaVuSans", 9)

width, height = A4

# Lề và khoảng cách căn chỉnh
margin_left = 50  # Lề trái
margin_right = 50
margin_top = 800
line_spacing = 13

usable_width = width - margin_left - margin_right
margin_bottom = 30

# ===============================================================================================================
# Tải API key từ file môi trường
load_dotenv("api_gemini.env")
api_key = os.getenv("GEMINI_API_KEY")

# Kiểm tra xem API key có tồn tại không
if not api_key:
    raise ValueError("API Key chưa được đặt. Vui lòng kiểm tra file .env")

# Cấu hình model Google Gemini
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="Chatbot này sẽ hoạt động như một broker chứng khoán chuyên nghiệp..."
)

# =========================================================================================================================

# ============================================================ TRANG 1 - TIÊU ĐỀ & PHÂN TÍCH KỸ THUẬT

# Tiêu đề chính (trên cùng)
c.setFont("DejaVuSans-Bold", 16)
c.setFillColor(red_color)
c.drawString(margin_left, margin_top, "BÁO CÁO TÀI CHÍNH SABECO")

# Ngày báo cáo căn phải
c.setFont("DejaVuSans", 9)
c.drawRightString(width - margin_left, margin_top, "Ngày 31/12/2024")

# Thông tin công ty
c.setFont("DejaVuSans", 9)
c.setFillColor(red_color)
start_y = margin_top - 30
info_labels = ["Tên công ty:", "Mã cổ phiếu:", "Sàn giao dịch:", "Ngành:"]
info_values = [company_name, company_symbol, company_exchange, company_sector]
for i, (label, value) in enumerate(zip(info_labels, info_values)):
    c.setFont("DejaVuSans-Bold", 9)
    c.drawString(margin_left, start_y - i * line_spacing, label)
    c.setFont("DejaVuSans", 9)
    c.drawString(margin_left + 100, start_y - i * line_spacing, value)

# Vẽ nét gạch đứt phân cách
dash_y = start_y - len(info_labels) * line_spacing - 5  # Căn vị trí ngay dưới thông tin công ty
c.setStrokeColor(colors.grey)
c.setLineWidth(0.5)
c.setDash(2, 2)  # Thiết lập nét gạch đứt: 2 chấm, 2 khoảng trắng
c.line(margin_left, dash_y, width - margin_left, dash_y)
c.setDash()  # Reset lại về nét liền sau khi vẽ xong

# ==========================================================================================================

# Tiêu đề "Phân Tích Kỹ Thuật" được đặt ngay dưới thông tin công ty (không trùng với tiêu đề chính)
tech_title_y = start_y - len(info_labels) * line_spacing - 30
c.setFillColor(blue_color)
c.setFont("DejaVuSans-Bold", 13)
c.drawString(margin_left, tech_title_y, "Phân tích kỹ thuật")

# Thêm gạch liền hơi đậm bên dưới tiêu đề
c.setStrokeColor(blue_color)
c.setLineWidth(3)  # Hơi đậm
line_y = tech_title_y - 8  # Khoảng cách dưới tiêu đề một chút
c.line(margin_left, line_y, width - margin_left, line_y)

# ******************************************************* Bố trí 3 biểu đồ chính theo dạng lưới 3×3
available_width = width - 2 * margin_left
cell_width = available_width / 3
cell_height = 50  # Chiều cao mỗi hàng

# Hình long_term_price (chiếm 1.5 cột, 3.3 hàng)
big_image_width = 1.5 * cell_width
big_image_height = 3.3 * cell_height

# Hình recent_price (chiếm 1.5 cột, 2 hàng) và volume_chart (chiếm 1.5 cột, 1 hàng)
right_image_width = 1.5 * cell_width
recent_price_height = 2 * cell_height
volume_chart_height = cell_height

chart_area_top = tech_title_y - 20  # Bắt đầu ngay dưới tiêu đề "Phân Tích Kỹ Thuật"

# --------- Hình long_term_price ---------
caption1 = "Giá cổ phiếu dài hạn"
c.setFont("DejaVuSans-Bold", 7)
c.drawString(margin_left, chart_area_top - 15, caption1)
c.drawImage("charts/long_term_price.png",
            margin_left,
            chart_area_top - big_image_height - 20,
            width=big_image_width,
            height=big_image_height)

# --------- Hình recent_price ---------
right_x = margin_left + big_image_width
caption2 = "Giá cổ phiếu 1 năm"
c.setFont("DejaVuSans-Bold", 7)
c.drawString(right_x, chart_area_top - 15, caption2)
c.drawImage("charts/recent_price.png",
            right_x,
            chart_area_top - recent_price_height - 20,
            width=right_image_width,
            height=recent_price_height)

# --------- Hình volume_chart ---------
caption3 = "KLGD 1 năm"
c.setFont("DejaVuSans-Bold", 7)
caption3_y = chart_area_top - recent_price_height - 25
c.drawString(right_x, caption3_y, caption3)
c.drawImage("charts/volume_chart.png",
            right_x,
            caption3_y - volume_chart_height - 5,
            width=right_image_width,
            height=volume_chart_height)

# ********************************************************** Chèn 4 biểu đồ bổ sung (2 hàng x 2 cột)
second_section_top = min(chart_area_top - big_image_height - 20, caption3_y - volume_chart_height - 5) - 30
col_gap = 20  # Khoảng cách giữa 2 cột
row_gap = 10  # Khoảng cách giữa 2 hàng
second_section_available_width = available_width
second_image_width = (second_section_available_width - col_gap) / 2
second_image_height = 120  # Chiều cao cố định cho hình bổ sung

# Hàng 1: bollinger.png và ma5_ma20.png
row1_y = second_section_top - second_image_height
c.drawImage("charts/bollinger.png",
            margin_left,
            row1_y,
            width=second_image_width,
            height=second_image_height)
c.drawImage("charts/ma5_ma20.png",
            margin_left + second_image_width + col_gap,
            row1_y,
            width=second_image_width,
            height=second_image_height)

# Hàng 2: macd.png và rsi.png
row2_y = row1_y - row_gap - second_image_height
c.drawImage("charts/macd.png",
            margin_left,
            row2_y,
            width=second_image_width,
            height=second_image_height)
c.drawImage("charts/rsi.png",
            margin_left + second_image_width + col_gap,
            row2_y,
            width=second_image_width,
            height=second_image_height)


# ============================================================ Nội dung nhận xét AI
# Nội dung nhận xét AI
# Tạo nhận xét từ AI dựa trên biểu đồ
def generate_ai_comment(chart_data_1, chart_data_2, chart_data_3):
    # Chuyển dữ liệu thành định dạng có thể đọc được (danh sách các tuple)
    data_string_1 = "\n".join([f"{date}: {price}" for date, price in chart_data_1])
    data_string_2 = "\n".join([f"{date}: {price}" for date, price in chart_data_2])
    data_string_3 = "\n".join([f"{date}: {volume}" for date, volume in chart_data_3])

    # Tạo yêu cầu cho AI để phân tích biểu đồ
    prompt = f""" 
        Bạn là một chuyên gia phân tích tài chính và có kiến thức sâu rộng về thị trường chứng khoán. 
        Hãy phân tích xu hướng giá cổ phiếu của một doanh nghiệp trong ngắn hạn (1 năm) và dài hạn (2019-2024). 
        Dữ liệu đã được cung cấp dưới dạng giá cổ phiếu và khối lượng giao dịch qua các năm từ 2019 đến 2024.
        Sử dụng văn phong nghiêm túc, chuyên nghiệp (không thêm vào những câu trả lời lại yêu cầu, ví dụ: Tuyệt vời! Dựa trên yêu cầu của bạn, tôi sẽ phân tích ...), dùng ngôi thứ ba để xưng hô (ví dụ: báo cáo này,...)
        Trình bày thẳng vào vấn đề, viết đoạn văn với nội dung giới hạn 150 từ.
        Bạn cần phân tích dữ liệu này và đưa ra nhận xét về các yếu tố sau:
        - Xu hướng giá cổ phiếu trong ngắn hạn (1 năm)
        + Xác định sự biến động của giá cổ phiếu trong khoảng thời gian gần nhất (1 năm). 
        + Phân tích các yếu tố có thể tác động đến xu hướng ngắn hạn, bao gồm các biến động bất thường, các sự kiện nổi bật (như báo cáo tài chính, thay đổi chiến lược kinh doanh, v.v.).
        + Đánh giá xu hướng tăng hay giảm giá trong ngắn hạn và mức độ ổn định của nó.

        - Xu hướng giá cổ phiếu trong dài hạn (2019-2024)
        + Phân tích xu hướng tổng thể của giá cổ phiếu từ năm 2019 đến 2024.
        + Xác định các đỉnh và đáy giá chính, và lý giải các yếu tố ảnh hưởng đến những thay đổi này (ví dụ: thay đổi trong môi trường kinh tế vĩ mô, sự thay đổi trong ngành công nghiệp, chiến lược dài hạn của công ty, v.v.).
        + Đánh giá tiềm năng phát triển trong dài hạn dựa trên các xu hướng lịch sử.

        - Khối lượng giao dịch
        + Phân tích sự thay đổi của khối lượng giao dịch trong khoảng thời gian trên.
        + Xem xét mối quan hệ giữa giá cổ phiếu và khối lượng giao dịch, chỉ ra các giai đoạn có sự thay đổi đáng chú ý trong cả hai yếu tố này.

        Dữ liệu cung cấp:
            Giá cổ phiếu dài hạn: {data_string_1}
            Giá cổ phiếu 1 năm: {data_string_2}
            Khối lượng giao dịch: {data_string_3}
        Hãy đảm bảo rằng các nhận xét của bạn dựa trên các chỉ số cụ thể và so sánh với các mốc thời gian quan trọng. 
        Ngoài ra, bạn cần chỉ rõ các yếu tố tiềm năng có thể ảnh hưởng đến giá cổ phiếu trong tương lai gần và xa. 
        Đầu ra của bạn sẽ là một phân tích rõ ràng, logic, ngắn gọn, có cơ sở với các số liệu cụ thể từ dữ liệu trên và đoạn văn viết luận (không xuống dòng) giới hạn 150 từ
    """
    # Gửi yêu cầu tới API Google Gemini (hoặc model khác)
    try:
        response = model.generate_content(prompt)
        if response and hasattr(response, 'text'):
            return response.text  # Trả về nhận xét AI
        else:
            return "Không có nhận xét từ AI."
    except Exception as e:
        print(f"Lỗi khi gọi API: {str(e)}")
        return "Có lỗi khi gọi API."


from draw_charts import filtered_trading_df, df_1y

# Cập nhật nhận xét cho từng biểu đồ
long_term_price_data = list(zip(filtered_trading_df["Date"], filtered_trading_df["Price"]))
recent_price_data = list(zip(df_1y["Date"], df_1y["Price"]))
volume_data = list(zip(df_1y["Date"], df_1y["Volume"]))

# Cập nhật phần nhận xét AI trong báo cáo PDF
ai_full_comment = generate_ai_comment(long_term_price_data, recent_price_data, volume_data)

# Define the style for justified text
style_justify = ParagraphStyle(
    name='Justify',
    fontName='DejaVuSans',
    fontSize=9,
    leading=line_spacing,  # Adjust this value for desired line spacing
    alignment=TA_JUSTIFY,
    spaceAfter=10,
    textColor=blue_color  # Replace this with your custom color if needed
)

# Create a frame to hold the paragraph
frame_top = row2_y - 10
frame_height = frame_top - margin_bottom
frame_width = usable_width

frame = Frame(
    margin_left,
    margin_bottom,
    frame_width,
    frame_height,
    showBoundary=0  # Đặt =1 để debug hiển thị khung
)

content = ai_full_comment.replace('\n', '<br />')
paragraph = Paragraph(content, style_justify)
frame.addFromList([paragraph], c)

c.showPage()

# =====================================================================================================

# ============================================================ TRANG 2 - PHÂN TÍCH BẢNG CÂN ĐỐI KẾ TOÁN
# Định nghĩa kích thước và vị trí
image_width = 250  # Độ rộng mỗi hình
image_height = 180  # Chiều cao mỗi hình

spacing = 15  # Khoảng cách giữa các hình (dành cho căn chỉnh theo chiều ngang)
margin_left = 50  # Lề trái
margin_right = 50
margin_top = 800  # Lề trên
usable_width = width - margin_left - margin_right
margin_bottom = 30

# Tiêu đề trang
c.setFont("DejaVuSans-Bold", 13)
c.setFillColor(blue_color)
c.drawString(margin_left, margin_top, "Phân tích Bảng cân đối kế toán")

# Thêm gạch liền bên dưới tiêu đề
c.setStrokeColor(blue_color)
c.setLineWidth(3)
line_y = margin_top - 8
c.line(margin_left, line_y, width - margin_left, line_y)

# ------------------ NHÓM 1: HÌNH STACKED ------------------
# Xác định vị trí của nhóm 1:
group1_top = margin_top - 5  # Khoảng cách từ đầu trang đến đầu nhóm 1
group1_title_y = group1_top - 40  # Tăng khoảng cách từ đầu nhóm 1 đến tiêu đề nhóm 1
image_y1 = group1_title_y - image_height - 10  # Điều chỉnh vị trí hình nhóm 1

# Vị trí theo chiều ngang cho 2 hình nhóm 1:
image_x1 = margin_left
image_x2 = margin_left + image_width + spacing

# Vẽ tiêu đề cho nhóm 1 (căn lề trái)
c.setFont("DejaVuSans-Bold", 7)
c.setFillColor(blue_color)
c.drawString(image_x1, group1_title_y, "Cấu trúc tài sản và Tổng tài sản")
c.drawString(image_x2, group1_title_y, "Cấu trúc nguồn vốn và Tổng nguồn vốn")

# Vẽ hình nhóm 1
c.drawImage("charts/structure_taisan_stacked_with_line.png",
            image_x1, image_y1, width=image_width, height=image_height)
c.drawImage("charts/structure_nguonvon_stacked_with_line.png",
            image_x2, image_y1, width=image_width, height=image_height)


# ------------------ NHÓM 2: HÌNH PERCENT ------------------
group2_top = image_y1 - 10
group2_title_y = group2_top - 20  # Tăng khoảng cách từ đầu nhóm 2 đến tiêu đề nhóm 2
image_y2 = group2_title_y - image_height - 10  # Điều chỉnh vị trí hình nhóm 2

# Vẽ tiêu đề cho nhóm 2 (căn lề trái)
c.setFont("DejaVuSans-Bold", 7)
c.setFillColor(blue_color)
c.drawString(image_x1, group2_title_y, "Tỷ trọng tài sản")
c.drawString(image_x2, group2_title_y, "Tỷ trọng nguồn vốn")

# Vẽ hình nhóm 2
c.drawImage("charts/structure_taisan_percent.png",
            image_x1, image_y2, width=image_width, height=image_height)
c.drawImage("charts/structure_nguonvon_percent.png",
            image_x2, image_y2, width=image_width, height=image_height)

#-------------------------------------------------------
# ------------------ BẢNG CÂN ĐỐI KẾ TOÁN ------------------
# Xử lý dữ liệu
selected_cols = [
    "CĐKT. VỐN CHỦ SỞ HỮU",
    "CĐKT. Tài sản cố định",
    "CĐKT. TỔNG CỘNG TÀI SẢN",
    "CĐKT. TÀI SẢN NGẮN HẠN",
    "CĐKT. Nợ ngắn hạn",
    "CĐKT. NỢ PHẢI TRẢ",
    "CĐKT. Vay và nợ thuê tài chính dài hạn"
]

# Sao chép dữ liệu và làm tròn số liệu
table_df = cdkt_df[selected_cols].copy().round(2)

# Nếu dữ liệu gốc chưa có cột "Năm", tạo cột này.
if "Năm" not in table_df.columns:
    table_df.reset_index(inplace=True)
    table_df.rename(columns={"index": "Năm"}, inplace=True)
    table_df["Năm"] = [2019, 2020, 2021, 2022, 2023]

# Chuyển vị bảng: đặt cột "Năm" làm index, sau đó transpose để các chỉ số tài chính trở thành dòng.
table_df_transposed = table_df.set_index("Năm").transpose()

# Đổi tên các chỉ số (tên dòng) theo yêu cầu
new_row_names = {
    "CĐKT. VỐN CHỦ SỞ HỮU": "Vốn chủ sở hữu",
    "CĐKT. Tài sản cố định": "Tài sản cố định",
    "CĐKT. TỔNG CỘNG TÀI SẢN": "Tổng cộng tài sản",
    "CĐKT. TÀI SẢN NGẮN HẠN": "Tài sản ngắn hạn",
    "CĐKT. Nợ ngắn hạn": "Nợ ngắn hạn",
    "CĐKT. NỢ PHẢI TRẢ": "Nợ phải trả",
    "CĐKT. Vay và nợ thuê tài chính dài hạn": "Vay và nợ thuê tài chính dài hạn"
}
table_df_transposed.rename(index=new_row_names, inplace=True)

# Đảm bảo các cột (năm) là kiểu số nguyên
table_df_transposed.columns = table_df_transposed.columns.astype(int)

# Tạo dữ liệu cho bảng:
# - Cột đầu tiên là tên chỉ số (index của table_df_transposed)
# - Sau đó là các cột năm.
header_row = [""] + list(table_df_transposed.columns)
table_data_transposed = [header_row]

for index_name, row in table_df_transposed.iterrows():
    table_data_transposed.append([index_name] + row.tolist())

# Xác định độ rộng bảng và cột
col_width_first = 150  # Độ rộng cột "Chỉ số" lớn hơn
col_width_years = (width - margin_left - col_width_first - 30) / len(table_df_transposed.columns)  # Độ rộng các cột năm nhỏ lại

# Tạo bảng với ReportLab
table_transposed = Table(table_data_transposed, colWidths=[col_width_first] + [col_width_years] * len(table_df_transposed.columns))
table_transposed.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), blue_color),  # Tiêu đề bảng
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Màu chữ tiêu đề là trắng
    ('TEXTCOLOR', (0, 1), (-1, -1), blue_color),  # Màu chữ các dòng khác là blue_color
    ('FONTNAME', (0, 0), (-1, -1), "DejaVuSans"),  # Font chữ
    ('FONTSIZE', (0, 0), (-1, -1), 9),  # Kích thước chữ
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Căn chỉnh nội dung bảng (giữa)
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),  # Cột chỉ số căn trái
    ('LINEBEFORE', (0, 0), (0, -1), 0.5, colors.white),  # Đường ngăn cách cột "Chỉ số"
    ('LINEAFTER', (0, 1), (0, -1), 0.5, colors.white),  # Đường ngăn cách cột "Chỉ số"
    ('GRID', (0, 1), (-1, -1), 0.5, colors.grey)  # Thêm đường phân cách giữa các cột
]))

table_top = image_y2 - 60  # Điều chỉnh khoảng cách từ hình đến bảng
table_transposed.wrapOn(c, width, height)
# Tính chiều cao bảng theo số hàng ước tính 12 đơn vị mỗi hàng
table_transposed.drawOn(c, margin_left, table_top - len(table_data_transposed) * 12)


#===================================================NHẬN XÉT AI
# Tạo nội dung prompt
table_transposed_str = table_df_transposed.to_string()

prompt_balance_sheet = f"""
    Cho các dữ liệu tính từ bảng cân đối kế toán của doanh nghiệp trong giai đoạn 2020–2024: {table_transposed_str} gồm:
    - Vốn chủ sở hữu
    - Tài sản cố định
    - Tổng cộng tài sản
    - Tài sản ngắn hạn
    - Nợ ngắn hạn
    - Nợ phải trả
    - Vay và nợ thuê tài chính dài hạn

    Tập trung vào việc nhận diện các xu hướng, sự thay đổi và mối quan hệ giữa các chỉ số này. 
    Cung cấp cái nhìn về sự thay đổi trong tình hình tài chính của công ty qua các năm, bao gồm các điểm mạnh, điểm yếu và các vấn đề cần lưu ý. 
    Đánh giá tổng thể sức khỏe tài chính của công ty dựa trên sự thay đổi của các chỉ số này.

    Sử dụng văn phong nghiêm túc, chuyên nghiệp (không thêm vào những câu trả lời lại yêu cầu, ví dụ: Tuyệt vời! Dựa trên yêu cầu của bạn, tôi sẽ phân tích ...) và nên dùng ngôi thứ ba để xưng hô (ví dụ: báo cáo này,...)
    Trình bày thẳng vào vấn đề, viết đoạn văn với nội dung giới hạn 100 từ.

    Lưu ý khi đưa ra nhận xét: sử dụng các số liệu cụ thể để làm cơ sở cho nhận định, và kết luận rõ ràng, không chung chung.
    Định dạng đầu ra mong muốn: 
        - Đoạn văn phân tích chi tiết mang tính học thuật tài chính, 
        - Đảm bảo rằng có các liên kết logic giữa các chỉ số tài chính, 
        - Giọng văn mượt mà, giống con người (chuyên gia phân tích), không cứng nhắc 
        - Đoạn văn viết luận (không xuống dòng) khoảng 100 từ.

    """

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    response = model.generate_content(prompt_balance_sheet)
    result = response.text
    balance_sheet_comment = result.replace("*", "")
except Exception as e:
    print(f"Lỗi khi gọi API: {str(e)}")

# --- Nội dung nhận xét từ AI ---
style_justify = ParagraphStyle(
    name='Justify',
    fontName='DejaVuSans',
    fontSize=9,
    leading=line_spacing,
    alignment=TA_JUSTIFY,
    spaceAfter=10,
    textColor=blue_color
)

# Xác định vị trí bắt đầu của phần nhận xét AI
frame_top = table_top - 110
frame_height = frame_top - margin_bottom  # Đảm bảo phần nhận xét có đủ không gian dưới cuối trang

# Khởi tạo frame để chứa văn bản
frame = Frame(
    margin_left,
    frame_top - frame_height,  # Đặt vị trí khung xuống gần dưới cùng trang
    usable_width,
    frame_height,  # Chiều cao của khung
    showBoundary=0  # Đặt =1 để debug hiển thị khung
)

# Chuyển đổi nội dung nhận xét thành <br /> cho các dòng mới
content = balance_sheet_comment.replace('\n', '<br />')

# Tạo một Paragraph với nội dung
paragraph = Paragraph(content, style_justify)

# Thêm đoạn văn vào frame
frame.addFromList([paragraph], c)

# Kết thúc trang
c.showPage()


# ===================================================================================================================

# ============================================================ TRANG 3 - PHÂN TÍCH HOẠT ĐỘNG KINH DOANH VÀ CHỈ SỐ TÀI CHÍNH
# Lề và khoảng cách căn chỉnh
margin_left = 50  # Lề trái
margin_right = 50
margin_top = 800
line_spacing = 13

usable_width = width - margin_left - margin_right
margin_bottom = 30


c.setFont("DejaVuSans-Bold", 13)
c.setFillColor(blue_color)
c.drawString(margin_left, margin_top, "Phân tích hoạt động kinh doanh và chỉ số tài chính")

# Thêm gạch liền bên dưới tiêu đề
c.setStrokeColor(blue_color)
c.setLineWidth(3)
line_y = margin_top - 8
c.line(margin_left, line_y, width - margin_left, line_y)

# Import bảng tính chỉ số từ calculated.py (đảm bảo biến df_transposed được export từ calculated.py)
from calculated import df_transposed

# Xử lý dữ liệu
df = df_transposed.copy().reset_index().rename(columns={"index": ""})
for col in df.columns:
    if col != "":
        df[col] = df[col].round(2)

# Định dạng style cho đoạn văn bản trong bảng
para_style = ParagraphStyle(name="TableText", fontName="DejaVuSans", fontSize=9, leading=11, textColor=blue_color)

# Chuyển DataFrame thành list-of-lists, sử dụng Paragraph cho mọi ô
table_data = [[Paragraph(str(cell), para_style) for cell in row] for row in df.itertuples(index=False, name=None)]

# Header row (in đậm + xanh)
header_style = ParagraphStyle(name="TableHeader", fontName="DejaVuSans-Bold", fontSize=9, leading=11,
                              textColor=blue_color)
header = [Paragraph(f"<b>{col}</b>", header_style) for col in df.columns]
table_data.insert(0, header)

# Xác định kích thước cột
num_cols = len(df.columns)
col_widths = [130] + [(A4[0] - 2 * margin_left - 130) / (num_cols - 1)] * (num_cols - 1)

# Tạo bảng
table = Table(table_data, colWidths=col_widths)

# Định dạng bảng
table.setStyle(TableStyle([
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
    ('TEXTCOLOR', (0, 0), (-1, -1), blue_color),  # Toàn bộ bảng chữ xanh

    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('WORDWRAP', (0, 0), (-1, -1), True),
    ('LINEBEFORE', (1, 0), (-1, -1), 0.25, colors.grey),
    ('LINEAFTER', (0, 0), (-2, -1), 0.25, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

    ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),  # Hàng đầu tiên in đậm
]))

# Chia bảng ra nếu bị tràn trang
table_width, table_height = table.wrap(0, 0)
x = (A4[0] - table_width) / 2
y = margin_top - 40 - table_height

if y < 50:  # Nếu bảng tràn ra ngoài trang
    parts = table.split(A4[0] - 2 * margin_left, A4[1] - 100)
    for i, part in enumerate(parts):
        if i > 0:
            c.showPage()  # Tạo trang mới
        part.wrapOn(c, A4[0] - 2 * margin_left, A4[1] - 100)
        part.drawOn(c, x, y)
else:
    table.drawOn(c, x, y)

# -------------Kết quả kinh doanh - Hiệu quả kinh doanh - Khả năng sinh lợi
# Đặt vị trí các hình ảnh
image_margin_top = y - 220  # Vị trí y để đặt các hình ảnh

# Căn chỉnh các hình ảnh (4 hình ảnh, chia thành 2 hàng)
image_width = 250  # Kích thước chiều rộng cho mỗi hình ảnh
image_height = 150  # Kích thước chiều cao cho mỗi hình ảnh

# Vị trí của hình ảnh đầu tiên, thứ hai, thứ ba và thứ tư
image1_x = margin_left
image2_x = image1_x + image_width + 30  # Khoảng cách giữa các hình ảnh
image3_x = margin_left  # Xác định vị trí cho hình ảnh thứ ba (dưới hàng đầu tiên)
image4_x = image3_x + image_width + 30  # Khoảng cách giữa hình ảnh thứ ba và thứ tư

# Cài đặt font, màu sắc cho tiêu đề
c.setFont("DejaVuSans-Bold", 7)
c.setFillColor(blue_color)

# Vị trí tiêu đề cho các biểu đồ
title1_x = margin_left
title1_y = image_margin_top + image_height + 10  # Khoảng cách giữa tiêu đề và hình ảnh (tăng khoảng cách thêm 10px)

title2_x = image1_x + image_width + 30  # Căn chỉnh theo vị trí hình ảnh thứ hai
title2_y = title1_y

# Vị trí tiêu đề cho các biểu đồ
title1_x = margin_left
title1_y = image_margin_top + image_height + 10  # Khoảng cách giữa tiêu đề và hình ảnh (tăng khoảng cách thêm 10px)

title2_x = image1_x + image_width + 30  # Căn chỉnh theo vị trí hình ảnh thứ hai
title2_y = title1_y

# Vị trí tiêu đề cho các biểu đồ tiếp theo (ngay bên trên hình ảnh 3 và 4)
title3_x = margin_left
title3_y = image_margin_top - 10  # Tiêu đề hình 3 nằm ngay bên trên hình ảnh thứ ba (giảm khoảng cách)

title4_x = image3_x + image_width + 30  # Đảm bảo khoảng cách với hình ảnh thứ ba
title4_y = title3_y

# Vẽ tiêu đề cho các biểu đồ
c.drawString(title1_x, title1_y, "Kết quả kinh doanh")
c.drawString(title2_x, title2_y, "Hiệu quả kinh doanh")
c.drawString(title3_x, title3_y, "Khả năng sinh lợi")
c.drawString(title4_x, title4_y, "Khả năng thanh khoản")

# Vẽ hình ảnh vào trang
c.drawImage("charts/page3_hieu_qua_kinh_doanh.png", image1_x, image_margin_top, width=image_width, height=image_height)
c.drawImage("charts/page3_kqkd.png", image2_x, image_margin_top, width=image_width, height=image_height)

# Điều chỉnh vị trí cho hình ảnh 3 và 4, để chúng nằm dưới hình ảnh 1 và 2
c.drawImage("charts/page3_profitability.png", image3_x, image_margin_top - image_height - 20, width=image_width,
            height=image_height)
c.drawImage("charts/page3_liquidity_indices.png", image4_x, image_margin_top - image_height - 20, width=image_width,
            height=image_height)

# Cập nhật vị trí y cho hình ảnh tiếp theo (sau khi vẽ hình ảnh trên)
image_margin_top -= image_height + 10  # Khoảng cách giữa các hàng hình ảnh

c.showPage()

# =============================================================================================================

# #===========================================Trang 4 - PHÂN TÍCH HOẠT ĐỘNG KINH DOANH VÀ CHỈ SỐ TÀI CHÍNH (tiếp)
# Lề và khoảng cách căn chỉnh
margin_left = 50  # Lề trái
margin_right = 50
margin_top = 800
line_spacing = 13

usable_width = width - margin_left - margin_right
margin_bottom = 30

# Kiểm tra nếu các biến dữ liệu chưa được khai báo
profitability_table = df_transposed

# Tạo nội dung prompt
from prompt import prompt_profitibility_table

prompt = prompt_profitibility_table

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    response = model.generate_content(prompt)
    result = response.text
    formatted_comment = result.replace("*", "")
    # print("API Response:", formatted_comment)  # Kiểm tra phản hồi từ API
except Exception as e:
    print(f"Lỗi khi gọi API: {str(e)}")

# --- Nội dung nhận xét từ AI ---
style_justify = ParagraphStyle(
    name='Justify',
    fontName='DejaVuSans',
    fontSize=9,
    leading=line_spacing,
    alignment=TA_JUSTIFY,
    spaceAfter=10,
    textColor=blue_color
)

# Khởi tạo frame để chứa văn bản
frame = Frame(margin_left, margin_bottom, usable_width, margin_top - margin_bottom, showBoundary=0)

# Chuyển đổi nội dung thành <br /> cho các dòng mới
content = formatted_comment.replace('\n', '<br />')

# Tạo một Paragraph với nội dung
paragraph = Paragraph(content, style_justify)

# Thêm đoạn văn vào frame
frame.addFromList([paragraph], c)

# Kết thúc trang và lưu PDF
c.showPage()
c.save()

print(f"✅ Báo cáo đã được lưu dưới dạng {pdf_filename}")
