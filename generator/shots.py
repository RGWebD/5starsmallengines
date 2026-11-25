import asyncio,sys,functools,threading,http.server,socketserver
from playwright.async_api import async_playwright
tag=sys.argv[1]; pages=sys.argv[2].split(',') if len(sys.argv)>2 else ['index']
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a):pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.ThreadingTCPServer(('127.0.0.1',8944),functools.partial(Q,directory='/workspace/fivestar/site'));threading.Thread(target=srv.serve_forever,daemon=True).start()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        for w,h in [(1440,900),(390,844)]:
            ctx=await b.new_context(viewport={'width':w,'height':h},device_scale_factor=1)
            pg=await ctx.new_page()
            await pg.add_init_script("sessionStorage.setItem('seen5','1')")
            for n in pages:
                await pg.goto(f'http://127.0.0.1:8944/{n}.html',wait_until='domcontentloaded'); await pg.wait_for_timeout(1500)
                await pg.screenshot(path=f'/workspace/fivestar-work/{tag}_{n}_{w}_top.png')
                H=await pg.evaluate('document.body.scrollHeight')
                for y in range(0,H,500): await pg.evaluate(f'scrollTo(0,{y})'); await pg.wait_for_timeout(90)
                await pg.wait_for_timeout(2200); await pg.evaluate('scrollTo(0,0)'); await pg.wait_for_timeout(400)
                await pg.screenshot(path=f'/workspace/fivestar-work/{tag}_{n}_{w}_full.png',full_page=True)
            await ctx.close()
        await b.close()
asyncio.run(main())
