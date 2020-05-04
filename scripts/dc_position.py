from common import *
import os, sys, re
import ROOT

ROOT.gStyle.SetOptStat(0)

nx = 80
ny = 80
xmin = 19 
xmax = 22 
ymin = 22 
ymax = 25
def draw_position_amp(tree,ch,ch_name,output):

    ##track_sel = "ntracks==1&&npix>0&&nback>0"
    #dist = "amp[{}]>11&&amp[{}]<30:y_dut[{}]:x_dut[{}]".format(ch,ch,dut,dut)
    #hist = "({},{},{},{},{},{})".format(nx,xmin,xmax,ny,ymin,ymax)
    #sel = "{}&&{}".format(track_sel,photek)
    #
    #c = ROOT.TCanvas("ch{}_ampslice_xy".format(ch_name),"",800,800)
    #tree.Draw("{}>>{}".format(dist,hist),sel,"PROFCOLZ")
    #
    #c.Print("plots/dc_position/ch{}_ampslice_xy.pdf".format(ch_name))

    name = "dc_amp_xy"
    hist = ROOT.TProfile2D(name,";x [mm];y [mm];Mean Amplitude [mV]",nx,xmin,xmax,ny,ymin,ymax,0,100)

    sel = "{}&&{}".format(track_sel,photek)
    #amp = "t_peak[%i]-LP2_20[3]>-0.5e-9 && t_peak[%i]-LP2_20[3]<2.0e-9"%(ch,ch)
    dist = "amp[{}]:y_dut[{}]:x_dut[{}]".format(ch,dut,dut)
    
    tree.Project(name,dist,sel,"PROFCOLZ")

    c = ROOT.TCanvas("slice_eff_xy","",900,800)
    c.SetTopMargin(0.1)
    c.SetLeftMargin(0.2)
    c.SetBottomMargin(0.20)
    c.SetRightMargin(0.2)
    #c.SetPadRightMargin()
    hist.Draw("COLZ") 
    hist.GetZaxis().SetTitleOffset(1.15)
    hist.GetYaxis().SetTitleOffset(1.3)
    hist.GetXaxis().SetNdivisions(505)
    hist.GetYaxis().SetNdivisions(505)
    hist.GetZaxis().SetRangeUser(10,60)
    c.Print("plots/dc_position/ch{}_meanamp_xy.pdf".format(ch_name))

    output.cd()
    hist.Write()

    return 
def draw_position_special(tree,ch,ch_name,output):

    ##track_sel = "ntracks==1&&npix>0&&nback>0"
    #dist = "amp[{}]>11&&amp[{}]<30:y_dut[{}]:x_dut[{}]".format(ch,ch,dut,dut)
    #hist = "({},{},{},{},{},{})".format(nx,xmin,xmax,ny,ymin,ymax)
    #sel = "{}&&{}".format(track_sel,photek)
    #
    #c = ROOT.TCanvas("ch{}_ampslice_xy".format(ch_name),"",800,800)
    #tree.Draw("{}>>{}".format(dist,hist),sel,"PROFCOLZ")
    #
    #c.Print("plots/dc_position/ch{}_ampslice_xy.pdf".format(ch_name))

    name_num = "dc_num_xy"
    name_den = "dc_den_xy"
    hist_num = ROOT.TH2F(name_num,";x [mm];y [mm];Events",nx,xmin,xmax,ny,ymin,ymax)
    hist_den = ROOT.TH2F(name_den,";x [mm];y [mm];Events",nx,xmin,xmax,ny,ymin,ymax)
    hist_num.Sumw2()
    hist_den.Sumw2()

    sel = "{}&&{}".format(track_sel,photek)
    amp = "amp[%i]>11 && amp[%i]<30 && t_peak[%i]-LP2_20[3]>-0.5e-9 && t_peak[%i]-LP2_20[3]<2.0e-9"%(ch,ch,ch,ch)
    dist = "y_dut[{}]:x_dut[{}]".format(dut,dut)
    
    tree.Project(name_num,dist,sel+"&&"+amp,"COLZ")
    tree.Project(name_den,dist,sel,"COLZ")

    hist = hist_num.Clone("slice_eff_xy")
    hist.Divide(hist_num,hist_den,1,1,"B")
    hist.GetZaxis().SetRangeUser(0,1)
    hist.GetZaxis().SetTitle("Efficiency, 11-30 mV")
    hist.GetXaxis().SetNdivisions(505)
    c = ROOT.TCanvas("slice_eff_xy","",900,800)
    c.SetTopMargin(0.1)
    c.SetLeftMargin(0.2)
    c.SetBottomMargin(0.20)
    c.SetRightMargin(0.2)
    #c.SetPadRightMargin()
    hist.Draw("COLZ") 
    hist.GetZaxis().SetTitleOffset(1.15)
    hist.GetYaxis().SetTitleOffset(1.3)
    hist.GetXaxis().SetNdivisions(505)
    hist.GetYaxis().SetNdivisions(505)
    c.Print("plots/dc_position/ch{}_ampslice_xy.pdf".format(ch_name))

    output.cd()
    hist.Write()

    return 

