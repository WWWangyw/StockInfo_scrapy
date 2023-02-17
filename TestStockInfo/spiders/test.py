import requests
from bs4 import BeautifulSoup
import traceback
import re


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getStockList(lst, stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', attrs={'class':'stock_table'})
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            string = re.findall(r'[s][h]\d{6}', href)[0].replace('sh', '')
            if lst == []:
                lst.append(string)
            if lst[-1] == string:
                continue
            else:
                lst.append(string)

        except:
            continue



def getStockInfo(lst, stockURL, fpath):
    regex_symbol = r'\"symbol\":\"\d{6}\"'
    regex_name = r'\"nameCN\":\".*?\"'
    regex_latestPrice = r'\"latestPrice\":[\d\.]*'
    count = 0
    for stock in lst:
        url = stockURL + stock
        html = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')

        try:
            if soup == '':
                continue
            stockInfo = []
            for match in re.finditer(regex_symbol, str(soup)):
                stockInfo.append(match.group().replace("\"symbol\":", ""))

            for match in re.finditer(regex_name, str(soup)):
                stockInfo.append(match.group().replace("\"nameCN\":", ""))
            for match in re.finditer(regex_latestPrice, str(soup)):
                stockInfo.append(match.group().replace("\"latestPrice\":", ""))

            with open(fpath, 'a', encoding='utf-8') as f:
                tmpl = '{0:^10}{1:{3}^6}{2:^8}\n'
                if count == 0:
                    string = tmpl.format('股票代码', '股票名称', '最新价', chr(12288))
                else:
                    string = tmpl.format(str(stockInfo[0]).replace('\"', ''), str(stockInfo[2].replace('\"', '')),
                                         str(stockInfo[3]).replace('\"', ''), chr(12288))
                f.write(string)

            count += 1
        except:
            traceback.print_exc()
            continue


def main():

    stock_list_url = 'http://app.finance.ifeng.com/list/stock.php?t=ha&f=chg_pct&o=desc&p=1'
    stock_info_url = 'https://www.laohu8.com/stock/'

    output_file = 'C:/Users/23235/PycharmProjects/TestStockInfo/BaiduStockInfo.txt'
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)

main()