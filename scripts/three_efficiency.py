from common import *
import os, sys, re
import ROOT

cfg = "config_211_4_13_12_photek"

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)

# in strip 4
ymin = 22.9
ymax = 24.1
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

track_sel = "ntracks==1&&nplanes>17&&npix>3&&nback>1&&abs(yResidBack)<250&&xResidBack>50&&xResidBack<250"
track_pos = "x_dut[{}]<{}&&x_dut[{}]>{}&&y_dut[{}]<{}&&y_dut[{}]>{}".format(dut,xmax,dut,xmin,dut,ymax,dut,ymin)

def get_efficiency_v_y(tree,thresh,output,opt="all"): 
    min_x = 20.45 
    max_x = 20.65 
    min_y = 22 
    max_y = 25 
    ny=60

    hnum = ROOT.TH1D("h_num_amp{}".format(thresh),";y [mm]",ny,min_y,max_y)
    hden = ROOT.TH1D("h_den_amp{}".format(thresh),";y [mm]",ny,min_y,max_y)
    hnum.Sumw2()
    hden.Sumw2()

    region = "x_dut[{}]>{}&&x_dut[{}]<{}&&y_dut[{}]>{}&&y_dut[{}]<{}".format(dut,min_x,dut,max_x,dut,min_y,dut,max_y)
    
    if thresh >= 200 :  sel="(amp[0]>%i||amp[1]>%i||amp[2]>%i)"%(thresh,thresh,thresh)
    else : 
        amp0 = "amp[0]>%i && t_peak[0]-LP2_20[3]>2.5e-9 && t_peak[0]-LP2_20[3]<5.5e-9"%(thresh)
        amp1 = "amp[1]>%i && t_peak[1]-LP2_20[3]>2.5e-9 && t_peak[1]-LP2_20[3]<5.5e-9"%(thresh)
        amp2 = "amp[2]>%i && t_peak[2]-LP2_20[3]>2.5e-9 && t_peak[2]-LP2_20[3]<5.5e-9"%(thresh)
        sel="({}||{}||{})".format(amp0,amp1,amp2)

    tree.Project("h_num_amp{}".format(thresh),"y_dut[%i]"%dut,"{}&&{}&&{}&&{}".format(photek,track_sel,region,sel))
    tree.Project("h_den_amp{}".format(thresh),"y_dut[%i]"%dut,"{}&&{}&&{}".format(photek,track_sel,region))

    hist = hnum.Clone("h_eff_amp{}".format(thresh))
    hist.Divide(hnum,hden,1,1,"B")
    hist.GetYaxis().SetRangeUser(0,1.3)
    hist.GetYaxis().SetTitle("Efficiency (amp > {} mV)".format(thresh))
    hist.SetLineColor(ROOT.kBlack)

    c = ROOT.TCanvas()
    hist.Draw("hist e")
    #fit.Draw("same")
    c.Print("plots/three_efficiency/all_effy_amp{}.pdf".format(thresh))
    output.cd()
    hist.Write()

    return hist 

def get_efficiency_v_x(tree,ch,ch_name,thresh,output,opt=""): 
    
    nx=100
    #nx=50

    hnum = ROOT.TH1D("h_num_{}_amp{}".format(ch_name,thresh),";x [mm]",nx,xmin,xmax)
    hden = ROOT.TH1D("h_den_{}_amp{}".format(ch_name,thresh),";x [mm]",nx,xmin,xmax)
    hnum.Sumw2()
    hden.Sumw2()

    region = "x_dut[{}]>{}&&x_dut[{}]<{}&&y_dut[{}]>{}&&y_dut[{}]<{}".format(dut,xmin,dut,xmax,dut,ymin,dut,ymax)
    
    if thresh >= 200 :  
        if opt == "all": sel="(amp[0]>%i||amp[1]>%i||amp[2]>%i)"%(thresh,thresh,thresh)
        else : sel = "amp[%i]>%i"%(ch,thresh)
    else :  
        if opt == "all" : 
            amp0 = "amp[0]>%i && t_peak[0]-LP2_20[3]>3e-9 && t_peak[0]-LP2_20[3]<5e-9"%(thresh)
            amp1 = "amp[1]>%i && t_peak[1]-LP2_20[3]>3e-9 && t_peak[1]-LP2_20[3]<5e-9"%(thresh)
            amp2 = "amp[2]>%i && t_peak[2]-LP2_20[3]>3e-9 && t_peak[2]-LP2_20[3]<5e-9"%(thresh)
            sel="({}||{}||{})".format(amp0,amp1,amp2)
        else : 
            sel = "amp[%i]>%i && t_peak[%i]-LP2_20[3]>3e-9 && t_peak[%i]-LP2_20[3]<5e-9"%(ch,thresh,ch,ch)

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

