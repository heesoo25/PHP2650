# PHP2650
Homework code for PHP 2650: Statistical Learning and Big Data

Assignment 1

Objective: Basic webscraping & manipulate .csv files

Techniques: Download html, html parsing, use cookies & crumbs to download files, make / edit / concatenate .csv files

Part 1: S & P Stock Prices
1) Download stock companies symbols and names from wikipedia page for S & P 100
2) Change BRK.B to BRK-B (in accordance to how the symbols are documented in Yahoo Finance)
3) Download historical stock prices from Yahoo
4) Edit the stock prices data by addition a column of corresponding stock symbol
5) Concatenate all of the .csv files for individual stocks into a single file

Part 2: Funding and Publications
1) Usng a .csv file of recent NIH awards from faculty at Harvard, extract the Award & PI names
2) Clean the extracted data by removing middle names of the PI
3) Extract number of publications for each PI on PubMed catalog
4) Save the number of publications for each PI in a .csv file


Assignment 2

Objective:


Assignment 3

Objective: Practice technolgies for basic predictions.

Technique: reading from sqlite3 tables, sklearn linear regression package

1) Find the IDs that are available in all tables (from the sqlite3 database) and the IDs that are available only in tables 'pred' and 'demo but not in table 'outcome'.
2) Build a model for predicting the outcome scores using the data from the first ID list, and generate predictions for the missing IDs.
3) Use additional data to predict the outcome scores.
4) Use even larger amount of data to see if the outcome score predictions improve.


Assignment 4

Objective: Objective function minimization (LASSO & EN)

Techniques: Elastic net (EN) penalized regression


Assignment 5

Objective:
