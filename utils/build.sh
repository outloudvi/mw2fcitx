#!/bin/bash
set -e

pushd /toolkit

pacman -Syu --noconfirm libime python-pip python-virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
mw2fcitx -c utils/moegirl_dict.py

useradd archbuild
chmod -R a+rwx .
export DATE=${1:-$(date +%Y%m%d)} # makepkg.sh also uses the variable
sed -i "s/0.0.1/$DATE/" utils/moegirl_dict.py
su archbuild utils/makepkg.sh

cp fcitx5-pinyin-moegirl* /artifacts
cp ./moegirl.dict /artifacts
cp ./moegirl.dict.yaml /artifacts
cp ./titles.txt /artifacts

popd
