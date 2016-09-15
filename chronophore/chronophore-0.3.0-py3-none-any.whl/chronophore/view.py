import contextlib
import tkinter
from tkinter import font, ttk, N, S, E, W
from chronophore import config, controller, utils


class ChronophoreUI():
    """Simple Tkinter GUI for chronophore :
            - Entry for user id input
            - Button to sign in or out
            - List of currently signed in users
    """

    def __init__(self, timesheet):
        self.t = timesheet

        self.root = tkinter.Tk()
        self.root.title("STEM Sign In")
        self.content = ttk.Frame(self.root, padding=(5, 5, 10, 10))

        # custom fonts
        self.large_font = font.Font(family='Helvetica', size=config.LARGE_FONT_SIZE)
        self.medium_font = font.Font(family='Helvetica', size=config.MEDIUM_FONT_SIZE)
        self.small_font = font.Font(family='Helvetica', size=config.SMALL_FONT_SIZE)
        self.tiny_font = font.Font(family='Helvetica', size=config.TINY_FONT_SIZE)

        self.large_header = self.large_font.copy()
        self.large_header.configure(weight='bold')

        self.tiny_header = self.tiny_font.copy()
        self.tiny_header.configure(weight='bold')

        # default widget fonts
        ttk.Style().configure('TLabel', font=self.medium_font)
        ttk.Style().configure('TButton', font=self.medium_font)
        # The following won't work for mysterious reasons internal to tk:
        # ttk.Style().configure('TEntry', font=self.medium_font)

        # variables
        self.signed_in = tkinter.StringVar()
        self.user_id = tkinter.StringVar()
        self.feedback = tkinter.StringVar()

        # widgets
        self.frm_signedin = ttk.Frame(
            self.content,
            borderwidth=5,
            relief="sunken",
            width=200,
            height=100
        )
        self.lbl_signedin = ttk.Label(
            self.content,
            text="Currently Signed In:",
            font=self.tiny_header
        )
        self.lbl_signedin_list = ttk.Label(
            self.frm_signedin,
            textvariable=self.signed_in,
            font=self.tiny_font
        )
        self.lbl_welcome = ttk.Label(
            self.content,
            text=config.GUI_WELCOME_LABLE,
            font=self.large_header
        )
        self.lbl_id = ttk.Label(
            self.content,
            text="Enter Student ID:",
        )
        self.ent_id = ttk.Entry(
            self.content,
            textvariable=self.user_id,
            font=self.small_font
        )
        self.lbl_feedback = ttk.Label(
            self.content,
            textvar=self.feedback,
        )
        self.btn_sign = ttk.Button(
            self.content,
            text="Sign In/Out",
            command=self._sign_in_button_press,
        )

        # assemble grid
        self.content.grid(column=0, row=0, sticky=(N, S, E, W))
        self.lbl_signedin.grid(column=0, row=0, pady=0)
        self.frm_signedin.grid(
            column=0, row=1, columnspan=1, rowspan=4, sticky=(N, S, E, W)
        )
        self.lbl_signedin_list.grid(column=0, row=0, columnspan=1, rowspan=4)
        self.lbl_welcome.grid(column=2, row=1, columnspan=1)
        # TODO(amin): figure out why lbl_id and btn_sign wiggle
        # when lbl_signedin_list updates
        self.lbl_id.grid(column=2, row=2, columnspan=1, sticky=(N))
        # TODO(amin): add select all shortcuts to this entry
        self.ent_id.grid(column=2, row=2, columnspan=1)
        self.lbl_feedback.grid(column=2, row=3)
        self.btn_sign.grid(column=2, row=4, columnspan=1, sticky=(N))

        # resize weights
        self.root.columnconfigure(0, weight=1, minsize=400)
        self.root.rowconfigure(0, weight=1, minsize=200)
        self.content.columnconfigure(0, weight=1, minsize=150)
        self.content.columnconfigure(1, weight=3)
        self.content.columnconfigure(2, weight=3)
        self.content.columnconfigure(3, weight=3)
        self.content.rowconfigure(0, weight=0)
        self.content.rowconfigure(1, weight=3, minsize=50)
        self.content.rowconfigure(2, weight=1, minsize=100)
        self.content.rowconfigure(3, weight=1)
        self.content.rowconfigure(4, weight=3)

        # key bindings
        self.root.bind('<Return>', self._sign_in_button_press)
        self.root.bind('<KP_Enter>', self._sign_in_button_press)

        self.ent_id.focus()
        self._set_signed_in()
        self.root.mainloop()

    def _set_signed_in(self):
        names = [
            " ".join([first, last])
            for first, last in controller.signed_in_names(self.t)
        ]
        self.signed_in.set('\n'.join(sorted(names)))

    def _show_feedback(self, message, seconds=None):
        """Display a message in lbl_feedback, which then times out
        after some number of seconds. Use after() to schedule a callback
        to hide the feedback message. This works better than using threads,
        which can cause problems in Tk.
        """
        if seconds is None:
            seconds = config.MESSAGE_DURATION

        # cancel any existing callback to clear the feedback
        # label. this prevents flickering and inconsistent
        # timing during rapid input.
        with contextlib.suppress(AttributeError):
            self.root.after_cancel(self.clear_feedback)

        self.feedback.set(message)
        self.clear_feedback = self.root.after(
            1000 * seconds, lambda: self.feedback.set("")
        )

    def _sign_in_button_press(self, *args):
        """Validate input from ent_id, then sign in to the Timesheet."""
        user_id = self.ent_id.get().strip()

        try:
            sign_in_status = controller.sign(user_id, self.t)
        except (ValueError, FileNotFoundError) as e:
            self._show_feedback(e)
        else:
            user_name = " ".join(utils.user_name(user_id, utils.get_users()))
            self._show_feedback("{}: {}".format(sign_in_status, user_name))
        finally:
            self._set_signed_in()

        self.ent_id.delete(0, 'end')
        self.ent_id.focus()


if __name__ == '__main__':
    # Usage example
    from chronophore.model import Timesheet
    t = Timesheet()
    ui = ChronophoreUI(timesheet=t)
