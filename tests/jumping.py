import os
import subprocess
import pytest
import tempfile
import logging

basedir = None


def _mkdir(path):
    pth = os.path.join(basedir, path)
    os.makedirs(pth, exist_ok=True)
    return os.path.abspath(pth)


@pytest.fixture
def setup():
    global basedir
    basedir = tempfile.mkdtemp(dir=".")
    os.environ['JDPATH'] = os.path.join(basedir, ".jdjump")


def jd(args):
    result = subprocess.run(f"_jd {args}", check=False, stdout=subprocess.PIPE, shell=True)
    logging.warning(f"*** got {result}")
    return result


def test_jump_back(setup):
    assert jd("-").stdout.decode() == "cd -\n"


def test_list(setup):
    p1 = _mkdir("jdpath1")
    p2 = _mkdir("jdpath2_two")
    p3 = _mkdir("jdpath2_two/jdpath3_three")
    assert jd(f"-a {p1}").returncode == 0
    assert jd(f"-a {p2}").returncode == 0
    assert jd(f"-a {p3}").returncode == 0
    lst1 = jd("").stdout.decode()
    lst2 = jd("-l").stdout.decode()

    assert lst1 == lst2
    assert p1 in lst1
    assert p2 in lst1
    assert p3 in lst1


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
    assert jd(f"-a {p2}").returncode == 0
    assert jd("th2").stdout.decode() == f"cd {p3}\n"
