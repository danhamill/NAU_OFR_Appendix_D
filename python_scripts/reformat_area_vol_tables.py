# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 12:12:23 2017

@author: dan
"""

import pandas as pd
import numpy as np
import csv
    
    
df = pd.read_csv(r"C:\workspace\sandbar_process\plotting_out\003L\003L_Merge_Site_Table.csv",sep=':')

#df = df.replace('NA*', np.nan,regex=True)

df=df.replace(u'±',u'\pm',regex=True)

df['Volume.High'] = '{$' + df['Volume.High'].astype(str) + '$}'
df['Volume.Fluc'] = '{$' + df['Volume.Fluc'].astype(str) + '$}'
df['Volume.Low'] = '{$' + df['Volume.Low'].astype(str) + '$}'
df['Volume.x'] = '{$' + df['Volume.x'].astype(str) + '$}'
df['Volume.y'] = '{$' + df['Volume.y'].astype(str) + '$}'
df['Total_Site_Vol'] = '{$' + df['Total_Site_Vol'].astype(str) + '$}'
df['Date'] = '{' + df['Date'].astype(str) + '}'
df = df.replace(u'{\$NA*', np.nan,regex=True)
df = df.replace(u'{\$na*', np.nan,regex=True)

#df.to_csv(r"C:\workspace\NAU_OFR_Appendix_D\003L\input\table3.tex",sep='&',header=False,index=False,quoting=csv.QUOTE_NONE,line_terminator='\\'+'\\')

print df.to_latex(escape=False,header=False,index=False,na_rep='',longtable=True)


with open(r"C:\workspace\NAU_OFR_Appendix_D\003L\input\tex_manual.tex", "w") as f:
    f.write("\\begin{longtable}{" + "".join(["c"] * len(df.columns)) + "}\n")
    f.write("\\caption{Long Table Example}  \\\\\n")
    
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
    f.write("\\end{longtable}")

replacements = {'nan':'---'}
lines = []
with open(r"C:\workspace\NAU_OFR_Appendix_D\003L\input\tex_manual.tex") as infile:
    for line in infile:
        for src, target in replacements.iteritems():
            line = line.replace(src, target)
        lines.append(line)
with open(r"C:\workspace\NAU_OFR_Appendix_D\003L\input\tex_manual.tex", 'w') as outfile:
    for line in lines:
        outfile.write(line)
        
        