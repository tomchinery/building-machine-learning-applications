import argparse
import nltk
import pyphen

def parse_arguments():
  """
  :return: The text to be edited
  """
  parser = argparse.ArgumentParser(description="Receive text to be edited")

  parser.add_argument(
    'text',
    metavar='input text',
    type=str
  )
  args = parser.parse_args()
  return args.text

def clean_input(text):
  """
  :param text: User input text
  :return: Sanitized text, without non ascii characters
  """
  # To keep things simple at the start, let's only keep ASCII characters
  return str(text.encode().decode('ascii', errors='ignore'))

def preprocess_input(text):
  """
    :param text: Sanitized Text
    :return: Text ready to be fed analysis, by having sentences and words
    tokenized
    """
  sentences = nltk.sent_tokenize(text)
  tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
  return tokens

def count_word_usage(tokens, word_list):
  """
  Counts occurances of a given list of words
  :param tokens: a list of tokens for one sentence
  :param word_list: a list of words to search for
  :return: the number of times the words appear in the list
  """
  return len([word for word in tokens if word.lower() in word_list])

def compute_average_word_length(tokens):
  """
  Calculate word length for a sentence
  :param tokens: a list of words
  :return: The average length of words in this list
  """
  word_lengths = [len(word) for word in tokens]
  return sum(word_lengths) / len(word_lengths)

def compute_total_average_word_length(sentence_list):
  """
  Calculate average word length for multiple sentences
  :param sentence_list: a list of sentences, each being a list of words
  :return: The average length of words in this list of sentences
  """
  lengths = [compute_average_word_length(tokens) for tokens in sentence_list]
  return sum(lengths) / len(lengths)

def compute_total_unique_words_fraction(sentence_list):
  """
  Compute fraction os unique words
  :param sentence_list: a list of sentences, each being a list of words
  :return: the fraction of unique words in sentences
  """
  all_words = [word for word_list in sentence_list for word in word_list]
  unique_words = set(all_words)
  return len(unique_words) / len(all_words)

def count_word_syllables(word):
  """
  Count syllables in a word
  :param word: a one word string
  :return: the number of syllables according to pyphen
  """
  dic = pyphen.Pyphen(lang="en_US")
  # this returns our word, with hyphens ("-") inserted in between each syllable
  hyphenated = dic.inserted(word)
  return len(hyphenated.split("-"))

def count_sentence_syllables(tokens):
  """
  Count syllables in a sentence
  :param tokens: a list of words and potientially punctuation
  :return: the number of syllables in the sentence
  """
  # Our tokenizer leaves punctuation as a seperate word, so we filter for it here
  punctuation = ".,!?/"
  return sum(
    [
      count_word_syllables(word)
      for word in tokens
      if word not in punctuation
    ]
  )

def count_total_syllables(sentence_list):
  """
  Count syllables in a list of sentences
  :param sentence_list: a list of sentences, each being a list of words
  :return: the number of syllables in the sentences
  """
  return sum(
    [count_sentence_syllables(sentence) for sentence in sentence_list]
  )

def count_words_per_sentence(sentence_tokens):
  """
  Count words in a sentence
  :param sentence_tokens: a list of words and potentially punctuation
  :return: the number of words in the sentence
  """
  punctuation = ".,!?/"
  return len([word for word in sentence_tokens if word not in punctuation])


def count_total_words(sentence_list):
  """
  Count words in a list of sentences
  :param sentence_list: a list of sentences, each being a list of words
  :return: the number of words in the sentences
  """
  return sum(
    [count_words_per_sentence(sentence) for sentence in sentence_list]
  )

def compute_flesch_reading_ease(total_syllables, total_words, total_sentences):
  """
  Computes readability score from summary statistics
  :param total_syllables: number of syllables in input text
  :param total_words: number of words in input text
  :param total_sentences: number of sentences in input text
  :return: A readability score: the lower the score, the more complex the text is deemed to be
  """
  return (
    206.85
    - 1.015 * (total_words / total_sentences)
    - 84.6 * (total_syllables / total_words)
  )

def get_reading_level_from_flesch(flesch_score):
  """
  Thresholds taken from https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
  :param flesch_score:
  :return: A reading level and difficulty for a given flesch score
  """
  if flesch_score < 30:
    return "Very difficult to read"
  elif flesch_score < 50:
    return "Difficult to read"
  elif flesch_score < 60:
    return "Fairly difficult to read"
  elif flesch_score < 70:
    return "Plain English"
  elif flesch_score < 80:
    return "Fairly easy to read"
  elif flesch_score < 90:
    return "Easy to read"
  else:
    return "Very easy to read"

def get_suggestions(sentence_list):
  """
    Returns a string containing our suggestions
    :param sentence_list: a list of sentences, each being a list of words
    :return: suggestions to improve the input
    """
  told_said_usage = sum(
    (count_word_usage(tokens, ["told", "said"]) for tokens in sentence_list)
  )
  but_and_usage = sum(
    (count_word_usage(tokens, ["but", "and"]) for tokens in sentence_list)
  )
  wh_adverbs_usage = sum(
    (
      count_word_usage(
        tokens,
        [
          "when",
          "where",
          "why",
          "whence",
          "whereby",
          "wherein",
          "whereupon"
        ]
      )
            for tokens in sentence_list
    )
  )
  result_str = ""
  adverb_usage = "Adverb usage: %s told/said, %s but/and, %s wh adverbs" % (
    told_said_usage,
    but_and_usage,
    wh_adverbs_usage
  )
  result_str += adverb_usage
  average_word_length = compute_total_average_word_length(sentence_list)
  unique_words_fraction = compute_total_unique_words_fraction(sentence_list)

  word_stats = "Average word length %.2f. fraction of unique words %.2f" % (
    average_word_length,
    unique_words_fraction
  )
  # Using HTML to later display on a webapp
  result_str += "<br/>"
  result_str += word_stats

  number_of_syllables = count_total_syllables(sentence_list)
  number_of_words = count_total_words(sentence_list)
  number_of_sentences = len(sentence_list)

  syllable_counts = "%d syllables, %d words, %d sentences"  % (
    number_of_syllables,
    number_of_words,
    number_of_sentences
  )

  result_str += "<br/>"
  result_str += syllable_counts


  flesch_score = compute_flesch_reading_ease(
    number_of_syllables, number_of_words, number_of_sentences
  )

  flesch = "%.2f flesch score: %s" % (
    flesch_score,
    get_reading_level_from_flesch(flesch_score),
  )

  result_str += "<br/>"
  result_str += flesch

  return result_str

input_text = parse_arguments()
processed = clean_input(input_text)
tokenized_sentences = preprocess_input(processed)
suggestions = get_suggestions(tokenized_sentences)

print(suggestions)

