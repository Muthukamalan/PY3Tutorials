# DataSet and DataLoader from scratch

```mermid
classDiagram
    class Dataset{
        <<abstract>>
        +__len__()
        +__getitem__()
    }

    class ImageDataset{
        <<abstract>>
        +get_img()
        +get_label()
        +class_mapping()
    }

    class TorchTextDataset
    class TextFileDataset
    class TorchImageDataset
    class ImgLoadDataset

    Dataset <|-- TorchTextDataset
    Dataset <|-- TextFileDataset
    Dataset <|-- ImageDataset
    ImageDataset <|-- TorchImageDataset
    ImageDataset <|-- ImgLoadDataset
```
