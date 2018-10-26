#!/usr/bin/env

git clone ssh://git@gitlab.cern.ch:7999/raggleto/test-gitlab-ci.git
cd test-gitlab-ci
git checkout -b dummy master
echo "test" >> dummy.txt
echo "$1" >> dummy.txt
echo "$2" >> dummy.txt
git add dummy.txt
git commit -m "Test Push"
git push origin dummy
echo "Pushed to origin/dummy"
git checkout master
cd ..
