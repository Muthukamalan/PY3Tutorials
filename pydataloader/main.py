import os 

from pydataloader.datasetss import Datasets,ImgLoadDataset,TextFileDataset,TextTorchDataset,TorchDataset
from pydataloader.dataloaders import DataLoader 

index = 24
fpath = os.path.join(os.getenv("HOME"),'DATA',"austen-emma.txt")


# --------------------------------------------------------------

txt_data:Datasets = TextFileDataset( file_path=fpath, context_size=8)

print(f"{txt_data=}")
print(f"inde:{index} of text dataset: {txt_data[index]}")
print(f"length of dataset: {len(txt_data)}")

img_data:Datasets = TorchDataset('ylecun/mnist','train')
print(f"{img_data=}")
print(f"inde:{index} of text dataset: {img_data[index]}")
print(f"length of dataset: {len(img_data)}")


# --------------------------------------------------------------

txt_dl = DataLoader(txt_data,16,drop_last=True,shuffle=True)

for txt_batch in txt_dl:
    pass 

print(len(txt_batch),type(txt_batch))
print(txt_batch[0].shape,txt_batch[1].shape)


img_dl = DataLoader(img_data,batch_size=32,shuffle=True,drop_last=False)
for img_batch in txt_dl:
    pass 

print(len(img_batch),type(img_batch))
print(img_batch[0].shape,img_batch[1].shape)