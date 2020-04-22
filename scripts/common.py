import ROOT

dut=12
track_sel = "ntracks==1&&nplanes>15&&npix>2&&nback>1&&abs(yResidBack)<500&&abs(xResidBack)<500"
photek = "amp[3]>50&&amp[3]<250"

one   = ROOT.TColor(2001,0.906,0.153,0.094)
two   = ROOT.TColor(2002,0.906,0.533,0.094)
three = ROOT.TColor(2003,0.086,0.404,0.576)
four  = ROOT.TColor(2004,0.071,0.694,0.18)
five  = ROOT.TColor(2005,0.388,0.098,0.608)
six   = ROOT.TColor(2006,0.906,0.878,0.094)
colors = [1,2001,2002,2003,2004,2005,2006,6,2,3,4,6,7,5,1,8,9,29,38,46,1,2001,2002,2003,2004,2005,2006]

colors_blue = []
colors_blue.append(ROOT.kViolet+3)
colors_blue.append(ROOT.kViolet+4)
colors_blue.append(ROOT.kViolet+2)
colors_blue.append(ROOT.kViolet+1)
colors_blue.append(ROOT.kViolet+6)
colors_blue.append(ROOT.kAzure+6)
colors_blue.append(ROOT.kAzure+5)
colors_blue.append(ROOT.kAzure+4)
colors_blue.append(ROOT.kAzure+3)
colors_blue.append(ROOT.kBlue+3)
colors_blue.append(ROOT.kBlue+4)

def get_t0(ch_name):
    if ch_name==4 : return 3.293#in ns
    if ch_name==5 : return 3.320#in ns
    if ch_name==6 : return 3.232#in ns
    if ch_name==11: return 3.284#in ns
    if ch_name==12: return 3.346#in ns
    if ch_name==13: return 3.333#in ns

def get_tree(cfg):
    
    # Open config file, get runs
    runs = []
    cfg_file = open("configs/{}.txt".format(cfg),"r")
    for line in cfg_file: 
        if "#" in line: continue
        run = line.strip()
        #print(run)
        runs.append(run)
    cfg_file.close()
    
    # Fill TChain
    tree = ROOT.TChain("pulse")
    for i,run in enumerate(runs):

        if int(run) <= 29100: version="v5"
        else : version="v6"
        rootfile = "root://cmseos.fnal.gov//store/group/cmstestbeam/2020_02_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/{}/run_scope{}_converted.root".format(version,run)
        tree.Add(rootfile)

    return tree

def strip_x(ch_name):
    if   ch_name==14 : xcenter = 20.85
    elif ch_name== 3 : xcenter = 20.75
    elif ch_name==13 : xcenter = 20.65
    elif ch_name== 4 : xcenter = 20.55
    elif ch_name==12 : xcenter = 20.45
    elif ch_name== 5 : xcenter = 20.35
    elif ch_name==11 : xcenter = 20.25
    elif ch_name== 6 : xcenter = 20.15
    else : xcenter = -99
    return xcenter

def in_strip(ch_name):
    ymin = 22.8
    ymax = 24.2
    
    xcenter = strip_x(ch_name)
    
    width=0.02 # +/-0.04 gives actual strip width 
    xmin = xcenter-width
    xmax = xcenter+width
    strip = "x_dut[{}]<{}&&x_dut[{}]>{}&&y_dut[{}]<{}&&y_dut[{}]>{}".format(dut,xmax,dut,xmin,dut,ymax,dut,ymin)
    return strip 


def cleanFit(fit,i):
    name = fit.GetName()
    index=i
    fit.SetLineColor(colors[index])
    #fit.SetLineWidth(size)
    return 

def cleanHist(hist,i,opt=""):
    name = hist.GetName()
    index=i
    #index=colorindex(name)
    col = colors[index]
    if "blue" in opt: col = colors_blue[index]
    hist.SetLineColor(col)
    hist.SetMarkerColor(col)
    size, style = 1.0, 20
    #if ucsc : style += 1
    #if cold : style += 4  
    #if dis : style+=1
    hist.SetMarkerSize(size)
    hist.SetMarkerStyle(style)
    return 


def setStyle():
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    ROOT.gROOT.ProcessLine( "gErrorIgnoreLevel = 1001;")
    #ROOT.Math.MinimizerOptions.SetPrintLevel(-1) # turn off print output? 
    ROOT.gStyle.SetLabelFont(42,"xyz")
    ROOT.gStyle.SetLabelSize(0.05,"xyz")
    ROOT.gStyle.SetTitleFont(42,"xyz")
    ROOT.gStyle.SetTitleFont(42,"t")
    ROOT.gStyle.SetTitleSize(0.06,"xyz")
    ROOT.gStyle.SetTitleSize(0.06,"t")
    ROOT.gStyle.SetPadBottomMargin(0.14)
    ROOT.gStyle.SetPadLeftMargin(0.14)
    ROOT.gStyle.SetTitleOffset(1,'y')
    ROOT.gStyle.SetLegendTextSize(0.035)
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetGridColor(14)
    ROOT.gStyle.SetOptFit(1)
    return 

setStyle()
