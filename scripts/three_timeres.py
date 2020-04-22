from common import *
import os, sys, re
import ROOT


threshold = 110 #mV, noise threshold

cfg = "config_211_4_13_12_photek"

# in strip 4
ymin = 22.8
ymax = 24.2
xmin = 20.55-0.1 #20.3 
xmax = 20.55+0.1 #20.9 

minTpre = 2.8e-9
maxTpre = 3.8e-9
minT = -0.5e-9 
maxT = 0.5e-9

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

def time_v_x(tree,ch,ch_name,output):

    histname = "h_time_v_x_ch{}".format(ch_name)
    plot = "LP2_20[%i]-LP2_20[3]:x_dut[%i]"%(ch,dut)
    sel = photek + "&& LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i"%(ch,ch,threshold)

    # fill hist
    hist = ROOT.TH2F(histname,";x [mm]; t_{0}-t_{ref} [s]",50,xmin,xmax,100,minTpre,maxTpre)
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
    c.Print("plots/three_timeres/ch{}_time_v_x.pdf".format(ch_name))

    output.cd()
    hist.Write()
    
    return 

def delay_correction(tree,ch,ch_name,output):

    rel_xmin = 0
    rel_xmax = 0.3
    histname1 = "h_time_v_x1_ch{}".format(ch_name)
    histname2 = "h_time_v_x2_ch{}".format(ch_name)
    plot = "LP2_20[%i]-LP2_20[3]:fabs(x_dut[%i]-%f)"%(ch,dut,strip_x(ch_name))
    sel = nhits + " > 1 && "+  photek + "&&" + track_sel + "&& LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i"%(ch,ch,threshold)

    # fill hist
    hist1 = ROOT.TH2F(histname1,";|x-xcenter| [mm]; t_{0}-t_{ref} [s]",50,0.04,rel_xmax,100,minTpre,maxTpre)
    hist2 = ROOT.TH2F(histname2,";|x-xcenter| [mm]; t_{0}-t_{ref} [s]",50,0.00,    0.04,100,minTpre,maxTpre)
    tree.Project(histname1,plot,sel,"COLZ")
    tree.Project(histname2,plot,sel,"COLZ")

    # do profile
    profile = hist1.ProfileX("{}_prof".format(histname1))
    profile.SetMarkerStyle(20);
    profile.SetMarkerSize(0.8);
    profile.SetMarkerColor(ROOT.kBlack);
    profile.SetLineColor(ROOT.kBlack);
    profile.SetLineWidth(1);

    #do fit 
    f1 = ROOT.TF1("f_delay_v_x1_ch{}".format(ch_name),"pol1",0.04,rel_xmax)
    hist1.Fit(f1,"Q")
    f2 = ROOT.TF1("f_delay_v_x2_ch{}".format(ch_name),"pol1",0.00,0.04)
    hist2.Fit(f2,"Q")
    
    print("channel {}".format(ch_name))
    print("xdiff >0.04 mm")
    print("x0 = {} pm {} ns".format(1e9*f1.GetParameter(0), 1e9*f1.GetParError(0)))
    print("x1 = {} pm {} ps per mm".format(1e12*f1.GetParameter(1), 1e12*f1.GetParError(1)))
    print("xdiff <0.04 mm")
    print("x0 = {} pm {} ns".format(1e9*f2.GetParameter(0), 1e9*f2.GetParError(0)))
    print("x1 = {} pm {} ps per mm".format(1e12*f2.GetParameter(1), 1e12*f2.GetParError(1)))

    # print
    c1 = ROOT.TCanvas(histname1)
    hist1.Draw("COLZ")
    profile.Draw("same")
    f1.Draw("same")
    c1.Print("plots/three_timeres/ch{}_delay_v_x1.pdf".format(ch_name))

    c2 = ROOT.TCanvas(histname2)
    hist2.Draw("COLZ")
    f2.Draw("same")
    c2.Print("plots/three_timeres/ch{}_delay_v_x2.pdf".format(ch_name))

    output.cd()
    hist1.Write()
    hist2.Write()
    
    return 

