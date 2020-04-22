from common import *
import os, sys, re
import ROOT


threshold = 110 #mV, noise threshold

cfg = "config_211_4_13_12_photek"

# in strip 4
ymin = 22.8
ymax = 24.2
xmin = 20.55-0.3 #20.3 
xmax = 20.55+0.3 #20.9 

minTpre = 2.8e-9
maxTpre = 3.8e-9
minT = -0.5e-9 
maxT = 0.5e-9

nhits = "(amp[0]>%i)+(amp[1]>%i)+(amp[2]>%i)"%(threshold,threshold,threshold)
nhits_1 = nhits+"==1" 
nhits_2 = nhits+"==2"
nhits_3 = nhits+"==3"

track_pos = "x_dut[{}]<{}&&x_dut[{}]>{}&&y_dut[{}]<{}&&y_dut[{}]>{}".format(dut,xmax,dut,xmin,dut,ymax,dut,ymin)

def get_channel(ch_name):
    if ch_name ==  4: return 0
    if ch_name == 13: return 1 
    if ch_name == 12: return 2 
    if ch_name ==  "4": return 0
    if ch_name == "13": return 1 
    if ch_name == "12": return 2 
    return -1

def col_index(ch_name):
    if ch_name ==  4: return 1
    if ch_name == 13: return 2 
    if ch_name == 12: return 3 
    if ch_name ==  "4": return 1
    if ch_name == "13": return 2 
    if ch_name == "12": return 3 
    return 0

def plot_v_x(tree,selection,ch,ch_name,output):

    # setup
    histname = "h_{}_v_x_ch{}".format(selection,ch_name)
    sel = photek + "&&" + track_sel + "&&" + track_pos
    #sel = photek + "&& amp[%i]>%i"%(ch,threshold) + "&&" + track_sel + "&&" + track_pos

    plot = "amp[%i]:x_dut[%i]"%(ch,dut)
    nY, minY , maxY = 100, 0, 2000
    axis = ";x [mm];amplitude [mV]"
    if "charge" in selection:
        plot = "-1000*integral[%i]*1e9*50/47000:x_dut[%i]"%(ch,dut)
        nY, minY , maxY = 100, 0, 25
        axis = ";x [mm];charge [fC]"
    elif "2hitCR" in selection: 
        ch1 = get_channel(selection.split("_")[1])
        ch2 = get_channel(selection.split("_")[2])
        print(selection,ch1,ch2)
        plot = "amp[%i]/amp[%i]:x_dut[%i]"%(ch1,ch2,dut)
        sel += "&& amp[%i]>%i && amp[%i]>%i"%(ch1,threshold,ch2,threshold) 
        sel += "&& {}".format(nhits_2) 
        axis = ";x [mm];amplitude ratio"
        nY ,minY , maxY = 80, 0, 10 
    elif "3hitCR" in selection: 
        ch1 = get_channel(selection.split("_")[1])
        ch2 = get_channel(selection.split("_")[2])
        print(selection,ch1,ch2)
        plot = "amp[%i]/amp[%i]:x_dut[%i]"%(ch1,ch2,dut)
        sel += "&& amp[0]>%i && amp[1]>%i && amp[2]>%i"%(threshold,threshold,threshold) 
        sel += "&& {}".format(nhits_3) 
        axis = ";x [mm];amplitude ratio"
        nY , minY , maxY = 80, 0, 10 

    # fill hist
    hist = ROOT.TH2F(histname,axis,100,xmin,xmax,nY,minY,maxY)
    tree.Project(histname,plot,sel,"COLZ")

    # do profile
    profile = hist.ProfileX("{}_prof".format(histname))
    profile.SetMarkerStyle(20);
    profile.SetMarkerSize(0.8);
    profile.SetMarkerColor(ROOT.kBlack);
    profile.SetLineColor(ROOT.kBlack);
    profile.SetLineWidth(1);

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    profile.Draw("same")
    c.Print("plots/three_position/ch{}_{}_v_x.pdf".format(ch_name,selection))

    output.cd()
    hist.Write()
    profile.Write()
    
    return 

