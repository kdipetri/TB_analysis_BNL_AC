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

#nhits = "(amp[0]>%i)+(amp[1]>%i)+(amp[2]>%i)"%(thresh,thresh,thresh)
#nhits_1 = nhits+"==1" 
#nhits_2 = nhits+"==2"
#nhits_3 = nhits+"==3"

track_pos = "x_dut[{}]<{}&&x_dut[{}]>{}&&y_dut[{}]<{}&&y_dut[{}]>{}".format(dut,xmax,dut,xmin,dut,ymax,dut,ymin)

photek = "amp[3]>50 && amp[3]<250"

def get_efficiency_v_y(tree,thresh,output,opt="all"): 
    min_x = 20.45 
    max_x = 20.65 
    min_y = 22 
    max_y = 25 
    ny=100

    hnum = ROOT.TH1D("h_num_amp{}".format(thresh),";y [mm]",ny,min_y,max_y)
    hden = ROOT.TH1D("h_den_amp{}".format(thresh),";y [mm]",ny,min_y,max_y)
    hnum.Sumw2()
    hden.Sumw2()

    region = "x_dut[{}]>{}&&x_dut[{}]<{}&&y_dut[{}]>{}&&y_dut[{}]<{}".format(dut,min_x,dut,max_x,dut,min_y,dut,max_y)
    
    sel="(amp[0]>%i||amp[1]>%i||amp[2]>%i)"%(thresh,thresh,thresh)

    tree.Project("h_num_amp{}".format(thresh),"y_dut[%i]"%dut,"{}&&{}&&{}&&{}".format(photek,track_sel,region,sel))
    tree.Project("h_den_amp{}".format(thresh),"y_dut[%i]"%dut,"{}&&{}&&{}".format(photek,track_sel,region))

    hist = hnum.Clone("h_eff_amp{}".format(thresh))
    hist.Divide(hnum,hden,1,1,"B")
    hist.GetYaxis().SetRangeUser(0,1.3)
    hist.GetYaxis().SetTitle("Efficiency (amp > {} mV)".format(thresh))
    hist.SetLineColor(ROOT.kBlack)
    

    fit = ROOT.TF1("f_tot_eff","pol0",22.8,24.2)
    hist.Fit(fit,"Q","",22.8,24.2)

    c = ROOT.TCanvas()
    hist.Draw("hist")
    fit.Draw("same")
    c.Print("plots/three_efficiency/all_effy_amp{}.pdf".format(thresh))
    output.cd()
    hist.Write()

    print("Total Eff Y: {:.3f} pm {:.3f}".format( fit.GetParameter(0), fit.GetParError(0) ) )

    return hist 
def get_efficiency_v_x(tree,ch,ch_name,thresh,output,opt=""): 
    
    nx=100

    hnum = ROOT.TH1D("h_num_{}_amp{}".format(ch_name,thresh),";x [mm]",nx,xmin,xmax)
    hden = ROOT.TH1D("h_den_{}_amp{}".format(ch_name,thresh),";x [mm]",nx,xmin,xmax)
    hnum.Sumw2()
    hden.Sumw2()

    region = "x_dut[{}]>{}&&x_dut[{}]<{}&&y_dut[{}]>{}&&y_dut[{}]<{}".format(dut,xmin,dut,xmax,dut,ymin,dut,ymax)
    
    if opt=="all": sel="(amp[0]>%i||amp[1]>%i||amp[2]>%i)"%(thresh,thresh,thresh)
    else : sel = "amp[%i]>%i"%(ch,thresh)

    tree.Project("h_num_{}_amp{}".format(ch_name,thresh),"x_dut[%i]"%dut,"{}&&{}&&{}&&{}".format(photek,track_sel,region,sel))
    tree.Project("h_den_{}_amp{}".format(ch_name,thresh),"x_dut[%i]"%dut,"{}&&{}&&{}".format(photek,track_sel,region))

    hist = hnum.Clone("h_eff_{}_amp{}".format(ch_name,thresh))
    hist.Divide(hnum,hden,1,1,"B")
    hist.GetYaxis().SetRangeUser(0,1.3)

    c = ROOT.TCanvas()
    hist.Draw()
    c.Print("plots/three_efficiency/ch{}_effx_amp{}.pdf".format(ch_name,thresh))
    output.cd()
    hist.Write()

    return hist 

