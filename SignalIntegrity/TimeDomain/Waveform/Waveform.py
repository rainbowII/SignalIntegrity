# Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
# Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
# All Rights Reserved.
# 
# Explicit license in accompanying README.txt file.  If you don't have that file
# or do not agree to the terms in that file, then you are not licensed to use
# this material whatsoever.

from copy import copy

from TimeDescriptor import TimeDescriptor
from AdaptedWaveforms import AdaptedWaveforms
from SignalIntegrity.PySIException import PySIExceptionWaveformFile,PySIExceptionWaveform

class Waveform(list):
    """base class for all waveforms"""
    adaptionStrategy='SinX'
    def __init__(self,x=None,y=None):
        """constructor
        @param x instance of class Waveform or TimeDescriptor
        @param y instance of float, int, or complex or list of such
        
        @note here are the outcomes for this constructor:
        
        |x type          |y type             |outcome                                            |
        |:--------------:|:-----------------:|:------------------------------------------------- |
        | Waveform       | don't care        | waveform is x provided (copy constructor)         |
        | TimeDescriptor | list              | waveform with td=x and values in list provided    |
        | TimeDescriptor | int,float,complex | waveform with td=x and list of constants provided |
        | TimeDescriptor | None              | waveform with td=x and list of zeros              |
        | other (None)   | don't care (None) | empty, uninitialized waveform                     |
        """
        if isinstance(x,Waveform):
            self.td=x.td
            list.__init__(self,x)
        elif isinstance(x,TimeDescriptor):
            self.td=x
            if isinstance(y,list):
                list.__init__(self,y)
            elif isinstance(y,(float,int,complex)):
                list.__init__(self,[y.real for _ in range(x.K)])
            else:
                list.__init__(self,[0 for _ in range(x.K)])
        else:
            self.td=None
            list.__init__(self,[])
    def Times(self,unit=None):
        """time values
        @param unit (optional) string containing unit for time values.
        @return list of time values
        @see TimeDescriptor for valid time units and return type.
        """
        return self.td.Times(unit)
    def TimeDescriptor(self):
        """time descriptor
        @return instance of class TimeDescriptor inherent to the waveform"""
        return self.td
    def Values(self,unit=None):
        """values
        returns the list of waveform values
        @param unit (optional) string containing unit for values in list
        @note valid waveform units are:
        - None - simple list of values returned
        -'abs' - list of absolute values returned
        """ 
        if unit==None:
            return list(self)
        elif unit =='abs':
            return [abs(y) for y in self]
    def OffsetBy(self,v):
        """offset by a dc value
        @param v float amount to offset the waveform by
        @return self
        @todo this is inconsistent and should be removed
        """
        list.__init__(self,[y+v for y in self])
        return self
    def DelayBy(self,d):
        """delay waveform
        @param d float amount to delay by
        @return instance of class waveform containing self delay by d
        @note does not affect self
        """
        return Waveform(self.td.DelayBy(d),self.Values())
    def __add__(self,other):
        """overloads +
        @param other instance of class Waveform or float, int, complex to add.
        @return instance of class Waveform with other added to self
        @note does not affect self
        @note
        valid types of other to add are:

        - Waveform - if the other waveform has the same time descriptor, returns the waveform
        with self and others values added together, otherwise adapts other to self and then
        adds them.
        - float,int,complex - adds the constant value to all values in self.
        @throw PySIExceptionWaveform if other cannot be added.
        @see AdaptedWaveforms
        """
        if isinstance(other,Waveform):
            if self.td == other.td:
                return Waveform(self.td,[self[k]+other[k] for k in range(len(self))])
            else:
                [s,o]=AdaptedWaveforms([self,other])
                return Waveform(s.td,[s[k]+o[k] for k in range(len(s))])
                #return awf[0]+awf[1]
        elif isinstance(other,(float,int,complex)):
            return Waveform(self.td,[v+other.real for v in self])
        # pragma: silent exclude
        else:
            raise PySIExceptionWaveform('cannot add waveform to type '+str(other.__class__.__name__))
        # pragma: include
    def __sub__(self,other):
        """overloads -
        @param other instance of class Waveform or float, int, complex to subtract.
        @return instance of class Waveform with other subtracted from self
        @note does not affect self
        @note
        valid types of other to subtract are:

        - Waveform - if the other waveform has the same time descriptor, returns the waveform
        with self and others values subtracted, otherwise adapts other to self and then
        subtracts them.
        - float,int,complex - subtracts the constant value from all values in self.
        @throw PySIExceptionWaveform if other cannot be subtracted.
        @see AdaptedWaveforms
        """
        if isinstance(other,Waveform):
            if self.td == other.td:
                return Waveform(self.td,[self[k]-other[k] for k in range(len(self))])
            else:
                [s,o]=AdaptedWaveforms([self,other])
                return Waveform(s.td,[s[k]-o[k] for k in range(len(s))])
        elif isinstance(other,(float,int,complex)):
            return Waveform(self.td,[v-other.real for v in self])
        # pragma: silent exclude
        else:
            raise PySIExceptionWaveform('cannot subtract type' + +str(other.__class__.__name__) + ' from waveform')
        # pragma: include
    def __radd__(self, other):
        """radd version
        this is used for summing waveforms in a list and is required.
        @param other instance of class Waveform or float, int, complex to add.
        @return self+other
        @see Waveform.__add__()
        """
        if other is 0:
            return Waveform(self)
        else:
            return self.__add__(other)
    def __mul__(self,other):
        """overloads *
        @param other instance of class WaveformProcessor or float, int, complex to multiply by.
        @return instance of class Waveform with other multiplied by self
        @note does not affect self
        @note Waveform multiplication is an abstraction in some cases. The result for types
        of other is:
        - WaveformProcessor - returns self processed by the instance of WaveformProcessor.
        - float,int,complex - returns the Waveform produced by multiplying all of the values in
        self multiplied by the constant value supplied.
        @note The most obvious type of WaveformProcessor is a FirFilter, but there are others like
        WaveformTrimmer and WaveformDecimator.
        @throw PySIExceptionWaveform if other cannot be multiplied.
        """
        # pragma: silent exclude
        from SignalIntegrity.TimeDomain.Filters.WaveformProcessor import WaveformProcessor
        # pragma: include
        if isinstance(other,WaveformProcessor):
            return other.ProcessWaveform(self)
        elif isinstance(other,(float,int,complex)):
            return Waveform(self.td,[v*other.real for v in self])
        # pragma: silent exclude
        else:
            raise PySIExceptionWaveform('cannot multiply waveform by type '+str(other.__class__.__name__))
        # pragma: include
    def __div__(self,other):
        """overloads /
        @param other instance of float, int, complex to divide by.
        @return instance of class Waveform with other divided into it.
        @note only handles float, int, complex where the constant values are divided into the
        values in self.
        @note should consider allowing a two waveforms to be divided, but frankly never came
        upon the need for that.
        @throw PySIExceptionWaveform if other cannot be multiplied.
        """
        if isinstance(other,(float,int,complex)):
            return Waveform(self.td,[v/other.real for v in self])
        # pragma: silent exclude
        else:
            raise PySIExceptionWaveform('cannot divide waveform by type '+str(other.__class__.__name__))
        # pragma: include
    def ReadFromFile(self,fileName):
        """reads a waveform from a file
        @param fileName string name of file to read
        @return self
        @note this DOES affect self
        """
        # pragma: silent exclude outdent
        try:
        # pragma: include
            with open(fileName,"rU") as f:
                data=f.readlines()
                HorOffset=float(data[0])
                NumPts=int(float(data[1])+0.5)
                SampleRate=float(data[2])
                Values=[float(data[k+3]) for k in range(NumPts)]
            self.td=TimeDescriptor(HorOffset,NumPts,SampleRate)
            list.__init__(self,Values)
        # pragma: silent exclude indent
        except IOError:
            raise PySIExceptionWaveformFile(fileName+' not found')
        # pragma: include
        return self
    def WriteToFile(self,fileName):
        """writes a waveform to a file
        @param fileName string name of file to write
        @return self
        """
        with open(fileName,"w") as f:
            td=self.td
            f.write(str(td.H)+'\n')
            f.write(str(int(td.K))+'\n')
            f.write(str(td.Fs)+'\n')
            for v in self:
                f.write(str(v)+'\n')
        return self
    def __eq__(self,other):
        """overloads ==
        @param other instance of other waveform.
        @return boolean whether the waveforms are equal to each other.
        @note an epsilon of 1e-6 is used for the compare.
        """
        if self.td != other.td:
            return False
        if len(self) != len(other):
            return False
        for k in range(len(self)):
            if abs(self[k]-other[k])>1e-6:
                return False
        return True
    def __ne__(self,other):
        """overloads !=
        @param other instance of other waveform.
        @return boolean whether the waveforms are not equal to each other.
        """
        return not self == other
    def Adapt(self,td):
        """adapts waveform to time descriptor

        Waveform adaption is performed using upsampling, decimation, fractional delay,
        and waveform point trimming.

        @param td instance of class TimeDescriptor to adapt waveform to
        @return instance of class Waveform containing self adapted to the time descriptor
        @note does not affect self.
        @note the static member variable adaptionStrategy determines how to interpolate.  'SinX' means
        to use sinx/x interpolation, 'Linear' means to use linear interpolation.
        @see InterpolatorSinX
        @see SignalIntegrity.TimeDomain.Filters.InterpolatorSinX.FractionalDelayFilterSinX
        @see SignalIntegrity.TimeDomain.Filters.InterpolatorSinX.FractionalDelayFilterSinX
        @see SignalIntegrity.TimeDomain.Filters.InterpolatorLinear.InterpolatorLinear
        @see SignalIntegrity.TimeDomain.Filters.InterpolatorLinear.FractionalDelayFilterLinear
        @see SignalIntegrity.TimeDomain.Filters.WaveformTrimmer.WaveformTrimmer
        @see SignalIntegrity.TimeDomain.Filters.WaveformDecimator.WaveformDecimator
        @see SignalIntegrity.Rat.Rat

        """
        # pragma: silent exclude
        from SignalIntegrity.TimeDomain.Filters.InterpolatorSinX import InterpolatorSinX
        from SignalIntegrity.TimeDomain.Filters.InterpolatorSinX import FractionalDelayFilterSinX
        from SignalIntegrity.TimeDomain.Filters.InterpolatorLinear import InterpolatorLinear
        from SignalIntegrity.TimeDomain.Filters.InterpolatorLinear import FractionalDelayFilterLinear
        from SignalIntegrity.TimeDomain.Filters.WaveformTrimmer import WaveformTrimmer
        from SignalIntegrity.TimeDomain.Filters.WaveformDecimator import WaveformDecimator
        from SignalIntegrity.Rat import Rat
        # pragma: include
        wf=self
        (upsampleFactor,decimationFactor)=Rat(td.Fs/wf.td.Fs)
        if upsampleFactor>1:
            wf=wf*(InterpolatorSinX(upsampleFactor) if wf.adaptionStrategy=='SinX'
                else InterpolatorLinear(upsampleFactor))
        ad=td/wf.td
        f=ad.D-int(ad.D)
        if not f==0.0:
            wf=wf*(FractionalDelayFilterSinX(f,True) if wf.adaptionStrategy=='SinX'
                else FractionalDelayFilterLinear(f,True))
            ad=td/wf.td
        if decimationFactor>1:
            decimationPhase=int(round(ad.TrimLeft())) % decimationFactor
            wf=wf*WaveformDecimator(decimationFactor,decimationPhase)
            ad=td/wf.td
        tr=WaveformTrimmer(max(0,int(round(ad.TrimLeft()))),
                           max(0,int(round(ad.TrimRight()))))
        wf=wf*tr
        return wf
    def Measure(self,time):
        """measures a value at a given time
        @param time float time to measure the value at.
        @return value at time specified
        @note will return None if time is not within the waveform
        @note linearly interpolates nearest point
        @todo this function can use a little work in providing some safety.
        """
        for k in range(len(self.td)):
            if self.td[k] > time:
                v = (time - self.td[k-1])/(self.td[k]-self.td[k-1])*\
                (self[k]-self[k-1])+self[k-1]
                return v
    def FrequencyContent(self,fd=None):
        """frequency content
        provides the frequency content equivalent of the waveform.
        @param fd (optional) instance of class FrequencyList providing
        frequencies to provide the content for (defaults to None)
        @return instance of class FrequencyContent containing the frequency content of the
        waveform.
        @note if None is supplied for fd, the frequency content is provided using the frequency
        list corresponding to the time descriptor inherent to the waveform.  In this way,
        self.FrequencyContent().Waveform() equals self.
        @see SignalIntegrity.FrequencyDomain.FrequencyContent
        @see SignalIntegrity.FrequencyDomain.FrequencyList
        """
        # pragma: silent exclude
        from SignalIntegrity.FrequencyDomain.FrequencyContent import FrequencyContent
        # pragma: include
        return FrequencyContent(self,fd)
    def Integral(self,c=0.,addPoint=True,scale=True):
        """integral of waveform

        the integral is calculated using Riemann sums (as opposed to trapezoidal
        integration.

        @param c (optional) float value to add to the integral waveform
        @param addPoint (optional) boolean whether to add a point to the waveform before
        the first point.  the value added is c.
        @param scale (optional) boolean whether to multiply each sum by the sample period
        providing a true integral.  Otherwise, the values are simply summed.
        """
        td=copy(self.td)
        i=[0 for k in range(len(self))]
        T=1./td.Fs if scale else 1.
        for k in range(len(i)):
            if k==0:
                i[k]=self[k]*T+c
            else:
                i[k]=i[k-1]+self[k]*T
        td.H=td.H+(1./2.)*(1./td.Fs)
        if addPoint:
            td.K=td.K+1
            td.H=td.H=td.H-1./td.Fs
            i=[c]+i
        return Waveform(td,i)
    def Derivative(self,c=0.,removePoint=True,scale=True):
        """derivative of waveform

        the derivative is calculated using the difference divided by the sample period.

        @param c (optional) this value is superfluous and not used.
        @param removePoint (optional) boolean whether to remove the first point.  If the
        first point is not removed, it is zero.
        @param scale (optional) boolean whether to divide each difference by the sample period
        providing a true derivative.  Otherwise, the values are simply subtracted.
        @todo remove argument c.
        """
        td=copy(self.td)
        vl=copy(self)
        T=1./td.Fs if scale else 1.
        for k in range(len(vl)):
            if k==0:
                vl[k]=0.
            else:
                vl[k]=(self[k]-self[k-1])/T
        td.H=td.H-(1./2.)*(1./td.Fs)
        if removePoint:
            td.K=td.K-1
            td.H=td.H+1./td.Fs
            vl=vl[1:]
        return Waveform(td,vl)

class WaveformFileAmplitudeOnly(Waveform):
    def __init__(self,fileName,td=None):
        if not td is None:
            HorOffset=td.H
            NumPts=td.K
            SampleRate=td.Fs
        else:
            HorOffset=0.0
            NumPts=0
            SampleRate=1.
        with open(fileName,'rb') as f:
            wf = [float(line) for line in f]
        if NumPts==0:
            NumPts=len(wf)
        else:
            if len(wf) > NumPts:
                wf = [wf[k] for k in range(NumPts)]
            else:
                NumPts=len(wf)
        Waveform.__init__(self,TimeDescriptor(HorOffset,NumPts,SampleRate),wf)