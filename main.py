import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import rich


def prompt_command(cwd: str) -> list[str]:
    # Need multiple prints to avoid "C:\" escaping color
    rich.print("[blue](wshell) ", end="")
    rich.print(f"[yellow]{cwd} ", end="")
    rich.print("[green]$ ", end="")
    user_input = input()
    words = user_input.split()
    return words


def echo(args: list[str]) -> None:
    print(" ".join(args))


def ls(cwd: str, args: list[str]) -> None:
    column_headers = ["Size", "Last modified", "Path"]
    path_metadata = defaultdict(dict)
    for path in Path(cwd).iterdir():
        path_str = str(path)
        if path.is_dir():
            path_str += "\\"

        stat = path.stat()
        path_metadata[path_str]["Size"] = str(stat.st_size) if path.is_file() else "0"
        path_metadata[path_str]["Last modified"] = datetime.fromtimestamp(
            stat.st_mtime
        ).strftime(r"%Y-%m-%d %H:%M:%S")

    column_widths = {header: len(header) for header in column_headers}
    for path, metadata in path_metadata.items():
        column_widths["Path"] = max(column_widths["Path"], len(path))
        for column_header, value in metadata.items():
            column_widths[column_header] = max(
                column_widths[column_header], len(metadata[column_header])
            )

    for index, header in enumerate(column_headers):
        print(
            header.ljust(column_widths[header]),
            end=" " if index != len(column_headers) - 1 else "\n",
        )
    for index, header in enumerate(column_headers):
        print(
            "-" * column_widths[header],
            end=" " if index != len(column_headers) - 1 else "\n",
        )

    for path, metadata in path_metadata.items():
        for column_header, value in metadata.items():
            print(value.ljust(column_widths[column_header]), end=" ")
        print(path.ljust(column_widths["Path"]))


def cd(cwd: str, args: list[str]) -> str:
    if len(args) == 0:
        return cwd

    if len(args) > 1:
        print("cd: too many arguments")
        return cwd

    path_parts = cwd.split("\\")
    arg_parts = args[0].replace("/", "\\").split("\\")
    if arg_parts[0] == "":
        path_parts = [path_parts[0]]
    arg_parts = list(filter(lambda part: part != "", arg_parts))

    for part in arg_parts:
        match part:
            case ".":
                pass
            case "..":
                if len(path_parts) > 1:
                    path_parts.pop()
            case _:
                path_parts.append(part)

    new_path = Path("\\".join(path_parts))
    if not new_path.is_dir():
        print(f"cd: {new_path} is not a recognized directory")
        return cwd

    new_cwd = str(new_path)
    # Needed to properly handle "C:"
    if "\\" not in new_cwd:
        new_cwd += "\\"
    return new_cwd


def cat(cwd: str, args: list[str]) -> None:
    for filename in args:
        try:
            with open(filename) as file:
                print(file.read())
        except OSError:
            print(f"cat: {filename} is not a recognized filename")


def main() -> None:
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
                print("TODO")
            case "mkdir":
                print("TODO")
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
