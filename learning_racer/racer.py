import argparse
from learning_racer.commands.subcommand import command_train
from learning_racer.config import ConfigReader

from logging import getLogger

logger = getLogger(__name__)

__version__ = '1.6.0'

parser = argparse.ArgumentParser(description='Learning Racer command.')
parser.add_argument('--version', action='version', version='learning_racer version {} .'.format(__version__))
subparser = parser.add_subparsers()

# train subcommand.
parser_train = subparser.add_parser('train', help='see `train -h`')
parser_train.add_argument('-config', '--config-path', help='Path to a config.yml path.',
                          default='config.yml', type=str)
parser_train.add_argument('-vae', '--vae-path', help='Path to a trained vae model path.',
                          default='vae.torch', type=str)
parser_train.add_argument('-device', '--device', help='torch device {"cpu" | "cuda"}',
                          default='cuda', type=str)
parser_train.add_argument('-robot', '--robot-driver', help='choose robot driver from {"rest"}',
                          default='rest', type=str)
parser_train.add_argument('-steps', '--time-steps', help='total step.',
                          default='5000', type=int)
parser_train.add_argument('-save_freq', '--save-freq-steps', help='number of step for each checkpoints.',
                          default='300', type=int)
parser_train.add_argument('-save_path', '--save-model-path', help='Model save path.',
                          default='model_log', type=str)
parser_train.add_argument('-s', '--save', help='save model file name.',
                          default='model', type=str)
parser_train.add_argument('-l', '--load-model', help='Define pre-train model path.',
                          default='', type=str)
parser_train.add_argument('-log', '--tb-log', help='Define logging directory name, If not set, Do not logging.',
                          default=None, type=str)
parser_train.set_defaults(handler=command_train)


def racer_func():
    config = ConfigReader()
    args = parser.parse_args()
    try:
        config.load(args.config_path)
    except AttributeError:
        logger.error("Choose subcommand from [train].")
        exit(-1)

    if hasattr(args, 'handler'):
        args.handler(args, config)
    else:
        parser.print_help()

if __name__ == '__main__':
    racer_func()
