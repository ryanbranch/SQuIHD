import datetime
from datetime import timedelta
import os
import sys
import pandas as pd

#NOTES
# - The Data Source appears to cap TICK downloads to 1,000,000 lines per file.
#   If you specify a time range which contains more than 1,000,000 lines, the downloaded file
#   will begin at the front of the time range and extend 1,000,000 lines forward.
# - The number of lines in a given tick data time period will vary heavily across stocks.
#   For HPQ, 1,000,000 lines tends to span from 4 to 6 months, by my observation
# - The Data Source does not seem to allow multiple years of MINUTE data to be downloaded at once.

#Specifies number of years in the past to attempt downloads
YEARS_BACK = 10

#Specifies directory in which data is saved, subdivided by ticker symbol
DATA_DIRECTORY = "finam_data"

#Specifies frequency of data to download
# 1 = TICK DATA
# 2 = MINUTE DATA
FREQUENCY = 2

#Dictionary pairing supported stock ticker symbols with corresponding "em" values
EM_DICT = {
"MMM":"18090",#     3M
"T":"19067",#       AT&T Inc.
"ADBE":"20563",#    Adobe Systems Inc.
"AA":"17997",#      Alcoa Inc.
"GOOG":"20590",#    Alphabet Inc.
"AXP":"18009",#     American Express
"AIG":"19070",#     American International Group
"AMT":"20568",#     American Tower Corporation
"AAPL":"20569",#    Apple Inc.
"AMAT":"20570",#    Applied Materials Inc.
"BAC":"18011",#     Bank of America
"BA":"18010",#      Boeing
"CA":"20576",#      CA Technologies
"CAT":"18026",#     Caterpillar Inc.
"CVX":"18037",#     Chevron
"CSCO":"20580",#    Cisco Systems Inc.
"C":"18023",#       Citigroup Inc.
"KO":"18076",#      The Coca-Cola Company
"GLW":"20582",#     Corning Inc.
"DD":"18039",#      DuPont
"EMC":"20585",#     Dell EMC
"XOM":"18149",#     Exxon Mobil
"FSLR":"20586",#    First Solar Inc.
"GE":"18055",#      General Electric
"GS":"47256",#      Goldman Sachs Group Inc.
"HPQ":"18068",#     Hewlett-Packard
"HD":"18063",#      Home Depot
"IBM":"18069",#     IBM
"IP":"22141",#      International Paper
"INTC":"19069",#    Intel
"JPM":"18074",#     JPMorgan Chase
"JNJ":"18073",#     Johnson & Johnson
"MCD":"18080",#     McDonalds
"MRK":"18094",#     Merck & Co
"MSFT":"19068",#    Microsoft Corp
"PFE":"18106",#     Pfizer Inc.
"PG":"18107",#      Procter & Gamble
"TRV":"22139",#     Travelers Companies Inc.
"UTX":"18134",#     United Technologies
"VZ":"18137",#      Verizon Communications
"WMT":"18146",#     Wal-Mart Stores
"DIS":"18041",#     Walt Disney
"WFC":"22138",#     Wells Fargo
"YHOO":"19075",#    Yahoo Inc.
}

#Creates a "finam_data" directory with subfolders for each of the supported stock ticker symbols
def makeFolders():

    #Stores full path so data directory is placed in the same directory as this script
    fullDirectory = os.path.join(sys.path[0], DATA_DIRECTORY)
    #If the data directory already exists, we assume the subfolders do as well, and return early
    if os.path.exists(fullDirectory):
        print("DIRECTORY EXISTS: " + DATA_DIRECTORY)
        return
    #Otherwise, we create subfolders for each ticker symbol, as long as they don't already exist
    else:
        print("DIRECTORY CREATED: " + DATA_DIRECTORY)
        os.makedirs(fullDirectory)

#Creates a URL which can be used to directly download CSV files of historical stock price data from finam.ru
def buildURL(tickerSymbol, fromDate, toDate, headers=False, saveAs="download"):

    url = "http://export.finam.ru/a?market=25"#         US markets
    url += ("&em=" + EM_DICT[tickerSymbol])#            Specifies "em" value for ticker symbol
    url += ("&code=US1." + tickerSymbol)#               Specifies ticker symbol
    url += ("&apply=0&df=" + str(fromDate.day))#        Specifies from-day
    url += ("&mf=" + str(fromDate.month - 1))#          Specifies from-month
    url += ("&yf=" + str(fromDate.year))#               Specifies from-year
    url += ("&from=a&dt=" + str(toDate.day))#           Specifies to-day
    url += ("&mt=" + str(toDate.month - 1))#            Specifies to-month
    url += ("&yt=" + str(toDate.year))#                 Specifies to-year
    url += ("&to=a&p=" + str(FREQUENCY))#               Specifies data frequency
    url += ("&f=" + saveAs + "&e=.csv")#                Specifies filename as saveAs with ".csv" extension
    url += ("&cn=" + tickerSymbol)#                     Specifies ticker symbol, as displayed in file
    url += ("&dtf=5&tmf=3")#                            Datetime format is MM/DD/YY hh:mm:ss
    url += ("&MSOR=1&mstimever=0")#                     Times designate END of candle and are local to US markets
    url += ("&sep=1&sep2=1")#                           Commas delimit columns, no row-delimiting characters
    url += ("&datf=1")#                                 Data format: TICKER, PER, DATE, TIME, OPEN, HIGH, LOW, CLOSE, VOL

    #Specifies whether or not to include column headers
    if headers:
        url += ("&at=1")#                               Yes, include column headers
    else:
        url += ("&at=0")#                               No, don't include column headers

    url += ("&fsp=0")#                                  No, don't fill in periods which have no transactions

    return url

