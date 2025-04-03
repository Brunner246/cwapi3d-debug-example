import os
import sys
from typing import List, Optional
import asyncio

site_packages_path = os.path.join(os.path.dirname(__file__), '.venv', 'Lib', 'site-packages')
paths = [
    site_packages_path,
    os.path.dirname(__file__),
    os.path.dirname("ui"),
    os.path.dirname("routes"),
]

os.environ['PYTHONPATH'] = os.pathsep.join([*paths, os.environ.get('PYTHONPATH', '')])
sys.path.extend(paths)

import uvicorn
from PyQt5.QtCore import QEventLoop, QTimer, QCoreApplication
from fastapi import FastAPI
import nest_asyncio
from pydantic import BaseModel, Field

# Enable nested event loops for asyncio in Qt
nest_asyncio.apply()

from endtype_surface import create_surface_with_endtype
from debug_manager import DebugManager
from routes.routes import router
from server.fast_api_server import FastAPIServer


app = FastAPI()
app.include_router(router)


async def run_server_and_app(rest_api_server: FastAPIServer, cadwork_qt_app: QCoreApplication): #, event_loop: QEventLoop
    server_task = asyncio.create_task(rest_api_server.start())

    print("FastAPI server started. Press Ctrl+C to exit.")

    try:
        while True:
            cadwork_qt_app.processEvents() # need to do this, otherwise cadwork is blocked forever...
            await asyncio.sleep(0.01)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        await rest_api_server.stop()
        server_task.cancel()
        # event_loop.exit()
        try:
            await server_task
        except asyncio.CancelledError:
            pass


if __name__ == '__main__':
    debug = DebugManager()
    debug.debug_enabled = False

    if debug.debug_enabled:
        import pydevd_pycharm

        pydevd_pycharm.settrace('localhost', port=3000, stdoutToServer=True,
                                stderrToServer=True, patch_multiprocessing=False)

    app_qt = QCoreApplication.instance()
    if not app_qt:
        print("No Qt application instance found. Exiting.")
        sys.exit(1)

    # Create an instance of QEventLoop to process Qt events within the asyncio event loop
    # We need this... otherwise cadwork is blocking...
    # loop = QEventLoop()

    try:
        api_server = FastAPIServer(app, port=3030)
        asyncio.run(run_server_and_app(api_server, app_qt)) # , loop
    except KeyboardInterrupt:
        print("Application terminated by user")
