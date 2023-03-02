import time
import platform
import subprocess
import os
from datetime import datetime

import click
from tqdm import tqdm
from colorama import Fore, Style

WORK_MESSAGE = "Back to work!"
REST_MESSAGE = "Take a break!"
SECONDS_IN_WEEK = 7 * 24 * 60 * 60


def get_notify_command(message):
    """Returns the appropriate notification command based on the platform"""
    if platform.system() == 'Darwin':  # macOS
        return f'osascript -e \'display notification "{message}" with title "Pomodoro Timer"\''

    if platform.system() == 'Linux':  # Linux
        return f'notify-send "Pomodoro Timer" "{message}"'

    # Windows
    return ''


def check_capabilities():
    """Determines if sound and notification are supported on the platform"""
    can_play_sound = False
    can_notify = False
    if platform.system() == 'Darwin':  # macOS
        can_play_sound = True
        can_notify = True
    elif platform.system() == 'Linux':  # Linux
        try:
            subprocess.call(['aplay', '--version'])
            can_play_sound = True
        except:
            pass

        try:
            subprocess.call(['notify-send', '--version'])
            can_notify = True
        except:
            pass

    else:  # Windows
        try:
            import winsound
            can_play_sound = True
        except ImportError:
            pass

    return can_play_sound, can_notify


def play_sound():
    """Plays a sound to indicate the end of a work session"""
    if platform.system() == 'Darwin':
        os.system('afplay /System/Library/Sounds/Ping.aiff')
    elif platform.system() == 'Linux':
        os.system('aplay /usr/share/sounds/speech-dispatcher/test.wav')
    else:  # Windows
        # winsound.PlaySound("*", winsound.SND_ALIAS)
        pass


def display_metrics(start_time, stop_time):
    pass


def get_epoch_time(date_str, delta):
    if not date_str:
        return time.time() - delta

    try:
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        return int(date_obj.timestamp())
    except ValueError:
        raise


def save_session(session_type, session_start_time, session_stop_time):
    pass


@click.command()
@click.option('--work', '-w', default=25, type=int, help='Work time in minutes (default: 25)')
@click.option('--rest', '-r', default=5, type=int, help='Break time in minutes (default: 5)')
@click.option('--notify', '-n', is_flag=True, help='Enable desktop notifications (default: False)')
@click.option('--metrics', '-m', is_flag=True, help='Show pomodoro metrics')
@click.option('--start', '-s', help='Date to fetch the metrics from in DD-MM-YYYY format')
@click.option('--end', '-e', help='Date to fetch the metrics to in DD-MM-YYYY format')
def main(work, rest, notify, metrics, start, stop):
    if metrics:
        if (start is None) ^ (stop is None):
            click.echo("ERROR: Both --stop and --start must be specified")
            return

        try:
            start_time = get_epoch_time(start, 0)
        except ValueError:
            click.echo("ERROR: Invalid format for --start")
            return

        try:
            stop_time = get_epoch_time(stop, SECONDS_IN_WEEK)
        except ValueError:
            click.echo("ERROR: Invalid format for --end")
            return

        display_metrics(start_time, stop_time)
        return

        # convert minutes to seconds
    work_time = work * 60
    break_time = rest * 60

    # Determine if sound and notification are supported
    can_play_sound, can_notify = check_capabilities()

    work_minutes_str = "minutes" if work > 1 else "minute"
    rest_minutes_str = "minutes" if work > 1 else "minute"

    def session(session_type, total_time):
        with tqdm(total=total_time, desc=session_type, unit='s',
                  bar_format='{l_bar}{bar}| [{elapsed}<{remaining}]') as pbar:
            session_start_time = time.time()
            for _ in range(total_time, 0, -1):
                pbar.update()
                time.sleep(1)
            session_stop_time = time.time()
            # play sound
            if can_play_sound:
                play_sound()
            # notify
            if can_notify and notify:
                message = REST_MESSAGE if session_type == 'Work' else WORK_MESSAGE
                notify_command = get_notify_command(message)
                os.system(notify_command)
            # Persist the record
            save_session(session_type, session_start_time, session_stop_time)

    while True:
        # work session
        print(f'{Fore.GREEN}{Style.BRIGHT}Work for {work} {work_minutes_str}!{Style.RESET_ALL}')
        session("Work", work_time)
        # break session
        print(f'{Fore.RED}{Style.BRIGHT}Break for {rest} {rest_minutes_str}!{Style.RESET_ALL}')
        session("Break", break_time)


if __name__ == '__main__':
    main()
