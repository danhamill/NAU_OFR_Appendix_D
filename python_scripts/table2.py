# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 12:12:23 2017

@author: dan
"""

import pandas as pd
from glob import glob
import numpy as np
import os

def latex_format_dataframe(df):
    
    try: #Sandbar with bathymetry
        working_copy = df.copy()
        working_copy = working_copy.replace('NA*', np.nan,regex=True)
        working_copy=working_copy.replace(u'±',u'\pm',regex=True)
        working_copy['Volume.High'] = '{$' + working_copy['Volume.High'].astype(str) + '$}'
        working_copy['Volume.Fluc'] = '{$' + working_copy['Volume.Fluc'].astype(str) + '$}'
        working_copy['Volume.Low'] = '{$' + working_copy['Volume.Low'].astype(str) + '$}'
        working_copy['Volume.x'] = '{$' + working_copy['Volume.x'].astype(str) + '$}'
        working_copy['Volume.y'] = '{$' + working_copy['Volume.y'].astype(str) + '$}'
        working_copy['Total_Site_Vol'] = '{$' + working_copy['Total_Site_Vol'].astype(str) + '$}'
        working_copy['Date'] = '{' + working_copy['Date'].astype(str) + '}'
        working_copy = working_copy.replace(u'{\$NA*', np.nan,regex=True)
        working_copy = working_copy.replace(u'{\$na*', np.nan,regex=True)
    except: #Sandbar without bathymetery
        working_copy = df.copy()
        working_copy = working_copy.replace('NA*', np.nan,regex=True)
        working_copy=working_copy.replace(u'±',u'\pm',regex=True)
        working_copy['Volume.High'] = '{$' + working_copy['Volume.High'].astype(str) + '$}'
        working_copy['Volume.Fluc'] = '{$' + working_copy['Volume.Fluc'].astype(str) + '$}'
        working_copy['Date'] = '{' + working_copy['Date'].astype(str) + '}'
        working_copy = working_copy.replace(u'{\$NA*', np.nan,regex=True)
        working_copy = working_copy.replace(u'{\$na*', np.nan,regex=True)
    return working_copy
    
def write_tex(df,oFile):
    '''
    Fucntion to output formatted tex file contaning tabular data for Table 2 for each site in appendix D
    '''
    if len(df.columns)==10: # Sandbars with bathymetry
        with open(oFile, "w") as f:
            f.write("\\begin{landscape} \n")
            f.write("\\begin{longtable}{" + "".join(["c"] * len(df.columns)) + "}\n")
            f.write("\\caption{Area and volume estimates derived from the DEMs $\\lbrack$volume error was determined by multiplying the assigned value of total surface uncertainty ($TU_Z$), for each elevation bin, depending on data collection method used to generate the surface$\\rbrack$ }  \\\\\n")
            
            f.write("\\toprule & \\multicolumn{2}{c}{High Elevation} & \\multicolumn{2}{c}{Fluctuating Zone}& \\multicolumn{2}{c}{Low Elevation}& {Total Eddy} & {Total Channel} & {Total Site} \\\\\n")
            f.write("\\cmidrule(r){2-3} \\cmidrule(r){4-5} \\cmidrule(r){6-7} \n")
            f.write("{Survey Date}& {Area (m{$^2$})}  &{Volume (m{$^3$})}&{Area (m{$^2$})}&{Volume (m{$^3$})}&{Area (m{$^2$})}&{Volume (m{$^3$})} &{Volume (m{$^3$})}&{Volume (m{$^3$})}&{Volume (m{$^3$})} \\\\\n")
            f.write("\\midrule\\endfirsthead\n")
            f.write("\\multicolumn{10}{l}	{{Table \\thetable\\ Continued from previous page}} \\\\\n")
            f.write("\\toprule & \\multicolumn{2}{c}{High Elevation} & \\multicolumn{2}{c}{Fluctuating Zone}& \\multicolumn{2}{c}{Low Elevation}& {Total Eddy} & {Total Channel} & {Total Site} \\\\\n")
            f.write("\\cmidrule(r){2-3} \\cmidrule(r){4-5} \\cmidrule(r){6-7} \n")
            f.write("{Survey Date}& {Area (m{$^2$})}  &{Volume (m{$^3$})}&{Area (m{$^2$})}&{Volume (m{$^3$})}&{Area (m{$^2$})}&{Volume (m{$^3$})} &{Volume (m{$^3$})}&{Volume (m{$^3$})}&{Volume (m{$^3$})} \\\\\n")
            f.write("\\midrule\\endhead \n")
            f.write("\\bottomrule\\endfoot \n")
            for i, row in df.iterrows():
                f.write(" & ".join([str(x) for x in row.values]) + " \\\\\n")
            f.write("\\end{longtable} \n")
            f.write("\\end{landscape} \n")
            
    elif len(df.columns) == 5: #Sandbars with out Bathymetry
        with open(oFile, "w") as f:
            f.write("\\begin{longtable}{" + "".join(["c"] * len(df.columns)) + "}\n")
            f.write("\\caption{Area and volume estimates derived from the DEMs $\\lbrack$volume error was determined by multiplying the assigned value of total surface uncertainty ($TU_Z$), for each elevation bin, depending on data collection method used to generate the surface$\\rbrack$ }  \\\\\n")
            f.write("\\toprule & \\multicolumn{2}{c}{High Elevation} & \\multicolumn{2}{c}{Fluctuating Zone} \\\\\n")
            f.write("\\cmidrule(r){2-3} \\cmidrule(r){4-5} \n")
            f.write("{Survey Date}& {Area (m{$^2$})}  &{Volume (m{$^3$})}&{Area (m{$^2$})}&{Volume (m{$^3$})} \\\\\n")
            f.write("\\midrule\\endfirsthead\n")
            f.write("\\multicolumn{5}{l}	{{Table \\thetable\\ Continued from previous page}} \\\\\n")
            f.write("\\toprule & \\multicolumn{2}{c}{High Elevation} & \\multicolumn{2}{c}{Fluctuating Zone} \\\\\n")
            f.write("\\cmidrule(r){2-3} \\cmidrule(r){4-5} \n")
            f.write("{Survey Date}& {Area (m{$^2$})}  &{Volume (m{$^3$})}&{Area (m{$^2$})}&{Volume (m{$^3$})} \\\\\n")
            f.write("\\midrule\\endhead \n")
            f.write("\\bottomrule\\endfoot \n")
            for i, row in df.iterrows():
                f.write(" & ".join([str(x) for x in row.values]) + " \\\\\n")
            f.write("\\end{longtable}")
    replacements = {'nan':'---'}
    lines = []
    
    #Search and replace nans to em dash
    with open(oFile,"r") as infile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            lines.append(line)
    with open(oFile,'w+') as outfile:
        for line in lines:
            outfile.write(line)
   
    
if __name__ =='_main__':
    
    files = glob(r"C:\workspace\sandbar_process\plotting_out\*\*_Merge_Site_Table.csv")
    tex_root = r"C:\workspace\NAU_OFR_Appendix_D"
    
    for file in files[10:11]:
        
        #Get site code
        site = file.split('\\')[-2]
        
        #check to see if output directories exist
        if os.path.exists(tex_root + os.sep + site):
            print 'Path Exists!!!'
        else:
            os.mkdir(tex_root + os.sep + site)
            os.mkdir(tex_root + os.sep + site + os.sep + 'input')
        
        out_root = tex_root + os.sep + site + os.sep + 'input'
    
        df = pd.read_csv(file,sep=':')
        
        df = latex_format_dataframe(df)
        oFile = out_root + os.sep + 'Table2.tex'
        write_tex(df,oFile)








        
        