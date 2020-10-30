import yfinance as yf
import datetime as dt


def get_returns(sym, year, qtr):
    if qtr == 'QTR1':
        start_date = str(year) + "-01-01"
        end_date = str(year) + "-12-31"
        q1_date = dt.datetime(year, 3, 31)
        q2_date = dt.datetime(year, 6, 30)
        q3_date = dt.datetime(year, 9, 30)
        q4_date = dt.datetime(year, 12, 31)
    elif qtr == 'QTR2':
        start_date = str(year) + "-04-01"
        end_date = str(year+1) + "-03-31"
        q1_date = dt.datetime(year, 6, 30)
        q2_date = dt.datetime(year, 9, 30)
        q3_date = dt.datetime(year, 12, 31)
        q4_date = dt.datetime(year+1, 3, 31)
    elif qtr == 'QTR3':
        start_date = str(year) + "-07-01"
        end_date = str(year+1) + "-06-30"
        q1_date = dt.datetime(year, 9, 30)
        q2_date = dt.datetime(year, 12, 31)
        q3_date = dt.datetime(year+1, 3, 31)
        q4_date = dt.datetime(year+1, 6, 30)
    else:
        start_date = str(year) + "-10-01"
        end_date = str(year+1) + "-09-30"
        q2_date = dt.datetime(year, 12, 31)
        q3_date = dt.datetime(year+1, 3, 31)
        q4_date = dt.datetime(year+1, 6, 30)
        q1_date = dt.datetime(year+1, 9, 30)
    # print(f"Downloading data for {sym} in year {year}")
    data = yf.download(sym, start=start_date, end=end_date, interval="1d")
    if len(data) == 0:
        return [0.0, 0.0, 0.0, 0.0]

    opening_date = min(data.index)
    opening_price = data.loc[opening_date]["Close"]

    q1_price = data.loc[max(data[data.index <= q1_date].index)]["Close"] if opening_date < q1_date else opening_price
    q2_price = data.loc[max(data[data.index <= q2_date].index)]["Close"] if opening_date < q2_date else opening_price
    q3_price = data.loc[max(data[data.index <= q3_date].index)]["Close"] if opening_date < q3_date else opening_price
    q4_price = data.loc[max(data[data.index <= q4_date].index)]["Close"] if opening_date < q4_date else opening_price

    return [q1_price, q2_price, q3_price, q4_price]/opening_price - 1


if __name__ == '__main__':
    sym = "MSFT"
    year = 2015
    quarter = 'QTR3'
    print(get_returns(sym, year, quarter))
