import os
from pathlib import Path
from typing import Literal

from datasets import load_dataset
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngImageFile
from pydataloader.datasetss.core import Datasets,ImageDataset

class TorchDataset(ImageDataset):
    def __init__(
        self,
        name: Literal["ylecun/mnist", "uoft-cs/cifar10"],
        split: Literal["train", "test"],
    ):
        self.name = name
        self.data = self._load_data(split)

    def class_mapping(self):
        return {k: v for k, v in enumerate(self.data.features["label"].names)}

    def _load_data(self, split):
        datapath = os.path.join(os.getenv("HOME"), "DATA")
        os.makedirs(datapath, exist_ok=True)
        return load_dataset(self.name, cache_dir=datapath, split=split)

    def get_img(self, idx):
        if self.name == "ylecun/mnist":
            img = self.data[idx].get("image")
        elif self.name == "uoft-cs/cifar10":
            img = self.data[idx].get("img")
        if isinstance(img, PngImageFile):
            img = np.array(img)
        return img

    def get_label(self, idx):
        return self.data[idx].get("label")

    def __getitem__(self, index):
        img = self.get_img(index)
        lbl = self.get_label(index)
        return (img, lbl)

    def __len__(self):
        return self.data.num_rows - 1


class ImgLoadDataset(ImageDataset):
    def __init__(self, img_dir: Path):
        """
        Docstring for __init__

        :param self: Description
        :param img_dir: Path to Train/Test Dir
        :type img_dir: Path


        ```
        dataset/
        ├── class1/
        │    ├── img1.jpg
        │    └── img2.jpg
        └── class2/
            ├── img3.jpg
            └── img4.jpg
        ```
        """
        super().__init__()

        img_dir = Path(img_dir)
        assert img_dir.exists(), "Path does not exist"

        self.root = img_dir

        self.classes = sorted([p.name for p in img_dir.iterdir() if p.is_dir()])
        self.class_to_idx = {c: i for i, c in enumerate(self.classes)}

        self.samples = []

        for cls in self.classes:
            class_dir = img_dir / cls

            for img_path in class_dir.glob("*"):
                if img_path.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                    self.samples.append((img_path, self.class_to_idx[cls]))

    def __len__(self):
        return len(self.samples)

    def get_img(self, idx):
        img_path, _ = self.samples[idx]
        return Image.open(img_path)

    def get_label(self, idx):
        _, label = self.samples[idx]
        return label

    def __getitem__(self, index):
        img = np.array(self.get_img(index)).sum(axis=2)
        lbl = self.get_label(index)
        return (img, lbl)

    def class_mapping(self):
        return self.class_to_idx
