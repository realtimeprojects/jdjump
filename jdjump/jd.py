import re
import os
import sys
import logging as log
import argparse

_jd_dir = os.path.expanduser("~/.jdjump")

_sourcejd = f"source {os.path.dirname(__file__)}/jdfunc"

parser = argparse.ArgumentParser(description="jd - a simple directory jumper")
parser.add_argument('--debug', action="store_true", help="enable debug mode")
parser.add_argument('--add', '-a', action="store_true", help="add current directory to quick jump list")
parser.add_argument('--ls', '-l', action="store_true", help="show quick jump list")
parser.add_argument('--edit', '-e', action="store_true", help="edit jump list in your favourite editor")
parser.add_argument('target', nargs="?", default=None)


class Commands:
    def __init__(self, args):
        self.args = args

    def ls(self):
        targets = self._read_targets()
        if len(targets) == 0:
            log.info(f"jumplist is empty ({self._jumplist()})")
            log.info("add entries to jumplist by:")
            log.info("\tjd -a <path>")
            return 0
        log.info("\n".join(targets))

    def jump(self):
        log.debug(f'target is "{self.args.target}"')
        if not self.args.target:
            return self.ls()

        if self.args.target == "-":
            print("cd -")
            return

        targets = self._read_targets()
        tgtlist = self.args.target.split("/")
        for target in targets:
            if _target_matches(target, tgtlist):
                log.info(f"jumping to: {target}")
                print(f"cd {target}")
                return

    def add(self):
        pth = self.args.target if self.args.target else os.getcwd()
        log.info(f"adding '{pth}' to jumplist: '{self._jd_file()}'")
        fp = open(self._jumplist(), "a")
        if not fp:
            log.error(f"could not open {self._jumplist()} for writing")
            return 1
        fp.write(f"{pth}\n")
        fp.close()
        return 0

    def edit(self):
        if 'EDITOR' not in os.environ:
            log.error("set EDITOR in environment in order to edit your jumplist with `jd -e`")
            return 1
        os.system(f"{os.environ.get('EDITOR')} {self._jumplist()} </dev/tty >/dev/tty 2>&1")

    def invoke(self):
        command = "jump"
        if self.args.add:
            command = "add"
        if self.args.ls:
            command = "ls"
        if self.args.edit:
            command = "edit"
        func = getattr(self, command)
        return func()

    def _read_targets(self):
        log.debug(f"reading {self._jumplist()}")
        try:
            jdfile = open(os.path.expanduser(self._jumplist()), "r")
        except Exception as e:
            log.warn(e)
            return []
        targets = jdfile.readlines()
        return [target.strip() for target in targets]

    def _jumplist(self):
        return os.path.join(_jd_dir, "default.jumplist")


def main():
    myargs = parser.parse_args()
    _setup(myargs)
    commands = Commands(myargs)
    commands.invoke()


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


def _target_matches(target, matchlist):
    for tgt in matchlist:
        if not re.search(tgt, target):
            return False
    return True


if __name__ == "__main__":
    ec = main()
    sys.exit(ec)