#Builds a list of tuples of datetime.date objects, of length "n" years, and of the following format,
#where Y represents today's year, M today's month, and D today's day:
#    (datetime.date(Y - 1, M, D + 1), datetime.date(Y, M, D))
#    (datetime.date(Y - 2, M, D + 1), datetime.date(Y - 1, M, D))
#    (datetime.date(Y - 3, M, D + 1), datetime.date(Y - 2, M, D))
def getYearTuplesList(n):
    ytl = []
    #tDate, tYear, tMonth, and tDay all refer to "today" and not "to-date"/"to-day"
    tDate = datetime.date.today()
    tYear = tDate.year
    tMonth = tDate.month
    tDay = tDate.day
    for i in range(n):
        ytl.append((datetime.date(tYear - (i + 1), tMonth, tDay + 1), datetime.date(tYear - i, tMonth, tDay)))
    return ytl

#Builds a list of tuples of datetime.date objects, of length "n" months, and of the following format,
#where Y represents today's year, M today's month, and D today's day:
#    (datetime.date(Y, M - 1, D + 1), datetime.date(Y, M, D))
#    (datetime.date(Y, M - 2, D + 1), datetime.date(Y, M - 1, D))
#    (datetime.date(Y, M - 3, D + 1), datetime.date(Y, M - 2, D))
#     ...
#    (datetime.date(Y - 1, M - 2, D + 1), datetime.date(Y - 1, M - 1, D))
def getMonthTuplesList(n):
    mtl = []
    tDate = datetime.date.today()
    tYear = tDate.year
    tMonth = tDate.month
    tDay = tDate.day
    startYear = tYear
    stopYear = tYear
    startMonth = tMonth
    stopMonth = tMonth
    startDay = tDay + 1
    stopDay = tDay

    for i in range(n):
        #Begin by adjusting the start date parameters
        startMonth = stopMonth - 1
        if (startMonth <= 0):
            startYear -= 1
            startMonth += 12

        mtl.append((datetime.date(startYear, startMonth, startDay), datetime.date(stopYear, stopMonth, stopDay)))

        #End by adjusting the stop date parameters for the next iteration
        stopMonth -= 1
        if (stopMonth <= 0):
            stopYear -= 1
            stopMonth += 12
    return mtl

def main():

    makeFolders()

    #A list of tuples of from-date and to-date pairs, every year spanning YEARS_BACK years into the past
    tuples = []
    if (FREQUENCY == 1):
        tuples = getMonthTuplesList(YEARS_BACK * 12)
    elif (FREQUENCY == 2):
        tuples = getYearTuplesList(YEARS_BACK)

    for tickerSymbol in EM_DICT.keys():

        symbolDirectory = os.path.join(os.path.join(sys.path[0], DATA_DIRECTORY), tickerSymbol)
        if os.path.exists(symbolDirectory):

            print("SUBFOLDER ALREADY EXISTS for ticker symbol " + tickerSymbol)
            print("To update contents, delete the subfolder and run this program again.")
        else:

            print("[==============================] Beginning work for ticker symbol: " + tickerSymbol + " [==============================]")
            os.makedirs(symbolDirectory)
            print("Created subfolder.")

            urlList = []
            for i, tuple in enumerate(tuples):
                urlList.append(buildURL(tickerSymbol, tuple[0], tuple[1], True))
            #Reverses the order of the download URLs, I just found things easier to comprehend while writing this way
            urlList = urlList[::-1]
            numURLs = len(urlList)

            #This is how the program figures out the first viable time period from which to fill the output CSV
            firstViable = numURLs
            found = False
            for i in range(numURLs):
                if not found:
                    print(str(i) + " in firstViable loop.")
                    try:
                        test_csv = pd.read_csv(urlList[i])
                        firstViable = i
                        found = True
                        print("FOUND viable data in year at position: " + str(i) + "    (traversing forward from " + str(numURLs) + " back)")
                    except Exception as e:
                        print(str(e))

            if (found):

                #In tick-level mode, a separate CSV file is generated for each 1-month period
                if (FREQUENCY == 1):
                    counter = 0
                    for i in range(firstViable, numURLs):
                        print(str(i) + " in merging loop.  Corresponds to file number " + str(counter) + " (0-indexed).")
                        main_csv = pd.read_csv(urlList[i])
                        nameString = (tickerSymbol + "_tick_" + str(counter) + ".csv")
                        main_csv.to_csv(os.path.join(DATA_DIRECTORY, tickerSymbol, nameString), index=False)
                        counter += 1

                #In minute-level mode, a single CSV file is generated, composed of all 1-year periods combined
                elif (FREQUENCY == 2):
                    main_csv = pd.read_csv(urlList[firstViable])
                    for i in range(firstViable + 1, numURLs):
                        print(str(i) + " in merging loop.")
                        temp_csv = pd.read_csv(urlList[i])
                        main_csv = main_csv.append(temp_csv)

                    nameString = (tickerSymbol + "_min.csv")
                    main_csv.to_csv(os.path.join(DATA_DIRECTORY, tickerSymbol, nameString), index=False)

            else:
                print("DATA UNAVAILABLE FOR TICKER: " + tickerSymbol)

main()
