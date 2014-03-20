#!/usr/bin/env python
import os
import sys
import time
from datetime import datetime, timedelta
 
def main():
    if len(sys.argv) >= 3:
        music_service = str(sys.argv[1])
        minutes_to_wait = float(sys.argv[2])
        handle_countdown(minutes_to_wait, music_service)
    else:
        print ("usage: [itunes or spotify] [minutes to wait (fractions are allowed)] "
               "[true (if you want to sleep your computer after)]")
    if len(sys.argv) == 4 and str_2_bool(sys.argv[3]):
        sleep_computer()
 
def handle_countdown(minutes_to_wait, music_service):
    start = datetime.now()
    # Calculate when we should be done, for display purposes
    finish = start + timedelta(minutes=minutes_to_wait)
 
    # Wait the proper amount of time, while printing a timer
    print "Turning off music in:"
    for i in xrange(1, int(minutes_to_wait * 60)):
        time.sleep(1)
        newtime = datetime.now()
        time_left = str(finish - newtime)
 
        sys.stdout.write("\r" + time_left)
        sys.stdout.flush()
    stop_music(music_service)
 
def stop_music(music_service):
    # Pause the music service to pause using osx's applescript
    os.system("osascript -e 'tell app \"" + music_service + "\" to playpause'")
 
def sleep_computer():
    os.system("osascript -e 'tell application \"Finder\" to sleep'")
 
def str_2_bool(value):
    return value.lower() in ("yes", "true", "t", "1")
 
if __name__ == '__main__':
    main()