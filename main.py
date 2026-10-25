import argparse

from config import Config
from destinations import CopyToClipboardDestination
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

    # @TODO: Open the GUI

    # dest = SaveDestination(config, wm)
    dest = CopyToClipboardDestination(config, wm)
    # dest = get_upload_destination(config, wm, config.upload_destination[0])
    # dest = get_upload_destination(config, wm, config.upload_destination[1])
    dest.action(screenshot)

if __name__ == "__main__":
    main()
