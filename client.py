import asyncio
from aiohttp import ClientSession


async def get_posts():
    async with ClientSession() as session:
        async with session.get("http://127.0.0.1:8080/posts") as resp:
            return await resp.json()


async def get_post(elem_id):
    async with ClientSession() as session:
        async with session.get(f"http://127.0.0.1:8080/post/{elem_id}") as resp:
            return await resp.text()


async def post_posts():
    async with ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8080/post", json={
            "title": "world",
            "text": "hello",
            "owners": 1
        }) as resp:
            if resp.status != 201:
                return await resp.text()
            return await resp.json()


async def patch_posts(owners, text, title, elem_id):
    async with ClientSession() as session:
        async with session.patch(f"http://127.0.0.1:8080/post/{elem_id}", json={
            "owners": owners,
            "title": title,
            "text": text,
        }) as resp:
            if resp.status != 200:
                return await resp.text()
            return await resp.json()


async def delete_post(elem_id):
    async with ClientSession() as session:
        async with session.delete(f"http://127.0.0.1:8080/post/{elem_id}") as resp:
            return {"status": resp.status}


async def main():
    pass



asyncio.run(main())