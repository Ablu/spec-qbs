Name:       qbs
Version:    1.4.0
Release:    1%{?dist}
Summary:    Next-generation build system for projects
# Same license exceptions as all Qt based packages.
# See: https://lists.fedoraproject.org/pipermail/legal/2013-July/002196.html
# Newer code is LGPLv3, some old code is still LGPLv2
License:    LGPLv2 with exceptions and LGPLv3 with exceptions
URL:        http://qt-project.org/wiki/qbs
Source0:    http://download.qt-project.org/official_releases/%{name}/%{version}/%{name}-%{version}.src.tar.gz

BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Script)

# Required for running the tests
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  mingw32-nsis

%description
The Qt Build Suite (Qbs) is a tool that helps simplify the build process for
developing projects across multiple platforms. Qbs can be used for any software
project, whether it is written in Qt or not.

Qbs is an all-in-one tool that generates a build graph from a high-level
project description (like qmake or cmake) and additionally undertakes the task
of executing the commands in the low-level build graph (like make).

%package devel
Summary:    Development files for qbs
License:    LGPLv2 with exceptions
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package is required to build native/C++ extensions for qbs

%package gui
Summary:    UI support for configuring qbs
License:    LGPLv2 with exceptions
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description gui
Provides a UI based help program for configuring qbs

%package qt
Summary:    Qt support for qbs
License:    LGPLv2 with exceptions
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   %{name}-cpp%{?_isa} = %{version}-%{release}

%description qt
Provides Qt support for the Qt Build Suite (qbs)

%package qt-devel
Summary:    Development files for the qbs Qt module
License:    LGPLv2 with exceptions
Requires:   %{name}-qt%{?_isa} = %{version}-%{release}

%description qt-devel
This package is required by packages which are using the
helper libraries for setting up the Qt module.

%package cpp
Summary:    C++ support for qbs
License:    LGPLv2 with exceptions
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description cpp
Provides C++ support for the Qt Build Suite (qbs)

%package nsis
Summary:   NSIS module for qbs
License:   LGPLv2 with exceptions
BuildArch: noarch
Requires:  %{name} = %{version}-%{release}
Requires:  mingw32-nsis

%description nsis
Provides the NSIS module for qbs for building Windows installers

%package nodejs
Summary:   Node.js module for qbs
License:   LGPLv2 with exceptions
BuildArch: noarch
Requires:  %{name} = %{version}-%{release}
Requires:  nodejs

%description nodejs
Provides the Node.js module for qbs for running Node.js applications

%package typescript
Summary:   TypeScript module for qbs
License:   LGPLv2 with exceptions
BuildArch: noarch
Requires:  %{name} = %{version}-%{release}
Requires:  %{name}-nodejs = %{version}-%{release}

%description typescript
The typescript module contains properties and rules for building
TypeScript applications and may be used in combination with the Node.js
module to run TypeScript applications directly from Qbs.

%package android
Summary:   Android module for qbs
License:   LGPLv2 with exceptions

%description android
Provides utilities for building android applications.

%package java
Summary:   Java module for qbs
License:   LGPLv2 with exceptions

%description java
Provides support for compiling Java applications.

%package archiver
Summary:   Archive module for qbs
License:   LGPLv2 with exceptions

%description archiver
Provides support for building archives as part of a build.

%package examples
Summary:    Examples for the usage of qbs
# See headers of the example files
License:    LGPLv2 with exceptions and BSD

%description examples
Provides examples for using the Qt Build Suite (qbs)

%package doc
Summary:    Documentation for qbs
License:    GFDL
BuildArch:  noarch

%description doc
HTML documentation for the Qt Build Suite

%prep
%setup -q

%build
%_qt5_qmake %{name}.pro -r \
    QBS_INSTALL_PREFIX=%{_prefix} \
    QBS_LIB_INSTALL_DIR=%{_libdir} \
    QBS_PLUGINS_INSTALL_DIR=%{_libdir} \
    QBS_LIBRARY_DIRNAME=%{_lib} \
    CONFIG+=disable_rpath \
    CONFIG+=nostrip \
    QMAKE_LFLAGS="-Wl,--as-needed" 

make %{?_smp_mflags}
make html_docs %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}
make install_docs INSTALL_ROOT=%{buildroot}

# Remove the IB-Module since it is only useful for OS X
rm -rf %{buildroot}/%{_datadir}/%{name}/modules/ib

# Remove the WiX-Module since it is only useful for Windows
rm -rf %{buildroot}/%{_datadir}/%{name}/modules/wix

# Remove the IB-Module since it is only useful for OS X or iOS
rm -rf %{buildroot}/%{_datadir}/%{name}/modules/bundle

# Manuall install the docs to prevent ownership
# on the whole docs directory
install -D -p -m 644 LICENSE.LGPLv21 LICENSE.LGPLv3 LGPL_EXCEPTION.txt README %{buildroot}/%{_docdir}/%{name}/

%check
bin/qbs setup-toolchains --type gcc /usr/bin/g++ qbs_autotests_gcc
bin/qbs setup-qt /usr/bin/qmake-qt5 qbs_autotests
bin/qbs config profiles.qbs_autottests.baseProfile qbs_autotests_gcc
make check %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post qt -p /sbin/ldconfig
%postun qt -p /sbin/ldconfig

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-config
%{_bindir}/%{name}-qmltypes
%{_bindir}/%{name}-setup-toolchains
%{_datadir}/%{name}/imports/
%{_datadir}/%{name}/modules/qbs/
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/modules/
%dir %{_libdir}/%{name}/
%dir %{_libdir}/%{name}/plugins/
%{_libdir}/lib%{name}core.so.*
%dir %{_docdir}/%{name}/
%{_docdir}/%{name}/LICENSE.*
%{_docdir}/%{name}/LGPL_EXCEPTION.txt
%{_docdir}/%{name}/README

