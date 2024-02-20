import aiohttp
import asyncio



async def send_post_request_with_file(session, url, file_path): 
    mpwriter = aiohttp.MultipartWriter('form-data')
    with open(file_path, 'rb') as f:
        part = mpwriter.append(f)
        part.set_content_disposition('form-data', name='file', filename='bsz1234.pdf')  
        async with session.post(url, data=mpwriter) as response:
            return await response.text()
        
async def send_post_chat(session, url, chatquestion): 
    payload = {
        "collection": "pelda-akta",
        "prompt": chatquestion,
        "temperature": 0
        }
    token = "5pBHDjr4bkNFc1xdqIMR6INLItKuPvZrf8zNdc6enlXqhy8qVO8YCYKRcdd"
    header = {"Authorization": f"Bearer {token}"}
    async with session.post(url, json=payload, headers=header) as response:
      if response.status == 200:
        data = await response.text()
        print(data)
      else:
        print(f"Error: {response.status}")      

        
async def main():
    summarizer_url = "http://localhost:5000/bmapi/uploadPdf"
    chat_url = "http://91.107.238.245:5000/collections/stream"
    epub_file_path = "c:\\tmp\\bszmokus.pdf"



    async with aiohttp.ClientSession() as session:   
        chat_response = await send_post_chat(session,chat_url,"Ki a feljelentő?")
        #summarizer_response = await send_post_request_with_file(session, summarizer_url, epub_file_path)
        print("Summarizer válasz:", chat_response)

asyncio.run(main())