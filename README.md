# FastAPI Logging (beans-logging-fastapi)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bybatkhuu/module-fastapi-logging/2.build-publish.yml?logo=GitHub)](https://github.com/bybatkhuu/module-fastapi-logging/actions/workflows/2.build-publish.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/bybatkhuu/module-fastapi-logging?logo=GitHub&color=blue)](https://github.com/bybatkhuu/module-fastapi-logging/releases)
[![PyPI](https://img.shields.io/pypi/v/beans-logging?logo=PyPi)](https://pypi.org/project/beans-logging-fastapi)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/beans-logging-fastapi?logo=Python)](https://docs.conda.io/en/latest/miniconda.html)

This is a HTTP access log module for **FastAPI** based on **'beans-logging'** package.

## ✨ Features

- **Logger** based on **'beans-logging'** package
- **FastAPI** HTTP access logging **middleware**
- HTTP access log as structured JSON format
- Predefined **configuration** for HTTP access logs
- Easy to **install** and **use**

---

## 🛠 Installation

### 1. 🚧 Prerequisites

- Install **Python (>= v3.10)** and **pip (>= 23)**:
    - **[RECOMMENDED] [Miniconda (v3)](https://www.anaconda.com/docs/getting-started/miniconda/install)**
    - *[arm64/aarch64] [Miniforge (v3)](https://github.com/conda-forge/miniforge)*
    - *[Python virutal environment] [venv](https://docs.python.org/3/library/venv.html)*

[OPTIONAL] For **DEVELOPMENT** environment:

- Install [**git**](https://git-scm.com/downloads)
- Setup an [**SSH key**](https://docs.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh)

### 2. 📦 Install the package

[NOTE] Choose one of the following methods to install the package **[A ~ F]**:

**OPTION A.** [**RECOMMENDED**] Install from **PyPi**:

```sh
pip install -U beans-logging-fastapi
```

**OPTION B.** Install latest version directly from **GitHub** repository:

```sh
pip install git+https://github.com/bybatkhuu/module-fastapi-logging.git
```

**OPTION C.** Install from the downloaded **source code**:

```sh
git clone https://github.com/bybatkhuu/module-fastapi-logging.git && \
    cd ./module-fastapi-logging

# Install directly from the source code:
pip install .

# Or install with editable mode:
pip install -e .
```

**OPTION D.** Install for **DEVELOPMENT** environment:

```sh
pip install -e .[dev]

# Install pre-commit hooks:
pre-commit install
```

**OPTION E.** Install from **pre-built release** files:

1. Download **`.whl`** or **`.tar.gz`** file from [**releases**](https://github.com/bybatkhuu/module-fastapi-logging/releases)
2. Install with pip:

```sh
# Install from .whl file:
pip install ./beans_logging_fastapi-[VERSION]-py3-none-any.whl

# Or install from .tar.gz file:
pip install ./beans_logging_fastapi-[VERSION].tar.gz
```

**OPTION F.** Copy the **module** into the project directory (for **testing**):

```sh
# Install python dependencies:
pip install -r ./requirements.txt

# Copy the module source code into the project:
cp -r ./src/beans_logging_fastapi [PROJECT_DIR]
# For example:
cp -r ./src/beans_logging_fastapi /some/path/project/
```

## 🚸 Usage/Examples

To use `beans_logging_fastapi`:

### **FastAPI**

[**`configs/logger.yml`**](./examples/configs/logger.yml):

```yaml
logger:
  app_name: "fastapi-app"
  level:
    base: TRACE
  http:
    std:
      format_str: '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}" {status_code} {content_length}B {response_time}ms'
      err_format_str: '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}" <n>{status_code}</n>'
      debug_format_str: '<n>[{request_id}]</n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"'
    file:
      format_str: '{client_host} {request_id} {user_id} [{datetime}] "{method} {url_path} HTTP/{http_version}" {status_code} {content_length} "{h_referer}" "{h_user_agent}" {response_time}'
      tz: "localtime"
    headers:
      has_proxy: false
      has_cf: false
  intercept:
    mute_modules: ["uvicorn.access"]
  handlers:
    http.access.file_handler:
      enabled: true
      sink: "http/{app_name}.http-access.log"
    http.err.file_handler:
      enabled: true
      sink: "http/{app_name}.http-err.log"
    http.access.json_handler:
      enabled: true
      sink: "http.json/{app_name}.http-access.json.log"
    http.err.json_handler:
      enabled: true
      sink: "http.json/{app_name}.http-err.json.log"
```

[**`.env`**](./examples/.env):

```sh
ENV=development
DEBUG=true
```

[**`config.py`**](./examples/config.py):

```python
import os

from pydantic_settings import BaseSettings

from potato_util import io as io_utils
from beans_logging_fastapi import LoggerConfigPM


_config_data = {}
_configs_dir = os.path.join(os.getcwd(), "configs")
if os.path.isdir(_configs_dir):
    _config_data = io_utils.read_all_configs(configs_dir=_configs_dir)


class MainConfig(BaseSettings):
    logger: LoggerConfigPM = LoggerConfigPM()


config = MainConfig(**_config_data)


__all__ = [
    "MainConfig",
    "config",
]
```

[**`logger.py`**](./examples/logger.py):

```python
from beans_logging_fastapi import logger

__all__ = [
    "logger",
]
```

[**`router.py`**](./examples/router.py):

```python
from pydantic import validate_call
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("/")
def root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@router.get("/continue", status_code=100)
def get_continue():
    return {}


@router.get("/redirect")
def redirect():
    return RedirectResponse("/")


@router.get("/error")
def error():
    raise HTTPException(status_code=500)


@validate_call(config={"arbitrary_types_allowed": True})
def add_routers(app: FastAPI) -> None:
    """Add routers to FastAPI app.

    Args:
        app (FastAPI): FastAPI app instance.
    """

    app.include_router(router)

    return


__all__ = ["add_routers"]
```

[**`bootstrap.py`**](./examples/bootstrap.py):

```python
# Standard libraries
from typing import Any
from collections.abc import Callable

# Third-party libraries
import uvicorn
from uvicorn._types import ASGIApplication
from pydantic import validate_call
from fastapi import FastAPI

from beans_logging_fastapi import add_logger

# Internal modules
from __version__ import __version__
from config import config
from lifespan import lifespan
from router import add_routers


def create_app() -> FastAPI:
    """Create FastAPI application instance.

    Returns:
        FastAPI: FastAPI application instance.
    """

    app = FastAPI(lifespan=lifespan, version=__version__)

    # Add logger before any other components:
    add_logger(app=app, config=config.logger)

    # Add any other components after logger:
    add_routers(app=app)

    return app


@validate_call(config={"arbitrary_types_allowed": True})
def run_server(
    app: FastAPI | ASGIApplication | Callable[..., Any] | str = "main:app",
) -> None:
    """Run uvicorn server.

    Args:
        app (Union[ASGIApplication, str], optional): ASGI application instance or module path.
    """

    uvicorn.run(
        app=app,
        host="0.0.0.0",  # nosec B104
        port=8000,
        access_log=False,  # Disable default uvicorn access log
        server_header=False,
        proxy_headers=False,
        forwarded_allow_ips="*",
    )

    return


__all__ = [
    "create_app",
    "run_server",
]
```

[**`main.py`**](./examples/main.py):

```python
#!/usr/bin/env python

# Third-party libraries
from dotenv import load_dotenv

load_dotenv(override=True)

# Internal modules
from bootstrap import create_app, run_server  # noqa: E402
from logger import logger  # noqa: E402


app = create_app()


def main() -> None:
    """Main function."""

    run_server(app=app)
    return


if __name__ == "__main__":
    logger.info("Starting server from 'main.py'...")
    main()


__all__ = ["app"]
```

Run the [**`examples`**](./examples):

```sh
cd ./examples
# Install python dependencies for examples:
pip install -r ./requirements.txt

uvicorn main:app --host=0.0.0.0 --port=8000
```

**Output**:

```txt
[2026-01-01 12:00:00.002 +09:00 | TRACE | beans_logging.intercepters:96]: Intercepted modules: ['uvicorn', 'potato_util', 'fastapi', 'uvicorn.error', 'watchfiles.watcher', 'concurrent.futures', 'watchfiles', 'asyncio', 'concurrent', 'potato_util._base', 'dotenv', 'dotenv.main', 'watchfiles.main', 'potato_util.io', 'potato_util.io._sync']; Muted modules: ['uvicorn.access'];
[2026-01-01 12:00:00.003 +09:00 | INFO  | uvicorn.server:84]: Started server process [88375]
[2026-01-01 12:00:00.003 +09:00 | INFO  | uvicorn.lifespan.on:48]: Waiting for application startup.
[2026-01-01 12:00:00.004 +09:00 | TRACE | lifespan:19]: TRACE diagnosis is ON!
[2026-01-01 12:00:00.004 +09:00 | DEBUG | lifespan:20]: DEBUG mode is ON!
[2026-01-01 12:00:00.004 +09:00 | INFO  | lifespan:21]: Preparing to startup...
[2026-01-01 12:00:00.004 +09:00 | OK    | lifespan:24]: Finished preparation to startup.
[2026-01-01 12:00:00.004 +09:00 | INFO  | lifespan:25]: Version: 0.0.0
[2026-01-01 12:00:00.005 +09:00 | INFO  | uvicorn.lifespan.on:62]: Application startup complete.
[2026-01-01 12:00:00.006 +09:00 | INFO  | uvicorn.server:216]: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
[2026-01-01 12:00:01.775 +09:00 | DEBUG ]: [80138308bc00406387fb804cf6cc0e11] 127.0.0.1 - "GET / HTTP/1.1"
[2026-01-01 12:00:01.783 +09:00 | OK    ]: [80138308bc00406387fb804cf6cc0e11] 127.0.0.1 - "GET / HTTP/1.1" 200 17B 5.7ms
^C[2026-01-01 12:00:02.368 +09:00 | INFO  | uvicorn.server:264]: Shutting down
[2026-01-01 12:00:02.470 +09:00 | INFO  | uvicorn.lifespan.on:67]: Waiting for application shutdown.
[2026-01-01 12:00:02.472 +09:00 | INFO  | lifespan:29]: Preparing to shutdown...
[2026-01-01 12:00:02.472 +09:00 | OK    | lifespan:31]: Finished preparation to shutdown.
[2026-01-01 12:00:02.473 +09:00 | INFO  | uvicorn.lifespan.on:76]: Application shutdown complete.
[2026-01-01 12:00:02.474 +09:00 | INFO  | uvicorn.server:94]: Finished server process [88375]
```

👍

---

## ⚙️ Configuration

[**`templates/configs/config.yml`**](./templates/configs/config.yml):

```yaml
logger:
  # app_name: fastapi-app
  level:
    base: INFO
    err: WARNING
  format_str: "[{time:YYYY-MM-DD HH:mm:ss.SSS Z} | {extra[level_short]:<5} | {name}:{line}]: {message}"
  file:
    logs_dir: "./logs"
    rotate_size: 10000000
    rotate_time: "00:00:00"
    retention: 90
    encoding: utf8
  use_custom_serialize: false
  http:
    std:
      msg_format_str: '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}" {status_code} {content_length}B {response_time}ms'
      err_msg_format_str: '<n><w>[{request_id}]</w></n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}" <n>{status_code}</n>'
      debug_msg_format_str: '<n>[{request_id}]</n> {client_host} {user_id} "<u>{method} {url_path}</u> HTTP/{http_version}"'
    file:
      format_str: '{client_host} {request_id} {user_id} [{datetime}] "{method} {url_path} HTTP/{http_version}" {status_code} {content_length} "{h_referer}" "{h_user_agent}" {response_time}'
      tz: localtime
    headers:
      has_proxy: false
      has_cf: false
  intercept:
    enabled: true
    only_base: false
    ignore_modules: []
    include_modules: []
    mute_modules: [uvicorn.access]
  handlers:
    all_std_handler:
      enabled: true
      h_type: STD
      format: "[<c>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</c> | <level>{extra[level_short]:<5}</level> | <w>{name}:{line}</w>]: <level>{message}</level>"
      colorize: true
    all_file_handler:
      enabled: true
      h_type: FILE
      sink: "{app_name}.all.log"
    err_file_handler:
      enabled: true
      h_type: FILE
      sink: "{app_name}.err.log"
      error: true
    all_json_handler:
      enabled: true
      h_type: FILE
      sink: "json/{app_name}.all.json.log"
      serialize: true
    err_json_handler:
      enabled: true
      h_type: FILE
      sink: "json/{app_name}.err.json.log"
      serialize: true
      error: true
    http_access_std_handler:
      enabled: true
      h_type: STD
      format: "[<c>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</c> | <level>{extra[level_short]:<5}</level> ]: <level>{message}</level>"
      colorize: true
    http_access_file_handler:
      enabled: true
      h_type: FILE
      sink: "http/{app_name}.http-access.log"
    http_err_file_handler:
      enabled: true
      h_type: FILE
      sink: "http/{app_name}.http-err.log"
      error: true
    http_access_json_handler:
      enabled: true
      h_type: FILE
      sink: "http.json/{app_name}.http-access.json.log"
    http_err_json_handler:
      enabled: true
      h_type: FILE
      sink: "http.json/{app_name}.http-err.json.log"
      error: true
  extra:
```

### 🌎 Environment Variables

[**`.env.example`**](./.env.example):

```sh
# ENV=LOCAL
# DEBUG=false
# TZ=UTC
```

---

## 🧪 Running Tests

To run tests, run the following command:

```sh
# Install python test dependencies:
pip install .[test]

# Run tests:
python -m pytest -sv -o log_cli=true
# Or use the test script:
./scripts/test.sh -l -v -c
```

## 🏗️ Build Package

To build the python package, run the following command:

```sh
# Install python build dependencies:
pip install -r ./requirements/requirements.build.txt

# Build python package:
python -m build
# Or use the build script:
./scripts/build.sh
```

## 📝 Generate Docs

To build the documentation, run the following command:

```sh
# Install python documentation dependencies:
pip install -r ./requirements/requirements.docs.txt

# Serve documentation locally (for development):
mkdocs serve -a 0.0.0.0:8000 --livereload
# Or use the docs script:
./scripts/docs.sh

# Or build documentation:
mkdocs build
# Or use the docs script:
./scripts/docs.sh -b
```

## 📚 Documentation

- [Docs](./docs)

---

## 📑 References

- <https://packaging.python.org/en/latest/tutorials/packaging-projects>
- <https://python-packaging.readthedocs.io/en/latest>
