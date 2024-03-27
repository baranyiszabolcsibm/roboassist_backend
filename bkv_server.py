from flask import Flask, jsonify,request,Response,send_file   #pip install  flask   flask[async]
from flask_cors import CORS #pip install -U flask-cors
import aiohttp
import asyncio
import json

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


#http://localhost:5000/todo/api/v1.0/extractPdf
#@app.route('/todo/api/v1.0/extractPdf', methods=['GET'])
@app.route('/bmapi/extractPdf', methods=['GET'])
async def extractPdf():
    filename = request.args.get('filename')
    pdf_file_path = './pdftmp/'+filename 

    # get parames from request
    #  use  paramless function async def extractPdf(filename)
    #     category = request.args.get('category')
    #     content_id = request.args.get('content_id')
    fullanswer = ""
    async with aiohttp.ClientSession() as session:
        reset_response = await empty_post(session, reset_url)
        print("Reset válasz:", reset_response)
        extract_response = await send_post_request_with_file(session, extract_url, pdf_file_path)
        print("File kivonatoló AI válasz:", extract_response)
        file_metadata = await get_metadata_summary(session, get_file_metadata_url)
        print("PDF file metadta tartalma:", file_metadata)  
        response = jsonify(file_metadata)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response



@app.route('/bmapi/aktakerdes', methods=['GET'])
async def send_post_chat(): 
    collection = request.args.get('collection')
    question = request.args.get('question')
    resultmsg="&#x1F601 P\u00c9TER\ud83d\udc6e: A dokumentumok alapj\u00e1n a feljelent\u0151 neve Imre P\u00e9ter. Sajnos a dokumentumokban nem tal\u00e1lhat\u00f3 meg a feljelent\u0151 telefonsz\u00e1ma.";

    #
    # response = response = jsonify(resultmsg)
    # resx = resultmsg.encode('utf-8').decode('utf-8')
    # print(resx)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    # return response 

    question += " A dokumentum első forrását a válaszod végén ismételten add meg a következő formában is {{oldalszám}}"
    payload = {
        "collection": collection,
        "prompt": question,
        "temperature": 0
        }
    token = "5pBHDjr4bkNFc1xdqIMR6INLItKuPvZrf8zNdc6enlXqhy8qVO8YCYKRcdd"
    header = {"Authorization": f"Bearer {token}"}
    async with aiohttp.ClientSession() as session:
        async with session.post(chat_url, json=payload, headers=header) as response:
            if response.status == 200:
                data = await response.text()
                print(data)
                resultmsg = data
            else:
                print(f"Error: {response.status}")  

        resultmsg =resultmsg.replace("\\\"","\"")     
        resultmsg = resultmsg.encode('ascii', 'xmlcharrefreplace').decode('utf-8')
        resultmsg =resultmsg.replace("\n","<br />")      
  
        response = jsonify(resultmsg)
        response.headers.add('Access-Control-Allow-Origin', '*')
        #response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return response 

    







@app.route('/bmapi/uploadPdf', methods=['GET', 'POST'])   # mondket method kell mert a browser elsőször egy getet küld implicite
async def uploadPdf():
    if request.method == 'GET':
        response_headers = {'Access-Control-Allow-Origin': '*'  }
        return response
    try:
        # Get file from request
        file = request.files['file']
        filename = file.filename
        file.save('./pdftmp/'+filename)
        response_text = "Mentve Rendbe"
        response = jsonify(response_text)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except:
        response = 'Hibavan' ,409



##################################################


async def empty_post(session, url):
    async with session.post(url) as response:
        return await response.json() 


async def send_post_request_with_file(session, url, file_path): 
    mpwriter = aiohttp.MultipartWriter('form-data')
    with open(file_path, 'rb') as f:
        part = mpwriter.append(f)
        part.set_content_disposition('form-data', name='file', filename=file_path)  
        async with session.post(url, data=mpwriter) as response:
            return await response.text()

async def get_metadata_summary(session, url):
    async with session.get(url) as response:
        if response.status == 200:              
            return await response.text()
        else:             
            raise Exception(f"Hiba a GET kérés során: {response.status}")


def json_to_array(json_obj):
    json_array = []
    for key, value in json_obj.items():
        json_array.append({"key":key,"value" :value})
    return json_array

if __name__ == '__main__':
    
    baseurl='http://91.107.238.245:8080'
    MISTRALURL ='http://91.107.238.245:8080'
    GPT4URL ='http://91.107.238.245:8008'
    chat_url = "http://91.107.238.245:5000/collections/stream"


    reset_url = baseurl+"/reset"
    extract_url = baseurl+"/extract-pdf/"
    get_file_metadata_url = baseurl+"/get-meta-pdf"

    extract_feljelentési_jegyzokonyv_metadata_url = baseurl+"/feljelentési jegyzokonyv_metadata/"
    get_feljelentési_jegyzokonyv_metadata_url =  baseurl+"/get_feljelentési_jegyzokonyv_metadata"

    extract_nyomozas_elrendelo_metadata_url = baseurl+"/nyomozas_elrendelo_metadata/"
    get_nyomozas_elrendelo_metadata_url  =  baseurl+"/get_nyomozas_elrendelo_metadata"   

    extract_stat_adatlap_fill_url = baseurl+"/stat_adatlap_fill/"
    get_stat_adatlap_fill_url  =  baseurl+"/get_stat_adatlap_fill"  

    extract_stat_adatlap_btk_full_categorize_url = baseurl+"/stat_adatlap_btk_full_categorize/"
    get_stat_adatlap_btk_categories_url  =  baseurl+"/get_stat_adatlap_btk_categories"  

    extract_summary_url = baseurl+"/summarizer/"
    get_summary_url  =  baseurl+"/get_summary" 

    
    app.run(debug=True)


