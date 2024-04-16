import json
import os
import aiohttp
import asyncio
from PyPDF2 import PdfMerger   ##pip install PyPDF2
import uuid
import re

basepath = "./pdftmp/"    ## global

async def send_post(session, url, chatquestion): 
    payload = {
        "input": chatquestion
        }
    async with session.post(url, json=payload ) as response:
      if response.status == 200:
        data = await response.text()
        print(data)
        return data
      else:
        print(f"Error: {response.status}")      

async def send_post_request_with_file(session, url, file_path): 
    mpwriter = aiohttp.MultipartWriter('form-data')
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        part = mpwriter.append(f)
        part.set_content_disposition('form-data', name='pdf_file', filename=file_name)  
        async with session.post(url, data=mpwriter) as response:
            resdata = await response.text()
            print(resdata)
            return resdata
        
def mergePdf(pdflist,summaryid):
  merger = PdfMerger()
  #pdflist = ["21.pdf", "25.pdf"]
  for p in pdflist:
    pdfpath=basepath+p
    try:
      merger.append(pdfpath)
    except:
      print("Hiba a fájl olvasásakor: ",pdfpath)
      continue
  merger.write(basepath+"summary_{}.pdf".format(summaryid))
  merger.close()

def find_page_numbers(text):
    pattern = r'Page (\d+)'
    matches = re.findall(pattern, text)
    return [int(num) for num in matches]

        
async def main():
    chat_url = "http://91.107.238.245:8016/mnb_metadataRAG"
    process_pdf_url = "http://91.107.238.245:8016/process-pdf/?question={}"
    
 

    async with aiohttp.ClientSession() as session:  
        while True:
          try:
              print("Adja meg a kérdést:")
              clv_question = input()
              chat_response = await send_post(session,chat_url,clv_question)
              print("Summarizer válasz: \n", chat_response)
              json_obj = json.loads(chat_response)
              sumid= str(uuid.uuid1())
              mergePdf(json_obj['outputs'],sumid)
              #for item in json_obj['outputs']:
              #   print(basepath+item)Milyen ajánlásokat készített az MNB hitelintézeti hitelvállalási kockázatok témakörben
                 

              ##print("File feltöltés")
              clv_file =  "C:\\Users\\szabaran\\OneDrive - Crayon Group\\source\\BMAI\\mnb_backend\\pdftmp\\summary_{}.pdf".format(sumid)  
              print(clv_file)   
              url_with_question = process_pdf_url.format(clv_question)
              restxt = await send_post_request_with_file(session,url_with_question,clv_file)
              json_obj = json.loads(restxt)
              page_numbers = find_page_numbers(json_obj['answer'])
              print(page_numbers)
            

              


          except KeyboardInterrupt:
              break 
        
    


asyncio.run(main())