def charge_overlay( output ):
    hists = [] 
    channels = [13,4,12]
    ymax = 0
    for ch in channels:  
        hist = output.Get("h_charge_v_x_ch{}_prof".format(ch))
        #for b in range(0,hist.GetNbinsX()+1):
        #    if hist.GetBinError(b)> 50: 
        #        hist.SetBinContent(b,0)
        #        hist.SetBinError(b,0)
        if hist.GetMaximum() > ymax : ymax = hist.GetMaximum()
        hists.append(hist)

    c = ROOT.TCanvas("charge_overlay")
    leg = ROOT.TLegend(0.6,0.7,0.88,0.88)
    for i,hist in enumerate(hists) :
        cleanHist(hist,col_index(channels[i]))
        leg.AddEntry(hist,"Channel {}".format(channels[i]))
        if i==0: 
            hist.Draw("hist")
            hist.GetYaxis().SetRangeUser(0,700)
            hist.GetYaxis().SetTitle("mean charge [fC]")
        else : hist.Draw("histsame")
    leg.Draw()
    c.Print("plots/three_position/overlay_charge.pdf")

def amp_overlay( output ):
    hists = [] 
    channels = [13,4,12]
    ymax = 0
    for ch in channels:  
        hist = output.Get("h_amp_v_x_ch{}_prof".format(ch))
        #for b in range(0,hist.GetNbinsX()+1):
        #    if hist.GetBinError(b)> 50: 
        #        hist.SetBinContent(b,0)
        #        hist.SetBinError(b,0)
        if hist.GetMaximum() > ymax : ymax = hist.GetMaximum()
        hists.append(hist)

    c = ROOT.TCanvas("amp_overlay")
    leg = ROOT.TLegend(0.6,0.7,0.88,0.88)
    for i,hist in enumerate(hists) :
        cleanHist(hist,col_index(channels[i]))
        leg.AddEntry(hist,"Channel {}".format(channels[i]))
        if i==0: 
            hist.Draw("hist")
            hist.GetYaxis().SetRangeUser(0,700)
            hist.GetYaxis().SetTitle("mean amplitude [mV]")
        else : hist.Draw("histsame")
    leg.Draw()
    c.Print("plots/three_position/overlay_amp.pdf")
    
def pos_overlay( output ):
    hist_names = []
    hist_names.append("h_threehitpos_13_4_12_v_x")
    hist_names.append("h_twohitpos_13_4_v_x")  
    hist_names.append("h_twohitpos_4_12_v_x")
    ymax = 0
    hists=[]
    for name in hist_names:  
        hist = output.Get(name)
        if hist.GetMaximum() > ymax : ymax = hist.GetMaximum()
        hist.Rebin()
        hists.append(hist)

    c = ROOT.TCanvas("pos_overlay")
    leg = ROOT.TLegend(0.5,0.7,0.88,0.88)
    for i,hist in enumerate(hists) :
        cleanHist(hist,i)
        if i==0: leg.AddEntry(hist,"Channels 12,4,13")
        if i==1: leg.AddEntry(hist,"Channels 4,13")
        if i==2: leg.AddEntry(hist,"Channels 12,4")
        if i==0: hist.Draw("hist")
        else : hist.Draw("histsame")
    leg.Draw()
    c.Print("plots/three_position/overlay_pos.pdf")

def charge_ratio_overlay( output ):
    hists = [] 
    channels = [13,4,12]
    ymax = 0
    for ch in channels:  
        hist = output.Get("h_amp_v_x_ch{}_prof".format(ch))
        if hist.GetMaximum() > ymax : ymax = hist.GetMaximum()
        hists.append(hist)

    c = ROOT.TCanvas("amp_overlay")
    leg = ROOT.TLegend(0.5,0.7,0.88,0.88)
    for i,hist in enumerate(hists) :
        cleanHist(hist,i)
        leg.AddEntry(hist,"Channel {}".format(channels[i]))
        if i==0: hist.Draw()
        else : hist.Draw("same")
    c.Print("plots/three_position/overlay_amp.pdf")

