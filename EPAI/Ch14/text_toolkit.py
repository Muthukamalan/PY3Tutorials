import re
from collections import Counter
from pathlib import Path
from typing import Generator,  Union
import numpy as np


TextInput = Union[str, Path]

__all__=['text_generator','clean_text','unique_words','word_frequency','create_co_occurrence_matrix']


def _is_path(text_or_path: TextInput) -> bool:
    """Heuristic to determine if input is likely a file path."""
    try:
        return Path(text_or_path).exists()
    except Exception:
        return False


def text_generator(text_or_path: TextInput) -> Generator[str, None, None]:
    """
    Internal generator yielding lines from either a file or string input.
    Uses a context manager when opening files.
    """
    if _is_path(text_or_path):
        with open(text_or_path, "r", encoding="utf-8") as f:
            for line in f:
                yield line.strip()
    else:
        for line in str(text_or_path).splitlines():
            yield line.strip()

def clean_text(text:str)->str:
    """Helper to tokenize and clean strings."""
    return re.findall(r'\b\w+\b', text.lower())

def unique_words(input_data:TextInput)->set:
    """Extracts a set of all unique words."""
    unique_set = set()
    for line in text_generator(input_data):
        unique_set.update(clean_text(line))
    return unique_set

def word_frequency(input_data):
    """Counts word frequency using a generator-based approach."""
    counts = Counter()
    for line in text_generator(input_data):
        counts.update(clean_text(line))
    return dict(counts)

def create_co_occurrence_matrix(corpus, window_size=1):
    vocabulary:set = set()
    co_occurrence_matrix:dict = {}

    # Tokenize the corpus
    tokenized_corpus:list[list[str]] = [line.split() for line in  text_generator(corpus)]

    for tokens in tokenized_corpus:
    # Build vocabulary and co-occurrence matrix
        for i, token in enumerate(tokens):
            if token not in vocabulary:
                vocabulary.add(token)
                co_occurrence_matrix[token] = {}
            
            for j in range(max(0, i - window_size), min(len(tokens), i + window_size + 1)):
                if i != j:
                    context_token = tokens[j]
                    if context_token not in co_occurrence_matrix[token]:
                        co_occurrence_matrix[token][context_token] = 0
                    co_occurrence_matrix[token][context_token] += 1

    # Convert co-occurrence matrix to numpy array
    vocab_list = list(vocabulary)
    matrix_size = len(vocabulary)
    co_occurrence_array = np.zeros((matrix_size, matrix_size), dtype=np.int32)
    
    for i, token1 in enumerate(vocab_list):
        for j, token2 in enumerate(vocab_list):
            if token2 in co_occurrence_matrix[token1]:
                co_occurrence_array[i, j] = co_occurrence_matrix[token1][token2]

    return co_occurrence_array, vocab_list

