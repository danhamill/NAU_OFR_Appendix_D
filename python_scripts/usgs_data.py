# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:07:33 2017

@author: dan
"""
import pandas as pd 
import numpy as np
import os
from StringIO import StringIO
import requests
from datetime import date, timedelta


def build_url(site,yesterday):
    url = 'https://waterdata.usgs.gov/az/nwis/dv?cb_00060=on&format=rdb&site_no=' + gc + '&referred_module=sw&period=&begin_date=1989-01-01&end_date=' + yesterday 
    return url

def get_data(site):
    '''
    Function to retreive daily discharge data between now and 1989-01-01
    Notes: Could not use the https://waterdata.usgs.gov/az/nwis/iv because the data only goes back to 2007
    Inputs: USGS gage number
    Outputs: Dataframe containing daily discharge measurements in cfs and cms
    
    '''
    #Get yesterdays date
    yesterday = date.today() - timedelta(1)
    yesterday=yesterday.strftime('%Y-%m-%d')
    
    #build url to tab sepearted data
    url = build_url(site,yesterday)
    
    #retreive data 
    t = requests.get(url)
    decoded = t.content.decode('utf-8')
    
    #convert data to stringio object for pandas csv reader
    c = StringIO(decoded)
    
    #make data frame and skip data file preamble
    tmp_df = pd.read_csv(c,sep='\t',skiprows=range(1,32)).reset_index()  #<---------------- if header changes, need to change the hard coded values in range()
    
    #format so the outpu makes sense
    tmp_df = tmp_df[['level_1','level_2','level_3']]
    tmp_df = tmp_df.rename(columns={'level_1':'Gage','level_2':'Date','level_3':'Flow_cfs'})
    tmp_df['Flow_cms'] = tmp_df['Flow_cfs']*0.3048**3
    return tmp_df



if __name__ =='__main__':
    
    # USGS gage numbers
    lf = '09380000'
    gc = '09402500'

    lf_data = get_data(lf)
    gc_data = get_data(gc)
    
    
