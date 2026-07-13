import os
import random
import socket

from fastmcp import FastMCP


# Create a FastMCP server instance

mcp = FastMCP(name="Simple Calculator Server")


def find_available_port(start_port: int = 8000, max_attempts: int = 20) -> int:
    """Return the first available TCP port starting from start_port."""
    for offset in range(max_attempts):
        candidate_port = start_port + offset
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind(("0.0.0.0", candidate_port))
                return candidate_port
            except OSError:
                continue
    raise RuntimeError(f"Unable to find an available port between {start_port} and {start_port + max_attempts - 1}")


@mcp.tool()
def roll_dice(n_dice: int = 1) -> list[int]:

    """

    Roll n_dice 6-sided dice and return the results.

    """

    return [random.randint(1, 6) for _ in range(n_dice)]


@mcp.tool()
def add_numbers(a: float, b: float) -> float:

    """

    Add two numbers together.

    """

    return a + b


if __name__ == "__main__":

    # For remote MCP server, use HTTP transport.
    # Fall back to the next available port when 8000 is already in use.
    host = os.getenv("MCP_HOST", "0.0.0.0")
    requested_port = int(os.getenv("MCP_PORT", "8000"))
    port = find_available_port(start_port=requested_port)
    print(f"Starting FastMCP server on http://{host}:{port}/mcp")
    mcp.run(transport="http", host=host, port=port)