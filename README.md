**The Exchange Rate Path Problem**

Hugo Brunet - 10th, november 2018

This exercice was completed using Python 3

## Download notebook.html 
Before running the project, I recommend to download the source files and to open the html file *notebook.html*. It is a **Jupyter notebook** 
which describes my work (and my code of course!) with explanations, comments and tests example in a user friendly interface.

## Description of exercice
This exercice deals with The Exchange Rate Path Problem  

We receive a serie of price updates:  
**[timestamp] [exchange] [source_currency] [destination_currency] [forward_factor] [backward_factor]**  
For instance:  
**2017-11-01T09:42:23+00:00 KRAKEN BTC USD 1000.0 0.0009**  
*Which means that **a price update was received** from Kraken on November 1, 2017 at 9:42 am. The update says **1 BTC = 1000 USD** and  **1 USD = 0.0009 BTC***  

Price updates are **not guaranteed** to arrive in chronological order so we have to consider only the most recent price update for each (source_currency, destination_currency) pair.  

We have to store these data in a graph:  
**Example:**  

We receive the following price_update stream:  
**2017-11-01T09:42:23+00:00 KRAKEN BTC USD 1000.0 0.0009  
2017-11-01T09:43:23+00:00 GDAX BTC USD 1001.0 0.0008**  

We have to create the following graph:  
(KRAKEN, BTC) -- 1000.0 --> (KRAKEN, USD)  
(KRAKEN, USD) -- 0.0009 --> (KRAKEN, BTC)  
(GDAX, BTC) -- 1001.0 --> (GDAX, USD)  
(GDAX, USD) -- 0.0008 --> (GDAX, BTC)  
(KRAKEN, BTC) -- 1.0 --> (GDAX, BTC)  
(GDAX, BTC) -- 1.0 --> (KRAKEN, BTC)  
(KRAKEN, USD) -- 1.0 --> (GDAX, USD)  
(GDAX, USD) -- 1.0 --> (KRAKEN, USD)  

Then we receive an exchange rate request:  
**EXCHANGE_RATE_REQUEST [source_exchange] [source_currency] [destination_exchange] [destination_currency]**  
For instance:  
**EXCHANGE_RATE_REQUEST KRAKEN BTC GDAX USD**  
***With this rate_request, we have to return the **best possible exchange rate** as well as the **trades and transfers needed** to achieve that rate***
       
  

### The main goal of this exercice is to create a program that can:  
* Manage the reception of price updates information  
* Organize them in a graph  
* Find the best rate for a trade between two pairs (ExchangeA, CurrencyA) / (ExchangeB, CurrencyB)  

## Download files
Clone or download the 4 python files of the *source* repository:   
- vertex.py  
- edge.py  
- graph.py  
- main.py  
The 4 files have to be in the same repository!

## Requirements
* Python 3  
* pip: $ python -m pip install -U pip
* Networkx: $ pip install networkx==2.2 (graph library)
* Matplotlib: $ pip install -U matplotlib (allows to draw and display a graph)


## Run the project
**Open the *main.py* file**  
Now, please, go to function main() line 10.  
On this function, you already have a scenario, you just have to run the file. A scenario is as follows:  
1. Creation of a graph  
2. Price_udates stream on stdin  
3. Add information to the raph  
4. New price_updates stream  
5. Update the graph  
6. Rate_request on stdin   
7. Find best rate and best related path  
8. Display the result of the rate request on stdout  

If you want to test the code with other price_updates value, please, modify the **stream_price_updates** list trying to respect
the price_update stream format: <timestamp> <exchange> <source_currency> <destination_currency> <forward_factor> <backward_factor>  
NB: if the input format is incorrect, you will have the error information displayed on stdout :) 

NB: Please don't forget to close the graph figure so as to end the program.
