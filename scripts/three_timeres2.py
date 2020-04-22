from common import *
import os, sys, re
import ROOT


threshold = 110 #mV, noise threshold

cfg = "config_214_6_5_11_photek"

ymin = 22.8
ymax = 24.2
xmin = 20.0 
xmax = 20.5 

minT = 2.7e-9 
maxT = 3.8e-9

nhits = "(amp[0]>%i)+(amp[1]>%i)+(amp[2]>%i)"%(threshold,threshold,threshold)
nhits_1 = nhits+"==1" 
nhits_2 = nhits+"==2"
nhits_3 = nhits+"==3"

tres_1 = "LP2_20[0]-LP2_20[3]" 
tres_2 = "LP2_20[1]-LP2_20[3]" 
tres_3 = "LP2_20[2]-LP2_20[3]" 

weighted_mean_3 = "({}*amp[0]+{}*amp[1]+{}*amp[2])/(amp[1]+amp[2]+amp[3])".format(tres_1,tres_2,tres_3)  

track_pos = "x_dut[{}]<{}&&x_dut[{}]>{}&&y_dut[{}]<{}&&y_dut[{}]>{}".format(dut,xmax,dut,xmin,dut,ymax,dut,ymin)

photek = "amp[3]>50 && amp[3]<250"


def delay_correction(tree,ch,ch_name,output):

    histname = "h_time_v_y_ch{}".format(ch_name)
    plot = "LP2_20[%i]-LP2_20[3]:y_dut[%i]"%(ch,dut)
    sel = photek + "&& LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i"%(ch,ch,threshold)

    # fill hist
    hist = ROOT.TH2F(histname,";y [mm], t_{0}-t_{ref}",50,ymin,ymax,100,minT,maxT)
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
    c.Print("plots/three_timeres/ch{}_time_v_y.pdf".format(ch_name))

    output.cd()
    hist.Write()
    
    return 

def time_v_amp(tree,ch,ch_name,output):

    histname = "h_time_v_amp_ch{}".format(ch_name)
    plot = "LP2_20[%i]-LP2_20[3]:amp[%i]"%(ch,ch)
    sel = photek + "&& LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i"%(ch,ch,threshold)

    # fill hist
    hist = ROOT.TH2F(histname,";amplitude [mV], t_{0}-t_{ref}",50,0,1000,100,minT,maxT)
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
    c.Print("plots/three_timeres/ch{}_time_v_amp.pdf".format(ch_name))

    output.cd()
    hist.Write()
    
    return 
def time_single(tree,ch,ch_name,output):

    # for plot 
    # for sel
    histname = "h_time_ch{}".format(ch_name)
    plot = "LP2_20[%i]-LP2_20[3]"%(ch)
    sel = photek + "&&" + nhits_1 + "&& LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i"%(ch,ch,threshold)

    # fill hist
    hist = ROOT.TH1F(histname,";t_{0}-t_{ref}",100,minT,maxT)
    tree.Project(histname,plot,sel,"COLZ")

    #do fit 
    f1 = ROOT.TF1("f_time_ch{}".format(ch_name),"gaus",minT,maxT)
    hist.Fit(f1,"Q")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    f1.Draw("same")
    c.Print("plots/three_timeres/time_single_ch{}.pdf".format(ch_name))

    output.cd()
    hist.Write()
    f1.Write()

    return  

