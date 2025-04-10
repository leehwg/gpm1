#calculated.py
import pandas as pd

# 1. Đọc dữ liệu từ các file CSV
cdkt = pd.read_excel("BCTC.xlsx", sheet_name="CDKT")  # Báo cáo Bảng cân đối kế toán
kqkd = pd.read_excel("BCTC.xlsx", sheet_name="KQKD")  # Báo cáo Kết quả kinh doanh
lctt = pd.read_excel("BCTC.xlsx", sheet_name="LCTT")  # Báo cáo Lưu chuyển tiền tệ


# 2. Định nghĩa các hàm tính chỉ số (sử dụng thuật ngữ tiếng Việt)

# Chỉ số lợi nhuận
def bien_loi_nhuan_rong(row):
    # = (Lợi nhuận sau thuế / Doanh thu thuần) * 100
    return row["KQKD. Lợi nhuận sau thuế thu nhập doanh nghiệp"] / row["KQKD. Doanh thu thuần"] * 100

def ebitda(row):
    # EBITDA = Lợi nhuận thuần từ hoạt động kinh doanh + Chi phí tài chính + Chi phí bán hàng + Chi phí quản lý doanh nghiệp
    ebitda = (row["KQKD. Lợi nhuận thuần từ hoạt động kinh doanh"] +
              row["KQKD. Chi phí tài chính"] +
              row["KQKD. Chi phí bán hàng"] +
              row["KQKD. Chi phí quản lý doanh nghiệp"])
    return ebitda

def bien_ebitda(row):
    # EBITDA = Lợi nhuận thuần từ hoạt động kinh doanh + Chi phí tài chính + Chi phí bán hàng + Chi phí quản lý doanh nghiệp
    ebitda = (row["KQKD. Lợi nhuận thuần từ hoạt động kinh doanh"] +
              row["KQKD. Chi phí tài chính"] +
              row["KQKD. Chi phí bán hàng"] +
              row["KQKD. Chi phí quản lý doanh nghiệp"])
    return ebitda / row["KQKD. Doanh thu thuần"] * 100


def bien_loi_nhuan_gop(row):
    # = (Lợi nhuận gộp về bán hàng và cung cấp dịch vụ / Doanh thu thuần) * 100
    return row["KQKD. Lợi nhuận gộp về bán hàng và cung cấp dịch vụ"] / row["KQKD. Doanh thu thuần"] * 100


def bien_loi_nhuan_hoat_dong(row):
    # = (Lợi nhuận thuần từ hoạt động kinh doanh / Doanh thu thuần) * 100
    return row["KQKD. Lợi nhuận thuần từ hoạt động kinh doanh"] / row["KQKD. Doanh thu thuần"] * 100


def bien_loi_nhuan_sau_thue(row):
    # = (Lợi nhuận sau thuế / Doanh thu thuần) * 100
    return row["KQKD. Lợi nhuận sau thuế thu nhập doanh nghiệp"] / row["KQKD. Doanh thu thuần"] * 100


def ROA(row):
    # = (Lợi nhuận sau thuế / TỔNG CỘNG TÀI SẢN) * 100
    return row["KQKD. Lợi nhuận sau thuế thu nhập doanh nghiệp"] / row["CĐKT. TỔNG CỘNG TÀI SẢN"] * 100


def ROE(row):
    # = (Lợi nhuận sau thuế / VỐN CHỦ SỞ HỮU) * 100
    return row["KQKD. Lợi nhuận sau thuế thu nhập doanh nghiệp"] / row["CĐKT. VỐN CHỦ SỞ HỮU"] * 100


# Chỉ số định giá (nếu có dữ liệu)
def ti_so_PE(row):
    # = Giá cổ phiếu / Lãi cơ bản trên cổ phiếu
    return row["Giá cổ phiếu"] / row["KQKD. Lãi cơ bản trên cổ phiếu"]


def ti_so_PB(row):
    # = Giá cổ phiếu / (VỐN CHỦ SỞ HỮU / Số cổ phiếu)
    gia_tri_tren_mot_cp = row["CĐKT. VỐN CHỦ SỞ HỮU"] / row["Số cổ phiếu"]
    return row["Giá cổ phiếu"] / gia_tri_tren_mot_cp


