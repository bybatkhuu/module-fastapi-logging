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