def time_double(tree,ch1,ch1_name,ch2,ch2_name,output):

    # for plot 
    # for sel
    histname = "h_time_ch{}_ch{}".format(ch1_name,ch2_name)
    plot = "(amp[%i]*(LP2_20[%i]-LP2_20[3])+amp[%i]*(LP2_20[%i]-LP2_20[3]))/(amp[%i]+amp[%i])"%(ch1,ch1,ch2,ch2,ch1,ch2)
    sel = photek + "&&" + nhits_2 + "&& LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i&& amp[%i]>%i"%(ch1,ch2,ch1,threshold,ch2,threshold)

    # fill hist
    hist = ROOT.TH1F(histname,";t_{0}-t_{ref}",100,minT,maxT)
    tree.Project(histname,plot,sel,"COLZ")

    #do fit 
    f1 = ROOT.TF1("f_time_ch{}_ch{}".format(ch1_name,ch2_name),"gaus",minT,maxT)
    hist.Fit(f1,"Q")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    f1.Draw("same")
    c.Print("plots/three_timeres/time_double_ch{}_ch{}.pdf".format(ch1_name,ch2_name))

    output.cd()
    hist.Write()
    f1.Write()

    return  

def time_triple(tree,ch1,ch1_name,ch2,ch2_name,ch3,ch3_name,output):

    # for plot 
    # for sel
    histname = "h_time_ch{}_ch{}_ch{}".format(ch1_name,ch2_name,ch3_name)
    plot = "(amp[%i]*(LP2_20[%i]-LP2_20[3])+amp[%i]*(LP2_20[%i]-LP2_20[3])+amp[%i]*(LP2_20[%i]-LP2_20[3]))/(amp[%i]+amp[%i]+amp[%i])"%(ch1,ch1,ch2,ch2,ch3,ch3,ch1,ch2,ch3)
    sel = photek + "&&" + nhits_3 + "&& LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i && amp[%i]>%i&& amp[%i]>%i"%(ch1,ch2,ch3,ch1,threshold,ch2,threshold,ch3,threshold)

    # fill hist
    hist = ROOT.TH1F(histname,";t_{0}-t_{ref}",100,minT,maxT)
    tree.Project(histname,plot,sel,"COLZ")

    #do fit 
    f1 = ROOT.TF1("f_time_ch{}_ch{}_ch{}".format(ch1_name,ch2_name,ch3_name),"gaus",minT,maxT)
    hist.Fit(f1,"Q")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    f1.Draw("same")
    c.Print("plots/three_timeres/time_triple_ch{}_ch{}_ch_{}.pdf".format(ch1_name,ch2_name,ch3_name))


    output.cd()
    hist.Write()
    f1.Write()

    return  

def time_triple_avg(tree,ch1,ch1_name,ch2,ch2_name,ch3,ch3_name,output):

    # for plot 
    # for sel
    histname = "h_time_ch{}_ch{}_ch{}".format(ch1_name,ch2_name,ch3_name)
    plot = "((LP2_20[%i]-LP2_20[3])+(LP2_20[%i]-LP2_20[3])+(LP2_20[%i]-LP2_20[3]))/3.0"%(ch1,ch2,ch3)
    sel = photek + "&&" + nhits_3 + "&& LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i && amp[%i]>%i&& amp[%i]>%i"%(ch1,ch2,ch3,ch1,threshold,ch2,threshold,ch3,threshold)

    # fill hist
    hist = ROOT.TH1F(histname,";t_{0}-t_{ref} [s]",100,minT,maxT)
    tree.Project(histname,plot,sel,"COLZ")

    #do fit 
    f1 = ROOT.TF1("f_time_ch{}_ch{}_ch{}".format(ch1_name,ch2_name,ch3_name),"gaus",minT,maxT)
    hist.Fit(f1,"Q")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    f1.Draw("same")
    c.Print("plots/three_timeres/time_triple_mean_ch{}_ch{}_ch_{}.pdf".format(ch1_name,ch2_name,ch3_name))


    output.cd()
    hist.Write()
    f1.Write()

    return  

def pos_single(tree,ch1,ch1_name,output):

    # for plot 
    # for sel
    histname = "h_pos_ch{}".format(ch1_name)
    plot = "x_dut[%i]"%(dut)
    sel = photek + "&&" + nhits_1 + "&&" + track_sel + "&&" + track_pos + "&& amp[%i]>%i"%(ch1,threshold)

    # fill hist
    hist = ROOT.TH1F(histname,";x [mm]",50,xmin,xmax)
    tree.Project(histname,plot,sel,"COLZ")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    c.Print("plots/three_timeres/pos_single_ch{}.pdf".format(ch1_name))

    output.cd()
    hist.Write()

    return  
