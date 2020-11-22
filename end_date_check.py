import PyPDF2
import re
import pandas as pd

import cv2
import pytesseract

ticker_pdf = ("52 HK 2020 A1 prelim.pdf", "8331 HK 2020 Q1 prelim.pdf", "823 HK 2020 S1 prelim.pdf")

# function for date find
def DateFinder(table):
    res_ticker = []
    res_date = []
    for i in table:
        pdf1 = open(i, "rb")
        pdf1_reader = PyPDF2.PdfFileReader(pdf1)
        pdf1_p1 = pdf1_reader.getPage(0)
        pdf1_p1.extractText()
        text1 = pdf1_p1.extractText()
        ##
        text1_nospace = text1.replace(" ","")
        res_1 = text1_nospace.find("ofthecontentsofthisannouncement")
        text1_r = text1[res_1+33: res_1+400]
        res_2 = text1_r.find("FORTHE")
        ##
        if res_2 == -1:
            res_2 = text1_r.find("FOR THE")
        else:
            pass
        ##
        text2 = text1_r[res_2:res_2+130]
        text3 = re.split("\n", text2)
        Date_str = text3[0]
        year_loc = re.search("\d\d\d\d",Date_str).start()
        Date = Date_str[0:year_loc+4]        
        res_ticker.append(i)
        res_date.append(Date)
        
        result = pd.DataFrame(
            {"Ticker document": res_ticker,
             "End date": res_date})
    return result

ticker_date = DateFinder(ticker_pdf)
ticker_date

tube_img = cv2.imread("flow.png")
text = pytesseract.image_to_string(tube_img)

