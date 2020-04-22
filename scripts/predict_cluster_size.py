import ROOT
import os, sys, re
from common import *

channels = [6,11,5,12,4,13,3,14]
rnd = ROOT.TRandom3()

f = ROOT.TFile.Open("plots/efficiency_v_x/tmp.root")


def has_hit(x,hist):
    eff = hist.GetBinContent(hist.GetXaxis().FindBin(x)) 
    if rnd.Rndm() < eff: return True 
    else: return False

def get_cluster_size(x,thresh,opt=""):
    
    nhits = 0
    hits = [0,0,0,0,0,0,0,0]
    
    for i,ch_name in enumerate(channels):  
        hist = f.Get("h_eff_{}_amp{}".format(ch_name,thresh))
        if opt=="3channels":
            if ch_name != 4 and ch_name!= 12 and ch_name!= 13: continue
            if has_hit(x,hist):
                nhits +=1
                hits[i] = 1
        else : 
            if has_hit(x,hist):
                nhits +=1
                hits[i] = 1
    
    nadjacent = 0
    ncurrent = 0
    for hit in hits:  
        # if hit update nadjacent_current
        if hit > 0 : ncurrent += 1  

        # if no hit reset nadjacent_current
        if hit == 0 : ncurrent = 0
    
        if ncurrent > nadjacent : nadjacent = ncurrent
        

    #print(nhits, nadjacent, hits)

    return nhits, nadjacent


def plot_cluster_size(x,thresh,opt=""):
    
    # for a fixed x 
    ntoys = 1000 
    
    hist_nhits = ROOT.TH1F("h_nhits_{}_{}_{}".format(x,thresh,opt),";N hits per event;Fraction of Events",9,-0.5,8.5)
    hist_nadjs = ROOT.TH1F("h_nadjs_{}_{}_{}".format(x,thresh,opt),";N hits per cluster;Fraction of Events",9,-0.5,8.5)
    hist_hits_v_cluster = ROOT.TH2F("h_nhits_v_nadj_{}_{}_{}".format(x,thresh,opt),";N hits per cluster;N hits per event;Events",9,-0.5,8.5,9,-0.5,8.5)

    for toy in range(0,ntoys):
        nhits,nadj = get_cluster_size(x,thresh,opt)
        hist_nhits.Fill(nhits)
        hist_nadjs.Fill(nadj)
        
        hist_hits_v_cluster.Fill(nadj,nhits)

    hist_nhits.Scale(1.0/hist_nhits.Integral(0,-1))
    hist_nadjs.Scale(1.0/hist_nadjs.Integral(0,-1))

    c = ROOT.TCanvas()
    hist_nhits.Draw("histe")
    c.Print("plots/cluster/nhits_total_{}_{}_{}.pdf".format(x,thresh,opt))
    hist_nadjs.Draw("histe")
    c.Print("plots/cluster/cluster_size__{}_{}_{}.pdf".format(x,thresh,opt))

    hist_hits_v_cluster.Draw("COLZ")
    c.Print("plots/cluster/2D_nhits_v_cluster_size_{}_{}_{}.pdf".format(x,thresh,opt))
    
    return hist_nadjs

def scan_cluster_size(opt=""):    
   
    thresh=110
    xs = [ 20.50 + 0.02*i for i in range(0,6)] 
    hists = []
    ymax = 0
    for i,x in enumerate(xs): 
        hist = plot_cluster_size(x,thresh,opt) 
        hists.append(hist)
        cleanHist(hist,i)
        if hist.GetMaximum() > ymax: ymax = hist.GetMaximum()
        
    c = ROOT.TCanvas()
    leg = ROOT.TLegend(0.6,0.5,0.88,0.88)
    for i,x in enumerate(xs):
        leg.AddEntry(hists[i],"x = {} mm".format(x),"l")
        hists[i].SetMaximum(1.1*ymax)
        if i==0: hists[i].Draw("hist e")
        else : hists[i].Draw("hist e same")
    leg.Draw()
    c.Print("plots/cluster/scan_x_thresh_{}_{}.pdf".format(thresh,opt))

    return

def scan_cluster_threshold(opt=""):    
   
    x = 20.55
    thresholds = range(80,130,10) 
    hists = []
    ymax = 0
    for i,thresh in enumerate(thresholds): 
        hist = plot_cluster_size(x,thresh,opt) 
        hists.append(hist)
        cleanHist(hist,i)
        if hist.GetMaximum() > ymax: ymax = hist.GetMaximum()
        
    c = ROOT.TCanvas()
    leg = ROOT.TLegend(0.6,0.5,0.88,0.88)
    for i,thresh in enumerate(thresholds):
        leg.AddEntry(hists[i],"amp > {} mV".format(thresh),"l")
        hists[i].SetMaximum(1.1*ymax)
        if i==0: hists[i].Draw("hist e")
        else : hists[i].Draw("hist e same")
    leg.Draw()
    c.Print("plots/cluster/scan_thresh_x_{}_{}.pdf".format(x,opt))

    return
    
ROOT.gStyle.SetOptFit(0)
ROOT.gStyle.SetOptStat(0)

# position 
# in 4 - 20.55 
# in between 4 and 13 - 20.6
#plot_cluster_size(20.55,100)
#plot_cluster_size(20.60,100)

scan_cluster_size()
scan_cluster_threshold()
scan_cluster_size("3channels")
scan_cluster_threshold("3channels")
