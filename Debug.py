import asyncio
import os
import sys

site_packages_path = os.path.join(os.path.dirname(__file__), '.venv', 'Lib', 'site-packages')
paths = [
    site_packages_path,
    os.path.dirname(__file__),
    os.path.dirname("ui"),
    os.path.dirname("routes"),
]

os.environ['PYTHONPATH'] = os.pathsep.join([*paths, os.environ.get('PYTHONPATH', '')])
sys.path.extend(paths)

from PyQt5.QtCore import QCoreApplication
from fastapi import FastAPI

from debug_manager import DebugManager
from routes.routes import router
from server.fast_api_server import FastAPIServer

app = FastAPI()
app.include_router(router)


async def run_server(rest_api_server: FastAPIServer, cadwork_qt_app: QCoreApplication):
    server_task = asyncio.create_task(rest_api_server.start())
    print("FastAPI server started. Press Ctrl+C to exit. "
          "Important to stop the server and close the application properly.")

    try:
        while True:
            cadwork_qt_app.processEvents()
            await asyncio.sleep(0.01)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        await rest_api_server.stop()
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            print("Error while stopping the server")
            pass


def main():
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
    try:
        api_server = FastAPIServer(app, port=3030)
        asyncio.run(run_server(api_server, app_qt))
    except KeyboardInterrupt:
        print("Application terminated by user")


if __name__ == '__main__':
    main()
