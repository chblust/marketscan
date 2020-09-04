import yfinance as yf
import math
import argparse

def get_mean(lst):
    sum = 0.0
    for i in lst:
        sum += i
    
    return sum/len(lst)

def calc_volatility_from_samples(samples):
    """
    Calculate the historical volatility of a stock price over a given number of samples.
    Use standard deviation as a metric of volatility.
    timeseries- list of stock price samples in order
    sample_interval- time between samples
    """
    mean = get_mean(samples)

    dev_sq_sum = 0.0
    for s in samples:
        # calc deviation
        dev = mean - s
        # add the squared deviation
        dev_sq_sum += dev*dev
    
    return math.sqrt(dev_sq_sum / len(samples))


def calc_volatility_over_time(timeseries, interval):
    """
    Generate volatility over time for given timeseries price data.
    i.e. Get a measure of volatility for each price entry of a stock over time.
    Return in list format.
    timeseries- list of stock price samples in order
    interval- how many samples to calculate the volatility over
    """

    # initialize volatility array, ensure it has the same length as the timeseries data
    vols = [None] * len(timeseries)

    # start at end of first interval. Dont calc vol for values before this, we cant
    for i in range(interval-1, len(timeseries)):
        vols[i] = calc_volatility_from_samples(timeseries[i-(interval-1):i+1])
    
    return vols

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

    print(calc_volatility_over_time(data['Open'], 10))

if __name__ == "__main__":
    main()