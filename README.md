# building-machine-learning-applications
This repository is for the training / examples in the book Building Machine Learning Powered Applications by Emmaneul Ameisen.

## Dependency Management

I'm using a standard `venv` setup with `pip freeze >> requirements.txt`. 

To install dependencies it should be:
`pip install -r requirements.txt`


### Chapter 3

This chapter gets you to create a basic CLI that generates some information about
how good a inputted question is:
- Adverb Usage
- Average Word Length + fraction of unique words
- Syllable, word, and sentence count
- A [Flesch Score](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests)