def time_v_amp(tree,ch,ch_name,output):

    histname = "h__v_amp_ch{}".format(ch_name)
    plot = "LP2_20[%i]-LP2_20[3]:amp[%i]"%(ch,ch)
    sel = photek + "&& LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i"%(ch,ch,threshold)

    # fill hist
    hist = ROOT.TH2F(histname,";amplitude [mV]; t_{0}-t_{ref} [s]",50,0,1000,100,minTpre,maxTpre)
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
    plot = "LP2_20[%i]-LP2_20[3]-%f*1e-9"%(ch,get_t0(ch_name))

    # for plot 
    # for sel
    histname = "h_time_ch{}".format(ch_name)
    plot = "LP2_20[%i]-LP2_20[3]-%f*1e-9"%(ch,get_t0(ch_name))
    sel = photek + "&&" + nhits_1 + "&& LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i"%(ch,ch,threshold)

    # fill hist
    hist = ROOT.TH1F(histname,";t_{0}-t_{ref} [s]",100,minT,maxT)
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
    time1 = "amp[%i]*(LP2_20[%i]-LP2_20[3]-%f*1e-9)"%(ch1,ch1,get_t0(ch1_name))
    time2 = "amp[%i]*(LP2_20[%i]-LP2_20[3]-%f*1e-9)"%(ch2,ch2,get_t0(ch2_name))
    den = "(amp[%i]+amp[%i])"%(ch1,ch2)
    plot = "({}+{})/{}".format(time1,time2,den)
    sel = photek + "&&" + nhits_2 + "&& LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i&& amp[%i]>%i"%(ch1,ch2,ch1,threshold,ch2,threshold)

    # fill hist
    hist = ROOT.TH1F(histname,";t_{0}-t_{ref} [s]",100,minT,maxT)
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
    time1 = "amp[%i]*(LP2_20[%i]-LP2_20[3]-%f*1e-9)"%(ch1,ch1,get_t0(ch1_name))
    time2 = "amp[%i]*(LP2_20[%i]-LP2_20[3]-%f*1e-9)"%(ch2,ch2,get_t0(ch2_name))
    time3 = "amp[%i]*(LP2_20[%i]-LP2_20[3]-%f*1e-9)"%(ch3,ch3,get_t0(ch3_name))
    den = "(amp[%i]+amp[%i]+amp[%i])"%(ch1,ch2,ch3)
    plot = "({}+{}+{})/{}".format(time1,time2,time3,den)
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
    c.Print("plots/three_timeres/time_triple_ch{}_ch{}_ch_{}.pdf".format(ch1_name,ch2_name,ch3_name))


    output.cd()
    hist.Write()
    f1.Write()

    return  

def time_triple_avg(tree,ch1,ch1_name,ch2,ch2_name,ch3,ch3_name,output):

    # for plot 
    # for sel
    histname = "h_time_ch{}_ch{}_ch{}".format(ch1_name,ch2_name,ch3_name)
    time1 = "(LP2_20[%i]-LP2_20[3]-%f*1e-9)"%(ch1,get_t0(ch1_name))
    time2 = "(LP2_20[%i]-LP2_20[3]-%f*1e-9)"%(ch2,get_t0(ch2_name))
    time3 = "(LP2_20[%i]-LP2_20[3]-%f*1e-9)"%(ch3,get_t0(ch3_name))
    plot = "({}+{}+{})/3.0".format(time1,time2,time3)
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

