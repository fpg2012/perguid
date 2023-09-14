import tornado
import asyncio
import json
import logging
from pathlib import Path

file_name = Path('markdown.md')
static_dir = Path('.')

class UpdateHander(tornado.web.RequestHandler):
    
    def put(self):
        args = json.loads(self.request.body)
        content = args['content']
        try:
            f = open(file_name, 'w')
            f.write(content)
        except Exception:
            print('error occurred')
            self.send_error(500)
        finally:
            f.close()

class MarkdownHandler(tornado.web.RequestHandler):
    
    def get(self):
        content = ''
        with open(file_name, 'r') as f:
            content = f.read()
        self.write(json.dumps({
            'status': 200,
            'content': content,
        }))

async def main(port, address):
    app = tornado.web.Application([
        (r'/update', UpdateHander),
        (r'/markdown', MarkdownHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, { 'path': static_dir, 'default_filename': 'index.html' })
    ])
    app.listen(port, address)
    await asyncio.Event().wait()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    tornado.options.define('file', default='markdown.md', help='file to store markdown')
    tornado.options.define('dir', default='./static', help='webpage directory')

    tornado.options.define('port', default=3451, help='port')
    tornado.options.define('ip', default='127.0.0.1', help='ip')
    
    file_name = Path(tornado.options.options.file).absolute()
    static_dir = Path(tornado.options.options.dir).absolute()

    logging.info(f'markdown file: {file_name}')
    logging.info(f'webpage directory: {static_dir}')
    logging.info(f'listen on: http://{tornado.options.options.ip}:{tornado.options.options.port}')

    asyncio.run(main(port=tornado.options.options.port, address=tornado.options.options.ip))