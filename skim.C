#include <iostream>
#include <fstream>
#include <TROOT.h>
#include <TChain.h>
#include <TTree.h>
#include <TFile.h>
#include <vector>


void single_skim(int run){
    TFile* infile  = new TFile(Form("/eos/uscms/store/group/cmstestbeam/2020_02_CMSTiming/KeySightScope/RecoData/TimingDAQRECO/RecoWithTracks/v6/run_scope%i_converted.root",run));
    TFile* outfile = new TFile(Form("skims/run_%i.root",run), "RECREATE");

    TTree *intree = (TTree*)infile->Get("pulse");
    gROOT->cd();
    TTree *outtree = intree->CopyTree("amp[0]>100||amp[1]>100||amp[2]>100");

    outfile->cd();
    outtree->Write();
    outfile->Close();
    infile->Close();

}

void skim(){
    
    single_skim(29167);
    single_skim(29168);
    single_skim(29169);
    single_skim(29170);
    single_skim(29171);
    single_skim(29172);
    single_skim(29173);
    single_skim(29174);
    single_skim(29175);
    single_skim(29176);
    single_skim(29177);
    single_skim(29178);
    single_skim(29181);
    single_skim(29183);
    single_skim(29184);
    single_skim(29186);
    single_skim(29187);
    single_skim(29189);
    single_skim(29190);
    single_skim(29191);
    single_skim(29192);
    single_skim(29193);
    single_skim(29194);
    single_skim(29197);
    single_skim(29198);
    //4_13_12
    //single_skim(29121);
    //single_skim(29122);
    //single_skim(29123);
    //single_skim(29124);
    //single_skim(29125);
    //single_skim(29126);
    //single_skim(29127);
    //single_skim(29128);
    //single_skim(29129);
    //single_skim(29130);
    //single_skim(29132);
    //single_skim(29133);
    //single_skim(29134);
    //single_skim(29135);
    //single_skim(29136);
    //single_skim(29137);
    //single_skim(29138);
    //single_skim(29139);
    //single_skim(29140);
    //single_skim(29141);
    //single_skim(29142);
    //single_skim(29143);
    //single_skim(29144);
    //single_skim(29145);
    //single_skim(29146);
    //single_skim(29147);
}
