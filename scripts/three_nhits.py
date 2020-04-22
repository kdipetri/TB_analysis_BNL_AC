from common import *
import os, sys, re
import ROOT


threshold = 110 #mV, noise threshold

cfg = "config_211_4_13_12_photek"

ymin = 22.8
ymax = 24.2
xmin = 20.55-0.05 #20.3 
xmax = 20.55+0.05 #20.9 

def n_hits(tree,output,opt=""):

    # for plot 
    nhits = "(amp[0]>110)+(amp[1]>110)+(amp[2]>110)"
    # for sel
    track_pos = "x_dut[{}]<{}&&x_dut[{}]>{}&&y_dut[{}]<{}&&y_dut[{}]>{}".format(dut,xmax,dut,xmin,dut,ymax,dut,ymin)
    photek = "amp[3]>50 && amp[3]<250"

    sel = "" 
    if opt == "photek" : sel = photek 
    if opt == "track_sel" : sel = "{}".format(track_sel) 
    if opt == "track_pos" : sel = "{}&&{}".format(track_sel,track_pos)
    if opt == "track_sel_photek" : sel = "{}&&{}".format(track_sel,photek)
    if opt == "track_pos_photek" : sel = "{}&&{}&&{}".format(track_sel,track_pos,photek)
    
    histname = "nhits_{}".format(opt)
    hist = ROOT.TH1F(histname,";Nhits;Events",4,-0.5,3.5)
    tree.Project(histname,nhits,sel)
    
    output.cd()
    hist.Write()
    print(sel)

    c = ROOT.TCanvas(histname)
    hist.Draw()
    c.Print("plots/three_efficiency/nhits_{}.pdf".format(opt))
    return 
    
    
def make_histos():
    # Loop through configurations 
    #


    output = ROOT.TFile.Open("plots/three_efficiency/tmp.root","RECREATE")
    chs = [2,0,1]  
    ch_names = [12,3,14]

    tree = get_tree(cfg)

    n_hits(tree,output) 
    n_hits(tree,output,"photek")
    n_hits(tree,output,"track_sel")
    n_hits(tree,output,"track_pos")
    n_hits(tree,output,"track_sel_photek")
    n_hits(tree,output,"track_pos_photek")

    return 

def make_plots():

    output = ROOT.TFile.Open("plots/three_efficiency/tmp.root")

    return

# Main
if __name__ == "__main__":

    make_histos()
    #make_plots()
