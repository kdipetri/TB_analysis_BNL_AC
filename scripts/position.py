from style import setStyle
from common import *
import os, sys, re
import ROOT


def get_position(tree,cfg,ch,ch_name):
    
    minAmp = 100 # for now 


    nx = 70
    ny = 70
    xmin = 18 
    xmax = 22 
    ymin = 22 
    ymax = 25

    track_sel = "ntracks==1&&npix>0&&nback>0"
    dist = "amp[{}]>{}:y_dut[{}]:x_dut[{}]".format(ch,minAmp,dut,dut)
    hist = "({},{},{},{},{},{})".format(nx,xmin,xmax,ny,ymin,ymax)
    
    c = ROOT.TCanvas()
    tree.Draw("{}>>{}".format(dist,hist),track_sel,"PROFCOLZ")
    c.Print("plots/position/{}_ch{}_xy.pdf".format(cfg,ch_name))

    return 
    
def get_position(tree,cfg,ch,ch_name):
    
    minAmp = 100 # for now 


    nx = 70
    ny = 70
    xmin = 18 
    xmax = 22 
    ymin = 22 
    ymax = 25

    track_sel = "ntracks==1&&npix>0&&nback>0"
    dist = "amp[{}]>{}:y_dut[{}]:x_dut[{}]".format(ch,minAmp,dut,dut)
    hist = "({},{},{},{},{},{})".format(nx,xmin,xmax,ny,ymin,ymax)
    
    c = ROOT.TCanvas()
    tree.Draw("{}>>{}".format(dist,hist),track_sel,"PROFCOLZ")
    c.Print("plots/position/{}_ch{}_xy.pdf".format(cfg,ch_name))

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
        get_position_v_x(tree,config,ch_names,outfile) 
     

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

