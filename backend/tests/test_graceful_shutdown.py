"""ASG-NFR-008: on SIGTERM stop accepting, finish in-flight requests, close pools, exit.

uvicorn installs ``Server.handle_exit`` as its SIGTERM handler; the test calls it with
SIGTERM while a request is in flight, which is the same code path as a real signal but
works on every platform and needs no sleeping: threading events order everything.
"""

import signal
import threading

import httpx2 as httpx
import pytest
import uvicorn

from app.config import Settings
from app.main import create_app
from tests.conftest import FakeProbe


class NotifyingServer(uvicorn.Server):
    def __init__(self, config: uvicorn.Config) -> None:
        super().__init__(config)
        self.ready = threading.Event()

    async def startup(self, sockets: list | None = None) -> None:  # type: ignore[type-arg,override]
        await super().startup(sockets)
        self.ready.set()


def test_an_in_flight_request_completes_after_sigterm_and_the_server_exits(
    settings: Settings, capsys: pytest.CaptureFixture[str]
) -> None:
    started = threading.Event()
    finish = threading.Event()
    app = create_app(settings, probes=[FakeProbe("postgres"), FakeProbe("redis")])

    @app.get("/slow")
    def slow() -> dict[str, bool]:
        started.set()
        finish.wait(timeout=10)
        return {"done": True}

    server = NotifyingServer(
        uvicorn.Config(app, host="127.0.0.1", port=0, log_config=None, lifespan="on")
    )
    server_thread = threading.Thread(target=server.run)
    server_thread.start()
    assert server.ready.wait(timeout=10), "the server did not start"
    port = server.servers[0].sockets[0].getsockname()[1]

    outcome: dict[str, httpx.Response] = {}

    def call() -> None:
        outcome["response"] = httpx.get(f"http://127.0.0.1:{port}/slow", timeout=15)

    caller = threading.Thread(target=call)
    caller.start()
    assert started.wait(timeout=10), "the request never reached the handler"

    server.handle_exit(signal.SIGTERM, None)  # what uvicorn does on SIGTERM
    finish.set()
    caller.join(timeout=15)
    server_thread.join(timeout=15)

    assert not caller.is_alive()
    assert outcome["response"].status_code == 200
    assert outcome["response"].json() == {"done": True}
    assert not server_thread.is_alive(), "the server did not exit after the signal"
    assert "shutdown: closing connection pools" in capsys.readouterr().out
