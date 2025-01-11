#!/bin/bash
cp utils/PKGBUILD.* .
sed -i "s/99999999/${DATE}/" PKGBUILD.*
makepkg -p PKGBUILD.pinyin
makepkg -p PKGBUILD.rime
