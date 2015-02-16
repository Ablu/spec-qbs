#!/usr/bin/bash

[ -d qbs ] || git clone https://gitorious.org/qt-labs/qbs.git

pushd qbs
    git fetch
    git reset --hard origin/master #v1.3.3
    VERSION=$(git describe | sed 's/^v//' | sed 's/-[^-]*$//' | sed 's/-/\./')
    git archive HEAD --prefix=qbs-$VERSION/ -o ../buildroot/SOURCES/qbs-$VERSION.src.tar.gz
popd

cat qbs.spec | sed "s/^Version:\(.*\)/Version: $VERSION/" > buildroot/SPECS/qbs_tmp.spec
rpmbuild --define "_topdir ${PWD}/buildroot/" -bb buildroot/SPECS/qbs_tmp.spec
