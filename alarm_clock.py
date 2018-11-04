''' Wake up watch for BBC micro:bit

    Shows a child when it's time to wake up mom and dad. Sleepy face when it's to sleep, clocks when
        it's almost time to wake up and happy face when it's time to wake up

    Assumes 0:00 is SLEEP_TIME, then comes ALMOST_WAKE_TIME, then WAKE_TIME, then SLEEP_TIME
    Show status between SHOW_START and SHOW_END. The rest of the time only when button A is pressed
'''
from microbit import *

TIME_MULTIPLIER = 1 # For testing. One minute is multiplied by this. For example, 60 means
                    # one minute in your world becomes one hour for this program
ALMOST_WAKE_TIME = 6.75 * 60 # 6:45 AM
WAKE_TIME = 7.25 * 60 # 7:15 AM
SLEEP_TIME = 21.5 * 60 # 9:30 PM
SHOW_START = 6 * 60
SHOW_END = 8 * 60


def scroll_stop_on_press(string):
    ''' Call display.scroll, but stop if button is pressed
        Release mechanism depends on any button being pressed or all ligths off. For this reason
            spaces are converted to underscore
        Resets was_pressed and get_presses on both buttons (note that was_pressed and get_presses
            are different counters; need to reset both)
    '''
    button_a.was_pressed() # Reset
    button_b.was_pressed()

    string = string.replace(' ', '_')
    display.scroll(string, wait=False)
    sleep(200) # Important to start with sleep. Otherwise, if the first character only has
               # left characters, the screen will be empty at the start
    while True:
        if button_a.was_pressed() or button_b.was_pressed() or all_pixels_are_off():
            break
        sleep(100)

    button_a.was_pressed() # Reset
    button_b.was_pressed()
    button_a.get_presses()
    button_b.get_presses()


def all_pixels_are_off():
    ''' Return true if all pixels are off'''
    for x in range(5):
        for y in range(5):
            if display.get_pixel(x, y):
                return False
    return True


class ManageTime(object):
    def __init__(self):
        self.initial_time_minutes = 0

    def get_current_minutes(self):
        running_time_minutes = running_time() / (1000 * 60) # Convert milliseconds to minutes
        current_time_minutes = TIME_MULTIPLIER * (running_time_minutes + self.initial_time_minutes)
        return int(current_time_minutes) % (60 * 24) # 24 h and 60 minutes in a day

    def show_current_time(self):
        minutes = self.get_current_minutes()
        scroll_stop_on_press('%02d:%02d'%(int(minutes / 60), minutes % 60))

    def interactive_set_initial_time(self):
        ''' Ask user for current time and set it'''
        scroll_stop_on_press('Click A to enter values, B to set.')
        hours = minutes = 0
        hours = self.get_initial_time_item('hours', 24)
        minutes = self.get_initial_time_item('minutes', 60)

        self.initial_time_minutes = hours * 60 + minutes

    @staticmethod
    def get_initial_time_item(name, maxval):
        ''' item is hours or minutes. Ask the user to set it and return the value
        '''
        scroll_stop_on_press('set ' + name)
        value = 0
        while True:
            value += button_a.get_presses()
            if button_b.was_pressed():
                break
            display.scroll('%02d' %(value % maxval))
            sleep(100)
        return value % maxval

    def show_sleep_awake_status(self):
        current_minutes = self.get_current_minutes()
        if current_minutes < ALMOST_WAKE_TIME or current_minutes > SLEEP_TIME:
            display.show(Image.ASLEEP)
        elif current_minutes < WAKE_TIME:
            display.show(Image.ALL_CLOCKS) # Don't sleep; this is an animation
        else:
            display.show(Image.HAPPY)

    def current_time_is_between_show_start_and_end(self):
        if SHOW_START < self.get_current_minutes() < SHOW_END:
            return True
        return False


def __main__():
    time_manager = ManageTime()
    time_manager.interactive_set_initial_time()

    button_a.was_pressed() # Reset
    while True:
        button_b_was_pressed = button_b.was_pressed() # So that I can use it multiple times (everytime you call the function the count is reset)
        if button_a.was_pressed():
            time_manager.show_current_time()
        elif button_b_was_pressed or time_manager.current_time_is_between_show_start_and_end():
            time_manager.show_sleep_awake_status()
            if button_b_was_pressed:
                sleep(2000) # Otherwise the static images are removed almost immediately
        else:
            display.clear()
        sleep(200)


if __name__ == '__main__':
    __main__()
