from common import *
import os, sys, re
import ROOT

cfg = "config_211_4_13_12_photek"

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)

# in strip 4
ymin = 22.8
ymax = 24.2
xmin = 20.55-0.50 #20.3 
xmax = 20.55+0.50 #20.9 

minTpre = 2.8e-9
maxTpre = 3.8e-9
minT = -0.5e-9 
maxT = 0.5e-9

track_pos = "x_dut[{}]<{}&&x_dut[{}]>{}&&y_dut[{}]<{}&&y_dut[{}]>{}".format(dut,xmax,dut,xmin,dut,ymax,dut,ymin)

photek = "amp[3]>50 && amp[3]<250"

def waveforms(tree,ch,ch_name,output): 
    min_x = 20.45 
    max_x = 20.65 
    min_y = 22.8 
    max_y = 24.2
    ny=100

    region = "x_dut[{}]>{}&&x_dut[{}]<{}&&y_dut[{}]>{}&&y_dut[{}]<{}".format(dut,min_x,dut,max_x,dut,min_y,dut,max_y)
    
    sel="amp[0]>100&&amp[0]<110"

    c = ROOT.TCanvas()
    tree.Draw("channel[%i]:time[0]"%ch,"{}&&{}&&{}&&{}&&i_evt<10000".format(photek,track_sel,region,sel),"l")
    

    c.Print("plots/waveforms_xcheck/waves_ch{}.pdf".format(ch_name))
    output.cd()


    return hist 

def make_histos():
    # Loop through configurations 
    #


    output = ROOT.TFile.Open("plots/waveforms_xcheck/tmp.root","RECREATE")
    chs = [2,0,1]  
    ch_names = [12,4,13]

    tree = get_tree(cfg)

    waveforms(tree,0,4,output)

    return 

def make_plots():

    output = ROOT.TFile.Open("plots/waveforms_xcheck/tmp.root")

    return

# Main
if __name__ == "__main__":

    make_histos()
