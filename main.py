import random as rnd
import sec
import pandas as pd
import returns as ret
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_sp500_companies():
    """
    Return a pandas dataframe containing the company name, symbol and CIK
    for all companies in the S&P 500 as listed in Wikipedia
    """
    sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    sym = []
    name = []
    cik = []
    r = requests.get(sp500_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find("table", {"id": "constituents"})
    table_body = table.find('tbody')

    rows = table_body.findAll('tr')
    for row in rows:
        cells = row.findAll('td')
        if len(cells) >= 8:
            sym.append(cells[0].text.strip())
            name.append(cells[1].text.strip())
            cik.append(cells[7].text.strip())

    return pd.DataFrame({"Name": name,
                         "Symbol": sym,
                         "CIK": cik})


def get_10K_risk_sentiments(companies, years, no_of_companies=5, shuffle=True):
    """
    Return a pandas dataframe containing the risk sentiments
    for a number of companies from a given list of companies (randomly shuffled)
    for a given list of years
    """
    quarters = ['QTR1', 'QTR2', 'QTR3', 'QTR4']
    year_lst = []
    name_lst = []
    sym_lst = []
    cik_lst = []
    sntmt_lst = []
    qtr_lst = []

    analyzer = SentimentIntensityAnalyzer()

    co_index = [*range(len(companies))]

    if shuffle:
        rnd.shuffle(co_index)

    for idx in co_index[:no_of_companies]:
        name, sym, cik = companies.loc[idx, :]
        for year in years:
            for qtr in quarters:
                print("... for co: ", sym, " year: ", year, " qtr: ", qtr)
                doc = sec.get_10K_doc(cik, year, qtr)
                if len(doc) > 0:
                    rsk_doc = sec.pull_risk_section(sec.parse_10K_doc(doc))
                    if len(rsk_doc) > 0:
                        score = analyzer.polarity_scores(rsk_doc).get('compound')
                        sntmt_lst.append(score)
                        year_lst.append(year)
                        qtr_lst.append(qtr)
                        name_lst.append(name)
                        sym_lst.append(sym)
                        cik_lst.append(cik)
                        break
                    else:
                        break

    return pd.DataFrame({"Name": name_lst,
                         "Symbol": sym_lst,
                         "CIK": cik_lst,
                         "Year": year_lst,
                         "Quarter": qtr_lst,
                         "Sentiment": sntmt_lst})


def get_returns_for_sentiment(sentiments):
    """
    Returns a pandas dataframe containing the quarterly returns
    of list of companies provided in the list of sentiments provided.
    This list of sentiments will be for a number of companies for a number of years.
    """
    year_lst = []
    qtr_lst = []
    name_lst = []
    sym_lst = []
    cik_lst = []
    senti_lst = []
    q1_lst = []
    q2_lst = []
    q3_lst = []
    q4_lst = []

    for index, row in sentiments.iterrows():
        name, sym, cik, year, qtr, senti = row["Name"], row["Symbol"], row["CIK"], row["Year"], row["Quarter"], row[
            "Sentiment"]
        q1, q2, q3, q4 = ret.get_returns(sym, year, qtr)
        q1_lst.append(q1)
        q2_lst.append(q2)
        q3_lst.append(q3)
        q4_lst.append(q4)
        year_lst.append(year)
        qtr_lst.append(qtr)
        name_lst.append(name)
        sym_lst.append(sym)
        cik_lst.append(cik)
        senti_lst.append(senti)

    return pd.DataFrame({"Name": name_lst,
                         "Symbol": sym_lst,
                         "CIK": cik_lst,
                         "Year": year_lst,
                         "Quarter": qtr_lst,
                         "Sentiment": senti_lst,
                         "Q1": q1_lst, "Q2": q2_lst, "Q3": q3_lst, "Q4": q4_lst})


if __name__ == '__main__':
    years = [*range(2018, 2015, -1)]
    no_cos = 50

    print("Getting companies ...")
    companies = get_sp500_companies()
    companies.to_csv(r".\Data\companies.csv", index=False)

    print("Getting sentiments ...")
    sentiments = get_10K_risk_sentiments(companies, years, no_of_companies=no_cos)
    sentiments.to_csv(r".\Data\sentiments.csv", index=False)

    print("Getting returns ...")
    returns = get_returns_for_sentiment(sentiments)
    returns.to_csv(r".\Data\returns.csv", index=False)
