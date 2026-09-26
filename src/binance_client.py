import asyncio
import json
import logging
import config
import websockets
from websockets.exceptions import ConnectionClosed

class BinanceWebSocketClient():
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.logger = logging.getLogger(__name__)
        
    async def websocket_connect(self):
        retry_delay = config.RETRY_DELAY
    
        while True:
            try:
                self.logger.info("Connecting to Binance Websocket")
                self.websocket = await websockets.connect(
                    self.uri,
                    ping_interval = config.PING_INTERVAL,
                    ping_timeout = config.PING_TIMEOUT
                )
                self.logger.info("Connected to Binance WebSocket")
                return
                
            except Exception as error:
                self.websocket = None
                self.logger.info(f"Binance WebSocket Connection Failed: {error}")
                self.logger.info(f"Retrying in {retry_delay} seconds")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, config.MAX_RETRY_DELAY)
        
    async def websocket_receive(self):
        async for message in self.websocket:
            data = json.loads(message)

            # Combined-stream URLs (/stream?...) wrap the payload
            if "data" in data:
                data = data["data"]

            # Ignore subscription acks like {"result": null, "id": 1}
            if data.get("e") != "24hrTicker":
                continue

            yield {
                "SYMBOL": data["s"],
                "BID": data["b"],
                "ASK": data["a"],
                "LAST": data["c"],
                "VOLUME": data["v"],
            }
            
    async def websocket_subscribe(self, symbols):
        
        if self.websocket is None:
            return
            
        streams = [
            f"{symbol.lower()}@ticker"
            for symbol in symbols
        ]
        
        print(streams)
            
        subscribe = {
            "method": "SUBSCRIBE",
            "params": streams,
            "id": 1
        }
        
        try:
            await self.websocket.send(json.dumps(subscribe))
            print("SUBSCRIPTION SENT")
        except ConnectionClosed:
            self.logger.warning(
                "Cannot subscribe: WebSocket connection is closed."
            )
        
    async def websocket_unsubscribe(self, symbols):
        
        if self.websocket is None:
            return
            
        streams = [
            f"{symbol.lower()}@ticker"
            for symbol in symbols
        ]
            
        unsubscribe = {
            "method": "UNSUBSCRIBE",
            "params": streams,
            "id": 2
        }
        
        try:
            await self.websocket.send(json.dumps(unsubscribe))
        except ConnectionClosed:
            self.logger.warning(
                "Cannot unsubscribe: WebSocket connection is closed."
            )
        
    async def websocket_disconnect(self):
        await self.websocket.close(
            code=1000, reason="user closed connection"
        )
        self.websocket = None
            
