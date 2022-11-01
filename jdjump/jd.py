import re
import os
import sys
import logging as log
import argparse
from pathlib import Path

_jd_dir = os.path.expanduser("~/.jdjump")
_jd_file = os.path.join(_jd_dir, "jumplist")

_sourcejd = f"source {os.path.dirname(__file__)}/jdfunc"

parser = argparse.ArgumentParser(description="jd - a simple directory jumper")
parser.add_argument('--debug', action="store_true", help="enable debug mode")
parser.add_argument('--add', '-a', action="store_true", help="add current directory to quick jump list")
parser.add_argument('--ls', '-l', action="store_true", help="show quick jump list")
parser.add_argument('target', nargs="?", default=None)


class Commands:
    @staticmethod
    def ls(myargs):
        targets = _read_targets()
        if len(targets) == 0:
            log.info(f"jumplist is empty ({_jd_file})")
            return 0
        log.info("\n".join(targets))

    @staticmethod
    def jump(myargs):
        log.debug(f'target is "{myargs.target}"')
        if not myargs.target:
            return Commands.ls(myargs)

        if myargs.target == "-":
            print("cd -")
            return

        targets = _read_targets()
        for target in targets:
            if re.search(myargs.target, target):
                log.info(f"jumping to: {target}")
                print(f"cd {target}")
                return

    @staticmethod
    def add(myargs):
        pth = myargs.target if myargs.target else os.getcwd()
        log.info(f"adding '{pth}' to jumplist: '{_jd_file}'")
        fp = open(_jd_file, "a")
        fp.write(f"{pth}\n")
        fp.close()


def main():
    myargs = parser.parse_args()
    _setup(myargs)
    command = "jump"
    if myargs.add:
        command = "add"
    if myargs.ls:
        command = "ls"
    func = getattr(Commands, command)
    func(myargs)


def _read_targets():
    log.debug(f"reading {_jd_file}")
    targets = open(os.path.expanduser(_jd_file), "r").readlines()
    return [target.strip() for target in targets]


def _setup(myargs):
    logfmt = "jd: %(message)s"
    log.basicConfig(format=logfmt)
    if myargs.debug:
        log.getLogger().setLevel(log.DEBUG)
    else:
        log.getLogger().setLevel(log.INFO)
    log.debug(myargs)
    _check_jdfunc()
    _check_jddir()


def _check_jddir():
    if not os.path.exists(_jd_dir):
        log.info(f"creating {_jd_dir} directory")
        os.mkdir(_jd_dir)
    if not os.path.exists(_jd_file):
        Path(_jd_file).touch()


def _check_jdfunc():
    if '_jd' not in sys.argv[0]:
        log.warning("jd function not installed")
        log.warning(f"add the following line to your favourite shell script:\n\n\t{_sourcejd}\n")
        rcfiles = _find_rc()
        for file in rcfiles:
            if _ask(f"Should I add the line to {file}"):
                _add_source(file)
                os.system(_sourcejd)
                sys.exit(0)
        log.warning("jd function not installed")
        exit(1)


def _add_source(file):
    print(f'echo "{_sourcejd}" >>{file}')
    os.system(f'echo "{_sourcejd}" >>~/{file}')


def _find_rc():
    candidates = [".zshrc", ".bashrc", ".bash_profile", ".profile"]
    existing = []
    for candidate in candidates:
        if os.path.exists(os.path.expanduser(f"~/{candidate}")):
            existing.append(candidate)
    return existing


def _ask(question):
    response = input(f"{question}? (y/N): ")
    if response.lower() == "y":
        return True
    if response.lower() == "n":
        return False
    if response == "":
        return False
    log.error(f"Unknown response: {response}")
    exit(1)


if __name__ == "__main__":
    main()
