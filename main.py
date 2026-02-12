import os

import rich

from commands.cat import cat
from commands.cd import cd
from commands.echo import echo
from commands.ls import ls
from commands.mkdir import mkdir
from commands.touch import touch


def print_banner() -> None:
    banner = r"""[blue]
                         /$$      
                        | $$      
 /$$  /$$  /$$  /$$$$$$$| $$$$$$$ 
| $$ | $$ | $$ /$$_____/| $$__  $$
| $$ | $$ | $$|  $$$$$$ | $$  \ $$
| $$ | $$ | $$ \____  $$| $$  | $$
|  $$$$$/$$$$/ /$$$$$$$/| $$  | $$
 \_____/\___/ |_______/ |__/  |__/
 """
    rich.print(banner)


def prompt_command(cwd: str) -> list[str]:
    rich.print(f"[blue]wsh[/] [yellow]{cwd} [/][green]$ ", end="")
    user_input = input()
    words = user_input.split()
    return words


def main() -> None:
    print_banner()
    cwd = os.getcwd()

    while True:
        words = prompt_command(cwd)
        if len(words) == 0:
            continue

        command = words[0]
        args = words[1:]

        match command:
            case "exit":
                break
            case "help":
                print("TODO")
            case "echo":
                echo(args)
            case "pwd":
                print(cwd)
            case "ls":
                ls(cwd, args)
            case "cat":
                cat(cwd, args)
            case "cd":
                cwd = cd(cwd, args)
            case "touch":
                touch(cwd, args)
            case "mkdir":
                mkdir(cwd, args)
            case "rm":
                print("TODO")
            case "rmdir":
                print("TODO")
            case "grep":
                print("TODO")
            case _:
                print(f"{command}: not a recognized command")


if __name__ == "__main__":
    main()
