from style import setStyle
from common import *
import os, sys, re
import ROOT

outfile = ROOT.TFile("plots/position/tmp.root","RECREATE")
def get_position(tree,cfg,ch,ch_name):
    
    #minAmp = 110 # for now 
    minAmp = 100 # for now 

    nx = 70
    ny = 70
    xmin = 18 
    xmax = 22 
    ymin = 22 
    ymax = 25

    name_num = "{}_{}_num_xy".format(cfg,ch_name)
    name_den = "{}_{}_den_xy".format(cfg,ch_name)
    hist_num = ROOT.TH2F(name_num,";x [mm];y [mm];Events",nx,xmin,xmax,ny,ymin,ymax)
    hist_den = ROOT.TH2F(name_den,";x [mm];y [mm];Events",nx,xmin,xmax,ny,ymin,ymax)
    hist_num.Sumw2()
    hist_den.Sumw2()

    sel = "{}&&{}".format(track_sel,photek)
    amp = "amp[%i]>%i && t_peak[%i]-LP2_20[3]>3.0e-9 && t_peak[%i]-LP2_20[3]<5.0e-9"%(ch,minAmp,ch,ch)
    dist = "y_dut[{}]:x_dut[{}]".format(dut,dut)
    
    tree.Project(name_num,dist,sel+"&&"+amp,"COLZ")
    tree.Project(name_den,dist,sel,"COLZ")

    hist = hist_num.Clone("{}_{}_eff_xy".format(cfg,ch_name))
    hist.Divide(hist_num,hist_den,1,1,"B")
    hist.GetZaxis().SetRangeUser(0,1)
    hist.GetZaxis().SetTitle("Efficiency, {} mV".format(minAmp))
    hist.GetXaxis().SetNdivisions(505)
    hist.GetYaxis().SetNdivisions(505)
    c = ROOT.TCanvas()
    hist.Draw("COLZ") 
    c.Print("plots/position/{}_ch{}_eff_xy.pdf".format(cfg,ch_name))

    outfile.cd()
    hist.Write()

    return 
    


def get_cfg_results(cfg):

    print(cfg)
    tree = get_tree(cfg)

    config = cfg.split("_")[1]
    ch_names = []
    ch_names.append(cfg.split("_")[2])
    ch_names.append(cfg.split("_")[3])
    ch_names.append(cfg.split("_")[4])

    for ch,ch_name in enumerate(ch_names):
        if ch_name != "14" and ch_name != "6" : continue
        get_position(tree,config,ch,ch_name) 
     

def get_configurations():
    # Loop through configurations 
    cfg_list = open("configs/configurations.txt","r")
    for i,line in enumerate(cfg_list): 
            
        # for tmp debugging
        #if i > 0: break 

        if "#" in line: continue
        cfg = line.strip()

        get_cfg_results(cfg)

# Main
if __name__ == "__main__":
    # execute only if run as a script
    #main()
    get_configurations()

