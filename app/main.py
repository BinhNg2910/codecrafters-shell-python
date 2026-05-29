import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        print(f"{command}: command not found")
    # sys.stdout.write("$ ")
    # command = input()
    # print(f'{command}: command not found')



if __name__ == "__main__":
    main()
