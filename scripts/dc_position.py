from common import *
import os, sys, re
import ROOT

ROOT.gStyle.SetOptStat(0)
def draw_position(tree,ch,ch_name,minAmp,output):

    nx = 70
    ny = 70
    xmin = 19 
    xmax = 22 
    ymin = 22 
    ymax = 25

    #track_sel = "ntracks==1&&npix>0&&nback>0"
    dist = "amp[{}]>{}:y_dut[{}]:x_dut[{}]".format(ch,minAmp,dut,dut)
    hist = "({},{},{},{},{},{})".format(nx,xmin,xmax,ny,ymin,ymax)
    sel = "{}&&{}".format(track_sel,photek)
    
    c = ROOT.TCanvas("ch{}_amp{}_xy".format(ch_name,minAmp),"",800,800)
    tree.Draw("{}>>{}".format(dist,hist),sel,"PROFCOLZ")

    
    c.Print("plots/dc_position/ch{}_amp{}_xy.pdf".format(ch_name,minAmp))

    return 


def make_histos():
    # Loop through configurations 
    #

    output = ROOT.TFile.Open("plots/dc_position/tmp.root","RECREATE")
    
    cfg = "config_209_4_13_DC_photek"
    ch_names = [4,13,"DC"]

    tree = get_tree(cfg)

    draw_position(tree,2,"DC",11,output)
    draw_position(tree,2,"DC",12,output)
    draw_position(tree,2,"DC",20,output)
    draw_position(tree,2,"DC",30,output)

    #for ch in range(0,3):
        #draw_amplitude(tree,ch,ch_names[ch],output,"low")
        #draw_charge(tree,ch,ch_names[ch],output,"low")
    
    return 

make_histos()
