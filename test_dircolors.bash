#!/bin/bash
# modified from https://gist.github.com/MicahElliott/719653

# test-dircolors — Fine-tune your dircolors for unique colorings of any file type
#
# Author: Micah Elliott http://MicahElliott.com
#
# Tools like ls, tree, zsh color completion, etc make use of dircolors
# settings. This script will show you bunches of files, colored by
# their various extensions (or non-extension files like Makefile).
# Useful for tuning your console color scheme and grouping files by
# type. ls's -X option is a nice way to group your file listings by
# extension.
#
# The philosophy behind this is that certain types of files are
# similar, and it's nice to be able to see them as such. For example,
# you may want to color scripts in purple,
# Makefiles/Rakefiles/Gemfiles in yellow, logs in red, archives in
# blue, images in brown, configs in green, generated stuff in dark
# gray, and so on. Choose the categories that suit you (you've only
# got a handful of colors to work with) and run this repeatedly until
# you're happy.
#
# See https://gist.github.com/718567 for an example xterm color
# scheme.

base_files="
tags
core
bug
fix
log
report
Makefile
makefile
README
README.md
README.markdown
INSTALL
LICENSE
.DS_Store
"

ext_files="
.tar
.tar.gzog
.tgz
.lzh
.zip
.bz2
.gz
.deb
.rpm
.jar
.jpg
.jpeg
.png
.gif
.bmp
.ppm
.tga
.xbm
.xpm
.tif
.png
.mpg
.avi
.fli
.gl
.dl
.zip
.z
.bz2
.deb
.rpm
.jar
.jpg
.png
.gif
.bmp
.ppm
.tif
.png
.avi
.gl
.dl
.cpp
.cxx
.C
.cc
.c
.esqlc
.pgc
.pgcc
.ii
.err
.h
.H
.hh
.inc
.hpp
.l
.ll
.y
.yy
.f
.F
.for
.F90
.FPP
.java
.py
.hs
.pl
.pm
.rb
.sql
.sh
.rc
.bash
.sh
.ksh
.tcsh
.csh
.s
.t
.o
.class
.pyc
.pyo
.mod
.res
.mk
.gmk
.html
.xml
.txt
.text
.log
.md
.mkd
.rst
.moin
.conf
.ini
.cfg
.mp3
.mp4
.mov
.mkv
.ogv
.ogg
.eo
.tmp
.swp
"
# TODO vim backup, *~

tmpdir=${TMPDIR:=.}/test-dircolors

echo "Now creating a bunch of temp files for you to look at."
mkdir -p $tmpdir
cd $tmpdir

# Extension files
for e in $ext_files; do
    #touch "The quick brown fox jumps over the lazy dog"$e
    touch "some_file"$e
done

# Files with no extension/suffix
for b in $base_files; do
    touch $b
done

# An executable
touch executable_demo test.dll test.exe test.so
chmod +x executable_demo test.dll test.exe test.so



# setuid
touch executable_demo_setuid_a executable_demo_setuid_u executable_demo_setuid_g
chmod +x executable_demo_setuid_a
chmod a+s executable_demo_setuid_a
chmod +x executable_demo_setuid_u
chmod u+s executable_demo_setuid_u
chmod +x executable_demo_setuid_g
chmod g+s executable_demo_setuid_g


# TODO more special file types/permissions
# from https://github.com/dracula/putty/issues/3
rmdir dracula_putty_issue_3
mkdir dracula_putty_issue_3
ls -altrhd dracula_putty_issue_3
chmod a+rwx dracula_putty_issue_3
ls -altrhd dracula_putty_issue_3

# Directories
mkdir directory-standard dir-sticky "directory_o+w" "directory_+t_o+w" "directory_g+w"
chmod +s dir-sticky
chmod g+w "directory_g+w"
chmod o+w "directory_o+w" "directory_+t_o+w"
chmod +t "directory_+t_o+w"

touch file-normal

ln -s file-normal link_to_normal
ln -s /dev/null link_to_device

ln -s file_does_not_exist link_to_missing_file
ln -s /dev/doesnotexist link_to_missing_device


# TODO more special file types/permissions

eval $(dircolors -b $DIR_COLORS)

#ls --color=always -lBX $tmpdir
#rm -rf $tmpdir
echo
echo "This test is mostly manual, but does create test files for you."
echo "Here's the test cycle:"
echo
echo ' 1. Edit your $DIR_COLORS file, or ~/.dircolors.'
echo ' 2. Run this to update visible colors: eval $(dircolors -b $DIR_COLORS)'
echo " 3. Do a colored ls on $tmpdir ; ls --color=always $tmpdir"
echo " 4. Rinse and repeat until you're happy with scheme."
echo
echo "Do this when you're done: rm -rf $tmpdir"

