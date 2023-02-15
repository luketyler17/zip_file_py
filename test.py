import sys

def main():
    try:
        print('hello world')  # print('string') - Always returns None
        print("Process finished with exit code 0")

        sys.exit(0)
    except Exception as ex:
        print("Error:" + ex)
        sys.exit(1)

if __name__ == '__main__':
    main()
