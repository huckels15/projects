#!/bin/bash
cd /gfs
echo foo contents > foo.txt
cat foo.txt
echo bar contents > bar.txt
cat bar.txt
cat foo.txt bar.txt > baz.txt
cat baz.txt
ls -la foo.txt
touch foo.txt
ls -la foo.txt
ls -la bar.txt
chmod 666 bar.txt
ls -la bar.txt
ln -s foo.txt foosymlink
mkdir folder
ls -la
cat foosymlink
rm foo.txt
ls -la
cat foosymlink
rmdir folder









