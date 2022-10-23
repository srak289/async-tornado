import argparse
import asyncio
import json
import logging
import subprocess
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

logger = logging.getLogger('server')

async def amain():
    class AsyncHandler(tornado.web.RequestHandler):
        async def get(self):
            logger.info("Running async process")
            r = await asyncio.create_subprocess_exec('sleep', '2')
            await r.wait()
            self.write(json.dumps(dict(response='pong'))+'\n')

    app = tornado.web.Application([
        (r"/", AsyncHandler),
    ])

    app.listen(8000)
    await asyncio.Event().wait()

def _main():
    class SlowHandler(tornado.web.RequestHandler):
        def get(self):
            logger.info("Running slow process")
            subprocess.run(['sleep', '2'])
            self.write(json.dumps(dict(response='pong'))+'\n')

    app = tornado.web.Application([
        (r"/", SlowHandler),
    ])

    app.listen(8000)
    IOLoop.current().start()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--debug', help='debug', action='store_true')
    ap.add_argument('-A', '--aio', help='run with async', action='store_true')
    args = ap.parse_args()

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    tlog = logging.getLogger('tornado.web')
    tlog.addHandler(ch)
    tlog.setLevel(logging.INFO)

    if args.debug:
        logger.setLevel(logging.DEBUG)
    if args.aio:
        asyncio.run(amain())
    else:
        _main()

if __name__ == '__main__':
    main()
