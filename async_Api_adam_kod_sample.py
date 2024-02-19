import aiohttp
import asyncio

async def reset_files(session, url):
    async with session.post(url) as response:
        return await response.json() 
    
async def process_summaries(session, url):
    print("A feldolgozás elindult, ez percekig is tarthat. Kérjük, legyen türelemmel...")
    async with session.post(url) as response:
        return await response.json()  
    
async def chain_analysis(session, url):
    print("A láncanalízis elindult, ez is percekig tarthat. Kérjük, legyen türelemmel...")
    async with session.post(url) as response:
        return await response.json()  

async def send_post_request_with_file(session, url, file_path):
    
    mpwriter = aiohttp.MultipartWriter('form-data')


    with open(file_path, 'rb') as f:
        part = mpwriter.append(f)
        part.set_content_disposition('form-data', name='file', filename=file_path)

       
        async with session.post(url, data=mpwriter) as response:
            return await response.text()


async def apple_categorize(session, url):
    async with session.post(url) as response:
        return await response.json()  

async def bisac_categorize(session, url):
    async with session.post(url) as response:
        return await response.json()

async def thema_categorize(session, url):
    async with session.post(url) as response:
        return await response.json()  

async def clil_categorize(session, url):
    async with session.post(url) as response:
        return await response.json() 

async def wgnr_categorize(session, url):
    async with session.post(url) as response:
        return await response.json()



async def get_big_summary(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            
            return await response.text()
        else:
            
            raise Exception(f"Hiba a GET kérés során: {response.status}")

async def main():
    reset_url = "http://91.107.238.245:8000/reset"
    summarizer_url = "http://91.107.238.245:8000/chapter-summarizer/"
    epub_file_path = "./epub/223723.epub"

    async with aiohttp.ClientSession() as session:
        
        reset_response = await reset_files(session, reset_url)
        print("Reset válasz:", reset_response)

     
        summarizer_response = await send_post_request_with_file(session, summarizer_url, epub_file_path)
        print("Summarizer válasz:", summarizer_response)
    
    
        process_summaries_url = "http://91.107.238.245:8000/process-summaries/"
        process_summaries_response = await process_summaries(session, process_summaries_url)
        print("Process summaries válasz:", process_summaries_response)
        
        chain_analysis_url = "http://91.107.238.245:8000/chain-analysis/"
        chain_analysis_response = await chain_analysis(session, chain_analysis_url)
        print("Chain analysis válasz:", chain_analysis_response)
        
        apple_categorize_url = "http://91.107.238.245:8000/apple_categorize/"
        apple_categorize_response = await apple_categorize(session, apple_categorize_url)
        print("Apple categorize válasz:", apple_categorize_response)
        
        bisac_categorize_url = "http://91.107.238.245:8000/bisac_categorize/"
        bisac_categorize_response = await bisac_categorize(session, bisac_categorize_url)
        print("Bisac categorize válasz:", bisac_categorize_response)

        thema_categorize_url = "http://91.107.238.245:8000/thema_categorize/"
        thema_categorize_response = await thema_categorize(session, thema_categorize_url)
        print("Thema categorize válasz:", thema_categorize_response)
        
        clil_categorize_url = "http://91.107.238.245:8000/clil_categorize/"
        clil_categorize_response = await clil_categorize(session, clil_categorize_url)
        print("Clil categorize válasz:", clil_categorize_response)
        
        wgnr_categorize_url = "http://91.107.238.245:8000/wgnr_categorize/"
        wgnr_categorize_response = await wgnr_categorize(session, wgnr_categorize_url)
        print("Wgnr categorize válasz:", wgnr_categorize_response)
        
        get_big_summary_url = "http://91.107.238.245:8000/get_big_summary/"
        big_summary = await get_big_summary(session, get_big_summary_url)
        print("Big Summary tartalma:", big_summary)


asyncio.run(main())
