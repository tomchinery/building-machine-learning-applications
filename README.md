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

Example input questions:

> Is this workflow any good?
```
Adverb usage: 0 told/said, 0 but/and, 0 wh adverbs
Average word length 3.67. fraction of unique words 1.00
6 syllables, 5 words, 1 sentences
100.26 flesch score: Very easy to read
```

> Here is a needlessly obscure question, that
> does not provide clearly which information it would
> like to aquire, does it?
```
Adverb usage: 0 told/said, 0 but/and, 0 wh adverbs
Average word length 4.39. fraction of unique words 0.87
29 syllables, 20 words, 1 sentences
63.88 flesch score: Plain English
```

> Ideally, we would like our workflow to return a positive
> score for the simple sentence, a negative score for the convoluted one, and 
> suggestions for improving our paragraph. Is that the case already?
```
Adverb usage: 0 told/said, 1 but/and, 0 wh adverbs
Average word length 4.03. fraction of unique words 0.76
52 syllables, 33 words, 2 sentences
56.79 flesch score: Fairly difficult to read
```

#### Improvements

While the example script works it could be improved from a software engineering perspective. 
- Functions could be split into their own files / modules
- Unit Tests could be written for each function
- The `get_suggestions` function could be broken down further to make it easier to read
