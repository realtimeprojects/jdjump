# jdjump

a smart directory jumper

## Description

Quickly jump between your bookmarked directories using the jd command.

## Quickstart

*   install jdjump:

        pip3 install git+https://github.com/realtimeprojects/jdjump.git

*   setup jdjump by running it once, make source the jd function is installed
    in your init script:

        jd

*   go to directory you want to bookmark add add it to the jumplist:

        cd ~/Downloads
        jd -a

*   now you can jump from anywhere to this directory:

        jd Down

`jd` will jump to the first directory in the jumplist which matches the
given pattern in the command line.

## Documentation

### Jump to directory

`gh <target>` will jump to the first directory in the jump list matching
the `<target>` pattern.

### Adding files to your jumplist

`gh -a <directory>` will add the given directory to your jump list. If target is ommitted,
the current working directory is added to your match list.

### Show jump list

Running `gh` without a target will print out the jump list.
Alternatively you can use `gh -l` to show the jump list.

### Multi-matching

Given you have multiple similar entries in your jump-list like:

        ~/greenhouse/greenhouse-test
        ~/greenhouse/greenhouse-lib
        ~/acre/acre-test
        ~/acre/acre-lib

If you jump using

    jd test

jd will jump to the first entry in your jumplist that matches the pattern. However,
you can separate multiple matches using the `/` sign:

    jd ac/te

will jump to the first entry matching all parts in your search pattern. In this case
jd will jump to `~/acre/acre-test`.

