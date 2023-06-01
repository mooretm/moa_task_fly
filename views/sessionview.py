""" Session parameters dialog
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# Import custom modules
from functions import functions


#########
# BEGIN #
#########
class SessionDialog(tk.Toplevel):
    """ Dialog for setting session parameters
    """
    def __init__(self, parent, sessionpars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.sessionpars = sessionpars

        self.withdraw()
        self.resizable(False, False)
        self.title("Session Parameters")
        self.grab_set()

        # Draw widgets
        self._draw_widgets()

        # Center the session dialog window
        self.center_window()


    def _draw_widgets(self):
            #################
            # Create Frames #
            #################
            # Shared frame settings
            frame_options = {'padx': 10, 'pady': (10, 0)}
            widget_options = {'padx': 5, 'pady': 5}

            # Session info frame
            frm_session = ttk.Labelframe(self, text='Session Information')
            frm_session.grid(row=5, column=5, **frame_options, sticky='nsew')

            # Session options frame
            frm_options = ttk.Labelframe(self, text='Stimulus Options')
            frm_options.grid(row=10, column=5, **frame_options, sticky='nsew')

            # Stimulus file browser frame
            frm_stimpath = ttk.Labelframe(self, text='Stimulus File Path')
            frm_stimpath.grid(row=15, column=5, **frame_options, ipadx=5, ipady=5)


            ##################
            # Create widgets #
            ##################
            # Session Information Frame
            # Subject
            ttk.Label(frm_session, text="Subject:"
                ).grid(row=5, column=5, sticky='e', **widget_options)
            ttk.Entry(frm_session, width=20, 
                textvariable=self.sessionpars['subject']
                ).grid(row=5, column=10, sticky='w')

            # Condition
            ttk.Label(frm_session, text="Condition:"
                ).grid(row=10, column=5, sticky='e', **widget_options)
            ttk.Entry(frm_session, width=20, 
                textvariable=self.sessionpars['condition']
                ).grid(row=10, column=10, sticky='w')

            # Trials
            ttk.Label(frm_session, text="Trials:"
                ).grid(row=15, column=5, sticky='e', **widget_options)
            ttk.Entry(frm_session, width=20, 
                textvariable=self.sessionpars['num_trials']
                ).grid(row=15, column=10, sticky='w')


            # Stimulus Paramters Frame
            # Column 1
            # ISI
            ttk.Label(frm_options, text="ISI (ms):"
                ).grid(row=5, column=5, sticky='e', **widget_options)
            ttk.Entry(frm_options, width=10, 
                textvariable=self.sessionpars['isi']
                ).grid(row=5, column=10, sticky='w')

            # Jitter
            ttk.Label(frm_options, text="Jitter (ms):"
                ).grid(row=10, column=5, sticky='e', **widget_options)
            ttk.Entry(frm_options, width=10, 
                textvariable=self.sessionpars['jitter']
                ).grid(row=10, column=10, sticky='w')

            # Train Reps
            ttk.Label(frm_options, text="Train Reps:"
                ).grid(row=15, column=5, sticky='e', **widget_options)
            ttk.Entry(frm_options, width=10, 
                textvariable=self.sessionpars['train_reps']
                ).grid(row=15, column=10, sticky='w')
            
            # Big step
            ttk.Label(frm_options, text="Big Step (dB):"
                ).grid(row=20, column=5, sticky='e', **widget_options)
            ttk.Entry(frm_options, width=10, 
                textvariable=self.sessionpars['big_step']
                ).grid(row=20, column=10, sticky='w')

            # Small step
            ttk.Label(frm_options, text="Small Step (dB):"
                ).grid(row=25, column=5, sticky='e', **widget_options)
            ttk.Entry(frm_options, width=10, 
                textvariable=self.sessionpars['small_step']
                ).grid(row=25, column=10, sticky='w')
            

            # Column 2
            # Max output
            ttk.Label(frm_options, text="Max Output (dB):"
                ).grid(row=5, column=15, sticky='e', **widget_options)
            ttk.Entry(frm_options, width=10, 
                textvariable=self.sessionpars['max_output']
                ).grid(row=5, column=20, sticky='w')
            
            # Min output
            ttk.Label(frm_options, text="Min Output (dB):"
                ).grid(row=10, column=15, sticky='e', **widget_options)
            ttk.Entry(frm_options, width=10, 
                textvariable=self.sessionpars['min_output']
                ).grid(row=10, column=20, sticky='w')

            # Max start
            ttk.Label(frm_options, text="Max Start (dB):"
                ).grid(row=15, column=15, sticky='e', **widget_options)
            ttk.Entry(frm_options, width=10, 
                textvariable=self.sessionpars['max_start']
                ).grid(row=15, column=20, sticky='w')

            # Min start
            ttk.Label(frm_options, text="Min Start (dB):"
                ).grid(row=20, column=15, sticky='e', **widget_options)
            ttk.Entry(frm_options, width=10, 
                textvariable=self.sessionpars['min_start']
                ).grid(row=20, column=20, sticky='w')
            

            # File Browsing Frame
            # Stimulus file
            ttk.Label(frm_stimpath, text="Path:"
                ).grid(row=30, column=5, sticky='e', **widget_options)
            # Get audio directory from sessionpars dict
            full_stim_path = self.sessionpars['stim_file_path'].get()
            # Truncate to fit in label
            short_stim_path = functions.truncate_path(full_stim_path)
            # Create textvariable
            self.stim_var = tk.StringVar(value=short_stim_path)
            ttk.Label(frm_stimpath, textvariable=self.stim_var, 
                borderwidth=2, relief="solid", width=60
                ).grid(row=30, column=10, sticky='w')
            ttk.Button(frm_stimpath, text="Browse", command=self._get_stimulus_file
                ).grid(row=35, column=10, sticky='w', pady=(0, 10))

            # Submit button
            btn_submit = ttk.Button(self, text="Submit", command=self._on_submit)
            btn_submit.grid(row=40, column=5, columnspan=2, pady=10)


            # # Randomize
            # #self.random_var = tk.IntVar(value=self.sessionpars['randomize'])
            # chk_random = ttk.Checkbutton(frm_options, text="Randomize",
            #     takefocus=0, variable=self.sessionpars['randomize'])
            # chk_random.grid(row=5, column=5,  columnspan=20, sticky='w', **widget_options)

            # # Repetitions
            # ttk.Label(frm_options, text="Presentation(s):"
            #     ).grid(row=10, column=5, sticky='e', **widget_options)
            # ttk.Entry(frm_options, width=20, 
            #     textvariable=self.sessionpars['repetitions']
            #     ).grid(row=10, column=10, sticky='w')


    #############
    # Functions #
    #############
    def center_window(self):
        """ Center the root window 
        """
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        size = tuple(int(_) for _ in self.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        self.geometry("+%d+%d" % (x, y))
        self.deiconify()


    def _get_stimulus_file(self):
        """ Get path to stimulus file
        """
        # Get file from dialog
        filename = filedialog.askopenfilename(title="Stimulus File", filetypes=[("WAV", "*.wav")])
        # Set file plus path to sessionpars
        self.sessionpars['stim_file_path'].set(filename)
        short_filename = functions.truncate_path(filename)
        self.stim_var.set(short_filename)


    # def _check_presentations(self):
    #     if self.sessionpars['repetitions'].get() == 0:
    #         self.sessionpars['repetitions'].set(1)
    #         messagebox.showwarning(title="Seriously?",
    #             message="Invalid number of presentations!",
    #             detail="You must have at least 1 round of presentations! " +
    #                 "Updating to 1 presentation."
    #         )


    def _on_submit(self):
        """ Check number of presentations != 0.
            Send submit event to controller.
        """
        # # Make sure the number of presentations isn't 0
        # self._check_presentations()

        print("\nsessionview: Sending save event to controller...")
        self.parent.event_generate('<<SessionSubmit>>')
        self.destroy()
