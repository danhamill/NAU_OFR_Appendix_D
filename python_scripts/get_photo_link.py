# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 15:47:46 2017

@author: dan
"""

import pandas as pd
import requests
from StringIO import StringIO
from bs4 import BeautifulSoup
import time

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
    df =pd.read_csv(c, delim_whitespace=True, skiprows=range(0,4),usecols=[0],names=['data'])
    
    df = df.apply(lambda x: x.str.slice(44,52))
    df['data'] = pd.to_datetime(df['data'].astype(str), format='%Y%m%d')
    return df

def get_cam_dates_bs4(cam_name):
    #build url to find data
    url = build_cam_url(cam_name)
    
    #Fetch Data
    t = requests.get(url)
    
    #Make Soup
    soup = BeautifulSoup(t.content)
    
    #find a hrefs
    thing = soup.find_all('a')
    
    #pares out dates
    a = [link.attrs['href'] for link in thing]
    a = a[1:]
    a = [g[-21:-13] for g in a]
    
    df = pd.DataFrame({'dates':a})
    df['dates'] = pd.to_datetime(df['dates'].astype(str), format='%Y%m%d')
    return df


if __name__ == '__main__':
    start = time.clock()
    df1 =get_cam_dates('RC0629R')
    elapsed = (time.clock() - start)
    print "Processing took ", elapsed , "seconds to analyse using requests"
    
    start = time.clock()
    df2 = get_cam_dates_bs4('RC0629R')
    elapsed = (time.clock() - start)
    print "Processing took ", elapsed , "seconds to analyse using beautiful soup"
