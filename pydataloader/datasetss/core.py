from abc import ABC, abstractmethod


class Datasets(ABC):
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass


class ImageDataset(Datasets):
    @abstractmethod
    def get_img(self, idx):
        pass

    @abstractmethod
    def get_label(self, idx):
        pass

    @abstractmethod
    def class_mapping(self) -> dict:
        pass

    def __getitem__(self, index):
        image = self.get_img(index)
        label = self.get_label(index)
        return image, label
