# draw_charts.py
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.colors import to_rgb, to_hex
import matplotlib.dates as mdates

from calculated import df_transposed



#==========================Đọc dữ liệu tài chính ===========================
info_df = pd.read_excel("info.xlsx", sheet_name="info")
trading_df = pd.read_excel("trading_data.xlsx")

cdkt_df = pd.read_excel("BCTC.xlsx", sheet_name="CDKT")  # Cân đối kế toán
kqkd_df = pd.read_excel("BCTC.xlsx", sheet_name="KQKD")  # Kết quả kinh doanh
lctt_df = pd.read_excel("BCTC.xlsx", sheet_name="LCTT")  # Lưu chuyển tiền tệ
tm_df = pd.read_excel("BCTC.xlsx", sheet_name="TM")  # Thuyết minh

#----------
# Chuyển đổi cột 'Date' thành dạng datetime
trading_df["Date"] = pd.to_datetime(trading_df["Date"])

# Chỉ lấy dữ liệu đến ngày 31/12/2024
end_date = pd.Timestamp("2024-12-31")
filtered_trading_df = trading_df[trading_df["Date"] <= end_date].copy()

# Lọc dữ liệu cho 1 năm gần nhất
df_1y = filtered_trading_df[(filtered_trading_df["Date"] >= end_date - pd.DateOffset(years=1)) & (filtered_trading_df["Date"] <= end_date)]
# Lọc dữ liệu cho 6 tháng gần nhất
start_6m = end_date - pd.DateOffset(months=6)
df_6m = filtered_trading_df[(filtered_trading_df["Date"] >= start_6m) & (filtered_trading_df["Date"] <= end_date)].copy()


# Tạo thư mục "charts" nếu chưa tồn tại
output_dir = "charts"
os.makedirs(output_dir, exist_ok=True)


#============================================Biểu đồ Trang 1 PHÂN TÍCH KỸ THUẬT=================================

#----------------------------------------------Giá cổ phiếu dài hạn


# Vẽ biểu đồ giá cổ phiếu dài hạn chỉ đến ngày 31/12/2024
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(filtered_trading_df["Date"], filtered_trading_df["Price"], color="grey", linestyle="-", linewidth=2)

# plt.title("Giá cổ phiếu dài hạn", fontsize=14, fontweight="bold", color="#003366", loc="left")

ax.set_xlabel("")
ax.set_ylabel("")
ax.grid(True, linestyle="--", alpha=0.5)

# Bỏ đường viền đen xung quanh biểu đồ
for spine in ax.spines.values():
    spine.set_visible(False)

