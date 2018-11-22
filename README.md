**The Exchange Rate Path Problem**

Hugo Brunet - 10th, november 2018

This exercice was completed using Python 3

## Download notebook.html 
Before downloading the source files of the project, I recommend to download and open the html file *notebook.html*. It is a **Jupyter notebook** 
which describes my work (and my code of course!) with explanations, comments and tests example in a user friendly interface.

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
