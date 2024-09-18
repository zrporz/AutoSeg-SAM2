# README
This is an automatic full segmentation  tool based on [Segment-Anything-2](https://github.com/facebookresearch/segment-anything-2) and [Segment-Anything-1](https://github.com/zrporz/segment-anything-1). Our tool performs automatic full segmentation of the video, enabling the tracking of each object and the detection of possible new objects.


## Demo

https://github.com/user-attachments/assets/12fc2c3f-b915-4f58-a492-fc74bbc31e52


https://github.com/user-attachments/assets/f080aab6-12a6-461b-8618-cc25bcf67a9b


https://github.com/user-attachments/assets/ef45b7ee-4d89-4096-87d7-24c273f9dc6e


## Environment Setup

We use SAM1 to provide static segmentation results and use the SAM2 to track the static segmentation results. Please follow their instruction to install according package
[SAM1](https://github.com/zrporz/segment-anything-1) and [SAM2](https://github.com/facebookresearch/segment-anything-2)


The code requires `python>=3.10`, as well as `torch>=2.3.1` and `torchvision>=0.18.1`
```bash
###
pip install -e submodule/segment-anything-1.
pip install -e submoudle/segment-anything-2

cd checkpoints/sam1
bash download.sh
cd ../sam2
bash download.sh
```
