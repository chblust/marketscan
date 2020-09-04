import yfinance as yf
import math

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
    


data = yf.download(
    tickers="TSLA",
    period="1mo",
    interval="30m",
    prepost=True,
    threads=True
)

print(calc_volatility_over_time(data['Open'], 10))
