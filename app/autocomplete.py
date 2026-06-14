import os
import readline


BUILT_INS = ["echo", "exit"]

def find_command_matches(text):
    # search for builtins and path
    pass
    matches = []
    seen = set()

    for command in BUILT_INS:
        if command.startswith(text) and command not in seen:
            matches.append(command + " ")
            seen.add(command)

    for directory in os.environ.get("PATH", "").split(os.pathsep):
        try:
            entries = os.listdir(directory)
        except OSError:
            continue

        for entry in entries:
            full_path = os.path.join(directory, entry)
            if (
                entry.startswith(text)
                and entry not in seen
                and os.path.isfile(full_path)
                and os.access(full_path, os.X_OK)
            ):
                matches.append(entry + " ")
                seen.add(entry)
    return matches

def find_filename_matches(text):
    # search files exist in current directory
    entries = os.listdir(".")
    matches = []
    for entry in entries:
        if entry.startswith(text):
            matches.append(text + " ")
    return matches

def completer(text, state):
    is_argument = readline.get_begidx() > 0
    matches = find_filename_matches(text) if is_argument else find_command_matches(text)
    return matches[state] if state < len(matches) else None


def configure_autocomplete():
    """Register completion using the local readline backend."""
    readline.set_completer(completer)

    if "libedit" in (readline.__doc__ or ""):
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
