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
import numpy as np

def build_water_url(site,yesterday):
    url = 'https://waterdata.usgs.gov/az/nwis/dv?cb_00060=on&format=rdb&site_no=' + gc + '&referred_module=sw&period=&begin_date=1989-01-01&end_date=' + yesterday 
    return url

def get_water_data(site):
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
    url = build_water_url(site,yesterday)
    
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
    tmp_df['Date'] = pd.to_datetime(tmp_df['Date'], format="%Y-%m-%d")
    tmp_df['Flow_cms'] = tmp_df['Flow_cfs']*0.3048**3
    return tmp_df.set_index('Date')

def build_cam_url(cam_name):
    base_url = 'http://grandcanyon.usgs.gov/photos/SandbarPhotos'
    cam_url = base_url + '/' + cam_name +'/'
    return cam_url

def get_cam_dates(cam_name):
    
    #build url to find data
    url = build_cam_url(cam_name)
    
    #Fetch Data
    t = requests.get(url)
    data = t.text
    data = data.decode('utf-8').replace('<A','\n')
    c = StringIO(data)
    df =pd.read_csv(c, delim_whitespace=True, skiprows=range(0,4),usecols=[0],names=['date'])
    
    df = df.apply(lambda x: x.str.slice(44,52))
    df['date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
    return df

def populate_cam_col(row):
    if (row.Survey_Date == cam_dates.date).any():
        return '{\\checkmark}'
    else:
        return np.nan
    
def formative_discharge(row,water):
    return water.loc[row['Survey_Date']-pd.Timedelta(days=30):row['Survey_Date']]['Flow_cms'].mean(axis=0)

def peak_discharge(row,water):
    return water.loc[row['Survey_Date']-pd.Timedelta(days=30):row['Survey_Date']]['Flow_cms'].max(axis=0)

def sbes_checker(row,errors):
    if errors.loc[row['Survey_Date']]['Uncertainty'].max(axis=0) ==0.18:
        return '{\\checkmark}'
    else:
        return np.nan
    
def mbes_checker(row,errors):
    if errors.loc[row['Survey_Date']]['Uncertainty'].max(axis=0) == 0.11:
        return '{\\checkmark}'
    else:
        return np.nan
    
def get_errors(sheet, lu_error):
    errors = lu_error.get_group(sheet)
    errors.loc[:,'SurveyDate'] = pd.to_datetime(errors.loc[:,'SurveyDate'], format = "%Y-%m-%d")
    return errors.set_index('SurveyDate')

if __name__ =='__main__':
    
    # USGS gage numbers
    lf = '09380000'
    gc = '09402500'

    lf_data = get_water_data(lf)
    gc_data = get_water_data(gc)
    
    lu_cam_names = pd.read_excel(r"C:\workspace\NAU_OFR_Appendix_D\lookup\Remote_Camera_LU.xlsx").set_index('SiteID')
    lu_cam_names['cam_name'] = lu_cam_names['cam_name'].astype(str)
    
    lu_error = pd.read_excel(r"C:\workspace\sandbar_process\Date_Error_lookup.xlsx",sheet_name='DateError_LU').groupby('Site')
    xl = pd.ExcelFile(r"C:\workspace\survey_stage\survey_stage.xlsm")
    
    xl.sheet_names
    
    for sheet in xl.sheet_names[:-4]:
        print sheet
        
        cam_name = lu_cam_names.loc[sheet].values[0]
        
        cam_dates = get_cam_dates(cam_name)
        df = xl.parse(sheet,parse_cols="H:I,M").dropna()
        
        df['Photo_Record'] = df.apply(lambda x: populate_cam_col(x), axis=1)
        df['Formative_Discharge'] = df.apply(lambda x: formative_discharge(x,lf_data),axis=1)
        df['Peak_Discharge'] =  df.apply(lambda x: peak_discharge(x,lf_data),axis=1)
        
        
        errors = get_errors(sheet,lu_error)
        
        df['MBES'] = df.apply(lambda x: mbes_checker(x, errors), axis=1)        
        df['SBES'] = df.apply(lambda x: sbes_checker(x, errors), axis=1)   
