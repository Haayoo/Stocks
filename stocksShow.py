import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
import os


def downloadtojson(symbol: str = "0050"):

    filepath = stockfolderpath + r"\stock" + symbol + ".json"

    if os.path.isfile(filepath):
        pass
    else:
        site = (
            "https://query1.finance.yahoo.com/v8/finance/chart/"
            + symbol
            + ".TW?period1=0&period2=9999999999&interval=1d&events=history&=hP2rOschxO0"
        )

        response = requests.get(site)
        with open(filepath, "w") as f:
            f.write(response.text)


def getstockfiles(dirpath):
    stockfiles = []
    for parent, dirnames, filenames in os.walk(dirpath):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            stockfiles.append([pathfile, filename[5:-5]])

    return stockfiles


def jsontoplt(symbol):

    data = json.loads(dict_contents[symbol])

    if data["chart"]["result"] == None or len(dict_contents[symbol]) < 100000:
        print("股票代碼: " + symbol + " 股票 資料不足，請檢查資訊內容")
    else:
        dict_quote = data["chart"]["result"][0]["indicators"]["quote"][0]
        lst_date_timestamp = data["chart"]["result"][0]["timestamp"]

        lst_date = []
        for i in range(len(lst_date_timestamp)):
            dt_object = datetime.fromtimestamp(lst_date_timestamp[i])
            lst_date.append(dt_object)

        lst_close = dict_quote["close"]

        plt.plot(lst_date, lst_close, ls="-", lw=2, label=symbol + "收盤價")


########################################
stockfolderpath = r".\stock"

if not os.path.isdir(stockfolderpath):
    os.mkdir(stockfolderpath, mode=0o777, dir_fd=None)

########################################

lst_stocks = ["0051", "0052", "0053", "0054", "0055", "00875"]  # * 個元素字串型態，內容為台灣股票代碼
try:
    for item in lst_stocks:
        downloadtojson(item)
except requests.exceptions.ConnectionError as identifier:
    print("無法取得資料，請檢查網路狀態，\n將嘗試取得資料檔案")

########################################


lst_stockfiles = getstockfiles(stockfolderpath)
if len(lst_stockfiles) == 0:
    print("沒有資料檔案，無法顯示圖表")
else:
    dict_contents = {}
    for file in lst_stockfiles:
        with open(file[0], "r") as f:
            dict_contents[file[1]] = f.read()
    ########################################
    font = {"family": "Microsoft JhengHei", "size": "12"}
    plt.rc("font", **font)
    for key in dict_contents.keys():
        jsontoplt(key)

    plt.title("歷史收盤價")
    plt.xlabel("年度")
    plt.ylabel("收盤價")
    plt.legend()
    plt.show()
