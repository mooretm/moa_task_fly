""" GUI for MOA task using on-the-fly stimulus generation from 
    provided .wav file. 

    OOP design allows for easy swapping of stimulus-specific 
    models. 

    Written by: Travis M. Moore
    Created: May 25, 2023
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import messagebox

# Import system packages
import os
from pathlib import Path
import random

# Import misc packages
import webbrowser
import markdown

# Import custom modules
# Menu imports
from menus import mainmenu
# Function imports
from functions import functions
# Model imports
from models import sessionmodel
from models import audiomodel
from models import calmodel
from models import csvmodel
from models import updatermodel
from models import tickmodel
# View imports
from views import mainview
from views import sessionview
from views import audioview
from views import calibrationview


#########
# BEGIN #
#########
class Application(tk.Tk):
    """ Application root window
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #############
        # Constants #
        #############
        self.NAME = 'MOA Task Controller (OTF)'
        self.VERSION = '0.2.0'
        self.EDITED = 'June 01, 2023'

        # Create menu settings dictionary
        self._menu_settings = {
            'name': self.NAME,
            'version': self.VERSION,
            'last_edited': self.EDITED
        }


        ######################################
        # Initialize Models, Menus and Views #
        ######################################
        # Setup main window
        self.withdraw() # Hide window during setup
        self.resizable(False, False)
        self.title(self.NAME)

        # Assign special quit function on window close
        # Used to close Vulcan session cleanly even if 
        # user closes window via "X"
        self.protocol('WM_DELETE_WINDOW', self._quit)

        # Data dictionary
        self._vars = {
            'button_id': tk.StringVar()
        }

        # Load current session parameters from file
        # Or load defaults if file does not exist yet
        self.sessionpars_model = sessionmodel.SessionParsModel()
        self._load_sessionpars()

        # Load CSV writer model
        self.csvmodel = csvmodel.CSVModel(self.sessionpars)

        # Load calibration model
        self.calmodel = calmodel.CalModel(self.sessionpars)

        # Load main view
        self.main_frame = mainview.MainFrame(self, self._vars)
        self.main_frame.grid(row=0, column=0)
        self.grid_columnconfigure(0, weight=1) # center widget
        self.grid_rowconfigure(0, weight=1) # center widget

        # Trial counter label
        self.counter = 1
        self.trial_var = tk.StringVar(value="Trial:")
        tk.Label(self, textvariable=self.trial_var).grid(
            row=1, column=0, sticky='w', padx=10)

        # Load menus
        menu = mainmenu.MainMenu(self, self._menu_settings)
        self.config(menu=menu)

        # Create callback dictionary
        event_callbacks = {
            # File menu
            '<<FileSession>>': lambda _: self._show_session_dialog(),
            '<<FileQuit>>': lambda _: self._quit(),

            # Tools menu
            '<<ToolsAudioSettings>>': lambda _: self._show_audio_dialog(),
            '<<ToolsCalibration>>': lambda _: self._show_calibration_dialog(),

            # Help menu
            '<<Help>>': lambda _: self._show_help(),

            # Session dialog commands
            '<<SessionSubmit>>': lambda _: self._save_sessionpars(),

            # Calibration dialog commands
            '<<CalPlay>>': lambda _: self.play_calibration_file(),
            '<<CalStop>>': lambda _: self.stop_calibration_file(),
            '<<CalibrationSubmit>>': lambda _: self._calc_offset(),

            # Audio dialog commands
            '<<AudioDialogSubmit>>': lambda _: self._save_sessionpars(),

            # Main View commands
            '<<MainStart>>': lambda _: self._on_start(),
            '<<MainArrowButton>>': lambda _: self._on_arrow_button(),
            '<<MainPlayAudio>>': lambda _: self._play(),
            '<<MainSave>>': lambda _: self._on_save(),
        }

        # Bind callbacks to sequences
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # Center main window
        self.center_window()

        # Check for updates
        if self.sessionpars['check_for_updates'].get() == 'yes':
            #_filepath = r'\\starfile\Public\Temp\MooreT\Custom Software\version_library.csv'
            _filepath = self.sessionpars['update_path'].get()
            u = updatermodel.VersionChecker(_filepath, self.NAME, self.VERSION)
            if not u.current:
                self.destroy()


    #####################
    # General Functions #
    #####################
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


    def _quit(self):
        """ Quit application.
        """
        # Quit app
        self.destroy()


    def _play(self):
        try:
            self.a.play(
                level=self.sessionpars['scaling_factor'].get(),
                device_id=self.sessionpars['audio_device'].get(),
                speaker=self.sessionpars['speaker_number'].get()
            )
        except AttributeError:
            messagebox.showerror(
                title="No Audio File",
                message="Cannot play audio!",
                detail="You must provide a valid audio path to play audio." +
                    "\nAborting!"
            )
            self.destroy()


    #######################
    # Main View Functions #
    #######################
    def _set_starting_level(self):
        print(f"\ncontroller: Setting random starting level")
        # Get random integer within range
        #starting_level = random.randint(50, 70)
        starting_level = random.randint(
            self.sessionpars['min_start'].get(), 
            self.sessionpars['max_start'].get()
        )

        # Test that random starting level is within min/max limits
        # Assign to nearest limit
        if starting_level > self.sessionpars['max_output'].get():
            starting_level = self.sessionpars['max_output'].get()
        if starting_level < self.sessionpars['min_output'].get():
            starting_level = self.sessionpars['min_output'].get()

        # Convert to dB using offset
        self._calc_level(starting_level)


    def _on_start(self):
        """ Increases trial counter, and if not at end of task, then 
            generates a new, random starting level, applies offset,
            and calls play function.
        """
        # Update trial label
        self.trial_var.set(f"Trial {self.counter} of " + 
            f"{self.sessionpars['num_trials'].get()}")

        # Update sessionpars['scaling_factor'] with starting level
        self._set_starting_level()

        print(f"\ncontroller: Creating new stimulus instance")
        try:
            # Create stimulus
            self.a = audiomodel.Audio(Path(self.sessionpars['stim_file_path'].get()))
            t = tickmodel.TickModel(self.sessionpars, self.a)
            singleton = t.make_train()
            self.a.signal = singleton
        except FileNotFoundError:
            print("\ncontroller: Cannot find audio! Aborting.")
            return

        # Play stimulus
        self._play()


    def _reset_arrow_message(self):
        self.main_frame.arrow_frm_text.set("Presentation Controls")
        self.main_frame.arrow_frm_label.config(foreground='black')


    def _check_limits(self, scaling):
        # Check that scaling factor is within limits
        max = self.sessionpars['max_output'].get() - \
            self.sessionpars['slm_offset'].get()
        min = self.sessionpars['min_output'].get() - \
            self.sessionpars['slm_offset'].get()
        if scaling > max:
            scaling = max
            self.main_frame.arrow_frm_text.set('UPPER LIMIT')
            self.main_frame.arrow_frm_label.config(foreground='red')
            self.after(2000, lambda: self._reset_arrow_message())
        if scaling < min:
            scaling = min
            self.main_frame.arrow_frm_text.set('LOWER LIMIT')
            self.main_frame.arrow_frm_label.config(foreground='red')
            self.after(2000, lambda: self._reset_arrow_message())
        self.update_idletasks()
        return scaling


    def _on_arrow_button(self):
        # Step sizes
        self.steps = {
            'bigup': self.sessionpars['big_step'].get(),
            'smallup': self.sessionpars['small_step'].get(),
            'bigdown': -self.sessionpars['big_step'].get(),
            'smalldown': -self.sessionpars['small_step'].get(),
        }
        step = self.steps[self._vars['button_id'].get()]

        # Get existing scaling factor
        scaling = self.sessionpars['scaling_factor'].get()
        print(f"\ncontroller: {self._vars['button_id'].get()} pressed.")
        print(f"controller: Adding {step}")
        print(f"controller: Previous scaling factor: {scaling}")

        # Adjusting scaling factor based on button press
        scaling += step

        # Check that new scaling factor is within limits
        scaling = self._check_limits(scaling)

        # Save scaling factor
        self.sessionpars['scaling_factor'].set(scaling)
        self.sessionpars['db_level'].set(scaling + self.sessionpars['slm_offset'].get())
        print(f"controller: New scaling factor: {scaling}")
        print(f"controller: New dB level: {self.sessionpars['db_level'].get()}")

        # Present audio
        self._play()


    def _on_save(self):
        """ Format values and send to csv model.
        """
        # Get tk variable values
        # data = dict()
        # for key in self.sessionpars:
        #     data[key] = self.sessionpars[key].get()

        # Save data
        print('controller: Calling save record function...')
        #self.csvmodel.save_record(data)
        self.csvmodel.save_record()

        # Increase counter and check for end of task
        self.counter += 1
        if self.counter > self.sessionpars['num_trials'].get():
            messagebox.showinfo(
                title="Done!",
                message="You have finished this task.",
                detail="Please wait for the investigator."
            )
            self.destroy()


    ############################
    # Session Dialog Functions #
    ############################
    def _show_session_dialog(self):
        """ Show session parameter dialog.
        """
        print("\ncontroller: Calling session dialog...")
        sessionview.SessionDialog(self, self.sessionpars)


    def _load_sessionpars(self):
        """ Load parameters into self.sessionpars dict. 
        """
        vartypes = {
        'bool': tk.BooleanVar,
        'str': tk.StringVar,
        'int': tk.IntVar,
        'float': tk.DoubleVar
        }

        # Create runtime dict from session model fields
        self.sessionpars = dict()
        for key, data in self.sessionpars_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.sessionpars[key] = vartype(value=data['value'])
        print("\ncontroller: Loaded sessionpars model fields into " +
            "running sessionpars dict")


    def _save_sessionpars(self, *_):
        """ Save current runtime parameters to file.
        """
        print("\ncontroller: Calling sessionpar model set and save funcs...")
        for key, variable in self.sessionpars.items():
            self.sessionpars_model.set(key, variable.get())
            self.sessionpars_model.save()


    ########################
    # Tools Menu Functions #
    ########################
    def _show_audio_dialog(self):
        """ Show audio settings dialog.
        """
        print("\ncontroller: Calling audio dialog...")
        audioview.AudioDialog(self, self.sessionpars)

    def _show_calibration_dialog(self):
        """ Display the calibration dialog window.
        """
        print("\ncontroller: Calling calibration dialog...")
        calibrationview.CalibrationDialog(self, self.sessionpars)


    ################################
    # Calibration Dialog Functions #
    ################################
    def play_calibration_file(self):
        """ Load calibration file and present.
        """
        # Get calibration file
        self.calmodel._get_cal_file()

        # Play calibration file
        self.calmodel.play_cal()


    def stop_calibration_file(self):
        """ Stop playback of calibration file.
        """
        # Stop calibration playback
        self.calmodel.stop_cal()


    def _calc_offset(self):
        """ Calculate offset based on SLM reading.
        """
        # Calculate new presentation level
        self.calmodel._calc_offset()
        # Save level - this must be called here!
        self._save_sessionpars()


    def _calc_level(self, desired_spl):
        """ Calculate new dB FS level using slm_offset.
        """
        self.calmodel._calc_level(desired_spl)
        # Save level - this must be called here!
        self._save_sessionpars()


    #######################
    # Help Menu Functions #
    #######################
    def _show_help(self):
        """ Create html help file and display in default browser
        """
        print("controller: Looking for help file in compiled " +
            "version temp location...")
        help_file = functions.resource_path('README\\README.html')
        #help_file = self.resource_path('README\\README.html')
        file_exists = os.access(help_file, os.F_OK)
        if not file_exists:
            print('controller: Not found!\nChecking for help file in ' +
                'local script version location')
            # Read markdown file and convert to html
            with open('README.md', 'r') as f:
                text = f.read()
                html = markdown.markdown(text)

            # Create html file for display
            with open('.\\assets\\README\\README.html', 'w') as f:
                f.write(html)

            # Open README in default web browser
            webbrowser.open('.\\assets\\README\\README.html')
        else:
            #help_file = self.resource_path('README\\README.html')
            webbrowser.open(help_file)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