%files devel
%dir %{_includedir}/%{name}/
%{_includedir}/%{name}/*/
%{_includedir}/%{name}/%{name}.h
%{_includedir}/%{name}/%{name}_version.pri
%{_includedir}/%{name}/use_installed_corelib.pri
%{_libdir}/lib%{name}core.so

%files gui
%{_bindir}/%{name}-config-ui

%files qt
%{_bindir}/%{name}-setup-qt
%{_libdir}/%{name}/plugins/lib%{name}_qt_scanner.so
%{_libdir}/lib%{name}qtprofilesetup.so.*

%files qt-devel
%{_includedir}/%{name}/qtenvironment.h
%{_includedir}/%{name}/qtprofilesetup.h
%{_includedir}/%{name}/use_installed_qtprofilesetup.pri
%{_libdir}/lib%{name}qtprofilesetup.so

%files cpp
%{_datadir}/%{name}/modules/cpp
%{_libdir}/%{name}/plugins/lib%{name}_cpp_scanner.so

%files nsis
%{_datadir}/%{name}/modules/nsis

%files nodejs
%{_datadir}/%{name}/modules/nodejs

%files typescript
%{_datadir}/%{name}/modules/typescript

%files typescript
%{_datadir}/%{name}/modules/typescript

%files android
%{_bindir}/%{name}-setup-android
%{_datadir}/%{name}/modules/Android

%files java
%{_datadir}/%{name}/modules/java

%files archiver
%{_datadir}/%{name}/modules/archiver

%files examples
%{_datadir}/%{name}/examples

%files doc
%{_docdir}/%{name}/html/
%dir %{_docdir}/%{name}/

%changelog
* Tue Apr 28 2015 Erik Schilling <ablu.erikschilling@googlemail.com> 1.4.0-1
- New release 1.4.0

* Thu Dec 11 2014 Erik Schilling <ablu.erikschilling@googlemail.com> 1.3.3-1
- New release 1.3.3
- Removed tests since it is too hard to maintain their lookup of plugins
  on different arches.

* Mon Oct 20 2014 Erik Schilling <ablu.erikschilling@googlemail.com> 1.3.2-1
- New release 1.3.2

* Mon Sep 29 2014 Erik Schilling <ablu.erikschilling@googlemail.com> 1.3.1-1
- New release 1.3.1
- Fixed copy paste error in typescript summary
- Fixed some words to their official use form
- Stopped removing some in theory unuseful files from the package
  This files might break projects because they are expected to be there and it
  is too annoying to maintain the list anyway
- Applied upstream patch to make running the tests easier

* Tue Aug 26 2014 Erik Schilling <ablu.erikschilling@googlemail.com> 1.3.0-1
- New release 1.3.0
- New modules: nodejs, typescript

* Thu Jul 03 2014 Erik Schilling <ablu.erikschilling@googlemail.com> 1.2.2-1
- New upstream release 1.2.2

* Tue Jun 24 2014 Erik Schilling <ablu.erikschilling@googlemail.com> 1.2.1-4
- Removed some files which are not required on linux
- Use upstream patch against double prefix libdirname qmake variable
- Use upstream patch rather than fixing permission myself
- Make clear which patches are from me and which from upstream

* Fri Jun 20 2014 Erik Schilling <ablu.erikschilling@googlemail.com> 1.2.1-3
- Fixed file ownership of the doc package
- Removed accidently added removals of files for testing

* Thu Jun 19 2014 Erik Schilling <ablu.erikschilling@googlemail.com> 1.2.1-2
- Corrected profile lib headers and library package assignment

* Fri Jun 13 2014 Erik Schilling <ablu.erikschilling@googlemail.com> 1.2.1-1
- New upstream release 1.2.1
- New subpackage: nsis
- Run the autotests

* Mon Jan 6 2014 Erik Schilling <ablu.erikschilling@googlemail.com> 1.1.1-2
- Made use of the %%_qt5_qmake makro

* Thu Dec 12 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.1.1-1
- New upstream release 1.1.1

* Wed Nov 6 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.1.0-1
- New upstream release 1.1.0
- Changed package to build with Qt 5
- Introduced new examples subpackage for the newly installed examples
- Made the qt module depend on the cpp one
- Updated summary of -devel to point out that it is only required for native modules

* Sat Jul 6 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.0.1-4
- Prevent linking to unneeded libs

* Sat Jul 6 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.0.1-3
- Added comment to license section to clarify the situation with the exceptions
- Added missing share/qbs dir to the main package

* Thu Jul 4 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.0.1-2
- Tried to make the summary of the main package better
- Splitted the ui part in order to prevent depedency on ui libs for the core packages
- Fixed ownership of the plugins (they are now actually owned by their subpackages)
- Fixed ownership of some directories
- Moved %%doc to the main package
- Made the requirement of the base package arch-specific
- Fixed html doc installation
- Made the doc package noarch

* Mon Jun 10 2013 Erik Schilling <ablu.erikschilling@googlemail.com> 1.0.1-1
- Initial packaging
