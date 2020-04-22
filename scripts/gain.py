from common import *
import os, sys, re
import ROOT

def draw_amplitude(tree,ch,ch_name,output,opt): 
    

    histname = "h_amp_{}".format(ch_name)
    if opt == "low" : 
        hist = ROOT.TH1D(histname,";amplitude [mV]",100,0,200)
        sel = photek + "&& amp[%i]>11"%ch
    else            : 
        hist = ROOT.TH1D(histname,";amplitude [mV]",100,0,2000)
        sel = photek + "&& amp[%i]>110"%ch

    plot = "amp[%i]"%ch

    tree.Project(histname,plot,sel)

    c = ROOT.TCanvas()
    hist.Draw()
    c.Print("plots/gain/amp_{}_{}.pdf".format(ch_name,opt))

    output.cd()
    hist.Write()
    return

def draw_charge(tree,ch,ch_name,output,opt): 
    

    histname = "h_integral_{}".format(ch_name)
    hist = ROOT.TH1D(histname,";charge [fC]",100,0,30)
    if opt == "low" : 
        charge = "-1000*integral[%i]*1e9*50/4700"%ch 
        sel = photek + "&& amp[%i]>11"%ch 
    else            : 
        charge = "-1000*integral[%i]*1e9*50/47000"%ch 
        sel = photek + "&& amp[%i]>110"%ch  


    tree.Project(histname,charge,sel)

    c = ROOT.TCanvas()
    hist.Draw()
    c.Print("plots/gain/charge_{}_{}.pdf".format(ch_name,opt))

    output.cd()
    hist.Write()
    return

def make_histos():
    # Loop through configurations 
    #

    output = ROOT.TFile.Open("plots/gain/tmp.root","RECREATE")
    
    cfg = "config_209_4_13_DC_photek"
    ch_names = [4,13,"DC"]

    tree = get_tree(cfg)

    for ch in range(0,3):
        draw_amplitude(tree,ch,ch_names[ch],output,"low")
        draw_charge(tree,ch,ch_names[ch],output,"low")

    cfg = "config_211_4_13_12_photek"
    ch_names = [4,13,12]

    tree = get_tree(cfg)

    for ch in range(0,3):
        draw_amplitude(tree,ch,ch_names[ch],output,"high")
        draw_charge(tree,ch,ch_names[ch],output,"high")
    
    return 

make_histos()