def two_pos(tree,ch1_name,ch2_name,output):

    # setup
    histname = "h_twohitpos_{}_{}_v_x".format(ch1_name,ch2_name)
    ch1 = get_channel(ch1_name)
    ch2 = get_channel(ch2_name)
    sel = photek 
    sel += "&& {}".format(nhits_2) 
    sel += "&& amp[%i]>%i"%(ch1,threshold) 
    sel += "&& amp[%i]>%i"%(ch2,threshold) 
    sel += "&& {}".format(track_sel)
    sel += "&& {}".format(track_pos)

    x1 = strip_x(ch1_name) 
    x2 = strip_x(ch2_name) 

    plot = "(amp[%i]*%f+amp[%i]*%f)/(amp[%i]+amp[%i]):x_dut[%i]"%(ch1,x1,ch2,x2,ch1,ch2,dut)
    print(plot)
    axis = ";track x [mm];est x [mm]"
    
    # fill hist
    hist = ROOT.TH2F(histname,axis,100,xmin,xmax,100,xmin,xmax)
    tree.Project(histname,plot,sel,"COLZ")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    c.Print("plots/three_position/twohit_pos_{}_{}_v_meas.pdf".format(ch1_name,ch2_name))

    output.cd()
    hist.Write()
    return 
    

def three_pos(tree,ch1_name,ch2_name,ch3_name,output):

    # setup
    histname = "h_threehitpos_{}_{}_{}_v_x".format(ch1_name,ch2_name,ch3_name)
    ch1 = get_channel(ch1_name)
    ch2 = get_channel(ch2_name)
    ch3 = get_channel(ch3_name)
    sel = photek 
    sel += "&& {}".format(nhits_3) 
    sel += "&& amp[%i]>%i"%(ch1,threshold) 
    sel += "&& amp[%i]>%i"%(ch2,threshold) 
    sel += "&& amp[%i]>%i"%(ch3,threshold) 
    sel += "&& {}".format(track_sel)
    sel += "&& {}".format(track_pos)

    x1 = strip_x(ch1_name) 
    x2 = strip_x(ch2_name) 
    x3 = strip_x(ch3_name) 

    plot = "(amp[%i]*%f+amp[%i]*%f+amp[%i]*%f)/(amp[%i]+amp[%i]+amp[%i]):x_dut[%i]"%(ch1,x1,ch2,x2,ch3,x3,ch1,ch2,ch3,dut)
    print(plot)
    axis = ";track x [mm];est x [mm]"
    
    # fill hist
    hist = ROOT.TH2F(histname,axis,100,xmin,xmax,100,xmin,xmax)
    tree.Project(histname,plot,sel,"COLZ")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    c.Print("plots/three_position/three_hit_pos_{}_{}_{}_v_meas.pdf".format(ch1_name,ch2_name,ch3_name))

    output.cd()
    hist.Write()
    return 

def make_histos():
    # Loop through configurations 
    #


    output = ROOT.TFile.Open("plots/three_position/tmp.root","RECREATE")
    chs = [2,0,1]  
    ch_names = [12,4,13]

    tree = get_tree(cfg)

    plot_v_x(tree,"charge",0, 4,output)
    plot_v_x(tree,"charge",1,13,output)
    plot_v_x(tree,"charge",2,12,output)

    plot_v_x(tree,"amp",0, 4,output)
    plot_v_x(tree,"amp",1,13,output)
    plot_v_x(tree,"amp",2,12,output)

    #plot_v_x(tree,"2hitCR_4_13" ,0, 4,output)
    #plot_v_x(tree,"2hitCR_13_4" ,1,13,output)
    #plot_v_x(tree,"2hitCR_4_12" ,0, 4,output)
    #plot_v_x(tree,"2hitCR_12_4" ,2,12,output)

    #plot_v_x(tree,"3hitCR_4_13" ,0, 4,output)
    #plot_v_x(tree,"3hitCR_4_12" ,0, 4,output)
    #plot_v_x(tree,"3hitCR_13_4" ,1,13,output)
    #plot_v_x(tree,"3hitCR_13_12",1,13,output)
    #plot_v_x(tree,"3hitCR_12_4" ,2,12,output)
    #plot_v_x(tree,"3hitCR_12_13",2,12,output)

    #two_pos(tree,13,4,output)
    #two_pos(tree,4,12,output)
    #three_pos(tree,13,4,12,output)

    return 

def make_plots():

    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetOptStat(0)
    output = ROOT.TFile.Open("plots/three_position/tmp.root")
    amp_overlay(output)
    charge_overlay(output)
    #pos_overlay(output)
    #CR_overlay(output,"2hit")
    #CR_overlay(output,"3hit")

    return

# Main
if __name__ == "__main__":

    make_histos()
    make_plots()
