"""Discord api wrapper without using any coroutine."""

import json
import time
import websocket
import requests
import threading

from typing import (
    List,
    Any,
    Union,
)

class Client:
    def __init__(self, token: str):
        self.ws = websocket.WebSocket()
        self.token = token
        self.event = None
        self.heartbeat_interval = None
        self.header = {
            "authorization": self.token,
            "content-type": "application/json"
        }
        self.slashies = {}

    def send(self, request) -> None:
        self.ws.send(json.dumps(request))

    def wait(self, seconds: float, mili: bool = True) -> None:
        time.sleep(seconds / 1000 if mili else seconds)

    def receive(self) -> dict:
        response = self.ws.recv()
        if response:
            return json.loads(response)

    def heartbeat(self) -> None:
        while True:
            self.wait(self.heartbeat_interval)
            content = {
                "op": 1,
                "d": "null"
            }
            self.send(content)

    def login(self, token) -> None:
        self.token = token
        self.ws.connect("wss://gateway.discord.gg/?v=6&encoding=json")
        self.event = self.receive()
        self.heartbeat_interval = self.event["d"]["heartbeat_interval"]

        threading.Thread(target=self.heartbeat).start()

        _payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "properties": {
                    "$os": "iOS",
                    "$browser": "Discord Android",
                    "$device": "phone"
                }
            }
        }
            
        self.send(_payload)

        while True:
            self.event = self.receive()

    def thread(self, func):
        def wrapper(*args, **kwargs):
            return threading.Thread(target=func, args=args, kwargs=kwargs).start()
        return wrapper

    def say(
        self,
        id: Union[str, int],
        content: Any = None,
        error: bool = True,
        components: List[dict] = None,
        embeds: List[dict] = None,
        nonce: str = None,
        tts: bool = False,
    ) -> Any:
        base = f"https://discord.com/api/v9/channels/{id}/messages"
        payload = {}

        if content:
            payload["content"] = content

        if components:
            payload["components"] = components

        if embeds:
            payload["embeds"] = embeds

        if nonce:
            payload["nonce"] = nonce

        if tts:
            payload["tts"] = tts

        response = requests.post(base, headers=self.header, json=payload)
        if error:
            response.raise_for_status()

        return response
