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
