"""
This file is responsible for processing input data, tokenize it and feed it to the model
"""
import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect

tokenizer = AutoTokenizer.from_pretrained("QuickRead/pegasus-reddit-7e05-new")
model = AutoModelForSeq2SeqLM.from_pretrained("QuickRead/pegasus-reddit-7e05-new")

def remove_emoji(input):
    """
    Return input without emoji
    """
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', input)

def remove_urls(input):
    """
    Return input without urls
    """
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', input)

def remove_html(input):
    """
    Return input without html tags
    """
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', input)

# return a boolean
def is_english(input):
    """
    Return boolean to determine if input is in english or not
    """
    return detect(input) == 'en'

def preprocess(inp):
    """
    Clean raw input and return input ids.
    If input is not english, or too long, input ids will be empty
    """
    # Remove emoji, URL, HTML tag
    clean_input = remove_emoji(inp)
    clean_input = remove_urls(clean_input)
    clean_input = remove_html(clean_input)

    # Filter english only
    if not is_english(clean_input) or len(clean_input) > 1500:
        return torch.zeros(size=(0,1))

    input_ids = tokenizer(clean_input, return_tensors="pt", max_length = 512,
                                        padding = 'max_length').input_ids
    return input_ids

def predict(input_ids):
    """
    Return model output in text form
    """
    outputs = model.generate(input_ids=input_ids)
    res = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return res
