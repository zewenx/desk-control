import time, threading, subprocess
from datetime import datetime, timedelta

# device address
mac_address = ''


def is_working_time(wait_minutes):
    current_time = datetime.now()
    start_time = current_time.replace(hour=9, minute=30)
    end_time = current_time.replace(hour=22, minute=30)
    if start_time < current_time < end_time:
        print(f"Next adjust time: {(current_time + timedelta(minutes=wait_minutes)).isoformat()}")
        return True
    return False


def adjust_desk(args):
    try:
        import sys
        sys.argv = args
        from idasen_controller.main import init, config
        config['move_to'] = args[-1]
        init()
    except:
        pass


def up(stand_time, sit_time, stand_height, sit_height):
    adjust_desk(['idasen-controller', '--mac-address', mac_address, '--move-to', stand_height])
    if is_working_time(stand_time):
        time.sleep(stand_time * 60)
        down(stand_time, sit_time, stand_height, sit_height)


def down(stand_time, sit_time, stand_height, sit_height):
    adjust_desk(['idasen-controller', '--mac-address', mac_address, '--move-to', sit_height])
    if is_working_time(sit_time):
        time.sleep(sit_time * 60)
        up(stand_time, sit_time, stand_height, sit_height)


def start(stand_time, sit_time, stand_height, sit_height):
    while True:
        if is_working_time(0):
            try:
                down(stand_time, sit_time, stand_height, sit_height)
            except:
                pass
        time.sleep(600)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Setup stand and sit time')
    parser.add_argument('--stand-time', type=int, default=60, help='stand time in minutes, default 30 mins')
    parser.add_argument('--sit-time', type=int, default=30, help='sit time in minutes, default 30 mins')
    parser.add_argument('--stand-height', type=str, default='1200', help='stand height in mm, default as 1200mm')
    parser.add_argument('--sit-height', type=str, default='820', help='sit height in mm, default as 820mm')
    args = parser.parse_args()
    start(args.stand_time, args.sit_time, args.stand_height, args.sit_height)
