# CrossViT
> [CrossViT: Cross-Attention Multi-Scale Vision Transformer for Image Classification](https://arxiv.org/abs/2103.14899)

## Requirements
| mindspore | ascend driver |  firmware   | cann toolkit/kernel |
| :-------: | :-----------: | :---------: | :-----------------: |
|   2.3.1   |   24.1.RC2    | 7.3.0.1.231 |    8.0.RC2.beta1    |

## Introduction

CrossViT is a type of vision transformer that uses a dual-branch architecture to extract multi-scale feature representations for image classification. The architecture combines image patches (i.e. tokens in a transformer) of different sizes to produce stronger visual features for image classification. It processes small and large patch tokens with two separate branches of different computational complexities and these tokens are fused together multiple times to complement each other.

Fusion is achieved by an efficient cross-attention module, in which each transformer branch creates a non-patch token as an agent to exchange information with the other branch by attention. This allows for linear-time generation of the attention map in fusion instead of quadratic time otherwise.[[1](#references)]

<p align="center">
  <img src="https://user-images.githubusercontent.com/52945530/223635248-5871596d-43f2-44ee-b8be-1e7927ade243.jpg" width=400 />
</p>
<p align="center">
  <em>Figure 1. Architecture of CrossViT [<a href="#references">1</a>] </em>
</p>


## Results

Our reproduced model performance on ImageNet-1K is reported as follows.

- ascend 910* with graph mode

<div align="center">



| model name | top-1 (%) | top-5 (%) | params (M) | batch size | cards | graph compile | ms/step | jit_level | recipe                                                                                            | download                                                                                                 |
| ---------- | --------- | --------- | ---------- | ---------- | ----- | ------------- | ------- | --------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| crossvit_9 | 73.38     | 91.51     | 8.55       | 256        | 8     | 3~5 mins      | 514.36  | O2        | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/crossvit/crossvit_9_ascend.yaml) | [weights](https://download-mindspore.osinfra.cn/toolkits/mindcv/crossvit/crossvit_9-32c69c96-910v2.ckpt) |

</div>

- ascend 910 with graph mode

<div align="center">



| model name | top-1 (%) | top-5 (%) | params (M) | batch size | cards | graph compile | ms/step | jit_level | recipe                                                                                            | download                                                                                   |
| ---------- | --------- | --------- | ---------- | ---------- | ----- | ------------- | ------- | --------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| crossvit_9 | 73.56     | 91.79     | 8.55       | 256        | 8     | 3~5 mins      | 550.79  | O2        | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/crossvit/crossvit_9_ascend.yaml) | [weights](https://download.mindspore.cn/toolkits/mindcv/crossvit/crossvit_9-e74c8e18.ckpt) |

</div>

#### Notes
- Top-1 and Top-5: Accuracy reported on the validation set of ImageNet-1K.

## Quick Start

### Preparation

#### Installation
Please refer to the [installation instruction](https://mindspore-lab.github.io/mindcv/installation/) in MindCV.

#### Dataset Preparation
Please download the [ImageNet-1K](https://www.image-net.org/challenges/LSVRC/2012/index.php) dataset for model training and validation.

### Training

* Distributed Training

It is easy to reproduce the reported results with the pre-defined training recipe. For distributed training on multiple Ascend 910 devices, please run

```shell
# distributed training on multiple NPU devices
msrun --bind_core=True --worker_num 8 python train.py --config configs/crossvit/crossvit_15_ascend.yaml --data_dir /path/to/imagenet
```


For detailed illustration of all hyper-parameters, please refer to [config.py](https://github.com/mindspore-lab/mindcv/blob/main/config.py).

**Note:**  As the global batch size  (batch_size x num_devices) is an important hyper-parameter, it is recommended to keep the global batch size unchanged for reproduction or adjust the learning rate linearly to a new global batch size.

* Standalone Training

If you want to train or finetune the model on a smaller dataset without distributed training, please run:

```shell
# standalone training on single NPU device
python train.py --config configs/crossvit/crossvit_15_ascend.yaml --data_dir /path/to/dataset --distribute False
```

### Validation

To validate the accuracy of the trained model, you can use `validate.py` and parse the checkpoint path with `--ckpt_path`.

```
python validate.py -c configs/crossvit/crossvit_15_ascend.yaml --data_dir /path/to/imagenet --ckpt_path /path/to/ckpt
```

## References

<!--- Guideline: Citation format should follow GB/T 7714. -->
[1] Chun-Fu Chen, Quanfu Fan, Rameswar Panda. CrossViT: Cross-Attention Multi-Scale Vision Transformer for Image Classification
