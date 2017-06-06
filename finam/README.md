# Finam SQuIHD

This (finam_squihd.py) is the Stock Quote Intraday History Downloader for [finam.ru](https://www.finam.ru/).
It sends all requests through their [public quote export interface](https://www.finam.ru/profile/akcii-usa-bats/3m-co/export/?market=25&em=18090&code=MMM&apply=0&df=1&mf=3&yf=1979&from=01.04.1979&dt=30&mt=5&yt=1979&to=30.06.1979&p=2&f=MMM_790401_790630&e=.txt&cn=MMM&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=1&sep2=1&datf=1&at=1). The data retreived by this tool can also be downloaded manually at that interface.

## Usage
To download minute-level data, everything is handled automatically! Just run the script with Python.

    % python finam_squihd.py
A list of the 44 US stocks available on Finam is written into the code. If the availability of these stocks changes in the future, the code will need to be updated accordingly.

Currently the program is only tested and confirmed to function with minute-level data.
For tick-level data, you can change the FREQUENCY variable from 2 to 1, but more modification is needed to make everything functional. 

## History

Written and released on 5 June 2017

## Credits

Written by [Ryan Branch](http://ryanbran.ch/)
For inquiries regarding this code, contact me at ryanbranch@ryanbran.ch


## License

As Finam states in their terms, their data is for personal, non-commercial use only. I do not authorize or endorse the use of this tool for any purposes that fall outside of [Finam's Market Data Terms and Conditions](https://www.finam.ru/about/quotes/).