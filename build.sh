#!/usr/bin/bash

[ -d qbs ] || git clone git://code.qt.io/qt-labs/qbs.git
[ -d buildroot ] || mkdir -p buildroot/{SOURCES,SPECS}

BRANCH=$(git rev-parse --abbrev-ref HEAD)
pushd qbs
    git fetch
    git reset --hard origin/$BRANCH
    VERSION=$(git describe | sed 's/^v//' | sed 's/-[^-]*$//' | sed 's/-/\./')
    git archive HEAD --prefix=qbs-$VERSION/ -o ../buildroot/SOURCES/qbs-$VERSION.src.tar.gz
popd

cat qbs.spec | sed "s/^Version:\(.*\)/Version: $VERSION/" > buildroot/SPECS/qbs_tmp.spec
rpmbuild --define "_topdir ${PWD}/buildroot/" -bb buildroot/SPECS/qbs_tmp.spec
