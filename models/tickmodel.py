""" Create tick train from imported .wav file.
"""

###########
# Imports #
###########
# Import data science packages
import numpy as np
import pandas as pd
import random


#########
# BEGIN #
#########
class TickModel:
    """ Create tick stimulus train from 
        imported .wav file.
    """
    def __init__(self, sessionpars, audio):
        # Initialize
        self.sessionpars = sessionpars
        self.audio = audio
        self.isi = self.sessionpars['isi'].get() / 1000
        self.jitter = self.sessionpars['jitter'].get() / 1000


    def _isi_in_samples(self):
        # Create silence
        self.isi = self.isi + random.uniform(-self.jitter, self.jitter)
        jittered_isi = self.isi * self.audio.fs

        return jittered_isi


    def _single_tick(self):
        # Get number of samples for isi + jitter
        samps = self._isi_in_samples()

        # Mono signal
        shh = np.zeros(int(samps))
        
        # Stereo signal
        #if self.audio.num_channels == 2:
        #    shh = np.array([shh,shh])

        # Signal + silence
        singleton = np.hstack([self.audio.signal, shh])

        return singleton


    def make_train(self):
        train = []
        for ii in range(0, self.sessionpars['train_reps'].get()):
            # Get a single tick plus randomly jittered isi
            singleton = self._single_tick()
            #train = np.hstack((justone,) * self.sessionpars['train_reps'])
            train.append(singleton)

        self.tick_train = np.hstack(train)
        return self.tick_train
