import torch

from stable_baselines3 import SAC

from learning_racer.agent import ControlCallback
from learning_racer.agent.agent import Agent
from learning_racer.exce.LearningRacerError import OptionsValueError
from learning_racer.robot import RestEnv
from learning_racer.sac import reward, CustomSAC
from learning_racer.teleoperate import Teleoperator
from learning_racer.vae.vae import VAE
from logging import getLogger

logger = getLogger(__name__)

robot_drivers = {'rest': RestEnv}

def _load_vae(model_path, variants_size, image_channels, device):
    vae = VAE(image_channels=image_channels, z_dim=variants_size)
    try:
        vae.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
    except FileNotFoundError:
        logger.error("Specify VAE model path can not find. Please specify correct vae path using -vae option.")
        raise OptionsValueError(
            "Specify VAE model path can not find. Please specify correct vae path using -vae option.")
    vae.to(torch.device(device)).eval()
    return vae

def _init_agent(args, config, train=True):
    torch_device = args.device
    vae = _load_vae(args.vae_path, config.sac_variants_size(), config.sac_image_channel(), torch_device)
    print(args.robot_driver)
    agent = None
    callback = None
    if args.robot_driver in ['rest']:
        teleop = Teleoperator()
        teleop.start_process()
        env = robot_drivers[args.robot_driver]()
        agent = Agent(env, vae, teleop=teleop, device=torch_device, reward_callback=reward, config=config, train=train)
        callback = ControlCallback(teleop)
    else:
        logger.error("{} is no supported robot name.".format(args.robot_driver))
        exit(-1)
    return agent, callback

def command_train(args, config):
    agent, callback = _init_agent(args, config)
    model = CustomSAC(agent, args, config)
    model.lean(callback=callback)
    model.save(args.save)
