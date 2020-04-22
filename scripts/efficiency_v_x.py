from common import *
import os, sys, re
import ROOT


#thresholds = [100]
thresholds = [50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]

#config_211_4_13_12_photek
#config_212_4_3_14_photek
#config_213_4_13_14_photek
#config_214_6_5_11_photek
# channel name, config, scope ch
infos=[]
infos.append([14, "config_212_4_3_14_photek", 2])
infos.append([3 , "config_212_4_3_14_photek", 1])
infos.append([13, "config_211_4_13_12_photek", 1])
infos.append([4 , "config_211_4_13_12_photek", 0])
infos.append([12, "config_211_4_13_12_photek", 2])
infos.append([5 , "config_214_6_5_11_photek", 1])
infos.append([11, "config_214_6_5_11_photek", 2])
infos.append([6 , "config_214_6_5_11_photek", 0])

def get_efficiency_v_x(tree,config,ch,ch_name,thresh,output): 
    
    minx=19.8
    maxx=21.8
    miny=22.8
    maxy=24.2
    nx=140

    hnum = ROOT.TH1D("h_num_{}_amp{}".format(ch_name,thresh),";x [mm]",nx,minx,maxx)
    hden = ROOT.TH1D("h_den_{}_amp{}".format(ch_name,thresh),";x [mm]",nx,minx,maxx)
    hnum.Sumw2()
    hden.Sumw2()

    region = "x_dut[{}]>{}&&x_dut[{}]<{}&&y_dut[{}]>{}&&y_dut[{}]<{}".format(dut,minx,dut,maxx,dut,miny,dut,maxy)
    
    sel = "amp[%i]>%i"%(ch,thresh)
    tree.Project("h_num_{}_amp{}".format(ch_name,thresh),"x_dut[%i]"%dut,"{}&&{}&&{}&&{}".format(track_sel,region,sel,photek))
    tree.Project("h_den_{}_amp{}".format(ch_name,thresh),"x_dut[%i]"%dut,"{}&&{}&&{}".format(track_sel,region,photek))

    hist = hnum.Clone("h_eff_{}_amp{}".format(ch_name,thresh))
    hist.Divide(hnum,hden,1,1,"B")


    c = ROOT.TCanvas()
    hist.Draw()
    c.Print("plots/efficiency_v_x/{}_effx_amp{}.pdf".format(ch_name,thresh))
    output.cd()
    hist.Write()

    return hist 

def plot_overlay(infos,thresh,output,opt=""):
    
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    c = ROOT.TCanvas("c","",1000,500)
    leg = ROOT.TLegend(0.73,0.2,0.88,0.88)
    for i,info in enumerate(infos):  
        
        ch_name = info[0]
    
        hist = output.Get("h_eff_{}_amp{}".format(ch_name,thresh))
        hist.SetMaximum(1.1)
        hist.SetMinimum(0)
        hist.GetYaxis().SetTitle("Efficiency (amp >{} mV)".format(thresh))
        hist.GetXaxis().SetTitle("x [mm]")
        hist.SetTitle("")
        cleanHist(hist,i)

        if i==0: hist.Draw("hist")
        else: hist.Draw("histsame")
        if "fit" in opt: 
    
            minx=19.8
            maxx=21.8
            f1 = ROOT.TF1("f_eff_{}_amp{}".format(ch_name,thresh),"gaus",minx,maxx)
            hist.Fit(f1,"Q")
            cleanFit(f1,i)
            f1.Draw("same")
            print(ch_name,f1.GetParameter(1),f1.GetParameter(2))
        
        leg.AddEntry(hist,"Channel {}".format(ch_name),"l")

    leg.Draw()
    if "fit" in opt: c.Print("plots/efficiency_v_x/eff_{}amp_fit.pdf".format(thresh)) 
    else: c.Print("plots/efficiency_v_x/eff_{}amp.pdf".format(thresh))

def make_histos():
    # Loop through configurations 
    #


    output = ROOT.TFile.Open("plots/efficiency_v_x/tmp.root","RECREATE")
    
    for info in infos:
        ch_name = info[0]
        cfg = info[1]
        ch = info[2]

        tree = get_tree(cfg)
        print(ch_name,cfg)

        for thresh in thresholds:     
            get_efficiency_v_x(tree,cfg,ch,ch_name,thresh,output) 
    

    return 

def make_plots():

    output = ROOT.TFile.Open("plots/efficiency_v_x/tmp.root")

    for thresh in thresholds: 
        plot_overlay(infos,thresh,output)
        if thresh == 110 : plot_overlay(infos,thresh,output,"fit")
        if thresh == 200 : plot_overlay(infos,thresh,output,"fit")
    return

# Main
if __name__ == "__main__":

    #make_histos()
    make_plots()