def ty_suat_co_tuc(row):
    # = (Cổ tức trên mỗi cổ phiếu / Giá cổ phiếu) * 100
    return row["Cổ tức trên mỗi cổ phiếu"] / row["Giá cổ phiếu"] * 100


def ti_le_chi_tra_co_tuc(row):
    # = (Cổ tức đã trả / Lợi nhuận sau thuế) * 100
    return row["LCTT. Cổ tức đã trả"] / row["KQKD. Lợi nhuận sau thuế thu nhập doanh nghiệp"] * 100


# Chỉ số thanh toán và vòng quay
def ty_so_hien_hanh(row):
    # Current Ratio = TÀI SẢN NGẮN HẠN / Nợ ngắn hạn
    return row["CĐKT. TÀI SẢN NGẮN HẠN"] / row["CĐKT. Nợ ngắn hạn"]


def ty_so_thanh_toan_nhanh(row):
    # Quick Ratio = (TÀI SẢN NGẮN HẠN - Hàng tồn kho, ròng) / Nợ ngắn hạn
    tai_san_nhanh = row["CĐKT. TÀI SẢN NGẮN HẠN"] - row["CĐKT. Hàng tồn kho, ròng"]
    return tai_san_nhanh / row["CĐKT. Nợ ngắn hạn"]


def he_so_thanh_toan_lai_vay(row):
    # Interest Coverage Ratio = (Lợi nhuận thuần từ hoạt động kinh doanh + Chi phí lãi vay) / Chi phí lãi vay
    return (row["KQKD. Lợi nhuận thuần từ hoạt động kinh doanh"] + row["KQKD. Trong đó: Chi phí lãi vay"]) / row[
        "KQKD. Trong đó: Chi phí lãi vay"]


def ty_so_tien_mat(row):
    # Cash Ratio = (Tiền và tương đương tiền) / Nợ ngắn hạn
    return row["CĐKT. Tiền và tương đương tiền"] / row["CĐKT. Nợ ngắn hạn"]


def vong_quay_hang_ton(row, inv_truoc):
    # Inventory Turnover = Doanh thu thuần / Trung bình Hàng tồn kho, ròng
    if pd.isna(inv_truoc):
        trung_binh = row["CĐKT. Hàng tồn kho, ròng"]
    else:
        trung_binh = (row["CĐKT. Hàng tồn kho, ròng"] + inv_truoc) / 2
    return row["KQKD. Doanh thu thuần"] / trung_binh


def he_so_vong_quay_khach_hang(row, receiv_truoc):
    # Receivables Turnover = Doanh thu thuần / Trung bình Các khoản phải thu ngắn hạn
    if pd.isna(receiv_truoc):
        trung_binh = row["CĐKT. Các khoản phải thu ngắn hạn"]
    else:
        trung_binh = (row["CĐKT. Các khoản phải thu ngắn hạn"] + receiv_truoc) / 2
    return row["KQKD. Doanh thu thuần"] / trung_binh


def so_ngay_thu(row, turnover_receiv):
    # Days Sales Outstanding = 365 / Receivables Turnover
    return 365 / turnover_receiv


def vong_quay_tong_tai_san(row, asset_truoc):
    # Total Asset Turnover = Doanh thu thuần / Trung bình TỔNG CỘNG TÀI SẢN
    if pd.isna(asset_truoc):
        trung_binh = row["CĐKT. TỔNG CỘNG TÀI SẢN"]
    else:
        trung_binh = (row["CĐKT. TỔNG CỘNG TÀI SẢN"] + asset_truoc) / 2
    return row["KQKD. Doanh thu thuần"] / trung_binh


def ti_so_no_tren_von(row):
    # Debt to Equity Ratio = NỢ PHẢI TRẢ / VỐN CHỦ SỞ HỮU
    return row["CĐKT. NỢ PHẢI TRẢ"] / row["CĐKT. VỐN CHỦ SỞ HỮU"]