def draw_position(tree,ch,ch_name,minAmp,output):

    ##track_sel = "ntracks==1&&npix>0&&nback>0"
    #dist = "amp[{}]>{}:y_dut[{}]:x_dut[{}]".format(ch,minAmp,dut,dut)
    #hist = "({},{},{},{},{},{})".format(nx,xmin,xmax,ny,ymin,ymax)
    #sel = "{}&&{}".format(track_sel,photek)
    #
    #c = ROOT.TCanvas("ch{}_amp{}_xy".format(ch_name,minAmp),"",800,800)
    #tree.Draw("{}>>{}".format(dist,hist),sel,"PROFCOLZ")

    #
    #c.Print("plots/dc_position/ch{}_amp{}_xy.pdf".format(ch_name,minAmp))

    name_num = "dc_num_xy"
    name_den = "dc_den_xy"
    hist_num = ROOT.TH2F(name_num,";x [mm];y [mm];Events",nx,xmin,xmax,ny,ymin,ymax)
    hist_den = ROOT.TH2F(name_den,";x [mm];y [mm];Events",nx,xmin,xmax,ny,ymin,ymax)
    hist_num.Sumw2()
    hist_den.Sumw2()

    sel = "{}&&{}".format(track_sel,photek)
    amp = "amp[%i]>%i && t_peak[%i]-LP2_20[3]>-0.5e-9 && t_peak[%i]-LP2_20[3]<2.0e-9"%(ch,minAmp,ch,ch)
    dist = "y_dut[{}]:x_dut[{}]".format(dut,dut)
    
    tree.Project(name_num,dist,sel+"&&"+amp,"COLZ")
    tree.Project(name_den,dist,sel,"COLZ")

    hist = hist_num.Clone("{}_eff_xy".format(minAmp))
    hist.Divide(hist_num,hist_den,1,1,"B")
    hist.GetZaxis().SetRangeUser(0,1)
    hist.GetZaxis().SetTitle("Efficiency, {} mV".format(minAmp))
    hist.GetXaxis().SetNdivisions(505)
    c = ROOT.TCanvas("{}_eff_xy".format(minAmp),"",900,800)
    c.SetTopMargin(0.1)
    c.SetLeftMargin(0.2)
    c.SetBottomMargin(0.20)
    c.SetRightMargin(0.2)
    #c.SetPadRightMargin()
    hist.Draw("COLZ") 
    hist.GetZaxis().SetTitleOffset(1.15)
    hist.GetYaxis().SetTitleOffset(1.3)
    hist.GetXaxis().SetNdivisions(505)
    hist.GetYaxis().SetNdivisions(505)
    c.Print("plots/dc_position/ch{}_amp{}_xy.pdf".format(ch_name,minAmp))

    output.cd()
    hist.Write()

    return 


def make_histos():
    # Loop through configurations 
    #

    output = ROOT.TFile.Open("plots/dc_position/tmp.root","RECREATE")
    
    cfg = "config_209_4_13_DC_photek"
    ch_names = [4,13,"DC"]

    tree = get_tree(cfg)

    draw_position_amp(tree,2,"DC",output)
    draw_position_special(tree,2,"DC",output)
    draw_position(tree,2,"DC",11,output)
    draw_position(tree,2,"DC",30,output)

    #for ch in range(0,3):
        #draw_amplitude(tree,ch,ch_names[ch],output,"low")
        #draw_charge(tree,ch,ch_names[ch],output,"low")
    
    return 

make_histos()
