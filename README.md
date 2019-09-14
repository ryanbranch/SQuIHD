
# SQuIHD

### This repository is a set of programs (Stock Quote Intraday History Downloaders) for automating the retrieval of stock price information.

Historical stock price data is useful for many tasks, from researching the response of a stock to historical events to developing a trading algorithm.

Data at the daily frequency level is freely available all over the internet. On Yahoo Finance one can obtain this information spanning back for the entire lifetimes of (most) major securities. Day-level provides good precision when viewing overall performance of a security in the long term.

However, knowing what the price was on a given day doesn't explain anything about what happened during that day. In a day, the price of a security can rise or fall or end up unchanged, all for any number of reasons. Without explicit knowledge of events that influenced the market, one can only make educated assumptions. Increasing the resolution of price data used is one way to gain insight for these assumptions.
Obtaining higher frequency data for free is more challenging.

On Stooq, hourly data reaching back 7 months and 5-minute data for the last 15 days can be found. These are great sources for examining intraday trends on a more recent timescale.

Through Google Finance, 1-minute data that spans the last 10 days is available.

To my knowledge, these are the longest spanning free sources for historical price data which cover (almost) every stock. In terms of algorithm development, proper backtesting requires many years of data, so these sources simply aren't long enough.

By narrowing the universe of stocks viewed, more possibilities open up:

## Sources of Historical 1-Minute and Tick Data
### Finam

The Russian financial services company Finam Holdings has a public quote export interface for 44 U.S. stocks. The service offers minute-level data reaching over 8 years into the past and tick-level data which goes back just shy of 6 years.

I've written finam_squihd.py, which automates the downloading of this data so that one can avoid filling out the webform hundreds of times.

### Dukascopy

The Swiss Forex Bank Dukascopy offers this service for 250 U.S. stocks. Tick data is available for the last 4 months for each of those stocks, however:

With the built-in CSV export feature, files can only be downloaded 1 day at a time. Download links present are for the binary data files which become the CSV

So automating this download process is much more involved than other hosts.


## License

Due to the terms and conditions of data sources used within, this code is for personal and non-commercial use only. I do not authorize or endorse the use of this tool for any purposes that fall outside of these terms.
