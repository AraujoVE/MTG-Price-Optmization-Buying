# WORK IN PROGRESS

# MTG Price Optimization Buying (Magic: The Gathering).

This project aims to minimize the cost of an order of card packs, considering the taxes and a lot of different sites.
To achieve the objective, we are using Neural Networks and HTML Scrapping.

## How does it work

### HTML Scrapping (Python)

First, a python script uses regex to find useful information on "Liga Magic" (Brazillian Magic Website). Then, it organizes it in a way to be used later in the next algorithm

### Data Processing (Neural Networks in C)

After data has been collected, it is passed to a C program that will use Genetic Algorithm allied with Neural Network techniques in order to find the best combinations of order(s) for a given set of cards.
For example, if you want to buy 2 cards, the program will start by analyzing the price of all sites for those two cards and then, apply the concepts of generations, best individual, fitness, mutation, genocide, etc. putting final price as a measure of fitness.
