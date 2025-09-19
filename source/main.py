### roblox-cli/source/roblox-cli.py
## Author: @nvttles
# Used to run Roblox actions from the console/command line.
## MIT License
### Have fun!


# - # Dependencies # - #

import sys
import typer
import robloxpy
import subprocess
from typing import Optional, Any

from rich import print
from rich.console import Console

app = typer.Typer()
console = Console()

# - # Methods # - #

def _get(section1: Optional[str], section2: Optional[str], part: Optional[str], cmd: Optional[str]) -> Optional[Any]:
    """
    Gets a method or property from robloxpy.

    :param section1: The first section to search in (e.g., 'User', 'Asset').
    :param section2: The second section to search in (e.g., 'Group').
    :param part: The method or property name to find.
    :param cmd: Optional command to find within the part.
    :return: The method or property if found, else None.
    """
    try:
        if section1 and section2 and part:
            section = getattr(getattr(robloxpy, section1), section2)
        elif section1 and part:
            section = getattr(robloxpy, section1)
        else:
            return None

        result = getattr(section, part)
        if cmd:
            if callable(result):
                return f"{result} - {result.__doc__}"
            else:
                return f"{result} - {type(result)}"
        return result
    except AttributeError:
        return None

# robloxpy.Group.External.GetOwner()

@app.command()
def install():
    """
    Installs robloxpy, rich, and typer packages.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "robloxpy", "rich", "typer"])
        console.print("[green]All dependencies installed successfully![/green]")
        subprocess.run("ls")
    except subprocess.CalledProcessError:
        console.print("[red]Failed to install dependencies.[/red]")

@app.command()
def find(section1: str, section2: Optional[str] = None, part: str = "", cmd: Optional[str] = None):
    """
    Finds a method or property in robloxpy.

    :param section1: First section (e.g., 'User').
    :param section2: Second section (optional, e.g., 'Group').
    :param part: The method or property name.
    :param cmd: Optional flag to include docstring/type info.
    """
    result = _get(section1, section2, part, cmd)
    if result:
        console.print(f"[green]{result}[/green]")
    else:
        console.print("[red]Not found.[/red]")
        sys.stderr.write("Error: Not found.\n")

# - # Code # - #

if __name__ == "__main__":
    app()