def ti_so_no_tren_tai_san(row):
    # Debt to Asset Ratio = NỢ PHẢI TRẢ / TỔNG CỘNG TÀI SẢN
    return row["CĐKT. NỢ PHẢI TRẢ"] / row["CĐKT. TỔNG CỘNG TÀI SẢN"]


# 3. Hợp nhất dữ liệu theo "Năm"
df_temp = pd.merge(kqkd, cdkt, on="Năm", how="inner")
df = pd.merge(df_temp, lctt, on="Năm", how="inner")

# Đảm bảo cột "Năm" là kiểu số nguyên và sau đó chuyển sang chuỗi cho hiển thị
df["Năm"] = df["Năm"].astype(int).astype(str)

# 4. Tính các chỉ số cho từng năm
ket_qua = []
inv_truoc = None
receiv_truoc = None
asset_truoc = None

for idx, row in df.iterrows():
    nam = row["Năm"]
    cs = {"Năm": nam}

    # Chỉ số lợi nhuận
    cs["Biên LN ròng (%)"] = bien_loi_nhuan_rong(row)
    cs["Biên EBITDA (%)"] = bien_ebitda(row)
    cs["Biên LN gộp (%)"] = bien_loi_nhuan_gop(row)
    cs["Biên LN hoạt động (%)"] = bien_loi_nhuan_hoat_dong(row)
    cs["Biên LN sau thuế (%)"] = bien_loi_nhuan_sau_thue(row)
    cs["ROA (%)"] = ROA(row)
    cs["ROE (%)"] = ROE(row)

    # Chỉ số thanh toán & vòng quay
    cs["Tỷ số thanh toán hiện hành"] = ty_so_hien_hanh(row)
    cs["Tỷ số thanh toán nhanh"] = ty_so_thanh_toan_nhanh(row)
    cs["Hệ số thanh toán lãi vay"] = he_so_thanh_toan_lai_vay(row)
    cs["Tỷ số tiền mặt"] = ty_so_tien_mat(row)
    cs["Vòng quay hàng tồn kho"] = vong_quay_hang_ton(row, inv_truoc)

    turnover_receiv = he_so_vong_quay_khach_hang(row, receiv_truoc)
    cs["Hệ số vòng quay các khoản phải thu"] = turnover_receiv
    cs["Số ngày thu khoản phải thu"] = so_ngay_thu(row, turnover_receiv)
    cs["Vòng quay tổng tài sản"] = vong_quay_tong_tai_san(row, asset_truoc)

    cs["Tỷ số nợ trên vốn cổ phần"] = ti_so_no_tren_von(row)
    cs["Tỷ số nợ trên tài sản"] = ti_so_no_tren_tai_san(row)

    # Các chỉ số định giá (nếu dữ liệu có sẵn)
    if "Giá cổ phiếu" in row and "KQKD. Lãi cơ bản trên cổ phiếu" in row:
        cs["Tỷ số P/E"] = ti_so_PE(row)
        if "Số cổ phiếu" in row:
            cs["Tỷ số P/B"] = ti_so_PB(row)
    if "Cổ tức trên mỗi cổ phiếu" in row:
        cs["Tỷ suất cổ tức (%)"] = ty_suat_co_tuc(row)
    if "LCTT. Cổ tức đã trả" in row:
        cs["Tỷ lệ chi trả cổ tức (%)"] = ti_le_chi_tra_co_tuc(row)

    ket_qua.append(cs)

    # Cập nhật giá trị năm trước dùng cho tính trung bình
    inv_truoc = row["CĐKT. Hàng tồn kho, ròng"]
    receiv_truoc = row["CĐKT. Các khoản phải thu ngắn hạn"]
    asset_truoc = row["CĐKT. TỔNG CỘNG TÀI SẢN"]

df_kq = pd.DataFrame(ket_qua)

# 5. Chuyển đổi (transpose) kết quả: các chỉ tiêu nằm theo hàng, các năm nằm theo cột.
df_transposed = df_kq.set_index("Năm").T

# 7. Sắp xếp lại thứ tự cột nếu cần (ví dụ: đưa "Trung bình" về cuối)
cols = list(df_transposed.columns)
df_transposed = df_transposed[cols]

# 8. Hiển thị kết quả
print(df_transposed)