def onebin_check(tree,thresh,output):
    min_x = 20.45 
    max_x = 20.65 
    min_y = 22.9 
    max_y = 24.1

    hnum = ROOT.TH1D("h_num_amp{}".format(thresh),";y [mm]",1,min_y,max_y)
    hden = ROOT.TH1D("h_den_amp{}".format(thresh),";y [mm]",1,min_y,max_y)
    hnum.Sumw2()
    hden.Sumw2()

    region = "x_dut[{}]>{}&&x_dut[{}]<{}&&y_dut[{}]>{}&&y_dut[{}]<{}".format(dut,min_x,dut,max_x,dut,min_y,dut,max_y)
    
    if thresh >= 200 :  sel="(amp[0]>%i||amp[1]>%i||amp[2]>%i)"%(thresh,thresh,thresh)
    else : 
        amp0 = "amp[0]>%i && t_peak[0]-LP2_20[3]>3.0e-9 && t_peak[0]-LP2_20[3]<5.0e-9"%(thresh)
        amp1 = "amp[1]>%i && t_peak[1]-LP2_20[3]>3.0e-9 && t_peak[1]-LP2_20[3]<5.0e-9"%(thresh)
        amp2 = "amp[2]>%i && t_peak[2]-LP2_20[3]>3.0e-9 && t_peak[2]-LP2_20[3]<5.0e-9"%(thresh)
        sel="({}||{}||{})".format(amp0,amp1,amp2)

    tree.Project("h_num_amp{}".format(thresh),"y_dut[%i]"%dut,"{}&&{}&&{}&&{}".format(photek,track_sel,region,sel))
    tree.Project("h_den_amp{}".format(thresh),"y_dut[%i]"%dut,"{}&&{}&&{}".format(photek,track_sel,region))

    hist = hnum.Clone("h_eff_amp{}".format(thresh))
    hist.Divide(hnum,hden,1,1,"B")
    hist.GetYaxis().SetRangeUser(0.9,1.1)
    hist.GetYaxis().SetTitle("Efficiency (amp > {} mV)".format(thresh))
    hist.SetLineColor(ROOT.kBlack)
    hist.Draw()

    c = ROOT.TCanvas()
    c.Print("plots/three_efficiency/singlebin_amp{}.pdf".format(thresh))
    output.cd()
    hist.Write()

    print("Total Eff {}: {:.3f} pm {:.3f}".format(thresh, hist.GetBinContent(1), hist.GetBinError(1) ) )

    return hist 
    
def threed_check(tree,thresh,output):
    min_x = 20.0 
    max_x = 21.2 
    min_y = 22 
    max_y = 25 

    hnum = ROOT.TH2D("h_num_amp{}".format(thresh),";x [mm];y [mm]",30,min_x,max_x,50,min_y,max_y)
    hden = ROOT.TH2D("h_den_amp{}".format(thresh),";x [mm];y [mm]",30,min_x,max_x,50,min_y,max_y)
    hnum.Sumw2()
    hden.Sumw2()

    region = "x_dut[{}]>{}&&x_dut[{}]<{}&&y_dut[{}]>{}&&y_dut[{}]<{}".format(dut,min_x,dut,max_x,dut,min_y,dut,max_y)
    
    if thresh >= 200 :  sel="(amp[0]>%i||amp[1]>%i||amp[2]>%i)"%(thresh,thresh,thresh)
    else : 
        amp0 = "amp[0]>%i && t_peak[0]-LP2_20[3]>3.0e-9 && t_peak[0]-LP2_20[3]<5.0e-9"%(thresh)
        amp1 = "amp[1]>%i && t_peak[1]-LP2_20[3]>3.0e-9 && t_peak[1]-LP2_20[3]<5.0e-9"%(thresh)
        amp2 = "amp[2]>%i && t_peak[2]-LP2_20[3]>3.0e-9 && t_peak[2]-LP2_20[3]<5.0e-9"%(thresh)
        sel="({}||{}||{})".format(amp0,amp1,amp2)

    tree.Project("h_num_amp{}".format(thresh),"y_dut[%i]:x_dut[%i]"%(dut,dut),"{}&&{}&&{}&&{}".format(photek,track_sel,region,sel))
    tree.Project("h_den_amp{}".format(thresh),"y_dut[%i]:x_dut[%i]"%(dut,dut),"{}&&{}&&{}".format(photek,track_sel,region))

    hist = hnum.Clone("h_eff_3D_amp{}".format(thresh))
    hist.Divide(hnum,hden,1,1,"B")
    hist.GetZaxis().SetRangeUser(0,1)
    hist.GetZaxis().SetTitle("Efficiency, {} mV".format(thresh))
    hist.GetXaxis().SetNdivisions(505)
    #hist.SetLineColor(ROOT.kBlack)

    c = ROOT.TCanvas()
    c.SetRightMargin(0.2)
    hist.Draw("COLZ")
    ROOT.gPad.SetTickx()
    ROOT.gPad.SetTicky()
    c.Print("plots/three_efficiency/threed_amp{}.pdf".format(thresh))

    hist.GetZaxis().SetRangeUser(0.9,1)
    c.Print("plots/three_efficiency/threed_amp{}_zoom.pdf".format(thresh))

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

        if i==0: hist.Draw("hist e ")
        else: hist.Draw("hist e same")
        
        leg.AddEntry(hist,"Channel {}".format(channel_names[i]),"l")


    leg.Draw()
    c.Print("plots/three_efficiency/overlay_eff_{}amp.pdf".format(thresh))

    fit = ROOT.TF1("f_tot_eff","pol0",20.47,20.63)
    hist_all.Fit(fit,"Q","",20.47,20.63)
    #fit.Draw("same")
    print("Total Eff X: {:.3f} pm {:.3f}".format(  fit.GetParameter(0), fit.GetParError(0) ) )
    

    

def make_histos():
    # Loop through configurations 
    #


    output = ROOT.TFile.Open("plots/three_efficiency/tmp.root","RECREATE")
    chs = [2,0,1]  
    ch_names = [12,4,13]

    tree = get_tree(cfg)


    thresholds = [90,100,110] 
    thresholds = [100,110] 
    thresholds = [100] 
    #thresh = 110 #mV, noise threshold
    for thresh in thresholds: 
        threed_check(tree,thresh,output)
        onebin_check(tree,thresh,output)
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
