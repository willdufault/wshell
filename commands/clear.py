def clear() -> None:
    # ANSI code to reset to initial state, see https://en.wikipedia.org/wiki/ISO/IEC_2022#Other_control_functions
    # Could have used `subproccess.run('clear')` instead, but that felt like cheating
    print("\033c", end="")
