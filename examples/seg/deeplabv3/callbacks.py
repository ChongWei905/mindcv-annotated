import logging
import os
import stat

from postprocess import apply_eval

# from mindspore import log as logger
from mindspore import save_checkpoint
from mindspore.train.callback import Callback, CheckpointConfig, LossMonitor, ModelCheckpoint, TimeMonitor

_logger = logging.getLogger(__name__)


class EvalCallBack(Callback):
    """
    Evaluation callback when training.
    Args:
        eval_function (function): evaluation function.
        eval_param_dict (dict): evaluation parameters' configure dict.
        interval (int): run evaluation interval, default is 1.
        eval_start_epoch (int): evaluation start epoch, default is 1.
        save_best_ckpt (bool): Whether to save best checkpoint, default is True.
        best_ckpt_name (str): best checkpoint name, default is `best.ckpt`.
        metrics_name (str): evaluation metrics name, default is `mIoU`.
    Returns:
        None
    Examples:
        >>> EvalCallBack(eval_function, eval_param_dict)
    """

    def __init__(
        self,
        eval_function,
        eval_param_dict,
        interval=1,
        eval_start_epoch=1,
        save_best_ckpt=True,
        ckpt_directory="./",
        best_ckpt_name="best.ckpt",
        metrics_name="mIoU",
    ) -> None:
        super(EvalCallBack, self).__init__()
        self.eval_function = eval_function
        self.eval_param_dict = eval_param_dict
        self.eval_start_epoch = eval_start_epoch

        if interval < 1:
            raise ValueError("interval should >= 1.")

        self.interval = interval
        self.save_best_ckpt = save_best_ckpt
        self.best_res = 0
        self.best_epoch = 0

        if not os.path.isdir(ckpt_directory):
            os.makedirs(ckpt_directory)

        self.best_ckpt_path = os.path.join(ckpt_directory, best_ckpt_name)
        self.metrics_name = metrics_name

    def remove_ckpoint_file(self, file_name):
        """Remove the specified checkpoint file from this checkpoint manager and also from the directory."""
        try:
            os.chmod(file_name, stat.S_IWRITE)
            os.remove(file_name)
        except OSError:
            _logger.warning("OSError, failed to remove the older ckpt file %s.", file_name)
        except ValueError:
            _logger.warning("ValueError, failed to remove the older ckpt file %s.", file_name)

    def on_train_epoch_end(self, run_context):
        """Callback when epoch end."""
        cb_params = run_context.original_args()
        cur_epoch = cb_params.cur_epoch_num

        if cur_epoch >= self.eval_start_epoch and (cur_epoch - self.eval_start_epoch) % self.interval == 0:
            res = self.eval_function(self.eval_param_dict)
            _logger.info("epoch: {}, {}: {}".format(cur_epoch, self.metrics_name, res), flush=True)

            if res >= self.best_res:
                self.best_res = res
                self.best_epoch = cur_epoch
                _logger.info("update best result: {}".format(res), flush=True)

                if self.save_best_ckpt:
                    if os.path.exists(self.best_ckpt_path):
                        self.remove_ckpoint_file(self.best_ckpt_path)

                    save_checkpoint(cb_params.train_network, self.best_ckpt_path)
                    _logger.info("update best checkpoint at: {}".format(self.best_ckpt_path), flush=True)

    def on_train_end(self, run_context):
        _logger.info(
            "End training, the best {0} is: {1}, the best {0} epoch is {2}".format(
                self.metrics_name, self.best_res, self.best_epoch
            ),
            flush=True,
        )


def get_segment_train_callback(args, steps_per_epoch, rank_id):
    callbacks = [TimeMonitor(data_size=steps_per_epoch), LossMonitor()]
    if rank_id == 0 or rank_id is None:
        ckpt_config = CheckpointConfig(
            save_checkpoint_steps=args.save_steps,
            keep_checkpoint_max=args.keep_checkpoint_max,
        )
        prefix_name = str(args.model) + "_s" + str(args.output_stride) + "_" + args.backbone
        ckpt_cb = ModelCheckpoint(prefix=prefix_name, directory=args.ckpt_save_dir, config=ckpt_config)
        callbacks.append(ckpt_cb)
    return callbacks


def get_segment_eval_callback(eval_model, eval_dataset, args):
    eval_param_dict = {"net": eval_model, "dataset": eval_dataset, "args": args}

    eval_cb = EvalCallBack(
        eval_function=apply_eval,
        eval_param_dict=eval_param_dict,
        interval=args.eval_interval,
        eval_start_epoch=args.eval_start_epoch,
        save_best_ckpt=True,
        ckpt_directory=args.ckpt_save_dir,
        best_ckpt_name="best.ckpt",
        metrics_name="mIoU",
    )

    return eval_cb
