from mullemeck import app


def main(args):
    debug = 'debug' in args
    app.run(debug=debug)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
