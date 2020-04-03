from style import setStyle
from common import *
import os, sys, re
import ROOT

setStyle()
dut=12

#thresholds = [100]
#thresholds = [50,60,70,80,90,100,110,120]

#config_211_4_13_12_photek
#config_212_4_3_14_photek
#config_213_4_13_14_photek
#config_214_6_5_11_photek

# channel name, scope ch, adjacent channel, scope ch, config
infos=[]
infos.append([4 , 0, 4 , 0, "config_211_4_13_12_photek"])
infos.append([4 , 0, 13, 1, "config_211_4_13_12_photek"])
infos.append([4 , 0, 3 , 1, "config_212_4_3_14_photek"])
infos.append([4 , 0, 14, 2, "config_212_4_3_14_photek"])

def get_landau(tree,ch,ch_name,adj_ch,adj_name,output,opt=""): 
    
    histname = "h_amp_ch_{}_track{}_in_{}".format(ch_name,opt,adj_name)
    hist = ROOT.TH1D(histname,";amplitude [mV]",70,0,1000)

    print(ch,ch_name,adj_ch,adj_name)
    track_pos = in_strip(adj_name)
    hit = "amp[%i]>100"%adj_ch 
    sel = "{}&&{}".format(track_sel,track_pos)
    if "hit" in opt: sel = "{}&&{}&&{}".format(track_sel,track_pos,hit)
    
    
    tree.Project(histname,"amp[%i]"%ch,sel)

    c = ROOT.TCanvas()
    hist.Draw()
    c.Print("plots/landau/amp_ch_{}_track{}_in_ch{}.pdf".format(ch_name,opt,adj_name))
    output.cd()
    hist.Write()

    return hist 

def label(i,opt):
    if i==0: 
        if "hit" in opt: return "Track & hit in strip"
        else : return "Track in strip"
    if i==1: return "in 1st adjacent strip"
    if i==2: return "in 2nd adjacent strip"
    if i==3: return "in 3rd adjacent strip"
    return ""

def plot_overlay(infos,output,opt=""):
    
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("c","",800,800)
    c.SetLeftMargin(0.18)
    c.SetBottomMargin(0.15)
    leg = ROOT.TLegend(0.5,0.65,0.88,0.88)
    for i,info in enumerate(infos):  
        
        ch_name = info[0]
        adj_name = info[2]
    
        histname = "h_amp_ch_{}_track{}_in_{}".format(ch_name,opt,adj_name)
        hist = output.Get(histname)
        hist.Scale(1.0/hist.Integral(0,-1))
        hist.SetMaximum(0.4)
        hist.SetMinimum(0)
        hist.GetYaxis().SetTitle("Fraction of Events")
        hist.GetXaxis().SetTitle("Amplitude [mV]")
        hist.GetYaxis().SetNdivisions(505)
        hist.GetXaxis().SetNdivisions(505)
        hist.GetYaxis().SetTitleOffset(1.1)
        hist.SetTitle("")
        cleanHist(hist,i)

        if i==0: hist.Draw("hist")
        else: hist.Draw("histsame")
        
        leg.AddEntry(hist,label(i,opt),"l")

    leg.Draw()
    c.Print("plots/landau/plot_amp_ch_{}_track{}.pdf".format(ch_name,opt))

def make_histos():
    # Loop through configurations 
    #


    output = ROOT.TFile.Open("plots/landau/tmp.root","RECREATE")
    
    for info in infos:
        ch_name = info[0]
        ch = info[1]
        adj_name = info[2]
        adj_ch = info[3]
        cfg = info[4]

        tree = get_tree(cfg)
        print(ch_name,cfg)

        get_landau(tree,ch,ch_name,adj_ch,adj_name,output) 
        get_landau(tree,ch,ch_name,adj_ch,adj_name,output,"hit") 
    

    return 

def make_plots():

    output = ROOT.TFile.Open("plots/landau/tmp.root")

    plot_overlay(infos,output)
    plot_overlay(infos,output,"hit")

    return

# Main
if __name__ == "__main__":

    #make_histos()
    make_plots()