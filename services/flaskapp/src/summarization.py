"""
This file is responsible for processing input data, \
    tokenize it and feed it to the model
"""
import os
import re
import torch
from transformers import \
    AutoTokenizer, \
    AutoModelForSeq2SeqLM
from langdetect import detect

cache_dir = os.getenv("TRANSFORMERS_CACHE")
print("Value of 'TRANSFORMERS_CACHE' environment variable :", cache_dir)

tokenizer = AutoTokenizer.from_pretrained(
    "QuickRead/pegasus-reddit-7e05-new",
    cache_dir=cache_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(
    "QuickRead/pegasus-reddit-7e05-new",
    cache_dir=cache_dir
)


def remove_emoji(inp):
    """
    Return input without emoji
    """
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', inp)


def remove_urls(inp):
    """
    Return input without urls
    """
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', inp)


def remove_html(inp):
    """
    Return input without html tags
    """
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', inp)


# return a boolean
def is_english(inp):
    """
    Return boolean to determine if input is in english or not
    """
    return detect(inp) == 'en'


def preprocess(inp):
    """
    Clean raw input and return input ids.
    If input is not english, or too long, input ids will be empty
    """
    # Filter english only
    if len(inp) <= 0 or len(inp) > 1500:
        return torch.zeros(size=(0, 1))

    # Remove emoji, URL, HTML tag
    clean_input = remove_emoji(inp)
    clean_input = remove_urls(clean_input)
    clean_input = remove_html(clean_input)

    if not is_english(clean_input):
        return torch.zeros(size=(0, 1))

    input_ids = tokenizer(clean_input, return_tensors="pt", max_length=512,
                          padding='max_length').input_ids
    return input_ids


def predict(inp):
    """
    Return model output in text form
    """
    outputs = model.generate(input_ids=inp)
    res = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    return res
