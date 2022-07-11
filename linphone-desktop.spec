Name:		linphone-desktop
Version:	4.4.8
Release:	1
Summary:	Voice over IP Application
License:	GPLv2+
Group:		Communications
URL:		http://www.linphone.org
Source0: 	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz	
# (debian)
#Patch0:		0001-do-not-build-linphone-sdk.patch
# (debian)
Patch1:		0002-remove-bc_compute_full_version-usage.patch

BuildRequires:	bctoolbox-static-devel
BuildRequires:	cmake
BuildRequires:	cmake(belcard)
BuildRequires:	cmake(belr)
BuildRequires:	cmake(bctoolbox)
BuildRequires:	cmake(ortp)
BuildRequires:	cmake(linphone)
BuildRequires:	cmake(linphonecxx)
BuildRequires:	cmake(mediastreamer2)
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

Requires:	mediastreamer
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
%{_includedir}/LinphoneApp
%{_libdir}/libapp-plugin.so
%{_datadir}/linphone/
%{_datadir}/applications/linphone.desktop
%{_iconsdir}/hicolor/*/apps/linphone.png
%{_iconsdir}/hicolor/scalable/apps/linphone.svg

#--------------------------------------------------------------------

%prep
%autosetup -p1

# Fix build
#sed -i -e 's,LINPHONE_QT_GIT_VERSION,"%{version}",' linphone-app/src/config.h.cmake
echo '#define LINPHONE_QT_GIT_VERSION "%{version}"' >> linphone-app/src/config.h.cmake
echo "project(linphoneqt VERSION %{version})" > linphone-app/linphoneqt_version.cmake
echo "set (APP_PROJECT_VERSION %{version})" > linphone-app/cmake_builder/linphone_package/linphoneapp_version.cmake
#sed -i -e 's|set(APPLICATION_OUTPUT_DIR "${CMAKE_BINARY_DIR}/OUTPUT")|set(APPLICATION_OUTPUT_DIR "%{_prefix}")|' CMakeLists.txt

# disable SDK
sed -i -e 's|set(APP_DEPENDS sdk)|#set(APP_DEPENDS sdk)|' CMakeLists.txt

%build
%cmake \
	-DENABLE_STATIC:BOOL=NO \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo \
	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
	-DCMAKE_INSTALL_RPATH:BOOL=OFF \
	-DENABLE_UPDATE_CHECK:BOOL=OFF \
	-DENABLE_NON_FREE_CODECS:BOOL=OFF \
	-DENABLE_OPENH264:BOOL=OFF \
	-DLINPHONE_QT_ONLY:BOOL=ON \
	-DENABLE_BUILD_VERBOSE:BOOL=ON \
	-G Ninja
%ninja_build

%install
# The upstream build system behaves weird if DESTDIR is set. Install manually.
sed -i '/linphone-sdk/d' build/linphone-app/cmake_builder/linphone_package/cmake_install.cmake
sed -i "s|${PWD}/build/OUTPUT|/usr|" build/linphone-app/cmake_install.cmake
sed -i "s|${PWD}/build/OUTPUT|/usr|" build/cmake_install.cmake
%ninja_install -C build

rm -f %{buildroot}%{_bindir}/qt.conf

