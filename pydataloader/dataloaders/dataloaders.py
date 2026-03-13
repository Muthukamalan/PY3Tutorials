# dataloader/dataloader.py

from collections import namedtuple
import os
import random
import numpy as np 
from common.utils import timer

from pydataloader.datasetss import Datasets


class DataLoader:
    def __init__(self,dataset:Datasets, batch_size: int = 32,shuffle: bool = True,drop_last: bool = False):
        self.data = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.drop_last = drop_last

        self.indices = list(range(len(self.data)))
        self.cursor = 0

    def __len__(self):
        if self.drop_last:
            return len(self.data) // self.batch_size
        return (len(self.data) + self.batch_size - 1) // self.batch_size
    
    def __iter__(self):
        self.cursor = 0
        if self.shuffle:
            random.shuffle(self.indices)
        return self

    def __next__(self):
        if self.cursor >= len(self.indices): raise StopIteration
        batch_indices = self.indices[ self.cursor : self.cursor + self.batch_size ]
        if self.drop_last and len(batch_indices) < self.batch_size: raise StopIteration
        batch = [self.data[i] for i in batch_indices]
        self.cursor += self.batch_size
        return self._collate(batch)

    def _collate(self, batch):
        x = []
        y = []

        for img, lbl in batch:
            x.append(img)
            y.append(lbl)

        try: X = np.stack(x)
        except Exception: X = np.array(x)
        Y = np.array(y)
        return X, Y
