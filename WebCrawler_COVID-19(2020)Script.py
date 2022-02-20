# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 00:24:30 2022

@author: onais
"""
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 00:24:30 2022

@author: onais
"""
from warcio.archiveiterator import ArchiveIterator
import re
import requests
import winsound

frequency = 2000
duration = 1000
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
URL_HalfPart=open("warc.paths","r")
Lines = URL_HalfPart.readlines()
k=0

ReCompile=re.compile(r'(?=.*\bcovid\b)(?=.*\beconomy\b).*',re.IGNORECASE)
for L in Lines:
    Preprocess=L.strip("\n")
    Archive_URL_2020="https://commoncrawl.s3.amazonaws.com/"+Preprocess
    stream = requests.get(Archive_URL_2020, stream=True).raw
    m=0
    for i in ArchiveIterator(stream):
        
            if i.rec_type == "warcinfo":
                continue
            #loop = asyncio.get_event_loop()
            #html=loop.run_until_complete(Search(i.rec_headers.get_header("WARC-Target-URI")))
            contents = (i.content_stream().read().decode("utf-8", "replace"))
            Comparision=BeautifulSoup(contents,features="lxml").find('body')
            if re.search(ReCompile,str(Comparision)):
                winsound.Beep(frequency, duration)
                with open("sample.txt", "a+") as file_object:
                    file_object.seek(0)
                    data = file_object.read(100)
                    if len(data) > 0 :
                        file_object.write("\n")
                    file_object.write(i.rec_headers.get_header("WARC-Target-URI"))
                    print(i.rec_headers.get_header("WARC-Target-URI"))
            m+=1
    print(m)