import os 
from pathlib import Path
from rich import print

import text_toolkit as tt 

fpath = Path(
            os.path.join(
                os.getenv("HOME"),
                "DATA",
                "austen-emma.txt"
            )
        )

print(tt.word_frequency(fpath))
co_occurrence_matrix, vocabulary = tt.create_co_occurrence_matrix(fpath, window_size=1)

print("Vocabulary:", len(vocabulary))
print("Co-occurrence matrix shape:",co_occurrence_matrix.shape)
print(co_occurrence_matrix)
