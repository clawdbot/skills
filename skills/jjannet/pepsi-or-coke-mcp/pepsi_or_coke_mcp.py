from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pepsi_or_coke_mcp")


@mcp.tool()
def choose_pepsi_or_coke() -> str:
    """
    Decide between Pepsi or Coke.
    """
    return "Coke"


if __name__ == "__main__":
    mcp.run()