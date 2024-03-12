%bcond_with		ffmpeg
%bcond_with		ldap
%bcond_without	oauth2
%bcond_with		static
%bcond_without	strict
%bcond_with		tests

%global commit_external_ispell	05574fe160222c3d0b6283c1433c9b087271fad1

Name:		linphone-desktop
Version:	5.2.2
Release:	1
Summary:	Voice over IP Application
License:	GPLv3+
Group:		Communications
URL:		https://www.linphone.org
Source0: 	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz	
Source10:	https://gitlab.linphone.org/BC/public/external/ispell/-/archive/%{commit_external_ispell}/ispell-%{commit_external_ispell}.tar.bz2

Patch0:		linphone-desktop-5.2.1-cmake_dont_use_git.patch
Patch1:		linphone-desktop-5.2.1-use_system_rootca.patch
Patch2:		linphone-desktop-5.2.1-cmake_external_libs.patch
Patch3:		linphone-desktop-5.2.2-cmake_fix_path.patch
Patch4:		linphone-desktop-5.2.1-bundle_ispell.patch
Patch5:		linphone-desktop-5.2.1-disable_spec.patch



BuildRequires:	cmake
BuildRequires:	cmake(belcard)
BuildRequires:	cmake(belr)
BuildRequires:	cmake(bctoolbox)
BuildRequires:	cmake(jsoncpp)
BuildRequires:	cmake(ortp)
BuildRequires:	cmake(liblinphone)
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
BuildRequires:	cmake(Qt5NetworkAuth)
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
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	qmake5

Requires:	belcard
Requires:	mediastreamer
Requires:	speech-dispatcher
Requires:	qt5-qtdeclarative
Requires:	qt5-qtgraphicaleffects
Requires:	qt5-qtquickcontrols
Requires:	qt5-qtquickcontrols2
Requires:	qt5-qtmultimedia

# This is from OM restricted repo
Suggests:	x265

Provides:	linphone = %{version}-%{release}
Provides:	bundled(ispell) = 3.4.05

%description
Linphone is a free VoIP and video softphone based on the SIP protocol.

%files
%license LICENSE.txt
%doc README.md CHANGELOG.md
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_bindir}/linphone
#{_bindir}/linphone-tester
%{_includedir}/LinphoneApp
%{_libdir}/libapp-plugin.so
%{_libdir}/%{name}/libISpell.so
%{_datadir}/linphone/
%{_datadir}/applications/linphone.desktop
%{_iconsdir}/hicolor/*/apps/linphone.png
%{_iconsdir}/hicolor/scalable/apps/linphone.svg

#--------------------------------------------------------------------

%prep
%autosetup -p1

# add external sources
pushd external
tar  --strip-components=1 --directory=ispell -xf %{SOURCE10}
popd

# fix build (patch0)
sed -i -e 's|@LINPHONEAPP_VERSION@|%{version}|' \
	linphone-app/CMakeLists.txt \
	linphone-app/cmake_builder/linphone_package/CMakeLists.txt \
	linphone-app/build/CMakeLists.txt

# disable SDK
sed -i -e 's|set(APP_DEPENDS sdk)|#set(APP_DEPENDS sdk)|' CMakeLists.txt

%build
%cmake -Wno-dev \
	-DENABLE_STATIC:BOOL=%{?with_static:ON}%{?!with_static:OFF} \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DCMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT:BOOL=OFF \
	-DCMAKE_PREFIX_PATH:PATH=%{_prefix} \
	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	-DLINPHONE_QT_ONLY:BOOL=ON \
	-DENABLE_APP_OAUTH2:BOOL=%{?with_oauth2:ON}%{?!with_oauth2:OFF} \
	-DENABLE_APP_PACKAGE_ROOTCA:BOOL=OFF \
	-DENABLE_BUILD_VERBOSE:BOOL=OFF \
	-DENABLE_CONSOLE_UI:BOOL=ON \
	-DENABLE_FFMPEG:BOOL=%{?with_ffmpeg:ON}%{?!with_ffmpeg:OFF} \
	-DENABLE_LDAP:BOOL=%{?with_ldap:ON}%{?!with_ldap:OFF} \
	-DENABLE_NON_FREE_CODECS:BOOL=OFF \
	-DENABLE_OPENH264:BOOL=OFF \
	-DENABLE_QT_KEYCHAIN:BOOL=OFF \
	-DENABLE_VIDEO:BOOL=ON \
	-DENABLE_UPDATE_CHECK:BOOL=OFF \
	-G Ninja

%ninja_build

%install
# The upstream build system behaves weird if DESTDIR is set. Install manually.
#sed -i '/linphone-sdk/d' build/linphone-app/cmake_builder/linphone_package/cmake_install.cmake
#sed -i "s|${PWD}/build/OUTPUT|/usr|" build/linphone-app/cmake_install.cmake
#sed -i "s|${PWD}/build/OUTPUT|/usr|" build/cmake_install.cmake
%ninja_install -C build

# move bundeld libs into special path
install -dm 0755 %{buildroot}%{_libdir}/%{name}/
mv %{buildroot}%{_libdir}/libISpell.so %{buildroot}%{_libdir}/%{name}/

# make library links
install -dm 0755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
/bin/echo "%{_libdir}/%{name}/" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

# remove unused
rm -f %{buildroot}%{_bindir}/qt.conf
rm -f %{buildroot}%{_datadir}/linphone/rootca.pem

