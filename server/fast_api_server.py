import asyncio

import uvicorn
from fastapi import FastAPI


class FastAPIServer:
    def __init__(self, app:FastAPI, host="127.0.0.1", port=12000):
        self.host = host
        self.port = port
        self.server = None
        self.app = app
        self.shutdown_event = asyncio.Event()

    async def start(self):
        """Start the FastAPI server asynchronously"""
        config = uvicorn.Config(
            self.app,
            host=self.host,
            port=self.port,
            log_level="debug",
        )
        self.server = uvicorn.Server(config)
        print(f"Starting FastAPI server at http://{self.host}:{self.port}")
        await self.server.serve()

    async def stop(self):
        if self.server:
            print("Stopping FastAPI server")
            await self.server.shutdown()