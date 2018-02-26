class DeviceFactory(list):
...
    def __init__Contd(self):
        list.__init__(self,list(self+[
        ParserDevice('tline','2,4',False,{'zc':50.,'td':0.},True,
            "TLineLossless(f,ports,float(arg['zc']),float(arg['td']))"),
        ParserDevice('telegrapher',2,False,{'r':0.,'rse':0.,'l':0.,'c':0.,'df':0.,
            'g':0.,'z0':50.,'sect':0},True,"TLineTwoPortRLGC(f,\
            float(arg['r']),float(arg['rse']),float(arg['l']),float(arg['g']),\
            float(arg['c']),float(arg['df']),float(arg['z0']),int(arg['sect']))"),
        ParserDevice('telegrapher',4,False,{'rp':0.,'rsep':0.,'lp':0.,'cp':0.,'dfp':0.,
            'gp':0.,'rn':0.,'rsen':0.,'ln':0.,'cn':0.,'dfn':0.,'gn':0.,'lm':0.,
            'cm':0.,'dfm':0.,'gm':0.,'z0':50.,'sect':0},
            True,"TLineDifferentialRLGC(f, float(arg['rp']),float(arg['rsep']),\
            float(arg['lp']),float(arg['gp']),float(arg['cp']),float(arg['dfp']),\
            float(arg['rn']),float(arg['rsen']),float(arg['ln']),float(arg['gn']),\
            float(arg['cn']),float(arg['dfn']),float(arg['cm']),float(arg['dfm']),\
            float(arg['gm']),float(arg['lm']),float(arg['z0']),int(arg['sect']))"),
        ParserDevice('shortstd',1,False,{'od':0.,'oz0':50.,'ol':0.0,
            'l0':0.0,'l1':0.0,'l2':0.0,'l3':0.0},True,
            "ShortStandard(f,float(arg['od']),float(arg['oz0']),float(arg['ol']),\
            float(arg['l0']),float(arg['l1']),float(arg['l2']),float(arg['l3']))"),
        ParserDevice('openstd',1,False,{'od':0.,'oz0':50.,'ol':0.0,
            'c0':0.0,'c1':0.0,'c2':0.0,'c3':0.0},True,
            "OpenStandard(f,float(arg['od']),float(arg['oz0']),float(arg['ol']),\
            float(arg['c0']),float(arg['c1']),float(arg['c2']),float(arg['c3']))"),
        ParserDevice('loadstd',1,False,{'od':0.,'oz0':50.,'ol':0.0,'tz0':50.0},
            True,"LoadStandard(f,float(arg['od']),float(arg['oz0']),float(arg['ol']),\
            float(arg['tz0']))"),
        ParserDevice('thrustd',2,False,{'od':0.,'oz0':50.,'ol':0.0},
            True,"ThruStandard(f,float(arg['od']),float(arg['oz0']),float(arg['ol']))")
        ]))
...
