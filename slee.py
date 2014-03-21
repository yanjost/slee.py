#!/usr/bin/env python

# Original code comes from https://gist.github.com/BobNisco/8703662

import os
import sys
import time
from datetime import datetime, timedelta
import subprocess

import argparse

import logging
import math

logger = logging.getLogger()
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('music_service', choices=['itunes', 'spotify'])
    parser.add_argument('minutes_to_wait', type=float)
    parser.add_argument('--mute', help="Mutes sound at the end of the countdown", action="store_true", default=False)
    parser.add_argument('--sleep', help="Makes computer sleep at the end of the countdown", action="store_true", default=False)
    parser.add_argument('--debug', action="store_true", default=False)
    parser.add_argument('--fade', help='Fade out', action="store_true", default=False)

    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Logging enabled")

    handle_countdown(args.minutes_to_wait, args.music_service, args.fade)

    if args.sleep :
        sleep_computer()

    if args.mute :
        mute_sound()


def set_volume(value):
    val = int(value)
    if val < 0 :
        val = 0
    osascript('set volume output volume {}'.format(val))


def handle_countdown(minutes_to_wait, music_service, fade_out):
    start = datetime.now()
    # Calculate when we should be done, for display purposes
    finish = start + timedelta(minutes=minutes_to_wait)

    ref_volume = 0

    if fade_out:
        ref_volume = get_current_volume()
 
    # Wait the proper amount of time, while printing a timer
    print "Turning off music in:"
    for i in xrange(1, int(minutes_to_wait * 60)):
        time.sleep(1)
        newtime = datetime.now()
        if newtime >= finish : break
        time_left = finish - newtime
        time_left_secs = time_left.seconds+time_left.microseconds/1000000
 
        sys.stdout.write("\r" + str(time_left))
        sys.stdout.flush()

        if fade_out:
            if time_left_secs > 0.0 :
                new_volume = math.log(time_left_secs+1.0)*10
                if new_volume < ref_volume :
                    set_volume(new_volume)


    print

    stop_music(music_service)

def osascript(command,app=None):
    cmd = ""
    if app :
        cmd = 'tell application \"{app}\" to {cmd}'.format(app=app, cmd=command)
    else :
        cmd = command

    cmd = "osascript -e '{cmd}'".format(cmd=cmd)

    logging.debug(cmd)

    ret = os.system(cmd)

    logging.debug("ret = {}".format(ret))

    return ret

def stop_music(music_service):
    # Pause the music service to pause using osx's applescript
    # os.system("osascript -e 'tell app \"" + music_service + "\" to playpause'")
    osascript('playpause',music_service)

def get_current_volume():
    val = subprocess.check_output("osascript -e 'output volume of (get volume settings)'", shell=True)
    return int(val)

 
def sleep_computer():
    # os.system("osascript -e 'tell application \"Finder\" to sleep'")
    osascript('sleep','Finder')

def get_current_track_playing_time():
    val = subprocess.check_output("osascript -e 'tell application \"Spotify\" to player position' 2>/dev/null", shell=True)
    return float(val)
    
def get_current_track_length():
    val = subprocess.check_output("osascript -e 'tell application \"Spotify\" to duration of current track' 2>/dev/null", shell=True)
    return float(val)
    
def get_current_track_remaining_time():
    return get_current_track_length() - get_current_track_playing_time()

def mute_sound():
    osascript('set volume output volume 0')


if __name__ == '__main__':
    main()