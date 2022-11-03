import os
import subprocess
import pytest
import tempfile
import logging


basedir = tempfile.mkdtemp(dir=".")


def _mkdir(path):
    pth = os.path.join(basedir, path)
    os.makedirs(pth, exist_ok=True)
    return os.path.abspath(pth)


@pytest.fixture
def setup():
    os.environ['JDPATH'] = os.path.join(basedir, ".jdjump")


def jd(args):
    result = subprocess.run(f"_jd {args}", check=False, stdout=subprocess.PIPE, shell=True)
    logging.warning(f"*** got {result}")
    return result


def test_add_jump(setup):
    p1 = _mkdir("jdpath1")
    p2 = _mkdir("jdpath2_two")
    p3 = _mkdir("jdpath2_two/jdpath3_three")
    os.chdir(p1)
    assert jd("-a").returncode == 0
    assert jd("th3").returncode != 0
    assert jd(f"-a {p3}").returncode == 0
    assert jd("path").stdout.decode() == f"cd {p1}\n"
    assert jd("th2").stdout.decode() == f"cd {p3}\n"
