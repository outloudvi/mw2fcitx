#!/bin/bash
set -e

pushd /toolkit

pacman -Syu --noconfirm libime python-pip python-virtualenv
virtualenv venv
source venv/bin/activate
pip install mw2fcitx
mw2fcitx -c utils/moegirl_dict.py

useradd archbuild
chmod -R a+rwx .
export DATE=$(date +%Y%m%d)
su archbuild utils/makepkg.sh

cp fcitx5-pinyin-moegirl* /artifacts
cp ./moegirl.dict /artifacts
cp ./moegirl.dict.yaml /artifacts
cp ./titles.txt /artifacts

popd
