from style import setStyle
from common import *
import os, sys, re
import ROOT

setStyle()

#thresholds = [100]
#thresholds = [50,60,70,80,90,100,110,120]

#config_211_4_13_12_photek
#config_212_4_3_14_photek
#config_213_4_13_14_photek
#config_214_6_5_11_photek

# channel name, scope ch, adjacent channel, scope ch, config
infos=[]
infos.append([4 , 0, 14, 2, "config_212_4_3_14_photek"])
infos.append([4 , 0, 3 , 1, "config_212_4_3_14_photek"])
infos.append([4 , 0, 13, 1, "config_211_4_13_12_photek"])
infos.append([4 , 0, 4 , 0, "config_211_4_13_12_photek"])

def label(i,opt):
    label = "Track in " 
    if "hit" in opt: label = "Track & hit in " 
    if i==3: label+= "strip"
    elif i==2: label+= "1st adjacent strip"
    elif i==1: label+= "2nd adjacent strip"
    elif i==0: label+= "3rd adjacent strip"
    else : return ""
    return label 

def rebin(i,opt):
    if   i==3: rebin = 5 
    elif i==2: rebin = 5
    elif i==1: rebin = 5
    elif i==0: rebin = 5
    else : rebin = 0 
    return rebin 

def get_landau_charge(tree,ch,ch_name,adj_ch,adj_name,output,opt=""): 
    
    histname = "h_integral_ch_{}_track{}_in_{}".format(ch_name,opt,adj_name)
    hist = ROOT.TH1D(histname,";charge [fC]",70,0,30)

    print(ch,ch_name,adj_ch,adj_name)
    track_pos = in_strip(adj_name)
    integral = "-1000*integral[%i]*1e9*50/47000"%ch
    hit = "amp[%i]>110"%adj_ch 
    sel = "{}&&{}&&{}".format(photek,track_sel,track_pos)
    if "hit" in opt: sel = "{}&&{}&&{}".format(track_sel,track_pos,hit)
    
    tree.Project(histname,integral,sel)

    c = ROOT.TCanvas()
    hist.Draw()
    c.Print("plots/landau/charge_ch_{}_track{}_in_ch{}.pdf".format(ch_name,opt,adj_name))
    output.cd()
    hist.Write()

    return hist 


def plot_overlay_charge(infos,output,opt=""):
    
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("c","",800,800)
    c.SetLeftMargin(0.18)
    c.SetBottomMargin(0.15)
    leg = ROOT.TLegend(0.5,0.65,0.88,0.88)
    for i,info in enumerate(infos):  
        
        ch_name = info[0]
        adj_name = info[2]
    
        histname = "h_integral_ch_{}_track{}_in_{}".format(ch_name,opt,adj_name)
        hist = output.Get(histname)
        hist.Scale(1.0/hist.Integral(0,-1))
        hist.SetMaximum(0.4)
        hist.SetMinimum(0)
        hist.GetYaxis().SetTitle("Fraction of Events")
        hist.GetXaxis().SetTitle("Charge [fC]")
        hist.GetYaxis().SetNdivisions(505)
        hist.GetXaxis().SetNdivisions(505)
        hist.GetYaxis().SetTitleOffset(1.1)
        hist.SetTitle("")
        cleanHist(hist,i)

        if i==0: hist.Draw("hist")
        else: hist.Draw("histsame")
        
        leg.AddEntry(hist,label(i,opt),"l")

    leg.Draw()
    c.Print("plots/landau/plot_charge_ch_{}_track{}.pdf".format(ch_name,opt))

def get_landau(tree,ch,ch_name,adj_ch,adj_name,output,opt=""): 
    
    histname = "h_amp_ch_{}_track{}_in_{}".format(ch_name,opt,adj_name)
    hist = ROOT.TH1D(histname,";amplitude [mV]",240,0,1200)

    print(ch,ch_name,adj_ch,adj_name)
    track_pos = in_strip(adj_name)
    hit = "amp[%i]>100"%adj_ch 
    sel = "{}&&{}&&{}".format(photek,track_sel,track_pos)
    if "hit" in opt: sel = "{}&&{}&&{}".format(track_sel,track_pos,hit)
    
    tree.Project(histname,"amp[%i]"%ch,sel)

    c = ROOT.TCanvas()
    hist.Draw()
    c.Print("plots/landau/amp_ch_{}_track{}_in_ch{}.pdf".format(ch_name,opt,adj_name))
    output.cd()
    hist.Write()

    return hist 


def plot_overlay(infos,output,opt=""):
    
    ROOT.gStyle.SetOptStat(0)
    c = ROOT.TCanvas("c","",800,800)
    c.SetLeftMargin(0.18)
    c.SetBottomMargin(0.15)
    leg = ROOT.TLegend(0.3,0.65,0.88,0.88)
    leg.SetBorderSize(0)
    hists=[]
    for i,info in enumerate(infos):  
        
        ch_name = info[0]
        adj_name = info[2]
    
        histname = "h_amp_ch_{}_track{}_in_{}".format(ch_name,opt,adj_name)
        hist = output.Get(histname)
    
        if rebin(i,opt) != 0: hist.Rebin(rebin(i,opt)) 
        hist.Scale(1.0/hist.Integral(0,-1))
        hist.SetMaximum(1.0)
        #hist.SetMinimum(0)
        hist.SetMinimum(0.004)
        hist.GetYaxis().SetTitle("Fraction of Events")
        hist.GetXaxis().SetTitle("Amplitude [mV]")
        hist.GetYaxis().SetNdivisions(505)
        hist.GetXaxis().SetNdivisions(505)
        hist.GetYaxis().SetTitleOffset(1.2)
        hist.SetTitle("")
        cleanHist(hist,3-i)

        if i==0: hist.Draw("hist")
        else: hist.Draw("histsame")
        hists.append(hist)
        
    leg.AddEntry(hists[3],label(3,opt),"l")
    leg.AddEntry(hists[2],label(2,opt),"l")
    leg.AddEntry(hists[1],label(1,opt),"l")
    leg.AddEntry(hists[0],label(0,opt),"l")

    leg.Draw()
    c.SetLogy(1)
    c.Print("plots/landau/plot_amp_ch_{}_track{}.pdf".format(ch_name,opt))
    c.SetLogy(0)

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
        #get_landau(tree,ch,ch_name,adj_ch,adj_name,output,"hit") 
        #get_landau_charge(tree,ch,ch_name,adj_ch,adj_name,output) 
        #get_landau_charge(tree,ch,ch_name,adj_ch,adj_name,output,"hit") 
    

    return 

def make_plots():

    output = ROOT.TFile.Open("plots/landau/tmp.root")

    plot_overlay(infos,output)
    #plot_overlay(infos,output,"hit")
    #plot_overlay_charge(infos,output)
    #plot_overlay_charge(infos,output,"hit")

    return

# Main
if __name__ == "__main__":

    #make_histos()
    make_plots()
