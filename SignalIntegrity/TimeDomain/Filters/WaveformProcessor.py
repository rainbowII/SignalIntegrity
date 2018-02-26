# Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
# Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
# All Rights Reserved.
# 
# Explicit license in accompanying README.txt file.  If you don't have that file
# or do not agree to the terms in that file, then you are not licensed to use
# this material whatsoever.

class WaveformProcessor(object):
    """base class for things that process waveforms"""
    def ProcessWaveform(self,wf):
        """function to be overloaded in a waveform processor

        if not overloaded, will simply return the waveform, unprocessed
        """
        return wf