def compare_double(tree,ch1,ch1_name,ch2,ch2_name,output,opt=""):

    # for plot 
    # for sel
    histname1 = "h_{}_ch{}".format(opt,ch1_name)
    histname2 = "h_{}_ch{}".format(opt,ch2_name)

    plot1 = "amp[%i]"%ch1
    plot2 = "amp[%i]"%ch2
    axis = ";amplitude [mV]"
    n,xmin,xmax=50,0,1800
    if "time" in opt: 
        plot1 = "LP2_20[%i]-LP2_20[3]-%f*1e-9"%(ch1,get_t0(ch1_name))
        plot2 = "LP2_20[%i]-LP2_20[3]-%f*1e-9"%(ch2,get_t0(ch2_name))
        axis = ";t_{0}-t_{ref} [s]"
        n,xmin,xmax=100,minT,maxT

    sel = photek + "&&" + nhits_2 + "&& LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i && amp[%i]>%i"%(ch1,ch2,ch1,threshold,ch2,threshold)

    # fill hists
    hist1 = ROOT.TH1F(histname1,axis,n,xmin,xmax)
    hist2 = ROOT.TH1F(histname2,axis,n,xmin,xmax)
    tree.Project(histname1,plot1,sel)
    tree.Project(histname2,plot2,sel)

    # print
    c = ROOT.TCanvas("compare_double_ch{}_ch_{}_{}".format(ch1_name,ch2_name,opt))
    hist1.SetLineColor(ROOT.kRed+1)
    hist2.SetLineColor(ROOT.kBlue+1)
    hist1.Draw()
    hist2.Draw("same")
    
    # fit
    if "time" in opt :
        f1 = ROOT.TF1("f_{}_ch{}".format(opt,ch1_name),"gaus",xmin,xmax)
        f2 = ROOT.TF1("f_{}_ch{}".format(opt,ch2_name),"gaus",xmin,xmax)
        hist1.Fit(f1,"Q")
        hist2.Fit(f2,"Q")
        f1.SetLineColor(ROOT.kRed+1)
        f2.SetLineColor(ROOT.kBlue+1)
        f1.Draw("same")
        f2.Draw("same")

        print(ch1_name,f1.GetParameter(1)*1e9,f1.GetParameter(2)*1e12)
        print(ch2_name,f2.GetParameter(1)*1e9,f2.GetParameter(2)*1e12)

    ymax = max(hist1.GetMaximum(),hist2.GetMaximum())
    hist1.GetYaxis().SetRangeUser(0,1.3*ymax)

    leg = ROOT.TLegend(0.5,0.7,0.88,0.88)
    leg.AddEntry(hist1,"Channel {}".format(ch1_name),"l")
    leg.AddEntry(hist2,"Channel {}".format(ch2_name),"l")
    leg.Draw()
    
    c.Print("plots/three_timeres/compare_double_{}_ch{}_ch{}.pdf".format(opt,ch1_name,ch2_name))

    output.cd()
    hist1.Write()
    hist2.Write()

    return  
