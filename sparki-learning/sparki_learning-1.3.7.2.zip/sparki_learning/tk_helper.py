# Helper functions to be used with tk
#
# 
# written by Jeremy Eglen
# Created: October 23, 2016
# Last Modified: October 23, 2016
#
# included with the sparki_learning library, though that is not required
#

from __future__ import print_function

DEBUG = True

def buttonWindow(buttonList, message = "Choose one", title = "Question", default = None, parent = None):
    """ Create a top level window having buttonList as the buttons
        Returns the button clicked by the user, or None if the window is destroyed

        arguments:
        buttonList - list of strings to put on button labels
        message - string message to appear above the buttons
        title - string title of the window
        default - string, must be a member of buttonList; default button
        parent - root window

        returns:
        string - text of the button which the user clicked (or None)
    """
    if DEBUG:
        print("In buttonWindow", file=sys.stderr)
    
    import tkinter as tk
    userChoice = None
    
    # start a new window
    butWin = tk.Toplevel(parent)
    butWin.title(title)
    Label(butWin, message).grid(row = 0, column = 0)

    # we'll use the grid layout manager
##    tk.Button(butWin, text = buttonText, command=lambda: userChoice = ).grid(row = 0, column = 1)
##
##    # weights for resizing
##    for i in range(3):
##        butWin.columnconfigure(i, weight=1)
##
##    for i in range(5):
##        butWin.rowconfigure(i, weight=1)

    butWin.lift()                 # move the window to the top to make it more visible
    butWin.wait_window(butWin)    # wait for this window to be destroyed (closed) before moving on

    return userChoice
