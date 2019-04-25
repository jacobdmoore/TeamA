# Code happily adapted from StackOverflow with additional features.
# https://stackoverflow.com/questions/45973453/using-mouse-and-keyboard-listeners-together-in-python
# Written by Jacob Moore, (c) 2019

def keyparser(start_time)

    from pynput.keyboard import Listener as KeyboardListener
    from pynput.mouse    import Listener as MouseListener
    from pynput.keyboard import Key
    import logging
    import time
    import datetime

    # MAKE CTRL + F5 an option to go to current slide, CTRL + SHIFT + F5 goes to beginning
    # CTRL SHIFT LEFT/RIGHT to switch desktops
    # ALT TAB

    # Prompt user to specify whether they will be using Google Slides
    yes = ['yes','Yes','y','Y']
    no = ['no','No','n','N']
    cancel = ['cancel','Cancel','c','C']
    valid_input = False
    prompt = '\nWill you be using Google Slides to present today? (y/n)\n'
    google = input(prompt)

    while not valid_input:
        if google in yes:
            google = True
            valid_input = 1
        elif google in no:
            google = False
            valid_input = 1
        elif google in cancel:
            raise SystemExit(0)
        else:
            google = input("\nInvalid response. Please respond with 'y' or 'n'. You may cancel by responding 'c'. \n" + prompt)

    # Log of all keystrokes.
    logging.basicConfig(filename=("full_keylog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

    # Log slide tracking.
    with open('action_key_tracker.txt','w+') as file:
        if google:
            program = 'Google Slides'
        else:
            program = 'desktop application'
        header = str(datetime.datetime.now()) + ': Tracking started using ' + program
        file.write(header)

    def on_press(key):
        global start_time
        global google

        # Timestamp of keypress.
        timestamp = time.time()-start_time

        # Lists containing all the shortcut keys that 
        # are used in presentation mode to either advance or retreat slides.
        next_keys = ["'n'",'Key.enter','Key.page_down','Key.right','Key.down','Key.space']
        prev_keys = ["'p'",'Key.page_up','Key.left','Key.up','Key.backspace']

        logging.info(str(key))

        # The cases are pretty self-explanatory. Shift and F5 are tracked as the 
        # ways the slideshow is restarted after it is exited with Esc.
        if str(key) in next_keys:
            print('NEXT with',key,'at ',timestamp)
            with open('action_key_tracker.txt', 'a') as file:
                file.write('\nNEXT with ' + str(key) + ' at ' + str(timestamp))
        elif str(key) in prev_keys:
            print('PREVIOUS with',key,'at ',timestamp)
            with open('action_key_tracker.txt', 'a') as file:
                file.write('\nPREVIOUS with ' + str(key) + ' at ' + str(timestamp))
        elif str(key) == 'Key.esc':
            print('EXIT with Esc at ',timestamp)
            with open('action_key_tracker.txt', 'a') as file:
                file.write('\nEXIT with Esc at ' + str(timestamp))
        elif str(key) in ['Key.ctrl_r','Key.ctrl']:
            print('CTRL KEY at ',timestamp)
            with open('action_key_tracker.txt', 'a') as file:
                file.write('\nCTRL with ' + str(key) + ' at ' + str(timestamp))
        elif str(key) in ['Key.shift_r','Key.shift']:
            print('SHIFT KEY at ',timestamp)
            with open('action_key_tracker.txt', 'a') as file:
                file.write('\nSHIFT with ' + str(key) + ' at ' + str(timestamp))
        elif str(key) == 'Key.f5':
            print('ENTER with F5 at ',timestamp)
            with open('action_key_tracker.txt', 'a') as file:
                file.write('\nENTER with F5 at ' + str(timestamp))

    def on_move(x, y):
        global start_time
        logging.info("Mouse moved to ({0}, {1})".format(x, y))

    def on_click(x, y, button, pressed):
        global start_time
        # Timestamp of click.
        timestamp = time.time()-start_time

        if pressed:
            logging.info('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
    
        # Only the left mouse click advances slides.
        if str(button) == 'Button.left':
            print('NEXT with left click at ',timestamp)
            with open('action_key_tracker.txt', 'a') as file:
                file.write('\nNEXT with left click at ' + str(timestamp))

    def on_scroll(x, y, dx, dy):
        global start_time
        # Timestamp of scroll.
        timestamp = time.time()-start_time

        logging.info('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
        # -1 is equivalent to a downscroll with the mouse.
        # 1 is an upscroll.
        if dy == -1:
            print('NEXT with down scroll at ',timestamp)
            with open('action_key_tracker.txt', 'a') as file:
                file.write('\nNEXT with down scroll at ' + str(timestamp))
        elif dy == 1:
            print('NEXT with up scroll',timestamp)
            with open('action_key_tracker.txt', 'a') as file:
                file.write('\nPREVIOUS with up scroll at ' + str(timestamp))

    # Listen to both mouse (click and scroll) and keyboard actions.
    with MouseListener(on_click=on_click, on_scroll=on_scroll) as listener:
        with KeyboardListener(on_press=on_press) as listener:
            listener.join()