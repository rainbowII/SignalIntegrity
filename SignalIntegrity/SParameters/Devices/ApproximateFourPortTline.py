'''
 Teledyne LeCroy Inc. ("COMPANY") CONFIDENTIAL
 Unpublished Copyright (c) 2015-2016 Peter J. Pupalaikis and Teledyne LeCroy,
 All Rights Reserved.

 Explicit license in accompanying README.txt file.  If you don't have that file
 or do not agree to the terms in that file, then you are not licensed to use
 this material whatsoever.
'''
from numpy import linalg

from SignalIntegrity.Conversions import S2T
from SignalIntegrity.Conversions import T2S
from SignalIntegrity.SParameters.SParameters import SParameters

class ApproximateFourPortTLine(SParameters):
    def __init__(self,f, Rp, Rsep, Lp, Gp, Cp, dfp,
                         Rn, Rsen, Ln, Gn, Cn, dfn,
                         Cm, dfm, Gm, Lm, Z0, K):
        self.m_K=K
        from SignalIntegrity.Devices import SeriesG
        from SignalIntegrity.Devices import SeriesZ
        from SignalIntegrity.Devices import TerminationG
        import SignalIntegrity.SParameters.Devices as dev
        from SignalIntegrity.SystemDescriptions.SystemSParametersNumeric import SystemSParametersNumeric
        self.m_sspn=SystemSParametersNumeric()
        self.m_spdl=[]
        self.m_sspn.AddDevice('rsep',2, self.m_spdl.append(('rsep',dev.SeriesRse(f,Rsep/K,Z0))))
        self.m_sspn.AddDevice('rp',2,SeriesZ(Rp/K,Z0))
        self.m_sspn.AddDevice('lp',2), self.m_spdl.append(('lp',dev.SeriesL(f,Lp/K,Z0)))
        self.m_sspn.AddDevice('gp',1,TerminationG(Gp/K,Z0))
        self.m_sspn.AddDevice('cp',1), self.m_spdl.append(('cp',dev.TerminationC(f,Cp/K,Z0,dfp)))
        self.m_sspn.AddDevice('rsen',2, self.m_spdl.append(('rsen',dev.SeriesRse(f,Rsen/K,Z0))))
        self.m_sspn.AddDevice('rn',2,SeriesZ(Rn/K,Z0))
        self.m_sspn.AddDevice('ln',2), self.m_spdl.append(('ln',dev.SeriesL(f,Ln/K,Z0)))
        self.m_sspn.AddDevice('gn',1,TerminationG(Gn/K,Z0))
        self.m_sspn.AddDevice('cn',1), self.m_spdl.append(('cn',dev.TerminationC(f,Cn/K,Z0,dfn)))
        self.m_sspn.AddDevice('lm',4), self.m_spdl.append(('lm',dev.Mutual(f,Lm/K,Z0)))
        self.m_sspn.AddDevice('gm',2,SeriesG(Gm/K,Z0))
        self.m_sspn.AddDevice('cm',2), self.m_spdl.append(('cm',dev.SeriesC(f,Cm/K,Z0,dfm)))
        self.m_sspn.ConnectDevicePort('rp',2,'rsep',1)
        self.m_sspn.ConnectDevicePort('rsep',2,'lp',1)
        self.m_sspn.ConnectDevicePort('rn',2,'rsen',1)
        self.m_sspn.ConnectDevicePort('rsen',2,'ln',1)
        self.m_sspn.ConnectDevicePort('lp',2,'lm',1)
        self.m_sspn.ConnectDevicePort('ln',2,'lm',3)
        self.m_sspn.ConnectDevicePort('lm',2,'gp',1)
        self.m_sspn.ConnectDevicePort('lm',2,'cp',1)
        self.m_sspn.ConnectDevicePort('lm',2,'gm',1)
        self.m_sspn.ConnectDevicePort('lm',2,'cm',1)
        self.m_sspn.ConnectDevicePort('lm',4,'gn',1)
        self.m_sspn.ConnectDevicePort('lm',4,'cn',1)
        self.m_sspn.ConnectDevicePort('lm',4,'gm',2)
        self.m_sspn.ConnectDevicePort('lm',4,'cm',2)
        self.m_sspn.AddPort('rp',1,1)
        self.m_sspn.AddPort('lm',2,2)
        self.m_sspn.AddPort('rn',1,3)
        self.m_sspn.AddPort('lm',4,4)
        self.lp=[1,3]
        self.rp=[2,4]
        SParameters.__init__(self,f,None,Z0)
    def __getitem__(self,n):
        for ds in self.m_spdl: self.m_sspn.AssignSParameters(ds[0],ds[1][n])
        sp=self.m_sspn.SParameters()
        if sp == 1: return sp
        return T2S(linalg.matrix_power(S2T(sp,self.lp,self.rp),self.m_K),self.lp,self.rp)
