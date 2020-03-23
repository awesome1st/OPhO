import asyncpg

class AsyncPostgresDB():
    def __init__(self, dsn, user, loop):
        self.dsn = dsn
        self.user = user
        self.loop = loop
        self.pool = None
    
    async def init(self):
        self.pool = await asyncpg.create_pool(
            dsn=self.dsn, 
            user=self.user, 
            command_timeout=60, 
            loop=self.loop
        )
    
    async def execute_job(self, query, *args):
	    # args = list(args)
        con = await self.pool.acquire()
        async with con.transaction():
            await con.execute(query, *args)
        await self.pool.release(con)
    
    async def fetchrow(self, query, *args):
        con = await self.pool.acquire()
        async with con.transaction():
            row = await con.fetchrow(query, *args)
        await self.pool.release(con)
        return row
    
    async def fetchval(self, query, *args):
        con = await self.pool.acquire()
        async with con.transaction():
            value = await con.fetchval(query, *args)
        await self.pool.release(con)
        return value
    
    async def close(self):
        await self.pool.close()