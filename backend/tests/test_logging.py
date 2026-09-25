"""ASG-NFR-009 and ASG-NFR-010: JSON logs on stdout only, every line with a request_id."""

import json
import logging

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.logging import configure_logging, request_id_var
from app.main import create_app
from tests.conftest import FakeProbe


def _json_lines(text: str) -> list[dict]:  # type: ignore[type-arg]
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def test_every_line_is_json_with_the_request_id_of_the_request(
    settings: Settings, capsys: pytest.CaptureFixture[str]
) -> None:
    app = create_app(settings, probes=[FakeProbe("postgres"), FakeProbe("redis")])
    with TestClient(app) as client:
        client.get("/health", headers={"X-Request-ID": "log-test-1"})

    lines = _json_lines(capsys.readouterr().out)
    assert lines, "nothing was written to stdout"
    for line in lines:
        assert {"timestamp", "level", "logger", "message", "request_id"} <= set(line)
    request_lines = [line for line in lines if line["message"] == "request"]
    assert request_lines[-1]["request_id"] == "log-test-1"
    assert request_lines[-1]["route"] == "/health"
    assert request_lines[-1]["status"] == 200


def test_lines_outside_a_request_carry_a_placeholder_request_id(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging("INFO")
    logging.getLogger("app.test").info("outside any request")

    (line,) = _json_lines(capsys.readouterr().out)
    assert line["request_id"] == "-"
    assert line["message"] == "outside any request"


def test_logging_goes_to_stdout_only_and_never_to_a_file() -> None:
    configure_logging("INFO")

    handlers = logging.getLogger().handlers
    assert len(handlers) == 1
    assert type(handlers[0]) is logging.StreamHandler
    assert not any(isinstance(handler, logging.FileHandler) for handler in handlers)


def test_an_exception_is_logged_with_its_traceback_and_the_request_id(
    capsys: pytest.CaptureFixture[str],
) -> None:
    configure_logging("INFO")
    token = request_id_var.set("exc-1")
    try:
        try:
            raise ValueError("bad")
        except ValueError:
            logging.getLogger("app.test").exception("failed")
    finally:
        request_id_var.reset(token)

    (line,) = _json_lines(capsys.readouterr().out)
    assert line["request_id"] == "exc-1"
    assert "ValueError: bad" in line["exception"]
