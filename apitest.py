import aiohttp
import asyncio



async def send_post_request_with_file(session, url, file_path): 
    mpwriter = aiohttp.MultipartWriter('form-data')
    with open(file_path, 'rb') as f:
        part = mpwriter.append(f)
        part.set_content_disposition('form-data', name='file', filename='bsz1234.pdf')  
        async with session.post(url, data=mpwriter) as response:
            return await response.text()
        
async def main():
    summarizer_url = "http://localhost:5000/bmapi/uploadPdf"
    epub_file_path = "c:\\tmp\\bszmokus.pdf"

    async with aiohttp.ClientSession() as session:
    
        summarizer_response = await send_post_request_with_file(session, summarizer_url, epub_file_path)
        print("Summarizer válasz:", summarizer_response)

asyncio.run(main())