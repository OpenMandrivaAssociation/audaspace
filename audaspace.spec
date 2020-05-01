# we don't want to provide private python extension libs
%global __exclude_provides_from %{python2_sitearch}/.*\\.so\\|%{python3_sitearch}/.*\\.so

# comment out when not pre-release
#define prel		rc1

%define rel		19

%define major		1
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

%bcond_with doc

Name:		audaspace
Version:	1.3.0
Release:	%mkrel %{?prel:0.%prel.}%{rel}
Summary:	A feature rich high level audio library
License:	Apache License
Group:		Sound/Utilities
URL:		http://audaspace.github.io/
Source0:	https://github.com/audaspace/%{name}/archive/v%{version}%{?prel:-%prel}/%{name}-%{version}%{?prel:-%prel}.tar.gz
# add missing "#include <functional>" picked up by gcc7
Patch0:		audaspace-gcc7.patch
Patch1:		audaspace-ffmpeg-4.0.patch
BuildRequires:	cmake
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:	python-setuptools
BuildRequires:	python-numpy-devel

%description
Audaspace (pronounced "outer space") is a high level audio library written
in C++ with language bindings for Python for example.
It started out as the audio engine of the 3D modelling application Blender
and is now released as a standalone library.

#------------------------------------------------

%if %{with doc}
%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
BuildArch:	noarch
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	python-audaspace
BuildRequires:	python-sphinx

%description	doc
This package contains documentation for %{name}.
%endif

#------------------------------------------------

%package -n	%{libname}
Summary:	Library for %{name}
Group:		System/Libraries

%description -n	%{libname}
Audaspace (pronounced "outer space") is a high level audio library written
in C++ with language bindings for Python for example.
It started out as the audio engine of the 3D modelling application Blender
and is now released as a standalone library.
This package contains library files for %{name}.

#------------------------------------------------

%package -n	%{develname}
Summary:	Development package for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains header files for development with %{name}.

#------------------------------------------------

%package -n	python3-%{name}
Summary:	Python3 bindings package for %{name}
Group:		Development/Python
Requires:	pythonegg(3)(numpy)

%description -n	python3-%{name}
This package contains Python3 bindings for %{name}.

#------------------------------------------------

%package -n	python3-%{name}-devel
Summary:	Python3 development package for %{name}
Group:		Development/Python
Requires:	python3-%{name} = %{version}-%{release}

%description -n	python3-%{name}-devel
This package contains Python3 header files for development with %{name}.

#------------------------------------------------
%prep
%setup -q -n %{name}-%{version}%{?prel:-%prel}
%autopatch -p1

%build
%cmake \
	-DWITH_STRICT_DEPENDENCIES:BOOL=TRUE \
	-DUSE_SDL2:BOOL=TRUE \
	%if %{with doc}
	-DSPHINX_EXECUTABLE=%{_bindir}/sphinx-build-%{python3_version} \
	-DDOCUMENTATION_INSTALL_PATH:PATH=%{_docdir}/%{name} \
	%else
	-DWITH_DOCS:BOOL=FALSE \
	-DWITH_BINDING_DOCS:BOOL=FALSE \
	%endif
	-DDEFAULT_PLUGIN_PATH:PATH=%{_libdir}/%{name}/plugins
%make_build

%install
%make_install -C build

%files
%doc AUTHORS LICENSE README.md
%{_bindir}/*

%if %{with doc}
%files doc
%{_docdir}/%{name}/
%endif

%files -n %{libname}
%doc AUTHORS LICENSE README.md
%{_libdir}/lib%{name}*.so.%{major}{,.*}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/libaud*.so.%{major}{,.*}

%files -n %{develname}
%doc AUTHORS LICENSE README.md
%{_includedir}/%{name}/
%{_libdir}/lib%{name}*.so
%{_libdir}/%{name}/plugins/libaud*.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n python3-%{name}
%doc AUTHORS LICENSE README.md
%{python3_sitearch}/aud.cpython-3?m-*.so
%{python3_sitearch}/%{name}-%{version}%{?prel}-py%{python3_version}.egg-info

%files -n python3-%{name}-devel
%doc AUTHORS LICENSE README.md
%{_includedir}/python*/%{name}/


%changelog
* Wed Jan 09 2019 daviddavid <daviddavid> 1.3.0-18.mga7
+ Revision: 1353054
- non-bootstrap build

* Mon Jan 07 2019 shlomif <shlomif> 1.3.0-17.mga7
+ Revision: 1351095
- Rebuild for python3 3.7

* Fri Sep 21 2018 umeabot <umeabot> 1.3.0-16.mga7
+ Revision: 1295121
- Mageia 7 Mass Rebuild

* Tue Aug 21 2018 wally <wally> 1.3.0-15.mga7
+ Revision: 1253228
- really build without docs on aarch64

