import html
from flask import Flask, jsonify,request,Response,send_file   #pip install  flask   flask[async]
from flask_cors import CORS #pip install -U flask-cors
import aiohttp
import asyncio
import json
import os
from PyPDF2 import PdfMerger   ##pip install PyPDF2
import uuid
import re


app = Flask(__name__)
CORS(app)   #https://flask-cors.readthedocs.io/en/latest/
#app.config['JSON_AS_ASCII'] = False

# CORS miatt kell
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res 



@app.route('/mnbapi/agentcall', methods=['GET'])
async def agentcall():
    question = request.args.get('question')
    payload = {
        "input": question,
        "chat_history": []
        }
    result = {
        'docs': [],
        'pages': [],
        'summarydoc': 's',
        'answer': 'x'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(agent_url, json=payload ) as response:
            if response.status == 200:
                data = await response.text()
                print(data)
                json_obj = json.loads(data)

                # await asyncio.sleep(10)

                # rag_response = await send_post(session,ragquery_url,question)
                # json_subobj = json.loads(rag_response)
                # if len(json_subobj['outputs']) >0:
                #     docs_str = ', '.join(json_subobj['docs'])
                #     result['answer'] += '\n Referencia: \n '+docs_str + '\n\n'

                result['answer'] = '<html><body>' + json_obj['output'].replace('\n', '<br>').encode('ascii', 'xmlcharrefreplace').decode() + '</body></html>'
                # result['summarydoc'] = json_subobj['docs'] [0]
            else:
                print(f"Error: {response.status}") 
                result['answer'] = "Hiba az agent hívásakor"

  
        return jsonify(result)


#http://localhost:5000//mnbapi/ragsearch?question="mi a szavatolótőke
#@app.route('/todo/api/v1.0/extractPdf', methods=['GET'])
    
@app.route('/mnbapi/ragsearch', methods=['GET'])
async def ragsearch():
    question = request.args.get('question')
    question = html.unescape(question)
    print(question)

    result = {
        'docs': [],
        'pages': [],
        'summarydoc': 's',
        'answer': 'x'
    }
    async with aiohttp.ClientSession() as session:  
        rag_response = await send_post(session,ragquery_url,question)
        json_obj = json.loads(rag_response)    ## válasz json doksikista ahol talált valamit
        print(rag_response )

        if len(json_obj['outputs']) == 0:
            result['answer'] = 'Nincs találat'      
            return jsonify(result)
        
        sumid= str(uuid.uuid1())
        result['summarydoc'] =  mergePdf(json_obj['outputs'],sumid) ## összefűzött doksikista
        summarypdfPath = basepath+result['summarydoc']
        result['docs'] = json_obj['outputs']
        
        #await asyncio.sleep(10)

        ## visszaadott összefűzött doksi elemzése
        url_with_question = process_pdf_url.format(question)
        analyzeResult = await send_post_request_with_file(session,url_with_question,summarypdfPath)
        print(analyzeResult)
        json_obj = json.loads(analyzeResult)
        page_numbers = find_page_numbers(json_obj['answer'])
        result['pages'] = page_numbers  ## a page_numbers a process-pdf válaszából jön
        result['answer'] = '<html><body>' + json_obj['answer'].replace('\n', '<br>').encode('ascii', 'xmlcharrefreplace').decode() + '</body></html>'

        return jsonify(result)
    

@app.route('/mnbapi/getPdf/<filename>', methods=['GET'])
def get_pdf(filename):   # igy az url vegen van a filename
     # filename = request.args.get('filename')         ez a likommentezett módszernél kell
    # Path to the PDF file
    pdf_path = './pdftmp/'+filename
    try:
        return send_file(pdf_path, download_name=filename, mimetype='application/pdf')
    except FileNotFoundError:
        # If the file is not found, return a 404 error
        return 'File not found', 404
    
##################################################
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
  return "summary_{}.pdf".format(summaryid)

def find_page_numbers(text):
    pattern = r'Page (\d+)'
    matches = re.findall(pattern, text)
    return [int(num) for num in matches]

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
    with open(file_path, 'rb') as f:
        part = mpwriter.append(f)
        part.set_content_disposition('form-data', name='pdf_file', filename=file_path)  
        async with session.post(url, data=mpwriter) as response:
            return await response.text()


def json_to_array(json_obj):
    json_array = []
    for key, value in json_obj.items():
        json_array.append({"key":key,"value" :value})
    return json_array

if __name__ == '__main__':
        # Process the JSON object here

    agent_url = "http://91.107.238.245:8015/mnb_qa_agent"
    ragquery_url = "http://91.107.238.245:8016/mnb_metadataRAG"
    process_pdf_url = "http://91.107.238.245:8016/process-pdf/?question={}"
    basepath = "./pdftmp/"    ## global
    
    app.run(debug=True)


