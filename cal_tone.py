import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

def doGate(sig,rampdur=0.02,fs=48000):
    """
        Apply rising and falling ramps to signal SIG, of 
        duration RAMPDUR. Takes a 1-channel or 2-channel 
        signal. 

            SIG: a 1-channel or 2-channel signal
            RAMPDUR: duration of one side of the gate in 
                seconds
            FS: sampling rate in samples/second

            Example: 
            [t, tone] = mkTone(100,0.4,0,48000)
            gated = doGate(tone,0.01,48000)

        Original code: Anonymous
        Adapted by: Travis M. Moore
        Last edited: Jan. 13, 2022          
    """
    gate =  np.cos(np.linspace(np.pi, 2*np.pi, int(fs*rampdur)))
    # Adjust envelope modulator to be within +/-1
    gate = gate + 1 # translate modulator values to the 0/+2 range
    gate = gate/2 # compress values within 0/+1 range
    # Create offset gate by flipping the array
    offsetgate = np.flip(gate)
    # Check number of channels in signal
    if len(sig.shape) == 1:
        # Create "sustain" portion of envelope
        sustain = np.ones(len(sig)-(2*len(gate)))
        envelope = np.concatenate([gate, sustain, offsetgate])
        gated = envelope * sig
    elif len(sig.shape) == 2:
        # Create "sustain" portion of envelope
        sustain = np.ones(len(sig[0])-(2*len(gate)))
        envelope = np.concatenate([gate, sustain, offsetgate])
        gatedLeft = envelope * sig[0]
        gatedRight = envelope * sig[1]
        gated = np.array([gatedLeft, gatedRight])
    return gated


def mkTone(freq, dur, phi=0, fs=48000):
    """ Create a pure tone. Returns the signal 
        AND the time base. 
    
        FREQ: frequency in Hz
        DUR: duration in SECONDS
        PHI: phase in DEGREES
        FS: sampling rate

        EXAMPLE: [t, sig] = (500,0.2,0,48000)

    Written by: Travis M. Moore
    Last edited: 1/12/2022
    """
    phi = np.deg2rad(phi) # to radians
    t = np.arange(0,dur,1/fs) # time base
    sig = np.sin(2*np.pi*freq*t+phi)
    return [t, sig]


def rms(sig):
    """ 
        Calculate the root mean square of a signal. 
        
        NOTE: np.square will return invalid, negative 
            results if the number excedes the bit 
            depth. In these cases, convert to int64
            EXAMPLE: sig = np.array(sig,dtype=int)

        Written by: Travis M. Moore
        Last edited: Feb. 3, 2020
    """
    theRMS = np.sqrt(np.mean(np.square(sig)))
    return theRMS


def mag2db(mag):
    """ 
        Convert magnitude to decibels. Takes a single
        value or a list of values.
    """
    try:
        db = [20 * np.log10(x) for x in mag]
        return db
    except:
        db = 20 * np.log10(mag)
        return db


def db2mag(db):
    """ 
        Convert decibels to magnitude. Takes a single
        value or a list of values.
    """
    # Must use this form to handle negative db values!
    try:
        mag = [10**(x/20) for x in db]
        return mag
    except:
        mag = 10**(db/20)
        return mag


def setRMS(sig, amp):
    """
        Set RMS level of a 1-channel or 2-channel signal.
    
        SIG: a 1-channel or 2-channel signal
        AMP: the desired amplitude to be applied to 
            each channel. Note this will be the RMS 
            per channel, not the total of both channels.
        EQ: takes 'y' or 'n'. Whether or not to equalize 
            the levels in a 2-channel signal. For example, 
            a signal with an ILD would lose the ILD with 
            EQ='y', so the default in 'n'.

        EXAMPLE: 
        Create a 2 channel signal
        [t, tone1] = mkTone(200,0.1,30,48000)
        [t, tone2] = mkTone(100,0.1,0,48000)
        combo = np.array([tone1, tone2])
        adjusted = setRMS(combo,-15)

        Written by: Travis M. Moore
        Created: Jan. 10, 2022
        Last edited: May 17, 2022
    """
    rmsdb = mag2db(rms(sig))
    refdb = amp
    diffdb = np.abs(rmsdb - refdb)
    if rmsdb > refdb:
        sigAdj = sig / db2mag(diffdb)
    elif rmsdb < refdb:
        sigAdj = sig * db2mag(diffdb)
    # Edit 5/17/22
    # Added handling for when rmsdb == refdb
    elif rmsdb == refdb:
        sigAdj = sig
    return sigAdj
    

########
# Tick #
########
# Load tick stimulus
_tick_path = r'C:\Users\MooTra\OneDrive - Starkey\Desktop\Tick\just the tick2.wav'
tick, fs = sf.read(_tick_path)

# Normalize tick stimulus
tick = tick / np.max(abs(tick))

# RMS of tick
tick_rms = rms(tick)
print(f"RMS of tick: {tick_rms}")


#############
# Pure tone #
#############
# Synthesize tone
t, tone = mkTone(1000, 30, 0, 48000)

# Gate tone
tone = doGate(tone, 0.04, 48000)

# RMS of tone
tone_rms = rms(tone)
print(f"Original RMS of tone: {tone_rms}")


#################
# Equalized RMS #
#################
# Calculate difference between RMS values
diff = tone_rms - tick_rms
print(f"RMS difference: {diff}")

# Set tone RMS to tick_rms
new_tone = setRMS(tone, mag2db(tick_rms))

new_tone_rms = rms(new_tone)
print(f"New RMS of tone: {new_tone_rms}")

plt.plot(new_tone)
plt.plot(tick)
plt.show()

sf.write('cal_stim.wav', new_tone, 48000)
