# CMT: Convolutional Neural Networks Meet Vision Transformers

> [CMT: Convolutional Neural Networks Meet Vision Transformers](https://arxiv.org/abs/2107.06263)

## Requirements
| mindspore | ascend driver |  firmware   | cann toolkit/kernel |
| :-------: | :-----------: | :---------: | :-----------------: |
|   2.3.1   |   24.1.RC2    | 7.3.0.1.231 |    8.0.RC2.beta1    |

## Introduction

CMT is a method to make full use of the advantages of CNN and transformers so that the model could capture long-range
dependencies and extract local information. In addition, to reduce computation cost, this method use lightweight MHSA(multi-head self-attention)
and depthwise convolution and pointwise convolution like MobileNet. By combing these parts, CMT could get a SOTA performance
on ImageNet-1K dataset.


## Results

Our reproduced model performance on ImageNet-1K is reported as follows.

- ascend 910* with graph mode

*coming soon*

- ascend 910 with graph mode

<div align="center">



| model name | top-1 (%) | top-5 (%) | params(M) | batch size | cards | graph compile | ms/step | jit_level | recipe                                                                                      | download                                                                             |
| ---------- | --------- | --------- | --------- | ---------- | ----- |---------------| ------- | --------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| cmt_small  | 83.24     | 96.41     | 26.09     | 128        | 8     | 5~7 mins      | 500.64  | O2        | [yaml](https://github.com/mindspore-lab/mindcv/blob/main/configs/cmt/cmt_small_ascend.yaml) | [weights](https://download.mindspore.cn/toolkits/mindcv/cmt/cmt_small-6858ee22.ckpt) |


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
msrun --bind_core=True --worker_num 8 python train.py --config configs/cmt/cmt_small_ascend.yaml --data_dir /path/to/imagenet
```


For detailed illustration of all hyper-parameters, please refer to [config.py](https://github.com/mindspore-lab/mindcv/blob/main/config.py).

**Note:**  As the global batch size  (batch_size x num_devices) is an important hyper-parameter, it is recommended to keep the global batch size unchanged for reproduction or adjust the learning rate linearly to a new global batch size.

* Standalone Training

If you want to train or finetune the model on a smaller dataset without distributed training, please run:

```shell
# standalone training on single NPU device
python train.py --config configs/cmt/cmt_small_ascend.yaml --data_dir /path/to/dataset --distribute False
```

### Validation

To validate the accuracy of the trained model, you can use `validate.py` and parse the checkpoint path with `--ckpt_path`.

```
python validate.py -c configs/cmt/cmt_small_ascend.yaml --data_dir /path/to/imagenet --ckpt_path /path/to/ckpt
```

## References

<!--- Guideline: Citation format should follow GB/T 7714. -->
[1] Guo J, Han K, Wu H, et al. Cmt: Convolutional neural networks meet vision transformers[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2022: 12175-12185.
