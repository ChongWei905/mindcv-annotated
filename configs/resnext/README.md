# ResNeXt

> [Aggregated Residual Transformations for Deep Neural Networks](https://arxiv.org/abs/1611.05431)

## Requirements
| mindspore | ascend driver |  firmware   | cann toolkit/kernel |
| :-------: | :-----------: | :---------: | :-----------------: |
|   2.3.1   |   24.1.RC2    | 7.3.0.1.231 |    8.0.RC2.beta1    |

## Introduction

The authors present a simple, highly modularized network architecture for image classification. The network is
constructed by repeating a building block that aggregates a set of transformations with the same topology. The simple
design results in a homogeneous, multi-branch architecture that has only a few hyper-parameters to set. This strategy
exposes a new dimension, which the authors call "cardinality" (the size of the set of transformations), as an essential
factor in addition to the dimensions of depth and width. On the ImageNet-1K dataset, the authors empirically show that
even under the restricted condition of maintaining complexity, increasing cardinality is able to improve classification
accuracy.[[1](#references)]

<p align="center">
  <img src="https://user-images.githubusercontent.com/53842165/223680439-ffd1747e-a423-4d6a-a680-f071e55fdfa4.png" width=700 />
</p>
<p align="center">
  <em>Figure 1. Architecture of ResNeXt [<a href="#references">1</a>] </em>
</p>

## Results

Our reproduced model performance on ImageNet-1K is reported as follows.

- ascend 910* with graph mode

<div align="center">



|   model name    | top-1 (%) | top-5 (%) | params (M) | batch size | cards | graph compile | ms/step | jit_level | recipe                                                                                                | download                                                                                                     |
| :-------------: | :-------: | :-------: | :--------: | ---------- | ----- | ------------- | ------- | --------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| resnext50_32x4d |   78.64   |   94.18   |   25.10    | 32         | 8     | 1~3 mins      | 44.61   | O2        | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/resnext/resnext50_32x4d_ascend.yaml) | [weights](https://download-mindspore.osinfra.cn/toolkits/mindcv/resnext/resnext50_32x4d-988f75bc-910v2.ckpt) |

</div>

- ascend 910 with graph mode

<div align="center">



|   model name    | top-1 (%) | top-5 (%) | params (M) | batch size | cards | graph compile | ms/step | jit_level | recipe                                                                                                | download                                                                                       |
| :-------------: | :-------: | :-------: | :--------: | ---------- | ----- | ------------- | ------- | --------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| resnext50_32x4d |   78.53   |   94.10   |   25.10    | 32         | 8     | 1~3 mins      | 37.22   | O2        | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/resnext/resnext50_32x4d_ascend.yaml) | [weights](https://download.mindspore.cn/toolkits/mindcv/resnext/resnext50_32x4d-af8aba16.ckpt) |

</div>

#### Notes

- Top-1 and Top-5: Accuracy reported on the validation set of ImageNet-1K.

## Quick Start

### Preparation

#### Installation

Please refer to the [installation instruction](https://mindspore-lab.github.io/mindcv/installation/) in MindCV.

#### Dataset Preparation

Please download the [ImageNet-1K](https://www.image-net.org/challenges/LSVRC/2012/index.php) dataset for model training
and validation.

### Training

* Distributed Training

It is easy to reproduce the reported results with the pre-defined training recipe. For distributed training on multiple
Ascend 910 devices, please run

```shell
# distributed training on multiple NPU devices
msrun --bind_core=True --worker_num 8 python train.py --config configs/resnext/resnext50_32x4d_ascend.yaml --data_dir /path/to/imagenet
```




For detailed illustration of all hyper-parameters, please refer
to [config.py](https://github.com/mindspore-lab/mindcv/blob/main/config.py).

**Note:**  As the global batch size  (batch_size x num_devices) is an important hyper-parameter, it is recommended to
keep the global batch size unchanged for reproduction or adjust the learning rate linearly to a new global batch size.

* Standalone Training

If you want to train or finetune the model on a smaller dataset without distributed training, please run:

```shell
# standalone training on single NPU device
python train.py --config configs/resnext/resnext50_32x4d_ascend.yaml --data_dir /path/to/dataset --distribute False
```

### Validation

To validate the accuracy of the trained model, you can use `validate.py` and parse the checkpoint path
with `--ckpt_path`.

```shell
python validate.py -c configs/resnext/resnext50_32x4d_ascend.yaml --data_dir /path/to/imagenet --ckpt_path /path/to/ckpt
```


## References

[1] Xie S, Girshick R, Dollár P, et al. Aggregated residual transformations for deep neural networks[C]//Proceedings of
the IEEE conference on computer vision and pattern recognition. 2017: 1492-1500.
