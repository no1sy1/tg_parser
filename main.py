import asyncio
import json
from datetime import datetime
from telethon import TelegramClient, events
import os

API_ID = '23034305'
API_HASH = 'e22460370b737649c1413e61dfa8b1e3'
PHONE_NUMBER = '+79872947427'

# Список каналов
CHANNELS = [
    'vipclean24',
    'rabotavmsk1', 
    'rabota0404',
    'gruzchiki_moskva77',
    'raznorabms',
    'repetitorsonline',
    'personalhoreca_chat'
]

class TelegramJobParser:
    def __init__(self):
        self.client = TelegramClient('job_parser', API_ID, API_HASH)
        self.results = []
        
    async def init_client(self):
        await self.client.start(PHONE_NUMBER)
        print("Клиент инициализирован")
        
    async def parse_channel(self, channel_username):
        try:
            print(f"Парсинг канала: {channel_username}")
            
            entity = await self.client.get_entity(channel_username)
            
            messages = []
            async for message in self.client.iter_messages(entity, limit=100):
                if message.text:
                    messages.append({
                        'channel': channel_username,
                        'date': message.date.isoformat(),
                        'text': message.text,
                        'id': message.id
                    })
                    
            return messages
            
        except Exception as e:
            print(f"Ошибка при парсинге {channel_username}: {e}")
            return []
    
    async def parse_all_channels(self):
        tasks = []
        for channel in CHANNELS:
            task = asyncio.create_task(self.parse_channel(channel))
            tasks.append(task)
            
        results = await asyncio.gather(*tasks)
        
        for channel_results in results:
            self.results.extend(channel_results)
            
        self.results.sort(key=lambda x: x['date'], reverse=True)
        
    def save_to_json(self):
        filename = f"telegram_jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"Результаты сохранены в {filename}")
        
    def print_results(self):
        for message in self.results:
            print(f"\n--- {message['channel']} ---")
            print(f"Дата: {message['date']}")
            print(f"Сообщение: {message['text'][:200]}...")
            print("-" * 50)

async def main():
    parser = TelegramJobParser()
    await parser.init_client()
    await parser.parse_all_channels()
    parser.print_results()
    parser.save_to_json()
    
    await parser.client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())