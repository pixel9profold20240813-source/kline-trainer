# pip install yfinance pandas requests
import yfinance as yf, pandas as pd, requests, json, os, time
from datetime import date

OUT = 'data'; os.makedirs(OUT, exist_ok=True)
start = date.today().replace(year=date.today().year - 15).isoformat()

# 上市公司清單（證交所 OpenAPI，JSON，比舊的 ISIN 網頁穩定）
print('取得上市股票清單...', flush=True)
res = requests.get('https://openapi.twse.com.tw/v1/opendata/t187ap03_L', timeout=30, headers={'User-Agent': 'Mozilla/5.0'})
res.raise_for_status()
stocks = {x['公司代號'].strip(): x['公司簡稱'].strip() for x in res.json()
          if len(x['公司代號'].strip()) == 4 and x['公司代號'].strip().isdigit()}
print('上市股票', len(stocks), '檔，開始下載（可隨時 Ctrl+C，重跑會接續）', flush=True)

codes = []
for k, (code, name) in enumerate(stocks.items(), 1):
    path = f'{OUT}/{code}.json'
    if not os.path.exists(path):
        try:
            df = yf.download(f'{code}.TW', start=start, auto_adjust=False, progress=False, threads=False, timeout=20)
            if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
            df = df.dropna(subset=['Open', 'High', 'Low', 'Close'])
            df = df[df['Volume'] > 0]
            if len(df) >= 450:
                rows = [[d.strftime('%Y-%m-%d'), round(float(r.Open), 2), round(float(r.High), 2),
                         round(float(r.Low), 2), round(float(r.Close), 2), int(r.Volume // 1000)]
                        for d, r in df.iterrows()]
                json.dump({'n': name, 'r': rows}, open(path, 'w', encoding='utf-8'), separators=(',', ':'), ensure_ascii=False)
                print(k, '/', len(stocks), code, name, len(rows), '筆', flush=True)
            else:
                print(k, '/', len(stocks), code, '資料不足，略過', flush=True)
        except Exception as e:
            print(k, code, '失敗', e, flush=True)
        time.sleep(0.3)
    if os.path.exists(path): codes.append(code)
json.dump(codes, open(f'{OUT}/index.json', 'w'))
print('完成，可用', len(codes), '檔', flush=True)