def pos_double(tree,ch1,ch1_name,ch2,ch2_name,output):

    # for plot 
    # for sel
    histname = "h_pos_ch{}_ch{}".format(ch1_name,ch2_name)
    plot = "x_dut[%i]"%(dut)
    sel = photek + "&&" + nhits_2 + "&&" + track_sel + "&&" + track_pos + "&& amp[%i]>%i && amp[%i]>%i "%(ch1,threshold,ch2,threshold)

    # fill hist
    hist = ROOT.TH1F(histname,";x [mm]",50,xmin,xmax)
    tree.Project(histname,plot,sel,"COLZ")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    c.Print("plots/three_timeres/pos_double_ch{}_ch{}.pdf".format(ch1_name,ch2_name))

    output.cd()
    hist.Write()

    return  

def pos_triple(tree,ch1,ch1_name,ch2,ch2_name,ch3,ch3_name,output):

    # for plot 
    # for sel
    histname = "h_pos_ch{}_ch{}_ch{}".format(ch1_name,ch2_name,ch3_name)
    plot = "x_dut[%i]"%(dut)
    #plot = "(amp[%i]*(LP2_20[%i]-LP2_20[3])+amp[%i]*(LP2_20[%i]-LP2_20[3])+amp[%i]*(LP2_20[%i]-LP2_20[3]))/(amp[%i]+amp[%i]+amp[%i])"%(ch1,ch1,ch2,ch2,ch3,ch3,ch1,ch2,ch3)
    sel = photek + "&&" + nhits_3 + "&&" + track_sel + "&&" + track_pos + "&& amp[%i]>%i && amp[%i]>%i&& amp[%i]>%i"%(ch1,threshold,ch2,threshold,ch3,threshold)

    # fill hist
    hist = ROOT.TH1F(histname,";x [mm]",50,xmin,xmax)
    tree.Project(histname,plot,sel,"COLZ")

    # print
    c = ROOT.TCanvas(histname)
    hist.Draw("COLZ")
    c.Print("plots/three_timeres/pos_triple_ch{}_ch{}_ch_{}.pdf".format(ch1_name,ch2_name,ch3_name))

    output.cd()
    hist.Write()

    return  
    
def make_histos():
    # Loop through configurations 
    #


    output = ROOT.TFile.Open("plots/three_efficiency/tmp2.root","RECREATE")

    tree = get_tree(cfg)

    delay_correction(tree,0,6,output)
    delay_correction(tree,1,5,output)
    delay_correction(tree,2,11,output)
    
    time_v_amp(tree,0,6,output)
    time_v_amp(tree,1,5,output)
    time_v_amp(tree,2,11,output)

    time_single(tree,0,6,output)
    time_single(tree,1,5,output)
    time_single(tree,2,11,output)
    pos_single(tree,0,6,output)
    pos_single(tree,1,5,output)
    pos_single(tree,2,11,output)
    
    time_double(tree,0,6,1,5,output)
    time_double(tree,0,6,2,11,output)
    time_double(tree,1,5,2,11,output)
    pos_double(tree,0,6,1,5,output)
    pos_double(tree,0,6,2,11,output)
    pos_double(tree,1,5,2,11,output)

    time_triple(tree,0,6,1,5,2,11,output)
    time_triple_avg(tree,0,6,1,5,2,11,output)
    pos_triple(tree,0,6,1,5,2,11,output) 


    return 

def make_plots():

    output = ROOT.TFile.Open("plots/three_efficiency/tmp2.root")

    return

# Main
if __name__ == "__main__":

    make_histos()
    #make_plots()
