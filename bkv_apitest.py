import aiohttp
import asyncio


async def send_post_chat(session, url, chatquestion): 
    payload = {
        "collection": "output",
        "prompt": chatquestion,
        "temperature": 0
        }
    token = "5pBHDjr4bkNFc1xdqIMR6INLItKuPvZrf8zNdc6enlXqhy8qVO8YCYKRcdd"
    header = {"Authorization": f"Bearer {token}"}
    async with session.post(url, json=payload, headers=header) as response:
      if response.status == 200:
        data = await response.text()
        print(data)
        return data
      else:
        print(f"Error: {response.status}")      

        
async def main():
    chat_url = "http://91.107.238.245:5000/collections/stream"
 

# Quadrant  DB  uRL: http://91.107.238.245:6333/dashboard#/collections

    async with aiohttp.ClientSession() as session:  
        while True:
          try:
              print("Adja meg a kérdést:")
              clv = input()
              chat_response = await send_post_chat(session,chat_url,clv)
              print("Summarizer válasz: \n", chat_response)
              
          except KeyboardInterrupt:
              break 
        
    


asyncio.run(main())