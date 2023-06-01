""" Model for storing session parameters 
"""

############
# IMPORTS  #
############
# Import system packages
from pathlib import Path

# Import data handling packages
import json


#########
# BEGIN #
#########
class SessionParsModel:
    # Define dictionary items
    fields = {
        # Session variables
        'subject': {'type': 'str', 'value': '999'},
        'condition': {'type': 'str', 'value': 'TEST'},
        'num_trials': {'type': 'int', 'value': 1},
        
        # Stimulus variables
        'isi': {'type': 'float', 'value': 60.0},
        'jitter': {'type': 'float', 'value': 0.5},
        'train_reps': {'type': 'int', 'value': 10},
        'big_step': {'type': 'float', 'value': 5.0},
        'small_step': {'type': 'float', 'value': 2.5},
        'max_output': {'type': 'float', 'value': 85.0},
        'min_output': {'type': 'float', 'value': 50.0},
        'max_start': {'type': 'float', 'value': 70.0},
        'min_start': {'type': 'float', 'value': 50.0},
        'stim_file_path': {'type': 'str', 'value': 'Please select a .wav file'},

        # Audio device variables
        'audio_device': {'type': 'int', 'value': 999},
        'speaker_number': {'type': 'int', 'value': 1},

        # Calibration variables
        'cal_scaling_factor': {'type': 'float', 'value': -30.0},
        'slm_reading': {'type': 'float', 'value': 82.0},
        'slm_offset': {'type': 'float', 'value': 100.0},
        'cal_file': {'type': 'str', 'value': 'cal_stim.wav'},

        # Presentation level variables
        'scaling_factor': {'type': 'float', 'value': -30.0},
        'db_level': {'type': 'float', 'value': -30.0},

        # Misc variables
        'check_for_updates': {'type': 'str', 'value': 'yes'},
        'update_path': {'type': 'str', 'value': r'\\starfile\Public\Temp\MooreT\Custom Software\version_library.csv'},
    }


    def __init__(self):
        # Create session parameters file
        filename = 'moa_task_fly.json'

        # Store settings file in user's home directory
        self.filepath = Path.home() / filename

        # Load settings file
        self.load()


    def load(self):
        """ Load session parameters from file
        """
        # If the file doesn't exist, abort
        print("\nsessionmodel: Checking for parameter file...")
        if not self.filepath.exists():
            return

        # Open the file and read in the raw values
        print("sessionmodel: File found - reading raw values from " +
            "parameter file...")
        with open(self.filepath, 'r') as fh:
            raw_values = json.load(fh)

        # Don't implicitly trust the raw values: only get known keys
        print("sessionmodel: Loading vals into sessionpars model " +
            "if they match model keys")
        # Populate session parameter dictionary
        for key in self.fields:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.fields[key]['value'] = raw_value


    def save(self):
        """ Save current session parameters to file 
        """
        # Write to JSON file
        print("sessionmodel: Writing session pars from model to file...")
        with open(self.filepath, 'w') as fh:
            json.dump(self.fields, fh)


    def set(self, key, value):
        """ Set a variable value.
        """
        print("sessionmodel: Setting sessionpars model " +
            "fields with running vals...")
        if (
            key in self.fields and 
            type(value).__name__ == self.fields[key]['type']
        ):
            self.fields[key]['value'] = value
        else:
            raise ValueError("sessionmodel: Bad key or wrong variable type")