def efficiency(tree,ch1,ch1_name,ch2,ch2_name,ch3,ch3_name,thresh,output):
    
    hist_1   = get_efficiency_v_x(tree,ch1  ,ch1_name,thresh,output)  
    hist_2   = get_efficiency_v_x(tree,ch2  ,ch2_name,thresh,output)  
    hist_3   = get_efficiency_v_x(tree,ch3  ,ch3_name,thresh,output)  
    hist_all = get_efficiency_v_x(tree,"all","all"   ,thresh,output,opt="all")  
    hists = []
    hists.append(hist_all)
    hists.append(hist_1  )
    hists.append(hist_2  )
    hists.append(hist_3  )
    channels = ["OR",ch1,ch2,ch3]
    channel_names = ["OR",ch1_name,ch2_name,ch3_name]

    c = ROOT.TCanvas("c","",800,500)
    leg = ROOT.TLegend(0.73,0.7,0.88,0.88)
    for i,hist in enumerate(hists):  
        
        hist.SetMaximum(1.1)
        hist.SetMinimum(0)
        hist.GetYaxis().SetTitle("Efficiency (amp > {} mV)".format(thresh))
        hist.GetXaxis().SetTitle("x [mm]")
        hist.SetTitle("")
        cleanHist(hist,i)

        if i==0: hist.Draw("hist")
        else: hist.Draw("histsame")
        
        leg.AddEntry(hist,"Channel {}".format(channel_names[i]),"l")


    fit = ROOT.TF1("f_tot_eff","pol0",20.45,20.65)
    hist_all.Fit(fit,"Q","",20.45,20.65)
    fit.Draw("same")
    print("Total Eff X: {:.3f} pm {:.3f}".format(  fit.GetParameter(0), fit.GetParError(0) ) )
    

    leg.Draw()
    c.Print("plots/three_efficiency/overlay_eff_{}amp.pdf".format(thresh))
    
def pos_single(tree,ch1,ch1_name,output):

    # for plot 
    # for sel
    histname = "h_pos_ch{}".format(ch1_name)
    plot = "x_dut[%i]"%(dut)
    sel = photek + "&&" + nhits_1 + "&&" + track_sel + "&&" + track_pos + "&& amp[%i]>%i"%(ch1,thres)

    # fill hist
    hist = ROOT.TH1F(histname,";x [mm]",50,xmin,xmax)
    tree.Project(histname,plot,sel,"COLZ")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    c.Print("plots/three_efficiency/pos_single_ch{}.pdf".format(ch1_name))

    output.cd()
    hist.Write()

    return  

def pos_double(tree,ch1,ch1_name,ch2,ch2_name,output):

    # for plot 
    # for sel
    histname = "h_pos_ch{}_ch{}".format(ch1_name,ch2_name)
    plot = "x_dut[%i]"%(dut)
    sel = photek + "&&" + nhits_2 + "&&" + track_sel + "&&" + track_pos + "&& amp[%i]>%i && amp[%i]>%i "%(ch1,thresh,ch2,thresh)

    # fill hist
    hist = ROOT.TH1F(histname,";x [mm]",50,xmin,xmax)
    tree.Project(histname,plot,sel,"COLZ")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    c.Print("plots/three_efficiency/pos_double_ch{}_ch{}.pdf".format(ch1_name,ch2_name))

    output.cd()
    hist.Write()

    return  

def pos_triple(tree,ch1,ch1_name,ch2,ch2_name,ch3,ch3_name,output):

    # for plot 
    # for sel
    histname = "h_pos_ch{}_ch{}_ch{}".format(ch1_name,ch2_name,ch3_name)
    plot = "x_dut[%i]"%(dut)
    #plot = "(amp[%i]*(LP2_20[%i]-LP2_20[3])+amp[%i]*(LP2_20[%i]-LP2_20[3])+amp[%i]*(LP2_20[%i]-LP2_20[3]))/(amp[%i]+amp[%i]+amp[%i])"%(ch1,ch1,ch2,ch2,ch3,ch3,ch1,ch2,ch3)
    sel = photek + "&&" + nhits_3 + "&&" + track_sel + "&&" + track_pos + "&& amp[%i]>%i && amp[%i]>%i&& amp[%i]>%i"%(ch1,thresh,ch2,thresh,ch3,thresh)

    # fill hist
    hist = ROOT.TH1F(histname,";x [mm]",50,xmin,xmax)
    tree.Project(histname,plot,sel,"COLZ")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    c.Print("plots/three_efficiency/pos_triple_ch{}_ch{}_ch_{}.pdf".format(ch1_name,ch2_name,ch3_name))

    output.cd()
    hist.Write()

    return  

def make_histos():
    # Loop through configurations 
    #


    output = ROOT.TFile.Open("plots/three_efficiency/tmp.root","RECREATE")
    chs = [2,0,1]  
    ch_names = [12,4,13]

    tree = get_tree(cfg)

    #pos_single(tree,0,4,output)
    #pos_single(tree,1,13,output)
    #pos_single(tree,2,12,output)
    #
    #pos_double(tree,0,4,1,13,output)
    #pos_double(tree,0,4,2,12,output)
    #pos_double(tree,1,13,2,12,output)
    #
    #pos_triple(tree,1,13,0,4,2,12,output) 

    thresholds = [90,100,110,120] 
    #thresh = 110 #mV, noise threshold
    for thresh in thresholds: 
        efficiency(tree,1,13,0,4,2,12,thresh,output)
        get_efficiency_v_y(tree,thresh,output,"all")

    return 

def make_plots():

    output = ROOT.TFile.Open("plots/three_efficiency/tmp.root")

    return

# Main
if __name__ == "__main__":

    make_histos()
    #make_plots()