# Chỉ hiển thị các mốc thời gian chính trên trục X
ax.set_xticks(filtered_trading_df["Date"][::max(1, len(filtered_trading_df) // 10)])
ax.set_xticklabels([d.strftime("%m/%Y") for d in filtered_trading_df["Date"][::max(1, len(filtered_trading_df) // 10)]], rotation=0)

# Lưu biểu đồ
plt.savefig("charts/long_term_price.png", dpi=300, bbox_inches="tight")
plt.close()


#**************************************************************************************
#----------------------------------------------Giá cổ phiếu 1 năm
fig, ax = plt.subplots(figsize=(8, 3))  # Kích thước hợp lý để sau này dễ căn chỉnh
ax.plot(df_1y["Date"], df_1y["Price"], color="grey", linestyle="-", linewidth=2)

# Tiêu đề căn trái, in đậm, xanh navy nhẹ
# plt.title("Giá cổ phiếu 1 năm", fontsize=13, fontweight="bold", color="#003366", loc="left")

# Tùy chỉnh trục
ax.set_xlabel("")
ax.set_ylabel("")
ax.grid(True, linestyle="--", alpha=0.5)

# Bỏ đường viền đen
for spine in ax.spines.values():
    spine.set_visible(False)

# Hiển thị mốc thời gian đầy đủ (dùng df_1y thay vì filtered_trading_df)
ax.set_xticks(df_1y["Date"][::max(1, len(df_1y) // 7)])
ax.set_xticklabels([d.strftime("%m/%Y") for d in df_1y["Date"][::max(1, len(df_1y) // 7)]], rotation=0)

# Lưu biểu đồ
plt.savefig("charts/recent_price.png", dpi=300, bbox_inches="tight")
plt.close()

#************************************************************************************
#--------------------------------------------Khối lượng giao dịch 1 năm
fig, ax = plt.subplots(figsize=(8, 2))  # Kích thước hợp lý để dễ căn chỉnh
ax.bar(df_1y["Date"], df_1y["Volume"], color="grey", alpha=0.7)  # Cột màu xám

# Tiêu đề căn trái, in đậm, xanh navy nhẹ
# plt.title("KLGD 1 năm", fontsize=13, fontweight="bold", color="#003366", loc="left")

# Tùy chỉnh trục
ax.set_xlabel("")
ax.set_ylabel("")
ax.grid(True, linestyle="--", alpha=0.5)

# Bỏ đường viền đen
for spine in ax.spines.values():
    spine.set_visible(False)

# Hiển thị mốc thời gian đầy đủ
ax.set_xticks(df_1y["Date"][::max(1, len(df_1y) // 7)])
ax.set_xticklabels([d.strftime("%m/%Y") for d in df_1y["Date"][::max(1, len(df_1y) // 7)]], rotation=0)
# Lưu biểu đồ
plt.savefig("charts/volume_chart.png", dpi=300, bbox_inches="tight")
plt.close()



#***********************************************************************************************
#----------------------------------------------------6 tháng Giá & Bollinger Band
# Tính toán Bollinger Bands
df_6m["MA20"] = df_6m["Price"].rolling(window=20).mean()
df_6m["Upper"] = df_6m["MA20"] + 2 * df_6m["Price"].rolling(window=20).std()
df_6m["Lower"] = df_6m["MA20"] - 2 * df_6m["Price"].rolling(window=20).std()

# Tạo biểu đồ
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df_6m["Date"], df_6m["Price"], label="Giá cổ phiếu", color="grey")
ax.plot(df_6m["Date"], df_6m["MA20"], label="MA20", color="#003366")
ax.fill_between(df_6m["Date"], df_6m["Upper"], df_6m["Lower"], color="lightblue", alpha=0.3)

# Định dạng trục X
ax.set_xlim([start_6m, end_date])  # Giới hạn đúng từ 01/07/2024 đến 31/12/2024
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Hiển thị mỗi tháng
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))  # Định dạng thành M/Y
plt.xticks(rotation=0)

# Tiêu đề và chú thích
plt.title("Giá & Bollinger Bands", fontsize=13, fontweight="bold", color="#003366", loc="left")
plt.legend()
plt.grid(False)

# Bỏ đường viền đen
for spine in ax.spines.values():
    spine.set_visible(False)

# Tạo thư mục nếu chưa có
os.makedirs("charts", exist_ok=True)

# Lưu hình ảnh
plt.savefig(os.path.join(output_dir, "bollinger.png"), dpi=300, bbox_inches="tight")
plt.close()

#*****************************************************************************************************
#--------------------------------------------------6 tháng Giá  & MA(5)& MA(20)
df_6m["MA5"] = df_6m["Price"].rolling(window=5).mean()
df_6m["MA20"] = df_6m["Price"].rolling(window=20).mean()

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df_6m["Date"], df_6m["Price"], label="Giá cổ phiếu", color="grey")
ax.plot(df_6m["Date"], df_6m["MA5"], label="MA5", color="red", linestyle="--")  # MA5 nét đứt
ax.plot(df_6m["Date"], df_6m["MA20"], label="MA20", color="#003366", linestyle="--")  # MA20 nét đứt

# Định dạng trục X
ax.set_xlim([start_6m, end_date])  # Giới hạn trục X từ 01/07/2024 đến 31/12/2024
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Hiển thị mỗi tháng
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))  # Định dạng thành M/Y
plt.xticks(rotation=0)

# Tiêu đề và chú thích
plt.title("Giá & MA(5) & MA(20)", fontsize=13, fontweight="bold", color="#003366", loc="left")
plt.legend()

# Bỏ lưới
ax.grid(False)

# Bỏ viền đen
for spine in ax.spines.values():
    spine.set_visible(False)

# Lưu hình ảnh
plt.savefig("charts/ma5_ma20.png", dpi=300, bbox_inches="tight")
plt.close()


#***************************************************************************
#---------6 tháng RSI
window_length = 14
delta = df_6m["Price"].diff()

gain = (delta.where(delta > 0, 0)).rolling(window=window_length).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=window_length).mean()

rs = gain / loss
df_6m["RSI"] = 100 - (100 / (1 + rs))

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(df_6m["Date"], df_6m["RSI"], label="RSI", color="#003366", linewidth=2)

# Vẽ ngưỡng quá mua (70) và quá bán (30) bằng nét đứt
ax.axhline(70, linestyle="--", color="red", linewidth=1)
ax.axhline(30, linestyle="--", color="green", linewidth=1)

# Định dạng trục X
ax.set_xlim([start_6m, end_date])  # Giới hạn trục X từ 01/07/2024 đến 31/12/2024
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Hiển thị mỗi tháng
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))  # Định dạng thành M/Y
plt.xticks(rotation=0)

plt.title("RSI (Relative Strength Index)", fontsize=13, fontweight="bold", color="#003366", loc="left")
plt.ylim(0, 100)
plt.legend()

# Bỏ lưới
ax.grid(False)

# Bỏ viền đen
for spine in ax.spines.values():
    spine.set_visible(False)

# Đảm bảo tạo thư mục 'charts' nếu chưa tồn tại
os.makedirs("charts", exist_ok=True)

# Lưu hình ảnh
plt.savefig("charts/rsi.png", dpi=300, bbox_inches="tight")
plt.close()

#***********************************************************************************************************
#--------6 tháng MACD
# Tính toán MACD
ema12 = df_6m["Price"].ewm(span=12, adjust=False).mean()
ema26 = df_6m["Price"].ewm(span=26, adjust=False).mean()
df_6m["MACD"] = ema12 - ema26
df_6m["Signal"] = df_6m["MACD"].ewm(span=9, adjust=False).mean()
df_6m["Histogram"] = df_6m["MACD"] - df_6m["Signal"]  # Histogram là hiệu MACD và Signal

# Tạo biểu đồ
fig, ax = plt.subplots(figsize=(10, 4))

# Vẽ Histogram (thanh màu)
ax.bar(df_6m["Date"], df_6m["Histogram"], color=np.where(df_6m["Histogram"] < 0, 'red', 'green'), alpha=0.7, label="Histogram")

# Vẽ đường MACD
ax.plot(df_6m["Date"], df_6m["MACD"], label="MACD", color="#003366", linewidth=2)

# Vẽ đường Signal (nét đứt)
ax.plot(df_6m["Date"], df_6m["Signal"], label="Signal", color="red", linewidth=2)

# Định dạng trục X
ax.set_xlim([start_6m, end_date])  # Giới hạn trục X từ 01/07/2024 đến 31/12/2024
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))  # Hiển thị mỗi tháng
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%Y"))  # Định dạng thành M/Y
plt.xticks(rotation=0)

# Cài đặt tiêu đề và các thông số khác
plt.title("MACD", fontsize=13, fontweight="bold", color="#003366", loc="left")
plt.legend()

# Lưới cho trục Y
ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

# Bỏ viền đen
for spine in ax.spines.values():
    spine.set_visible(False)

# Lưu ảnh
plt.savefig("charts/macd.png", dpi=300, bbox_inches="tight")
plt.close()


#==========================Biểu đồ Trang 2 PHÂN TÍCH BẢNG CÂN ĐỐI KẾ TOÁN=================================
#-------------------------------------------------------Cấu trúc tài sản và nguồn vốn

#--------------------------------------------------------------------1. Tỷ trọng Tài sản
# Chuyển đổi các cột giá trị thành float
cdkt_df["CĐKT. TÀI SẢN NGẮN HẠN"] = cdkt_df["CĐKT. TÀI SẢN NGẮN HẠN"].astype(float)
cdkt_df["CĐKT. TÀI SẢN DÀI HẠN"] = cdkt_df["CĐKT. TÀI SẢN DÀI HẠN"].astype(float)
cdkt_df["CĐKT. TỔNG CỘNG TÀI SẢN"] = cdkt_df["CĐKT. TỔNG CỘNG TÀI SẢN"].astype(float)

# Tính tỷ trọng %
cdkt_df["ShortPct"] = cdkt_df["CĐKT. TÀI SẢN NGẮN HẠN"] / cdkt_df["CĐKT. TỔNG CỘNG TÀI SẢN"] * 100
cdkt_df["LongPct_ts"] = cdkt_df["CĐKT. TÀI SẢN DÀI HẠN"] / cdkt_df["CĐKT. TỔNG CỘNG TÀI SẢN"] * 100

# Tạo DataFrame chứa năm và tỷ trọng, đặt "Năm" làm index
df_pct = cdkt_df[["Năm", "ShortPct", "LongPct_ts"]].copy()
df_pct.set_index("Năm", inplace=True)

# Lấy danh sách năm (chuyển sang dạng string để vẽ nhãn trục Y)
years = sorted(df_pct.index.astype(str).tolist())
# Reindex theo thứ tự tăng dần (sử dụng giá trị số)
df_pct = df_pct.reindex([int(y) for y in years])

# Vẽ biểu đồ horizontal 100% stacked
fig, ax = plt.subplots(figsize=(5, 3))
bar_height = 0.6
index = np.arange(len(years))

# Vẽ thanh tài sản ngắn hạn
ax.barh(index, df_pct["ShortPct"], bar_height, label="Tài sản ngắn hạn", color="#1F4E79")
# Vẽ thanh tài sản dài hạn, đặt bên phải của thanh ngắn hạn
ax.barh(index, df_pct["LongPct_ts"], bar_height, left=df_pct["ShortPct"], label="Tài sản dài hạn", color="#5B9BD5")

# Thiết lập trục Y là năm
ax.set_yticks(index)
ax.set_yticklabels(years, fontsize=7)
ax.set_ylabel("", fontsize=7)
# Trục X là tỷ trọng (%)
ax.set_xlabel("Tỷ trọng (%)", fontsize=7)

# plt.title("Tỷ trọng tài sản", fontsize=14, fontweight="bold", color="#003366", loc="left")
plt.legend(loc="lower right", fontsize=7)

# Thiết lập lưới theo trục X (mềm, nhu nhu)
ax.xaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

# Bỏ viền đen
for spine in ax.spines.values():
    spine.set_visible(False)

os.makedirs("charts", exist_ok=True)
plt.tight_layout()
plt.savefig("charts/structure_taisan_percent.png", dpi=300, bbox_inches="tight")
plt.close()

#-----------------------------------------------------Cấu trúc tài sản
# Hàm điều chỉnh sắc độ màu
def adjust_color_intensity(base_color, intensity):
    rgb = np.array(to_rgb(base_color))
    new_rgb = intensity * rgb + (1 - intensity) * np.array([1, 1, 1])
    return to_hex(new_rgb)

# Danh sách các cột tài sản cần vẽ
columns_asset = [
    "CĐKT. Tiền và tương đương tiền",
    "CĐKT. Đầu tư tài chính ngắn hạn",
    "CĐKT. Các khoản phải thu ngắn hạn",
    "CĐKT. Hàng tồn kho, ròng",
    "CĐKT. Tài sản ngắn hạn khác",
    "CĐKT. Phải thu dài hạn",
    "CĐKT. Tài sản cố định",
    "CĐKT. Giá trị ròng tài sản đầu tư",
    "CĐKT. Tài sản dở dang dài hạn",
    "CĐKT. Đầu tư dài hạn",
    "CĐKT. Tài sản dài hạn khác"
]

# Định nghĩa màu gốc
base_colors = {
    "CĐKT. Tiền và tương đương tiền": "#4c72b0",
    "CĐKT. Đầu tư tài chính ngắn hạn": "#dd8452",
    "CĐKT. Các khoản phải thu ngắn hạn": "#55a868",
    "CĐKT. Hàng tồn kho, ròng": "#c44e52",
    "CĐKT. Tài sản ngắn hạn khác": "#8172b3",
    "CĐKT. Phải thu dài hạn": "#ccb974",
    "CĐKT. Tài sản cố định": "#64b5cd",
    "CĐKT. Giá trị ròng tài sản đầu tư": "#8c8c8c",
    "CĐKT. Tài sản dở dang dài hạn": "#f39c12",
    "CĐKT. Đầu tư dài hạn": "#27ae60",
    "CĐKT. Tài sản dài hạn khác": "#2980b9"
}

# Lấy danh sách năm và dữ liệu
years = sorted(cdkt_df["Năm"].astype(str).unique())
df_asset = cdkt_df.set_index("Năm")[columns_asset + ["CĐKT. TỔNG CỘNG TÀI SẢN"]].T
df_asset.columns = df_asset.columns.astype(str)

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(7, 4))
index = np.arange(len(years))
bar_width = 0.4  # Thu nhỏ cột

bottom = np.zeros(len(years))

# Vẽ cột chồng
for asset in columns_asset:
    values = df_asset.loc[asset, years].values.astype(float)
    max_val = np.max(values) if np.max(values) != 0 else 1
    colors_asset = [adjust_color_intensity(base_colors[asset], val / max_val) for val in values]
    label_clean = asset.replace("CĐKT. ", "")
    ax.bar(index, values, bar_width, bottom=bottom, color=colors_asset, label=label_clean)
    bottom += values

# Xử lý giá trị tuyệt đối của Tổng tài sản (tránh dấu trừ)
total_assets = np.abs(df_asset.loc["CĐKT. TỔNG CỘNG TÀI SẢN", years].values.astype(float))

# Thêm trục y phụ và vẽ biểu đồ đường (Màu #003366)
ax2 = ax.twinx()
ax2.plot(index, total_assets, color="#003366", marker="o", linestyle="-", linewidth=2.5, markersize=6, label="Tổng tài sản")

# Thiết lập trục x
ax.set_xticks(index)
ax.set_xticklabels(years, rotation=0, fontsize=12)
ax.set_xlabel("", fontsize=12)

# Định dạng trục y
ax.set_ylabel("Giá trị (tỷ VND)", fontsize=12)
ax2.set_ylabel("Tổng tài sản (tỷ VND)", fontsize=12, color="#003366")

# Bỏ viền đen xung quanh biểu đồ
for spine in ax.spines.values():
    spine.set_visible(False)
for spine in ax2.spines.values():
    spine.set_visible(False)

# Tiêu đề và lưới
# plt.title("Cấu trúc tài sản và Tổng tài sản", fontsize=14, fontweight="bold", color="#003366", loc="left")
ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

# Đặt chú thích xuống dưới
legend = ax.legend(
    fontsize=9, loc="upper center", bbox_to_anchor=(0.5, -0.15),
    fancybox=True, shadow=False, ncol=3
)
ax2.legend(fontsize=10, loc="upper right", bbox_to_anchor=(1, 1))

# Tối ưu bố cục
plt.tight_layout()
plt.savefig("charts/structure_taisan_stacked_with_line.png", dpi=300, bbox_inches="tight")


#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------2. Nguồn vốn
# Chuyển đổi các cột giá trị thành float
cdkt_df["CĐKT. NỢ PHẢI TRẢ"] = cdkt_df["CĐKT. NỢ PHẢI TRẢ"].astype(float)
cdkt_df["CĐKT. VỐN CHỦ SỞ HỮU"] = cdkt_df["CĐKT. VỐN CHỦ SỞ HỮU"].astype(float)
cdkt_df["CĐKT. TỔNG CỘNG NGUỒN VỐN"] = cdkt_df["CĐKT. TỔNG CỘNG NGUỒN VỐN"].astype(float)

# Tính tỷ trọng %
cdkt_df["Nophaitra_Pct"] = cdkt_df["CĐKT. NỢ PHẢI TRẢ"] / cdkt_df["CĐKT. TỔNG CỘNG NGUỒN VỐN"] * 100
cdkt_df["VCSH_Pct"] = cdkt_df["CĐKT. VỐN CHỦ SỞ HỮU"] / cdkt_df["CĐKT. TỔNG CỘNG NGUỒN VỐN"] * 100

# Tạo DataFrame chứa Năm và tỷ trọng, đặt "Năm" làm index
df_pct_nv = cdkt_df[["Năm", "Nophaitra_Pct", "VCSH_Pct"]].copy()
df_pct_nv.set_index("Năm", inplace=True)

# Lấy danh sách năm (chuyển sang dạng string để vẽ nhãn trục Y)
years = sorted(df_pct_nv.index.astype(str).tolist())
# Reindex theo thứ tự tăng dần (sử dụng giá trị số)
df_pct_nv = df_pct_nv.reindex([int(y) for y in years])

# Vẽ biểu đồ horizontal 100% stacked
fig, ax = plt.subplots(figsize=(5, 3))
bar_height = 0.6
index = np.arange(len(years))

# Vẽ thanh "Nợ phải trả"
ax.barh(index, df_pct_nv["Nophaitra_Pct"], bar_height, label="Nợ phải trả", color="#D15B00")
# Vẽ thanh "Vốn chủ sở hữu", đặt bên phải của "Nợ phải trả"
ax.barh(index, df_pct_nv["VCSH_Pct"], bar_height, left=df_pct_nv["Nophaitra_Pct"], label="Vốn chủ sở hữu", color="#F7A700")

# Thiết lập trục Y là năm
ax.set_yticks(index)
ax.set_yticklabels(years, rotation=0, fontsize=7)
ax.set_ylabel("", fontsize=7)
# Trục X là tỷ trọng (%)
ax.set_xlabel("Tỷ trọng (%)", fontsize=7)

# plt.title("Tỷ trọng nguồn vốn", fontsize=14, fontweight="bold", color="#003366", loc="left")
plt.legend(loc="lower right", fontsize=7)

# Thiết lập lưới theo trục X
ax.xaxis.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

# Bỏ viền đen
for spine in ax.spines.values():
    spine.set_visible(False)

os.makedirs("charts", exist_ok=True)
plt.tight_layout()
plt.savefig("charts/structure_nguonvon_percent.png", dpi=300, bbox_inches="tight")
plt.close()

#---------------------------Cấu trúc nguồn vốn
# Danh sách các cột nguồn vốn cần vẽ
columns_nguonvon = [
    "CĐKT. Phải trả người bán ngắn hạn",
    "CĐKT. Người mua trả tiền trước ngắn hạn",
    "CĐKT. Doanh thu chưa thực hiện ngắn hạn",
    "CĐKT. Vay và nợ thuê tài chính ngắn hạn",
    "CĐKT. Phải trả nhà cung cấp dài hạn",
    "CĐKT. Người mua trả tiền trước dài hạn",
    "CĐKT. Doanh thu chưa thực hiện dài hạn",
    "CĐKT. Vay và nợ thuê tài chính dài hạn",
    "CĐKT. Vốn góp của chủ sở hữu",
    "CĐKT. Thặng dư vốn cổ phần",
    "CĐKT. Vốn khác",
    "CĐKT. LNST chưa phân phối lũy kế đến cuối kỳ trước",
    "CĐKT. LNST chưa phân phối kỳ này",
    "CĐKT. Lợi ích cổ đông không kiểm soát"
]

# Định nghĩa màu gốc cho từng chỉ số nguồn vốn
base_colors_nv = {
    "CĐKT. Phải trả người bán ngắn hạn": "#1f77b4",
    "CĐKT. Người mua trả tiền trước ngắn hạn": "#ff7f0e",
    "CĐKT. Doanh thu chưa thực hiện ngắn hạn": "#2ca02c",
    "CĐKT. Vay và nợ thuê tài chính ngắn hạn": "#d62728",
    "CĐKT. Phải trả nhà cung cấp dài hạn": "#9467bd",
    "CĐKT. Người mua trả tiền trước dài hạn": "#8c564b",
    "CĐKT. Doanh thu chưa thực hiện dài hạn": "#e377c2",
    "CĐKT. Vay và nợ thuê tài chính dài hạn": "#7f7f7f",
    "CĐKT. Vốn góp của chủ sở hữu": "#bcbd22",
    "CĐKT. Thặng dư vốn cổ phần": "#17becf",
    "CĐKT. Vốn khác": "#aec7e8",
    "CĐKT. LNST chưa phân phối lũy kế đến cuối kỳ trước": "#ffbb78",
    "CĐKT. LNST chưa phân phối kỳ này": "#98df8a",
    "CĐKT. Lợi ích cổ đông không kiểm soát": "#ff9896"
}

# Lấy danh sách năm và dữ liệu
years = sorted(cdkt_df["Năm"].astype(str).unique())
df_nguonvon = cdkt_df.set_index("Năm")[columns_nguonvon + ["CĐKT. TỔNG CỘNG NGUỒN VỐN"]].T
df_nguonvon.columns = df_nguonvon.columns.astype(str)

# Vẽ biểu đồ
fig, ax = plt.subplots(figsize=(10, 6))
index = np.arange(len(years))
bar_width = 0.4  # Thu nhỏ cột

bottom = np.zeros(len(years))

# Vẽ cột chồng
for nguonvon in columns_nguonvon:
    values = df_nguonvon.loc[nguonvon, years].values.astype(float)
    max_val = np.max(values) if np.max(values) != 0 else 1
    colors_nguonvon = [adjust_color_intensity(base_colors_nv[nguonvon], val / max_val) for val in values]
    label_clean = nguonvon.replace("CĐKT. ", "")
    ax.bar(index, values, bar_width, bottom=bottom, color=colors_nguonvon, label=label_clean)
    bottom += values

# Xử lý giá trị tuyệt đối của Tổng tài sản (tránh dấu trừ)
total_nguonvon = np.abs(df_nguonvon.loc["CĐKT. TỔNG CỘNG NGUỒN VỐN", years].values.astype(float))

# Thêm trục y phụ và vẽ biểu đồ đường (Màu #003366)
ax2 = ax.twinx()
ax2.plot(index, total_nguonvon, color="#003366", marker="o", linestyle="-", linewidth=2.5, markersize=6, label="Tổng nguồn vốn")

# Thiết lập trục x
ax.set_xticks(index)
ax.set_xticklabels(years, rotation=0, fontsize=12)
ax.set_xlabel("", fontsize=12)

# Định dạng trục y
ax.set_ylabel("Giá trị (tỷ VND)", fontsize=12)
ax2.set_ylabel("Tổng nguồn vốn (tỷ VND)", fontsize=12, color="#003366")

# Bỏ viền đen xung quanh biểu đồ
for spine in ax.spines.values():
    spine.set_visible(False)
for spine in ax2.spines.values():
    spine.set_visible(False)

# Tiêu đề và lưới
# plt.title("Cấu trúc nguồn vốn và Tổng nguồn vốn", fontsize=14, fontweight="bold", color="#003366", loc="left")
ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

# Đặt chú thích xuống dưới
legend = ax.legend(
    fontsize=9, loc="upper center", bbox_to_anchor=(0.5, -0.15),
    fancybox=True, shadow=False, ncol=3
)
ax2.legend(fontsize=10, loc="upper right", bbox_to_anchor=(1, 1))

# Tối ưu bố cục
plt.tight_layout()
plt.savefig("charts/structure_nguonvon_stacked_with_line.png", dpi=300, bbox_inches="tight")



#==========================Biểu đồ Trang 3 PHÂN TÍCH KẾT QUẢ HOẠT ĐỘNG KINH DOANH VÀ CHỈ SỐ TÀI CHÍNH =================================
#==================================================Kết quả kinh doanh
# Đảm bảo cột "Năm" là dạng chuỗi
kqkd_df["Năm"] = kqkd_df["Năm"].astype(str)
years = kqkd_df["Năm"]

# Lấy dữ liệu
doanh_thu = kqkd_df["KQKD. Doanh thu thuần"].astype(float)
ln_gop = kqkd_df["KQKD. Lợi nhuận gộp về bán hàng và cung cấp dịch vụ"].astype(float)
ln_hoat_dong = kqkd_df["KQKD. Lợi nhuận thuần từ hoạt động kinh doanh"].astype(float)
ln_sau_thue = kqkd_df["KQKD. Lợi nhuận sau thuế thu nhập doanh nghiệp"].astype(float)
net_profit_growth = ln_sau_thue.pct_change() * 100

# Tạo biểu đồ
x = np.arange(len(years))
width = 0.2

fig, ax1 = plt.subplots(figsize=(5, 3))

# Biểu đồ cột
ax1.bar(x - 2*width, doanh_thu, width, label="Doanh thu thuần", color="#1F4E79")
ax1.bar(x - width, ln_gop, width, label="LN gộp", color="#5B9BD5")
ax1.bar(x, ln_hoat_dong, width, label="LN kinh doanh", color="#25A18E")

ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylabel("Giá trị (tỷ VND)")

# Trục phụ (đường tăng trưởng LN ròng)
ax2 = ax1.twinx()
ax2.plot(x, net_profit_growth, color="#D15B00", marker="o", linestyle="-", linewidth=2, label="Tăng trưởng LN ròng (%)")
ax2.set_ylabel("Tăng trưởng (%)")

# Bỏ viền đen quanh biểu đồ (cả hai trục)
for ax in [ax1, ax2]:
    for spine in ax.spines.values():
        spine.set_visible(False)

# Lưới nhẹ
ax1.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)
ax1.grid(axis="x", visible=False)

# Gộp chú thích từ cả 2 trục và chỉnh font nhỏ lại
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left", fontsize=5)

plt.tight_layout()
plt.savefig("charts/page3_kqkd.png", dpi=300, bbox_inches="tight")

#============================================================Hiệu quả kinh doanh
# Chuẩn bị dữ liệu
kqkd_df["Năm"] = kqkd_df["Năm"].astype(str)
years = kqkd_df["Năm"]
x = np.arange(len(years))
width = 0.25

# Lấy dữ liệu từ kqkd_df
ln_gop = kqkd_df["KQKD. Lợi nhuận gộp về bán hàng và cung cấp dịch vụ"].astype(float)
ln_sau_thue = kqkd_df["KQKD. Lợi nhuận sau thuế thu nhập doanh nghiệp"].astype(float)

# Lấy dữ liệu từ df_transposed (đảm bảo cột index là "Năm" giống với kqkd_df)
bien_ln_gop = df_transposed.loc["Biên LN gộp (%)", years].astype(float)
bien_ln_rong = df_transposed.loc["Biên LN ròng (%)", years].astype(float)

# Tạo biểu đồ
fig, ax1 = plt.subplots(figsize=(5, 3))

# Biểu đồ cột: Lợi nhuận gộp và sau thuế
ax1.bar(x - width/2, ln_gop, width, label="LN gộp", color="#5B9BD5")
ax1.bar(x + width/2, ln_sau_thue, width, label="LN sau thuế", color="#25A18E")

ax1.set_xticks(x)
ax1.set_xticklabels(years)
ax1.set_ylabel("Giá trị (tỷ VND)")

# Trục phụ: Biên lợi nhuận gộp và ròng (%)
ax2 = ax1.twinx()
ax2.plot(x, bien_ln_gop, color="#D15B00", marker="o", linewidth=2, label="Biên LN gộp (%)")
ax2.plot(x, bien_ln_rong, color="#1F4E79", marker="s", linewidth=2, label="Biên LN ròng (%)")
ax2.set_ylabel("Biên lợi nhuận (%)")

# Bỏ viền biểu đồ
for ax in [ax1, ax2]:
    for spine in ax.spines.values():
        spine.set_visible(False)

# Lưới và định dạng
ax1.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)
ax1.grid(axis="x", visible=False)

# Gộp chú thích và thu nhỏ font
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=5)

plt.tight_layout()
plt.savefig("charts/page3_hieu_qua_kinh_doanh.png", dpi=300, bbox_inches="tight")


#====================================================Chỉ số thanh khoản
# Các chỉ số thanh khoản cần vẽ:
liquidity_indices = ["Tỷ số thanh toán hiện hành", "Tỷ số thanh toán nhanh", "Tỷ số tiền mặt"]

# Lấy danh sách các năm từ các cột của df_transposed
years = df_transposed.columns.tolist()

# Tạo biểu đồ
fig, ax = plt.subplots(figsize=(5, 3))

# Định nghĩa danh sách màu cho 3 chỉ số thanh khoản
colors = ["#1F4E79", "#25A18E", "#D15B00"]

# Vẽ từng chỉ số thanh khoản dưới dạng đường với màu đã chỉ định
for i, index_name in enumerate(liquidity_indices):
    values = df_transposed.loc[index_name, years].astype(float)
    ax.plot(years, values, marker="o", linewidth=2, label=index_name, color=colors[i])

# Thiết lập tiêu đề và nhãn trục
# ax.set_title("Chỉ số thanh khoản", fontsize=12, fontweight="bold")
ax.set_xlabel("", fontsize=7)
ax.set_ylabel("", fontsize=7)

for spine in ax.spines.values():
    spine.set_visible(False)

# Hiển thị lưới nhẹ
ax1.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)
ax1.grid(axis="x", visible=False)

# Thêm chú thích nhỏ gọn
ax.legend(fontsize=5, loc="best")

plt.tight_layout()
plt.savefig("charts/page3_liquidity_indices.png", dpi=300, bbox_inches="tight")
#-------------Khả năng thanh toán

#-------------Khả năng sinh lợi
years = df_transposed.columns.tolist()  # Lấy danh sách các năm
x = np.arange(len(years))
width = 0.25  # Chiều rộng của mỗi cột

# Lấy dữ liệu ROA (%) và ROE (%) từ df_transposed (chúng nằm ở index)
roa = df_transposed.loc["ROA (%)"].astype(float)
roe = df_transposed.loc["ROE (%)"].astype(float)

# Nếu "Đòn bẩy tài chính" chưa có trong index, tính và thêm nó từ cdkt_df
if "Đòn bẩy tài chính" not in df_transposed.index:
    financial_leverage_series = cdkt_df["CĐKT. TỔNG CỘNG TÀI SẢN"] / cdkt_df["CĐKT. VỐN CHỦ SỞ HỮU"]
    financial_leverage_series.index = cdkt_df["Năm"].astype(str)
    df_transposed.loc["Đòn bẩy tài chính"] = financial_leverage_series
financial_leverage = df_transposed.loc["Đòn bẩy tài chính"].astype(float)

# Tạo figure và trục chính
fig, ax1 = plt.subplots(figsize=(5, 3))

# Vẽ biểu đồ cột cho ROA và ROE
ax1.bar(x - width/2, roa, width, label="ROA (%)", color="#1F4E79")
ax1.bar(x + width/2, roe, width, label="ROE (%)", color="#25A18E")
ax1.set_xlabel("", fontsize=10)
ax1.set_ylabel("ROA, ROE (%)", fontsize=10)
ax1.set_xticks(x)
ax1.set_xticklabels(years)

# Tạo trục phụ để vẽ biểu đồ đường cho Đòn bẩy tài chính
ax2 = ax1.twinx()
ax2.plot(x, financial_leverage.reindex(years).values, marker="o", linestyle="-", linewidth=2, color="#D15B00", label="Đòn bẩy tài chính")
ax2.set_ylabel("Đòn bẩy tài chính", fontsize=10)

# Gộp chú thích từ cả 2 trục
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=5)

# Xóa đường viền (spines) của biểu đồ
for axis in [ax1, ax2]:
    for spine in axis.spines.values():
        spine.set_visible(False)

# Tùy chỉnh lưới (chỉ lưới theo trục y của ax1)
ax1.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)
ax1.grid(axis="x", visible=False)

plt.tight_layout()
plt.savefig("charts/page3_profitability.png", dpi=300, bbox_inches="tight")









#==========================Biểu đồ Trang 4 PHÂN TÍCH CÁC THÔNG SỐ TÀI CHÍNH=================================
#----------1. Phân tích khả năng thanh toán

#---------2. Phân tích tỷ số hiệu quả hoạt động

#---------3. Phân tích tỷ số đòn bẩy tài chính (

#---------4. Phân tích khả năng sinh lời

#--------5. Phân tích dòng tiền