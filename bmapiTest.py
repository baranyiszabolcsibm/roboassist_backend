import aiohttp
import asyncio

async def reset_files(session, url):
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

async def main():
    reset_url = "http://91.107.238.245:8080/reset"
    extract_url = "http://91.107.238.245:8080/extract-pdf/"
    pdf_file_path = "c:\\tmp\\1.pdf"

    async with aiohttp.ClientSession() as session:
        
        reset_response = await reset_files(session, reset_url)
        print("Reset válasz:", reset_response)

     
        extract_response = await send_post_request_with_file(session, extract_url, pdf_file_path)
        print("Summarizer válasz:", extract_response)

        get_file_metadata_url = "http://91.107.238.245:8080/get-meta-pdf"
        file_metadata = await get_metadata_summary(session, get_file_metadata_url)
        print("Metadta tartalma:", file_metadata)


        
    
    


asyncio.run(main())





