import argparse
import nltk

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
    return result_str



input_text = parse_arguments()
processed = clean_input(input_text)
tokenized_sentences = preprocess_input(processed)
suggestions = get_suggestions(tokenized_sentences)

print(suggestions)

