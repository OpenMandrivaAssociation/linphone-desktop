Name:		linphone-desktop
Version:	4.2.5
Release:	1
Summary:	Voice over IP Application
License:	GPLv2+
Group:		Communications
URL:		http://www.linphone.org
Source0: 	https://gitlab.linphone.org/BC/public/linphone-desktop/-/archive/%{version}/linphone-desktop-%{version}.tar.bz2
Patch1:		0001-Don-t-build-linphone-sdk.patch
Patch2:		0002-Fix-building-out-of-git.patch
Patch3:		0001-Further-fixes-for-building-out-of-git.patch
BuildRequires:	bctoolbox-static-devel
BuildRequires:	git
BuildRequires:	cmake
BuildRequires:	cmake(belcard)
BuildRequires:	cmake(Linphone)
BuildRequires:	cmake(Qt5)
BuildRequires:	cmake(Qt5Concurrent)
BuildRequires:	cmake(Qt5DBus)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	cmake(Qt5Quick)
BuildRequires:	cmake(Qt5QuickControls2)
BuildRequires:	cmake(Qt5Svg)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5TextToSpeech)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	ninja
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(bctoolbox)
BuildRequires:	qmake5

Requires:	mediastreamer >= 1:2.16.1
Requires:	qt5-qtdeclarative
Requires:	qt5-qtquickcontrols
Requires:	qt5-qtquickcontrols2
Requires:	qt5-qtgraphicaleffects

Provides:	linphone = %{version}-%{release}
Obsoletes:	linphone < 4.1.1

%description
Linphone is a free VoIP and video softphone based on the SIP protocol.

%files
%license LICENSE.txt
%doc README.md CHANGELOG.md
%{_bindir}/linphone
#%{_bindir}/linphone-tester
%{_datadir}/linphone/
%{_datadir}/applications/linphone.desktop
%{_iconsdir}/hicolor/*/apps/linphone.png
%{_iconsdir}/hicolor/scalable/apps/linphone.svg

#--------------------------------------------------------------------

%prep
%autosetup -p1 -n linphone-desktop-%{version}

%build
%cmake\
	-DENABLE_BUILD_VERBOSE:BOOL=ON \
	-DENABLE_UPDATE_CHECK:BOOL=OFF \
	-DENABLE_NON_FREE_CODECS:BOOL=OFF \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_INSTALL_RPATH:BOOL=OFF \
	-DENABLE_NON_FREE_CODECS:BOOL=OFF \
	-G Ninja
%ninja_build

sed "/linphone-sdk/d" -i %{_vpath_builddir}/linphone-app/cmake_builder/linphone_package/cmake_install.cmake
sed "s|$(pwd)/%{_vpath_builddir}/OUTPUT|%{_prefix}|" -i %{_vpath_builddir}/cmake_install.cmake


%install
%ninja_install -C build

rm -f %{buildroot}%{_bindir}/qt.conf

