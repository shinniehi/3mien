import pandas as pd
from datetime import datetime
from dateutil import parser

# ====== FORMAT KQ XSMB ĐẸP (ĐB luôn đủ 5 số) ======

def format_xsmb_ketqua(r, ngay_str):
    db = str(r['DB']).strip().zfill(5)
    text = f"🎉 *KQ XSMB {ngay_str}* 🎉\n\n"
    text += f"*Đặc biệt*:   `{db}`\n"
    text += f"*Giải 1*:  `{str(r['G1']).strip()}`\n"
    for label, col in [
        ("*G. 2*", "G2"),
        ("*G. 3*", "G3"),
        ("*G. 4*", "G4"),
        ("*G. 5*", "G5"),
        ("*G. 6*", "G6"),
        ("*G. 7*", "G7"),
    ]:
        nums = str(r[col]).replace(",", " ").split()
        if len(nums) <= 4:
            text += f"{label}:  " + "  ".join(f"`{n.strip()}`" for n in nums) + "\n"
        else:
            n_half = (len(nums) + 1) // 2
            text += f"{label}:\n"
            text += "  ".join(f"`{n.strip()}`" for n in nums[:n_half]) + "\n"
            text += "  ".join(f"`{n.strip()}`" for n in nums[n_half:]) + "\n"
    return text

# ====== TRA KẾT QUẢ XSMB (CHUẨN HÓA XỬ LÝ NGÀY, KHÔNG LỖI UNPACK) ======

def tra_ketqua_theo_ngay(ngay_str):
    try:
        df = pd.read_csv('xsmb.csv')

        # Nhận diện định dạng ngày - chỉ parse, không ép dayfirst nếu là dạng ISO
        date_examples = df['date'].astype(str).head(3).tolist()
        if all('-' in d and len(d.split('-')[0]) == 4 for d in date_examples):
            # ISO format: 2025-07-23
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        else:
            # Việt format: 23-07-2025
            df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

        df['DB'] = df['DB'].astype(str).str.zfill(5)
        day_now = datetime.now()
        try:
            parsed = parser.parse(ngay_str, dayfirst=True, yearfirst=False, default=day_now)
        except Exception:
            return "❗ Định dạng ngày không hợp lệ! Hãy nhập ngày dạng 23-07 hoặc 2025-07-23."
        ngay_input = parsed.replace(hour=0, minute=0, second=0, microsecond=0).date()

        df['date_only'] = df['date'].dt.date
        row = df[df['date_only'] == ngay_input]
        if row.empty:
            return f"⛔ Không có kết quả cho ngày {ngay_input.strftime('%d-%m-%Y')}."
        r = row.iloc[0]
        ngay_str = ngay_input.strftime('%d-%m-%Y')
        return format_xsmb_ketqua(r, ngay_str)
    except Exception as e:
        return f"❗ Lỗi tra cứu: {e}"

async def tra_ketqua_moi_nhat():
    try:
        df = pd.read_csv('xsmb.csv')
        # Tự động nhận diện định dạng ngày
        date_examples = df['date'].astype(str).head(3).tolist()
        if all('-' in d and len(d.split('-')[0]) == 4 for d in date_examples):
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
        else:
            df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
        df['DB'] = df['DB'].astype(str).str.zfill(5)
        row = df.sort_values('date', ascending=False).iloc[0]
        ngay_str = row['date'].strftime('%d-%m-%Y')
        return format_xsmb_ketqua(row, ngay_str)
    except Exception as e:
        return f"❗ Lỗi tra cứu: {e}"
