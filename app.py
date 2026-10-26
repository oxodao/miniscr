# SPDX-License-Identifier: GPL-3.0-only
# Copyright (C) 2026 Oxodao

import argparse

from config import Config
from destinations import get_destination
from utils import send_notification
from wm import get_current_wm


def main():
    parser = argparse.ArgumentParser(
        description="MiniScr screenshoting utility",
    )

    parser.add_argument(
        '-m', '--mode',
        choices=['region', 'window', 'monitor'],
        default='region',
        help='Screenshot mode (default: region)'
    )

    args = parser.parse_args()

    config = Config.load()
    wm = get_current_wm()

    region = None

    if args.mode == 'region':
        region = wm.wait_for_region()
    elif args.mode == 'window':
        region = wm.wait_for_window()
    elif args.mode == 'monitor':
        region = wm.wait_for_monitor()

    if not region:
        print("No region selected. Exiting.")

        return

    screenshot = wm.take_screenshot(region)
    if not screenshot:
        send_notification('Screenshot failure', 'Failed to take a screenshot, no data received')

        return

    from gui import Menu
    menu = Menu(config, wm)
    
    has_next_step = True
    while has_next_step:
        try:
            action = menu.run()
            if not action or action == 'cancel' or not screenshot:
                return

            dest = get_destination(
                app_config=config,
                wm=wm,
                action=action,
            )

            screenshot = dest.action(screenshot)
            has_next_step = isinstance(screenshot, bytes)
        except Exception as e:
            send_notification(
                title='Screenshot failure',
                description=f'Failed to screenshot: {e}'
            )

            return
