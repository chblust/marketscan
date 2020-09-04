import argparse
import yfinance as yf
import volatility_scan as vs

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", type=str, action="store", dest="ticker", default="SPY", help="The ticker for the stock to analyze")
    parser.add_argument("-p", type=str, action="store", dest="period", default="1mo", help="The period of time to analyze")
    parser.add_argument("-i", type=str, action="store", dest="interval", default="30m", help="The measurement intervals to be interpretted from")
    parser.add_argument("-v", action="store_true", dest="verbose", help="Toggles verbosity")

    args = parser.parse_args()

    data = yf.download(
        tickers=args.ticker.upper(),
        period=args.period,
        interval=args.interval,
        prepost=True,
        threads=True
    )

    print(vs.calc_volatility_over_time(data['Open'], 10))


if __name__ == "__main__":
    main()