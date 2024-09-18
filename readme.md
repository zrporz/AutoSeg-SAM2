# README
This is an automatic full segmentation  tool based on [Segment-Anything-2](https://github.com/facebookresearch/segment-anything-2) and [Segment-Anything-1](https://github.com/zrporz/segment-anything-1). Our tool performs automatic full segmentation of the video, enabling the tracking of each object and the detection of possible new objects.


## Demo
https://github.com/user-attachments/assets/cfc71c45-7d12-410a-8668-f290c260511e


https://github.com/user-attachments/assets/cb942b7a-1960-41e7-8143-71d37fab89b1

https://github.com/user-attachments/assets/1135813a-6d21-4dde-ab37-46bde32bd971


Our method detects segmentations in the scene every certain number of frames, so it can identify potential new objects in the scene

https://github.com/user-attachments/assets/0b3039a9-b546-40a7-8051-f7b28099b477

https://github.com/user-attachments/assets/1ca3d6cc-2ece-473b-85ef-b412260af383

https://github.com/user-attachments/assets/ee21f192-4749-4084-926c-9574e0676336

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
