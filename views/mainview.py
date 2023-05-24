""" Main view for Vesta
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import ttk

# Import custom modules
from widgets import arrowbuttons


#########
# BEGIN #
#########
class MainFrame(ttk.Frame):
    def __init__(self, parent, _vars, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Initialize
        self._vars = _vars

        # Start flag
        self.flag = 'ready'

        # Populate frame with widgets
        self.draw_widgets()


    def draw_widgets(self):
        """ Populate the main view with all widgets
        """
        ##########
        # Styles #
        ##########
        style = ttk.Style(self)
        style.configure('Big.TLabel', font=("Helvetica", 14))
        style.configure('Big.TLabelframe.Label', font=("Helvetica", 11))
        style.configure('Big.TButton', font=("Helvetica", 11))
        style.configure('Red.TFrame', background='red')


        #################
        # Create frames #
        #################
        options = {'padx':10, 'pady':10}

        # Main container
        frm_main = ttk.Frame(self)
        frm_main.grid(column=5, row=5, **options)

        # Arrow buttons frame
        self.frm_arrows = ttk.LabelFrame(frm_main, text="Presentation Controls")
        self.frm_arrows.grid(row=1, column=0, padx=15, pady=15)

        # Button frame
        frm_button = ttk.Frame(frm_main)
        frm_button.grid(row=1, column=1)


        ##################
        # Create Widgets #
        ##################
        # Arrow buttons controls
        self.button_text = tk.StringVar(value="Start")
        arrowbuttons.ArrowGroup(self.frm_arrows, button_text=self.button_text, 
            command_args = {
                'bigup': self._big_up,
                'smallup': self._small_up,
                'bigdown': self._big_down,
                'smalldown': self._small_down
            },
            repeat_args = {
                'repeat': self._repeat
            }).grid(row=0, column=0)
        
        # Submit button
        self.btn_submit = ttk.Button(frm_button, text="Submit", 
            command=self._on_submit, style='Big.TButton',
            state="disabled", takefocus=0)
        self.btn_submit.grid(row=0, column=0, padx=(0,15))


    #############
    # Functions #
    #############
    # Button functions
    def _big_up(self):
        """ Send button_id and play event """
        self._vars['button_id'].set("bigup")
        self.event_generate('<<MainArrowButton>>')


    def _small_up(self):
        """ Send button_id and play event """
        self._vars['button_id'].set("smallup")
        self.event_generate('<<MainArrowButton>>')


    def _big_down(self):
        """ Send button_id and play event """
        self._vars['button_id'].set("bigdown")
        self.event_generate('<<MainArrowButton>>')


    def _small_down(self):
        """ Send button_id and play event """
        self._vars['button_id'].set("smalldown")
        self.event_generate('<<MainArrowButton>>')


    def _repeat(self):
        """ Present audio. Can be repeated as many times as 
            the listener wants without incrementing the 
            file list.
        """
        # Create stimulus on first "START"
        if self.flag == 'ready':
            print(f"\nmainview: Task started")
            print("mainview: Sending create stimulus event to controller")
            self.event_generate('<<MainStart>>')
            self.flag = 'running'
        
        # Send play audio event to app
        self.button_text.set("Repeat")
        self.btn_submit.config(state="enabled")
        self.event_generate('<<MainPlayAudio>>')

    
    def _on_submit(self):
        # Send save data event to app
        self.button_text.set("Start")
        
        # Recreate stimulus on each new trial
        # In this case, changing the jitter
        self.flag = 'ready'
        self.event_generate('<<MainSave>>')


    def get(self):
        """ Retrieve data as dictionary """
        data = dict()
        for key, variable in self._vars.items():
            try:
                data[key] = variable.get()
            except tk.TclError:
                message=f'Error with: {key}.'
                raise ValueError(message)
        return data


    def reset(self):
        """ Clear all values """   
        for var in self._vars.values():
            var.set('')
        # Disable submit button on press
        # Set focus to play button
        self.btn_submit.config(state="disabled")
