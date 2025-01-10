import coloredlogs
import uvicorn

from app.server import app

if __name__ == "__main__":
    coloredlogs.install(level='DEBUG')

    app.debug = True

    config = uvicorn.Config(app, host="localhost", port=8000)
    server = uvicorn.Server(config)
    server.run()