def compare_triple(tree,ch1,ch1_name,ch2,ch2_name,ch3,ch3_name,output,opt=""):

    # for plot 
    # for sel
    histname1 = "h_{}_ch{}".format(opt,ch1_name)
    histname2 = "h_{}_ch{}".format(opt,ch2_name)
    histname3 = "h_{}_ch{}".format(opt,ch3_name)

    plot1 = "amp[%i]"%ch1
    plot2 = "amp[%i]"%ch2
    plot3 = "amp[%i]"%ch3
    axis = ";amplitude [mV]"
    n,xmin,xmax=50,0,1800
    if "time" in opt: 
        plot1 = "LP2_20[%i]-LP2_20[3]-%f*1e-9"%(ch1,get_t0(ch1_name))
        plot2 = "LP2_20[%i]-LP2_20[3]-%f*1e-9"%(ch2,get_t0(ch2_name))
        plot3 = "LP2_20[%i]-LP2_20[3]-%f*1e-9"%(ch3,get_t0(ch3_name))
        axis = ";t_{0}-t_{ref} [s]"
        n,xmin,xmax=100,minT,maxT

    sel = photek + "&&" + nhits_3 + "&& LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i && amp[%i]>%i&& amp[%i]>%i"%(ch1,ch2,ch3,ch1,threshold,ch2,threshold,ch3,threshold)

    # fill hists
    hist1 = ROOT.TH1F(histname1,axis,n,xmin,xmax)
    hist2 = ROOT.TH1F(histname2,axis,n,xmin,xmax)
    hist3 = ROOT.TH1F(histname3,axis,n,xmin,xmax)
    tree.Project(histname1,plot1,sel)
    tree.Project(histname2,plot2,sel)
    tree.Project(histname3,plot3,sel)

    # print
    c = ROOT.TCanvas("compare_triple_"+opt)
    hist1.SetLineColor(ROOT.kRed+1)
    hist2.SetLineColor(ROOT.kBlue+1)
    hist3.SetLineColor(ROOT.kGreen+1)
    hist1.Draw()
    hist2.Draw("same")
    hist3.Draw("same")
    
    # fit
    if "time" in opt :
        f1 = ROOT.TF1("f_{}_ch{}".format(opt,ch1_name),"gaus",xmin,xmax)
        f2 = ROOT.TF1("f_{}_ch{}".format(opt,ch2_name),"gaus",xmin,xmax)
        f3 = ROOT.TF1("f_{}_ch{}".format(opt,ch3_name),"gaus",xmin,xmax)
        hist1.Fit(f1,"Q")
        hist2.Fit(f2,"Q")
        hist3.Fit(f3,"Q")
        f1.SetLineColor(ROOT.kRed+1)
        f2.SetLineColor(ROOT.kBlue+1)
        f3.SetLineColor(ROOT.kGreen+1)
        f1.Draw("same")
        f2.Draw("same")
        f3.Draw("same")

        print(ch1_name,f1.GetParameter(1)*1e9,f1.GetParameter(2)*1e12)
        print(ch2_name,f2.GetParameter(1)*1e9,f2.GetParameter(2)*1e12)
        print(ch3_name,f3.GetParameter(1)*1e9,f3.GetParameter(2)*1e12)

    ymax = max(hist1.GetMaximum(),hist2.GetMaximum(),hist3.GetMaximum())
    hist1.GetYaxis().SetRangeUser(0,1.3*ymax)

    leg = ROOT.TLegend(0.5,0.7,0.88,0.88)
    leg.AddEntry(hist1,"Channel {}".format(ch1_name),"l")
    leg.AddEntry(hist2,"Channel {}".format(ch2_name),"l")
    leg.AddEntry(hist3,"Channel {}".format(ch3_name),"l")
    leg.Draw()
    
    c.Print("plots/three_timeres/compare_triple_{}_ch{}_ch{}_ch_{}.pdf".format(opt,ch1_name,ch2_name,ch3_name))

    output.cd()
    hist1.Write()
    hist2.Write()
    hist3.Write()

    return  
    
def compare_channels(tree,ch1,ch1_name,ch2,ch2_name,output,opt,selection):
    
    # for plot 
    histname = "h_{}_{}_ch{}_ch{}".format(opt,selection,ch1_name,ch2_name)

    plot = "amp[%i]:amp[%i]"%(ch2,ch1)
    axis = ";amplitude ch{} [mV];amplitude ch{} mV".format(ch1_name,ch2_name)
    n,xmin,xmax=50,0,1800
    if "time" in opt: 
        plot = "LP2_20[%i]-LP2_20[3]-%f*1e-9:LP2_20[%i]-LP2_20[3]-%f*1e-9"%(ch2,get_t0(ch2_name),ch1,get_t0(ch1_name))
        axis = ";t_{0}-t_{ref} ch%i[s];t_{0}-t_{ref} ch%i[s]"%(ch1_name,ch2_name)
        n,xmin,xmax=100,minT,maxT

    sel = photek + "&&" + nhits_2 + "&& LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i && amp[%i]>%i"%(ch1,ch2,ch1,threshold,ch2,threshold)
    if "nhits3" in selection: 
        sel = photek + "&&" + nhits_3 + "&& LP2_20[%i]!=0 && LP2_20[%i]!=0 && LP2_20[3]!=0 && amp[%i]>%i && amp[%i]>%i"%(ch1,ch2,ch1,threshold,ch2,threshold)

    # fill hists
    hist = ROOT.TH2F(histname,axis,n,xmin,xmax,n,xmin,xmax)
    tree.Project(histname,plot,sel)

    # print
    c = ROOT.TCanvas("compare_channels_{}_{}_ch{}_ch{}".format(opt,selection,ch1_name,ch2_name))
    hist.Draw("COLZ")
    
    
    c.Print("plots/three_timeres/compare_channels_{}_{}_ch{}_ch{}.pdf".format(opt,selection,ch1_name,ch2_name))

    output.cd()
    hist.Write()

    return 

