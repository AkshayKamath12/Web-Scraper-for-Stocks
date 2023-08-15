import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


def updateStocks(urls):
    stocks = []
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        price = float(soup.find_all("div", class_="text-5xl font-bold leading-9 md:text-[42px] md:leading-[60px] text-[#232526]")[0].text)
        company = soup.find_all('h1', attrs={"class": "text-xl text-left font-bold leading-7 md:text-3xl md:leading-8 mb-2.5 md:mb-2 text-[#232526] rtl:soft-ltr"})[0].text
        change = float(soup.find_all('div',attrs={"class": "text-base font-bold leading-6 md:text-xl md:leading-7 rtl:force-ltr"})[0].text)
        changePercentage = soup.find_all('div', attrs={"class": "text-base font-bold leading-6 md:text-xl md:leading-7 rtl:force-ltr"})[1].text

        if changePercentage[1].__eq__('+'):
            changePercentage = float(changePercentage[2: 6])
        else:
            changePercentage = float(changePercentage[2: 6]) * -1

        stocks.append([company, price, change, changePercentage])
    return stocks


def createTable(stockInfo):
    for stock in stockInfo:
        stock[1], stock[2], stock[3] = '$' + str(stock[1]), "{:.2f}".format(stock[2]), str(stock[3]) + '%'
        if stock[2][0].__eq__("-"):
            stock[2] = "-$" + stock[2][1:]
        else:
            stock[2] = "$" + stock[2]

    colNames = ["Company name", "Price", "Change", "Percentage Change"]
    print(tabulate(stockInfo, headers=colNames, tablefmt="fancy_grid"))


def reorder(stockInfo, attribute):
    j = 0
    if attribute.__eq__("price"):
        j = 1
    elif attribute.__eq__("changeInPrice"):
        j = 2
    elif attribute.__eq__("changeInPercentage"):
        j = 3
    i = 0
    while i < (len(stockInfo) - 1):
        if stockInfo[i][j] < stockInfo[i + 1][j]:
            stockInfo[i], stockInfo[i + 1] = stockInfo[i + 1], stockInfo[i]
            i = 0
        else:
            i += 1

    return stockInfo


if __name__ == "__main__":
    stockList = []
    urls = ['https://www.investing.com/equities/amazon-com-inc',
            'https://www.investing.com/equities/apple-computer-inc',
            'https://www.investing.com/equities/google-inc',
            'https://www.investing.com/equities/home-depot',
            'https://www.investing.com/equities/intel-corp',
            'https://www.investing.com/equities/nike',
            'https://www.investing.com/equities/tesla-motors',
            'https://www.investing.com/equities/wal-mart-stores',
            'https://www.investing.com/equities/disney']

    while True:
        userInput = input("Enter 1 to retrieve latest updates on stocks.\nEnter 2 to reorder this based on total stock "
                          "price.\nEnter 3 to reorder this based on change in stock price.\nEnter 4 to reorder"
                          " this based on change in stock price as a percentage. \nEnter anything else to quit:\n")
        if userInput.__eq__("1"):
            print("Retrieving latest stock data. Please wait a few seconds.")
            stockList = updateStocks(urls)
            createTable(stockList)
        elif userInput.__eq__("2"):
            print("Retrieving latest stock data and reordering. Please wait a few seconds.")
            stockList = updateStocks(urls)
            stockList = reorder(stockList, "price")
            createTable(stockList)
        elif userInput.__eq__("3"):
            print("Retrieving latest stock data and reordering. Please wait a few seconds.")
            stockList = updateStocks(urls)
            stockList = reorder(stockList, "changeInPrice")
            createTable(stockList)
        elif userInput.__eq__("4"):
            print("Retrieving latest stock data and reordering. Please wait a few seconds.")
            stockList = updateStocks(urls)
            stockList = reorder(stockList, "changeInPercentage")
            createTable(stockList)
        else:
            break
