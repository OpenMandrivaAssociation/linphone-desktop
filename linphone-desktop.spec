%bcond_with	ffmpeg
%bcond_with	ldap
%bcond_with	static
%bcond_without	strict
%bcond_with	tests

Name:		linphone-desktop
Version:	5.1.2
Release:	1
Summary:	Voice over IP Application
License:	GPLv3+
Group:		Communications
URL:		https://www.linphone.org
Source0: 	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz	
Patch0:		linphone-desktop-5.1.2-cmake-dont-use-git.patch

BuildRequires:	bctoolbox-static-devel
BuildRequires:	cmake
BuildRequires:	cmake(belcard)
BuildRequires:	cmake(belr)
BuildRequires:	cmake(bctoolbox)
BuildRequires:	cmake(jsoncpp)
BuildRequires:	cmake(ortp)
BuildRequires:	cmake(linphone)
BuildRequires:	cmake(linphonecxx)
BuildRequires:	cmake(mediastreamer2)
BuildRequires:	cmake(Qt5)
BuildRequires:	cmake(Qt5Concurrent)
BuildRequires:	cmake(Qt5DBus)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Keychain)
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	cmake(Qt5Multimedia)
BuildRequires:	cmake(Qt5Network)
BuildRequires:	cmake(Qt5Pdf)
BuildRequires:	cmake(Qt5PdfWidgets)
BuildRequires:	cmake(Qt5Qml)
BuildRequires:	cmake(Qt5Quick)
BuildRequires:	cmake(Qt5QuickControls2)
BuildRequires:	cmake(Qt5Svg)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5TextToSpeech)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	ninja
BuildRequires:	pkgconfig(bctoolbox)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(speech-dispatcher)
BuildRequires:	qmake5

Requires:	belcard
Requires:	mediastreamer
Requires:	speech-dispatcher
Requires:	qt5-qtdeclarative
Requires:	qt5-qtgraphicaleffects
Requires:	qt5-qtquickcontrols
Requires:	qt5-qtquickcontrols2
Requires:	qt5-qtmultimedia

Provides:	linphone = %{version}-%{release}
Obsoletes:	linphone < 4.1.1

%description
Linphone is a free VoIP and video softphone based on the SIP protocol.

%files
%license LICENSE.txt
%doc README.md CHANGELOG.md
%{_bindir}/linphone
#%{_bindir}/linphone-tester
%{_includedir}/LinphoneApp
%{_libdir}/libapp-plugin.so
%{_datadir}/linphone/
%{_datadir}/applications/linphone.desktop
%{_iconsdir}/hicolor/*/apps/linphone.png
%{_iconsdir}/hicolor/scalable/apps/linphone.svg

#--------------------------------------------------------------------

%prep
%autosetup -p1

# fix build (patch0)
sed -i -e 's|@FULLVERSION@|%{version}|' \
	linphone-app/CMakeLists.txt \
	linphone-app/cmake_builder/linphone_package/CMakeLists.txt \
	linphone-app/build/CMakeLists.txt

# disable SDK
sed -i -e 's|set(APP_DEPENDS sdk)|#set(APP_DEPENDS sdk)|' CMakeLists.txt

%build
alias 'git=%{_bindir}/true'
%cmake \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	-DCMAKE_INSTALL_RPATH:BOOL=OFF \
	-DENABLE_UPDATE_CHECK:BOOL=OFF \
	-DENABLE_NON_FREE_CODECS:BOOL=OFF \
	-DENABLE_OPENH264:BOOL=OFF \
	-DLINPHONE_QT_ONLY:BOOL=ON \
	-DENABLE_QT_KEYCHAIN:BOOL=OFF \
	-DENABLE_VIDEO:BOOL=ON \
	-DENABLE_FFMPEG:BOOL=%{?with_ffmpeg:ON}%{?!without_ffmpeg:OFF} \
	-DENABLE_LDAP:BOOL=%{?with_ldap:ON}%{?!without_ldap:OFF} \
	-DENABLE_BUILD_VERBOSE:BOOL=OFF \
	-G Ninja

%ninja_build

%install
# The upstream build system behaves weird if DESTDIR is set. Install manually.
sed -i '/linphone-sdk/d' build/linphone-app/cmake_builder/linphone_package/cmake_install.cmake
sed -i "s|${PWD}/build/OUTPUT|/usr|" build/linphone-app/cmake_install.cmake
sed -i "s|${PWD}/build/OUTPUT|/usr|" build/cmake_install.cmake
%ninja_install -C build

rm -f %{buildroot}%{_bindir}/qt.conf

