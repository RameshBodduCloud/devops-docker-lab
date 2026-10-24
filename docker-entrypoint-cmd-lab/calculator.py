import sys

def calculate():
    print("Docker Calculator Started!")

    if len(sys.argv) != 3:
        print("Usage: calculator <num1> <num2>")
        sys.exit(1)

    num1 = int(sys.argv[1])
    num2 = int(sys.argv[2])

    result = num1 + num2

    print(f"Result: {result}")

if __name__ == "__main__":
    calculate()
