import sys
import getopt


def usage():
    return 'Usage : argstest.py –n <name> or argstest.py --name <name>'


def run(arguments):
    try:
        opts, args = getopt.getopt(arguments, "ho:v", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    output = None
    verbose = False
    for option, argument in opts:
        print(option)
        if option == "-v":
            verbose = True
        elif option in ("-h", "--help"):
            print(usage())
            sys.exit()
        elif option in ("-o", "--output"):
            output = argument
        else:
            assert False, "unhandled option"

    print(output)


if __name__ == "__main__" :
    run(sys.argv[1:])