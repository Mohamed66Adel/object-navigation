#!/usr/bin/env python3

import argparse
from gym_minigrid.wrappers import *
from mini_behavior.window import Window
from mini_behavior.utils.save import get_step, save_demo

import mini_behavior.envs
import numpy as np
from object_nav.envs.igridson.igridson_env import *

# Size in pixels of a tile in the full-scale human view
TILE_PIXELS = 32
show_furniture = False


def redraw(img):
    if not args.agent_view:
        img = env.render('rgb_array', tile_size=args.tile_size)

    window.no_closeup()
    window.set_inventory(env)
    window.show_img(img)


def show_states():
    imgs = env.render_states()
    window.show_closeup(imgs)


def reset():
    if args.seed != -1:
        env.seed(args.seed)

    obs = env.reset()

    if hasattr(env, 'mission'):
        print('Mission: %s' % env.mission)
        window.set_caption(env.mission)

    redraw(obs)


def load():
    if args.seed != -1:
        env.seed(args.seed)

    env.reset()
    obs = env.load_state(args.load)

    if hasattr(env, 'mission'):
        print('Mission: %s' % env.mission)
        window.set_caption(env.mission)

    redraw(obs)


def step(action):
    prev_obs = env.gen_obs()
    obs, reward, done, info = env.step(action)

    print('step=%s, reward=%.2f' % (env.step_count, reward))

    if args.save:
        all_steps[env.step_count] = (prev_obs, action)

    if done:
        print('done!')
        if args.save:
            save_demo(all_steps, args.env, env.episode)
        reset()
    else:
        redraw(obs)


# def switch_dim(dim):
#     env.switch_dim(dim)
#     print(f'switching to dim: {env.render_dim}')
#     obs = env.gen_obs()
#     redraw(obs)


def key_handler_primitive(event):
    print('pressed', event.key)
    if event.key == 'backspace':
        reset()
        return
    if event.key == 'escape':
        window.close()
        return
    if event.key == 'left':
        step(env.actions.left)
        return
    if event.key == 'right':
        step(env.actions.right)
        return
    if event.key == 'up':
        step(env.actions.forward)
        return
    if event.key == '0':
        step(env.actions.pickup_0)
        return
    if event.key == '1':
        step(env.actions.pickup_1)
        return
    if event.key == '2':
        step(env.actions.pickup_2)
        return
    if event.key == '3':
        step(env.actions.drop_0)
        return
    if event.key == '4':
        step(env.actions.drop_1)
        return
    if event.key == '5':
        step(env.actions.drop_2)
        return
    if event.key == 't':
        step(env.actions.toggle)
        return
    if event.key == 'o':
        step(env.actions.open)
        return
    if event.key == 'c':
        step(env.actions.close)
        return
    if event.key == 'k':
        step(env.actions.cook)
        return
    if event.key == 's':
        step(env.actions.slice)
        return
    if event.key == 'i':
        step(env.actions.drop_in)
        return
    if event.key == 'pagedown':
        show_states()
        return


parser = argparse.ArgumentParser()
parser.add_argument(
    "--env",
    help="gym environment to load",
    default='MiniGrid-igridson-16x16-N2-v0'
)
parser.add_argument(
    "--seed",
    type=int,
    help="random seed to generate the environment with",
    default=-1
)
parser.add_argument(
    "--tile_size",
    type=int,
    help="size at which to render tiles",
    default=32
)
parser.add_argument(
    '--agent_view',
    default=False,
    help="draw the agent sees (partially observable view)",
    action='store_true'
)
# NEW
parser.add_argument(
    "--save",
    default=False,
    help="whether or not to save the demo_16"
)
# NEW
parser.add_argument(
    "--load",
    default=None,
    help="path to load state from"
)

args = parser.parse_args()

env = gym.make(args.env)

if args.save:
    # We do not support save for cartesian action space
    assert env.mode == "primitive"

all_steps = {}

if args.agent_view:
    env = RGBImgPartialObsWrapper(env)
    env = ImgObsWrapper(env)

window = Window('mini_behavior - ' + args.env)
window.reg_key_handler(key_handler_primitive)

if args.load is None:
    reset()
else:
    load()

# Blocking event loop
window.show(block=True)
