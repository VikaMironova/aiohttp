import sys
import asyncio
import aiopg
from aiohttp import web
from models import db, return_all_posts, AD


postgres = "postgres://new:0806@localhost:5432/aiohttp"


class ADPage(web.View):

    async def get(self):
        return web.json_response({"status": "OK"})


class ADSView(web.View):

    async def get(self):
        get_all = await return_all_posts()
        return web.json_response(get_all)


class ADView(web.View):

    async def get(self):
        post = int(self.request.match_info["elem_id"])
        get_post = await AD.by_id(post)
        return web.json_response(get_post.to_dict())

    async def post(self):
        data = await self.request.json()
        if bool("owners" and "title" and "text" not in data.keys()):
            raise web.HTTPBadRequest()
        create = await AD.create_model(**data)
        return web.json_response(create.to_dict())

    async def patch(self):
        data = await self.request.json()
        post = int(self.request.match_info["elem_id"])
        updated_data = await AD.update_model(post, **data)
        return web.json_response(updated_data.to_dict())

    async def delete(self):
        post = int(self.request.match_info["elem_id"])
        get_post = await AD.by_id(post)
        if not get_post:
            return web.HTTPNotFound()
        await get_post.delete()
        return web.HTTPNoContent()


async def register_pg_pool(app):
    print("start")
    async with aiopg.pool.create_pool(postgres) as pool:
        app['pg_pool'] = pool
        yield
        pool.close()
    print("end")


async def register_orm(app):
    await db.set_bind(postgres)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()

if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get("/", ADPage)
    ])
    app.add_routes([
        web.get("/posts", ADSView)
    ])
    app.add_routes([
        web.get("/post/{elem_id:\d+}", ADView),
        web.post("/post", ADView),
        web.patch("/post/{elem_id:\d+}", ADView),
        web.delete("/post/{elem_id:\d+}", ADView)
    ])
    app.cleanup_ctx.append(register_pg_pool)
    app.cleanup_ctx.append(register_orm)
    web.run_app(app)