""" Class for loading calibration file, determining calibration 
    offset, and calculating presentation level.

    Written by: Travis M. Moore
"""

############
# IMPORTS  #
############
# Import system packages
import os

# Import custom modules
from models import audiomodel
from functions import functions


#########
# MODEL #
#########
class CalModel:
    """ Write provided dictionary to .csv
    """
    def __init__(self, sessionpars):
        self.sessionpars = sessionpars


    def _get_cal_file(self):
        """ Load specified calibration file
        """
        print("calmodel: Locating calibration file...")
        if self.sessionpars['cal_file'].get() == 'cal_stim.wav':
            self.cal_file = functions.resource_path('cal_stim.wav')
            #self.cal_file = self.resource_path('cal_stim.wav')
            file_exists = os.access(self.cal_file, os.F_OK)
            if not file_exists:
                self.cal_file = '.\\assets\\cal_stim.wav'
        else: # Custom file was provided
            self.cal_file = self.sessionpars['cal_file'].get()

        print(f"calmodel: Using {self.cal_file}")


    def _calc_offset(self):
        """ Calculate adjusted presentation level
        """
        # Calculate SLM offset
        print("\ncalmodel: Calculating new presentation level...")
        slm_offset = self.sessionpars['slm_reading'].get() - self.sessionpars['cal_scaling_factor'].get()
        self.sessionpars['slm_offset'].set(slm_offset)
        # Provide console feedback
        print(f"calmodel: Starting level (dB FS): " +
              f"{self.sessionpars['cal_scaling_factor'].get()}")
        print(f"calmodel: SLM reading (dB): " +
              f"{self.sessionpars['slm_reading'].get()}")
        print(f"calmodel: SLM offset: {slm_offset}")

        # SLM offset not yet saved!
        # This must happen in controller using: self._save_sessionpars()


    def _calc_level(self, desired_spl):
        # Calculate presentation level
        self.sessionpars['desired_spl'].set(desired_spl)
        self.sessionpars['scaling_factor'].set(desired_spl - self.sessionpars['slm_offset'].get())
        print(f"calmodel: Desired level (dB): " +
              f"{self.sessionpars['desired_spl'].get()}")
        print(f"calmodel: Scaling factor: " +
            f"{self.sessionpars['scaling_factor'].get()}")

        # Calculated level not yet saved! 
        # This must happen in controller using: self._save_sessionpars()


    def play_cal(self):
        # Present calibration file
        self.cal = audiomodel.Audio(file_path=self.cal_file)
        self.cal.play(
            level=self.sessionpars['cal_scaling_factor'].get(),
            device_id=self.sessionpars['audio_device'].get()
        )

    
    def stop_cal(self):
        try:
            self.cal.stop()
        except AttributeError:
            print("calmodel: No calibration stimulus found!")
