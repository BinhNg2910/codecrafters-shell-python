import sys
import os
import subprocess
from contextlib import ExitStack

def parse_commandlind(command):
    """Split a command line while preserving quoted and escaped characters."""
    args = list()
    current = ""
    isSingleQuote = False
    isDoubleQuote = False
    isBackSlash = False
    for char in command:
        if char == '\\' and not isBackSlash and not isSingleQuote:
            isBackSlash = not isBackSlash
        elif isBackSlash:
            current += char
            isBackSlash = not isBackSlash
        # A quote is special only when it is not inside the other quote type.
        elif char == "'" and not isDoubleQuote:
            isSingleQuote = not isSingleQuote
        elif char == '"' and not isSingleQuote:
            isDoubleQuote = not isDoubleQuote
        # Whitespace separates arguments only when it is outside quotes.
        elif char.isspace() and not isSingleQuote and not isDoubleQuote:
            if current:
                args.append(current)
                current = ""
        else:
            current += char

    if current:
        args.append(current)

    return args

def handle_echo(args, stdout=sys.stdout):
    """Write echo arguments to the selected output stream."""
    stdout.write(" ".join(args) + "\n")

def handle_exit(_):
    sys.exit()

def handle_type(args):
    command = "".join(args)

    if command_map.get(command):
        sys.stdout.write(f"{command} is a shell builtin\n")
        return
    
    path = os.environ.get("PATH")
    osDelimeter = os.pathsep
    if path:
        os_paths = path.split(osDelimeter)
        for path in os_paths:
            splitPaths = path.split("/")
            check = ""
            for splitPath in splitPaths:
                check += f"{splitPath}/"
                if os.access(check + command, os.X_OK):
                    sys.stdout.write(f"{command} is {check + command}\n")
                    return
    sys.stdout.write(f"{command}: not found\n")

command_map = {
    "echo": handle_echo,
    "exit": handle_exit,
    "type": handle_type
}

def find_executable_file(command):
    """Return whether an executable command can be found in PATH."""
    path = os.environ.get("PATH")
    for dir in path.split(os.pathsep):
        executable_path = os.path.join(dir, command)
        if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
            return True
    return False

def handle_execution(command, args, stdout=None, stderr=None):
    """Run an external command with optional output and error redirection."""
    if find_executable_file(command):
        subprocess.run([command] + args, stdout=stdout, stderr=stderr)
        return True
    return False

def redirection_detect_and_extract(args):
    """Separate command arguments from stdout and stderr redirect targets."""
    commandArg, outputFile, outputErrFile = args, None, None
    idx = 0
    while idx < len(args):
        arg = args[idx]
        if arg in [">", "1>"]:
            outputFile = args[idx+1]
            idx += 2
        elif arg in ["2>"]:
            outputErrFile = args[idx+1]
            idx += 2
        else:
            commandArg.append(arg)
    return [commandArg, outputFile, outputErrFile]
    
def handle_command(command, args):
    """Dispatch a builtin or external command using any requested redirects."""
    args, stdout_file, stderr_file = redirection_detect_and_extract(args)
    # ExitStack closes whichever redirect files were opened when this block ends.
    with ExitStack() as stack:
        stdout = (
            stack.enter_context(open(stdout_file, "w"))
            if stdout_file
            else None
        )
        stderr = (
            stack.enter_context(open(stderr_file, "w"))
            if stderr_file
            else None
        )
        if command_map.get(command):
            output = stdout if stdout is not None else sys.stdout
            command_map[command](args, stdout=output)
            return
        if handle_execution(command, args, stdout=stdout, stderr=stderr):
            return
        
    sys.stdout.write(f"{" ".join([command] + args)}: command not found\n")
