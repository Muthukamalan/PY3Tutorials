import os
from pathlib import Path
from typing import Literal

from datasets import load_dataset
from common.utils import CounterStats
from pydataloader.datasetss.core import Datasets


class TextFileDataset(Datasets):
    def __init__(self, file_path, context_size=8):

        file_path = Path(file_path)
        assert file_path.exists() and str(file_path).endswith(".txt"), (
            "file not found or Not txt file"
        )

        self.filepath = file_path
        self.context_size = context_size

        self.samples = self._load(self.filepath)

    def _load(self, fname) -> list[tuple[str, str]]:
        sample = []
        with CounterStats() as stats, open(fname, "r") as file:
            for line in file:
                stats.lines += 1

                tokens = line.strip().split()
                line_length_tokens = len(tokens)

                if line_length_tokens <= self.context_size:
                    continue

                for i in range(line_length_tokens - self.context_size):
                    x = tokens[i : i + self.context_size]
                    y = tokens[i : i + self.context_size + 1]

                    sample.append((x, y))

                    stats.num_samples += 1
        return sample

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        return self.samples[index]


class TextTorchDataset(Datasets):
    def __init__(
        self,
        name: Literal[
            "karpathy/tinystories-gpt4-clean",
            "lsb/simplewiki2023",
            "rahular/simple-wikipedia",
        ],
        context_window=8,
    ):
        super().__init__()
        self.name = name

        # text data have only train
        self.data = self._load_data()
        self.context_window = context_window

    def _load_data(self):
        data_path = os.path.join(os.getenv("HOME"), "DATA")
        os.makedirs(data_path, exist_ok=True)
        return load_dataset(self.name, cache_dir=data_path).get("train")

    def _build_context(self, sentence: str, context_size: int, unk_token="UNK"):
        tokens = str(sentence).strip().split()

        # build x (context_size)
        x = tokens[:context_size]

        if len(x) < context_size:
            x += [unk_token] * (context_size - len(x))

        # build y (context_size + 1)
        y = tokens[: context_size + 1]

        if len(y) < context_size + 1:
            y += [unk_token] * ((context_size + 1) - len(y))

        return x, y

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        txt = self.data[index].get("text")
        return self._build_context(txt, self.context_window)
