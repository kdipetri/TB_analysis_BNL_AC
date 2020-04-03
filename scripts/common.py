import ROOT

dut=12
track_sel = "ntracks==1&&nplanes>15&&npix>2&&nback>0"

one   = ROOT.TColor(2001,0.906,0.153,0.094)
two   = ROOT.TColor(2002,0.906,0.533,0.094)
three = ROOT.TColor(2003,0.086,0.404,0.576)
four  = ROOT.TColor(2004,0.071,0.694,0.18)
five  = ROOT.TColor(2005,0.388,0.098,0.608)
six   = ROOT.TColor(2006,0.906,0.878,0.094)
colors = [1,2001,2002,2003,2004,2005,2006,6,2,3,4,6,7,5,1,8,9,29,38,46,1,2001,2002,2003,2004,2005,2006]

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

        rootfile = "root://cmseos.fnal.gov//store/group/cmstestbeam/2020_02_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6/run_scope{}_converted.root".format(run)
        tree.Add(rootfile)

    return tree

def in_strip(ch_name):
    ymin = 22.8
    ymax = 24.2

    if ch_name==14 : xcenter = 20.85
    if ch_name== 3 : xcenter = 20.75
    if ch_name==13 : xcenter = 20.65
    if ch_name== 4 : xcenter = 20.55
    if ch_name==12 : xcenter = 20.45
    if ch_name== 5 : xcenter = 20.35
    if ch_name==11 : xcenter = 20.25
    if ch_name== 6 : xcenter = 20.15
    width=0.02 # probably 0.4 total width 
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

def cleanHist(hist,i):
    name = hist.GetName()
    index=i
    #index=colorindex(name)
    hist.SetLineColor(colors[index])
    hist.SetMarkerColor(colors[index])
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
