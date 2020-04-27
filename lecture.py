import requests
import re
import sys
import os
from PIL import Image
import urllib.request
import time


# Static Stuff
HOST='https://lecturenotes.in/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'x-requested-with': 'XMLHttpRequest',
    'DNT': '1',
    'Connection': 'keep-alive',
}

# Initialization

url=input('Enter The URL: ')
id=re.findall(r"(?<=lecturenotes\.in\/)(m|notes)\/(\d+)(?=-)",url)
try:
    id = int(id[0][1])
except:
    print("Invalid URL")
    sys.exit(1)
print('Collecting Pages....')

# Start Collection

flag = True
page_no=1
buffer=20
page_urls=[]
while flag:
    response = requests.get('https://lecturenotes.in/material/v2/'+str(id)+'/page-'+str(page_no)+'?noOfItems='+str(buffer), headers=headers).json()['page']
    received_buffer = len(response)
    page_urls+=response

    if received_buffer<buffer:
        flag=False
    else:
        page_no+=buffer
    print('Collected Pages: ',len(page_urls))
print('Starting Download of {pages} pages...'.format(pages=len(page_urls)))
for page in page_urls:
    print(page)
sys.exit(0)
# Download Pages

os.mkdir("lecture_data")
images=[]
for page in page_urls:
    image_url = "https://lecturenotes.in" + page['path']
    r = requests.get(image_url)
    imPath="lecture_data/{}.jpg".format(page['pageNum'])
    with open(imPath, 'wb') as f:
        f.write(r.content)
    
    images.append(Image.open(imPath).convert('RGB'))
print('[+] Images Downloaded !!')
print('[-] Converting to PDF ...')
# Saves As PDF
front=Image.open(urllib.request.urlopen('https://avatars3.githubusercontent.com/u/42498830')).convert('RGB')
pdfPath='lecture_'+str(id)+"_"+time.strftime("%Y%m%d-%H%M%S")+'.pdf'
front.save(pdfPath,save_all=True, append_images=images)

print('[+] PDF Saved as {file}...'.format(file=pdfPath))