def make_histos():
    # Loop through configurations 
    #


    output = ROOT.TFile.Open("plots/three_timeres/tmp.root","RECREATE")
    chs = [2,0,1]  
    ch_names = [12,4,13]

    tree = get_tree(cfg)

    #time_v_x(tree,0,4,output)
    #time_v_x(tree,1,13,output)
    #time_v_x(tree,2,12,output)
    #
    #delay_correction(tree,0,4,output)
    #delay_correction(tree,1,13,output)
    #delay_correction(tree,2,12,output)
    #
    #time_v_amp(tree,0,4,output)
    #time_v_amp(tree,1,13,output)
    #time_v_amp(tree,2,12,output)

    #time_single(tree,0,4,output)
    #time_single(tree,1,13,output)
    #time_single(tree,2,12,output)
    #pos_single(tree,0,4,output)
    #pos_single(tree,1,13,output)
    #pos_single(tree,2,12,output)
    #
    time_double(tree,0,4,1,13,output)
    time_double(tree,0,4,2,12,output)
    time_double(tree,1,13,2,12,output)
    #pos_double(tree,0,4,1,13,output)
    #pos_double(tree,0,4,2,12,output)
    #pos_double(tree,1,13,2,12,output)

    time_triple(tree,1,13,0,4,2,12,output)
    #time_triple_avg(tree,1,13,0,4,2,12,output)
    #pos_triple(tree,1,13,0,4,2,12,output) 

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    ## what the hell is going onnn
    compare_triple(tree,1,13,0,4,2,12,output,"amp")
    compare_triple(tree,1,13,0,4,2,12,output,"time")

    compare_double(tree,0, 4,1,13,output,"amp")
    compare_double(tree,0, 4,2,12,output,"amp")
    compare_double(tree,1,13,2,12,output,"amp")
    compare_double(tree,0, 4,1,13,output,"time")
    compare_double(tree,0, 4,2,12,output,"time")
    compare_double(tree,1,13,2,12,output,"time")

    #compare_channels(tree,0, 4,1,13,output,"amp" ,"nhits2")
    #compare_channels(tree,0, 4,2,12,output,"amp" ,"nhits2")
    #compare_channels(tree,1,13,2,12,output,"amp" ,"nhits2")
    #compare_channels(tree,0, 4,1,13,output,"time","nhits2")
    #compare_channels(tree,0, 4,2,12,output,"time","nhits2")
    #compare_channels(tree,1,13,2,12,output,"time","nhits2")
    #compare_channels(tree,0, 4,1,13,output,"amp" ,"nhits3")

    return 

def pos_overlay(output):
    #
    hist_names = []
    hist_names.append("h_pos_ch13_ch4_ch12")
    hist_names.append("h_pos_ch4_ch13")  
    hist_names.append("h_pos_ch4_ch12")
    ymax = 0
    hists=[]
    for name in hist_names:  
        hist = output.Get(name)
        hist.Rebin()
        if hist.GetMaximum() > ymax : ymax = hist.GetMaximum()
        hists.append(hist)

    c = ROOT.TCanvas("pos_overlay")
    leg = ROOT.TLegend(0.5,0.7,0.88,0.88)
    for i,hist in enumerate(hists) :
        cleanHist(hist,i)
        hist.GetYaxis().SetRangeUser(0,ymax*1.3)
        hist.GetXaxis().SetNdivisions(505)
        if i==0: leg.AddEntry(hist,"Channels 12,4,13")
        if i==1: leg.AddEntry(hist,"Channels 4,13")
        if i==2: leg.AddEntry(hist,"Channels 12,4")
        if i==0: hist.Draw()
        else : hist.Draw("same")
    leg.Draw()
    c.Print("plots/three_timeres/overlay_pos.pdf")

def make_plots():

    output = ROOT.TFile.Open("plots/three_timeres/tmp.root")
    pos_overlay(output)

    return

# Main
if __name__ == "__main__":

    make_histos()
    #make_plots()
