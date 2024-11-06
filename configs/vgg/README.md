# VGGNet

<!--- Guideline: please use url linked to the paper abstract in ArXiv instead of PDF for fast loading.  -->
> [Very Deep Convolutional Networks for Large-Scale Image Recognition](https://arxiv.org/abs/1409.1556)

## Requirements
| mindspore | ascend driver |  firmware   | cann toolkit/kernel |
| :-------: | :-----------: | :---------: | :-----------------: |
|   2.3.1   |   24.1.RC2    | 7.3.0.1.231 |    8.0.RC2.beta1    |

## Introduction

<!--- Guideline: Introduce the model and architectures. Please cite if you use/adopt paper explanation from others. -->
<!--- Guideline: If an architecture table/figure is available in the paper, please put one here and cite for intuitive illustration. -->

Figure 1 shows the model architecture of VGGNet. VGGNet is a key milestone on image classification task. It expands the
model to 16-19 layers for the first time. The key motivation of this model is
that it shows usage of 3x3 kernels is efficient and by adding 3x3 kernels, it could have the same effect as 5x5 or 7x7
kernels. VGGNet could achieve better model performance compared with previous
methods such as GoogleLeNet and AlexNet on ImageNet-1K dataset.[[1](#references)]

<p align="center">
  <img src="https://user-images.githubusercontent.com/77485245/223675336-ca8b0411-86fd-4134-9b37-e601ff82f64b.jpeg" width=800 />
</p>
<p align="center">
  <em>Figure 1. Architecture of VGG [<a href="#references">1</a>] </em>
</p>

## Results

<!--- Guideline:
Table Format:
- Model: model name in lower case with _ seperator.
- Top-1 and Top-5: Keep 2 digits after the decimal point.
- Params (M): # of model parameters in millions (10^6). Keep 2 digits after the decimal point
- Recipe: Training recipe/configuration linked to a yaml config file. Use absolute url path.
- Download: url of the pretrained model weights. Use absolute url path.
-->

Our reproduced model performance on ImageNet-1K is reported as follows.

- ascend 910* with graph mode

<div align="center">



| model | top-1 (%) | top-5 (%) | params (M) | batch size | cards | graph compile | ms/step | jit_level | recipe                                                                                  | download                                                                                       |
| :---: | :-------: | :-------: | :--------: | ---------- | ----- | ------------- | ------- | --------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| vgg13 |   72.81   |   91.02   |   133.04   | 32         | 8     | 1~2 mins      | 30.52   | O2        | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/vgg/vgg13_ascend.yaml) | [weights](https://download-mindspore.osinfra.cn/toolkits/mindcv/vgg/vgg13-7756f33c-910v2.ckpt) |
| vgg19 |   75.24   |   92.55   |   143.66   | 32         | 8     | 1~2 mins      | 39.17   | O2        | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/vgg/vgg19_ascend.yaml) | [weights](https://download-mindspore.osinfra.cn/toolkits/mindcv/vgg/vgg19-5104d1ea-910v2.ckpt) |

</div>

- ascend 910 with graph mode

<div align="center">



| model | top-1 (%) | top-5 (%) | params (M) | batch size | cards | graph compile | ms/step | jit_level | recipe                                                                                  | download                                                                         |
| :---: | :-------: | :-------: | :--------: | ---------- | ----- | ------------- | ------- | --------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| vgg13 |   72.87   |   91.02   |   133.04   | 32         | 8     | 1~2 mins      | 55.20   | O2        | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/vgg/vgg13_ascend.yaml) | [weights](https://download.mindspore.cn/toolkits/mindcv/vgg/vgg13-da805e6e.ckpt) |
| vgg19 |   75.21   |   92.56   |   143.66   | 32         | 8     | 1~2 mins      | 67.42   | O2        | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/vgg/vgg19_ascend.yaml) | [weights](https://download.mindspore.cn/toolkits/mindcv/vgg/vgg19-bedee7b6.ckpt) |

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

<!--- Guideline: Please avoid using shell scripts in the command line. Python scripts preferred. -->

* Distributed Training

It is easy to reproduce the reported results with the pre-defined training recipe. For distributed training on multiple
Ascend 910 devices, please run

```shell
# distrubted training on multiple GPU/Ascend devices
msrun --bind_core=True --worker_num 8 python train.py --config configs/vgg/vgg16_ascend.yaml --data_dir /path/to/imagenet
```


For detailed illustration of all hyper-parameters, please refer
to [config.py](https://github.com/mindspore-lab/mindcv/blob/main/config.py).

**Note:**  As the global batch size  (batch_size x num_devices) is an important hyper-parameter, it is recommended to
keep the global batch size unchanged for reproduction or adjust the learning rate linearly to a new global batch size.

* Standalone Training

If you want to train or finetune the model on a smaller dataset without distributed training, please run:

```shell
# standalone training on single NPU device
python train.py --config configs/vgg/vgg16_ascend.yaml --data_dir /path/to/dataset --distribute False
```

### Validation

To validate the accuracy of the trained model, you can use `validate.py` and parse the checkpoint path
with `--ckpt_path`.

```
python validate.py -c configs/vgg/vgg16_ascend.yaml --data_dir /path/to/imagenet --ckpt_path /path/to/ckpt
```


## References

<!--- Guideline: Citation format GB/T 7714 is suggested. -->

[1] Simonyan K, Zisserman A. Very deep convolutional networks for large-scale image recognition[J]. arXiv preprint
arXiv:1409.1556, 2014.