* Mon Aug 20 2018 wally <wally> 1.3.0-14.mga7
+ Revision: 1253150
- build without docs on aarch64

* Fri Jun 08 2018 daviddavid <daviddavid> 1.3.0-13.mga7
+ Revision: 1235531
- add upstream patch to properly support newer ffmpeg versions

* Sun Apr 29 2018 daviddavid <daviddavid> 1.3.0-12.mga7
+ Revision: 1223549
- non bootstrap build

* Sun Apr 29 2018 daviddavid <daviddavid> 1.3.0-11.mga7
+ Revision: 1223536
- add patch to fix build with ffmpeg 4.0
- rebuild for new ffmpeg 4.0
- do a bootstrap build

* Thu Sep 14 2017 daviddavid <daviddavid> 1.3.0-10.mga7
+ Revision: 1153844
- add missing #include <functional> to fix build with gcc7

* Fri Aug 04 2017 daviddavid <daviddavid> 1.3.0-9.mga7
+ Revision: 1134851
- reenable build of documentation

* Fri Aug 04 2017 daviddavid <daviddavid> 1.3.0-8.mga7
+ Revision: 1134791
- rebuild for Python 3.6 (do a bootstrap build)

* Wed Mar 29 2017 neoclust <neoclust> 1.3.0-7.mga6
+ Revision: 1095176
- Enable bootstrap for armv5 build
- Enable bootstrap for armv5 build

* Sun Mar 12 2017 daviddavid <daviddavid> 1.3.0-6.mga6
+ Revision: 1092158
- reenable build of documentation for ARMv7

* Sun Mar 12 2017 neoclust <neoclust> 1.3.0-5.mga6
+ Revision: 1092117
- Disable doc for armv7 bootstrap

* Sun Mar 12 2017 neoclust <neoclust> 1.3.0-4.mga6
+ Revision: 1092106
- Rebuild for armv7

* Wed Mar 08 2017 akien <akien> 1.3.0-3.mga6
+ Revision: 1090408
- Reenable building documentation with own lib

* Wed Mar 08 2017 akien <akien> 1.3.0-2.mga6
+ Revision: 1090225
- Do a bootstrap build (doc needs python3-audaspace)
- Rebuild for ffmpeg 3.2.4

* Tue Nov 08 2016 daviddavid <daviddavid> 1.3.0-1.mga6
+ Revision: 1065925
- new version: 1.3.0

* Fri May 20 2016 daviddavid <daviddavid> 1.2-3.mga6
+ Revision: 1017234
- reenable build of documentation for ARMv7

* Fri May 20 2016 daviddavid <daviddavid> 1.2-2.mga6
+ Revision: 1017229
- disable build on ARMv5 as std::future does not exist on ARMv5
- disable build of documentation for first build on ARMv7

* Sun Mar 13 2016 daviddavid <daviddavid> 1.2-1.mga6
+ Revision: 990226
- new version: 1.2
- remove merged upstream patch
- add BR pkgconfig(fftw3)

* Wed Feb 03 2016 daviddavid <daviddavid> 1.1-4.mga6
+ Revision: 933342
- now reenable build of documentation for arm

* Wed Feb 03 2016 daviddavid <daviddavid> 1.1-3.mga6
+ Revision: 933338
- disable build of documentation to first generate python3-audaspace on arm

* Wed Feb 03 2016 daviddavid <daviddavid> 1.1-2.mga6
+ Revision: 933334
- rebuild for arm
- move python3-numpy requirement to the python3-audaspace subpackage

* Fri Oct 16 2015 daviddavid <daviddavid> 1.1-1.mga6
+ Revision: 892002
- new version: 1.1
- add upstream patch to make cmake finds correct numpy path

* Sat Oct 10 2015 daviddavid <daviddavid> 1.0-6.mga6
+ Revision: 889278
- reenable build of documentation
- add BR python3-sphinx_rtd_theme

* Thu Oct 08 2015 daviddavid <daviddavid> 1.0-5.mga6
+ Revision: 887244
- rebuild for python 3.5
- use new python macros
- disable build of documentation

* Sun Aug 30 2015 daviddavid <daviddavid> 1.0-4.mga6
+ Revision: 871356
- remove no more needed previous patch 'fix python3 link flags' (mga#16570)

* Sat Aug 15 2015 daviddavid <daviddavid> 1.0-3.mga6
+ Revision: 864813
- add patch to fix python3 link flags (mga#16570)

* Fri Aug 14 2015 daviddavid <daviddavid> 1.0-2.mga6
+ Revision: 864799
- enable build of documentation

* Fri Aug 14 2015 daviddavid <daviddavid> 1.0-1.mga6
+ Revision: 864793
- initial package audaspace

