from argparse import ArgumentParser

from attack import Attack


def main():
    # Parse command line arguments.
    parser = ArgumentParser(prog='Password Hacker')
    parser.add_argument('host')
    parser.add_argument('port')
    args = parser.parse_args()

    # Attack server.
    Attack.attack(args.host, int(args.port))


if __name__ == '__main__':
    main()
