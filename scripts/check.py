import json
import os
from pathlib import Path
import shlex
import signal
import subprocess
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import uuid4

ROOT = Path(__file__).resolve().parent.parent
PROJECT = "hw3-check-" + uuid4().hex[:12]
ENV = dict(os.environ, HOST_PORT="0", GREETING="hello world")
N = 3


def docker(*args, output=None):
    print("$ docker", shlex.join(args), flush=True)
    result = subprocess.run(
        ["docker", *args], cwd=ROOT, env=ENV, check=True, timeout=120,
        stdout=output if output is not None else subprocess.PIPE,
        text=output is None,
    )
    text = result.stdout or ""
    print(text, end="", flush=True)
    return text.strip()


def compose(*args):
    return docker("compose", "-p", PROJECT, "-f", str(ROOT / "compose.yaml"), *args)


def request(url, method, path, status=200, count=None):
    try:
        response = urlopen(Request(url + path, method=method), timeout=5)
    except HTTPError as error:
        response = error
    with response:
        data = json.load(response)
        actual_status = response.getcode()
    print(method, path, actual_status, json.dumps(data), flush=True)
    assert actual_status == status, f"HTTP {actual_status}, expected {status}"
    if count is not None:
        assert data["count"] == count, data


def main():
    stage = "start"
    passed = backup_running = False
    backup = ROOT / "backups" / (PROJECT + ".tar")
    try:
        compose("up", "-d", "--no-build", "--wait", "--wait-timeout", "90")
        url = "http://" + compose("port", "app", "8000")
        request(url, "GET", "/", count=0)

        stage = "increment"
        for _ in range(N):
            request(url, "POST", "/increment")
        request(url, "GET", "/", count=N)

        stage = "recreate app"
        compose("up", "-d", "--no-build", "--no-deps", "--force-recreate",
                "--wait", "--wait-timeout", "90", "app")
        url = "http://" + compose("port", "app", "8000")
        request(url, "GET", "/", count=N)

        stage = "restart Redis"
        compose("stop", "--timeout", "30", "redis")
        request(url, "GET", "/healthz")
        request(url, "GET", "/readyz", status=503)
        request(url, "POST", "/increment", status=503)
        compose("start", "--wait", "--wait-timeout", "90", "redis")
        request(url, "GET", "/", count=N)
        request(url, "POST", "/increment", count=N + 1)

        stage = "backup"
        compose("stop", "--timeout", "30", "app")
        compose("stop", "--timeout", "30", "redis")
        backup.parent.mkdir(exist_ok=True)
        with backup.open("wb") as output:
            backup_running = True
            docker("run", "--rm", "--name", PROJECT + "-backup", "--user", "0:0",
                   "--mount", f"type=volume,source={PROJECT}_redis-data,target=/data,readonly",
                   "--entrypoint", "tar", "redis:7.4-alpine", "-C", "/data", "-cpf", "-", ".", output=output)
            backup_running = False
        passed = True
    except (Exception, KeyboardInterrupt) as error:
        print(f"FAIL [{stage}]: {error or 'interrupted'}", flush=True)
    finally:
        if backup_running:
            try:
                subprocess.run(["docker", "rm", "-f", PROJECT + "-backup"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
            except Exception as error:
                print(f"FAIL [backup cleanup]: {error}", flush=True)
                passed = False
        try:
            compose("down", "--volumes", "--timeout", "30")
        except Exception as error:
            print(f"FAIL [cleanup]: {error}", flush=True)
            passed = False
    if passed:
        print("PASS. Backup:", backup, flush=True)
    return 0 if passed else 1


def interrupted(signum, frame):
    raise KeyboardInterrupt


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, interrupted)
    sys.exit(main())
