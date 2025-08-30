# We don't want to provide private python extension libs
%global __exclude_provides_from %{python2_sitearch}/.*\\.so\\|%{python3_sitearch}/.*\\.so

# Comment out when not pre-release
#define prel		20220508

%define		rel		1

%define		major		1
%define		libname		%mklibname %{name}
%define		develname	%mklibname %{name} -d

%bcond_with	doc

Summary:		A feature rich high level audio library
Name:		audaspace
Version:		1.7.0
Release:		%{?prel:0.%prel.}%{rel}2
License:		Apache-2.0
Group:		Sound/Utilities
Url:		https://audaspace.github.io/
%if 0%{?prel:1}
Source0:	https://github.com/audaspace/audaspace/archive/refs/heads/master.tar.gz#/audaspace-%{prel}.tar.gz
%else
Source0:	https://github.com/audaspace/%{name}/archive/v%{version}%{?prel:-%prel}/%{name}-%{version}%{?prel:-%prel}.tar.gz
%endif
Patch0:		audaspace-1.6.0-python3.8.patch
BuildRequires:		cmake >= 3.10
BuildRequires:		ninja
BuildRequires:		pkgconfig(fftw3)
BuildRequires:		pkgconfig(jack)
BuildRequires:		pkgconfig(libavcodec)
BuildRequires:		pkgconfig(libavformat)
BuildRequires:		pkgconfig(libavutil)
BuildRequires:		pkgconfig(openal)
BuildRequires:		pkgconfig(python)
BuildRequires:		pkgconfig(sdl2)
BuildRequires:		pkgconfig(sndfile)
BuildRequires:		pkgconfig(libpipewire-0.3) >= 1.1.0
BuildRequires:		pkgconfig(libpulse)
BuildRequires:		python-setuptools
BuildRequires:		python-numpy-devel

%description
Audaspace (pronounced "outer space") is a high level audio library written
in C++ with language bindings for Python for example.
It started out as the audio engine of the 3D modelling application Blender
and is now released as a standalone library.

%files
%doc AUTHORS LICENSE README.md
%{_bindir}/*

#------------------------------------------------

%if %{with doc}
%package	doc
Summary:		Documentation for %{name}
Group:	Documentation
BuildArch:		noarch
BuildRequires:		doxygen
BuildRequires:		graphviz
BuildRequires:		python-audaspace
BuildRequires:		python-sphinx

%description	doc
This package contains documentation for %{name}.

%files doc
%{_docdir}/%{name}/
%endif

#------------------------------------------------

%package -n	%{libname}
Summary:		Library for %{name}
Group:		System/Libraries

%description -n	%{libname}
Audaspace (pronounced "outer space") is a high level audio library written
in C++ with language bindings for Python for example.
It started out as the audio engine of the 3D modelling application Blender
and is now released as a standalone library.
This package contains library files for %{name}.

%files -n %{libname}
%doc AUTHORS LICENSE README.md
%{_libdir}/lib%{name}*.so.%{major}{,.*}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/libaud*.so.%{major}{,.*}

#------------------------------------------------

%package -n	%{develname}
Summary:	Development package for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains header files for development with %{name}.

%files -n %{develname}
%doc AUTHORS LICENSE README.md
%{_includedir}/%{name}/
%{_libdir}/lib%{name}*.so
%{_libdir}/%{name}/plugins/libaud*.so
%{_libdir}/pkgconfig/%{name}.pc

#------------------------------------------------

%package -n	python-%{name}
Summary:		Python3 bindings package for %{name}
Group:		Development/Python
Provides:	python3-%{name}
Requires:	python3dist(numpy)

%description -n	python-%{name}
This package contains Python3 bindings for %{name}.

%files -n python-%{name}
%doc AUTHORS LICENSE README.md
%{python_sitearch}/aud.cpython-*
%{python_sitearch}/%{name}-*py%{python_version}.egg-info

#------------------------------------------------

%package -n	python-%{name}-devel
Summary:	Python3 development package for %{name}
Group:		Development/Python
Provides:	python3-%{name}-devel
Requires:	python-%{name} = %{version}-%{release}

%description -n	python-%{name}-devel
This package contains Python3 header files for development with %{name}.

%files -n python-%{name}-devel
%doc AUTHORS LICENSE README.md
%{_includedir}/python*/%{name}/

#------------------------------------------------

%prep
%if 0%{?prel:1}
%autosetup -p1 -n %{name}-master
%else
%autosetup -p1 -n %{name}-%{version}%{?prel:-%prel}
%endif


%build
%cmake \
	-DWITH_STRICT_DEPENDENCIES:BOOL=TRUE \
	-DUSE_SDL2:BOOL=TRUE \
	%if %{with doc}
	-DSPHINX_EXECUTABLE=%{_bindir}/sphinx-build \
	-DDOCUMENTATION_INSTALL_PATH:PATH=%{_docdir}/%{name} \
	%else
	-DWITH_DOCS:BOOL=FALSE \
	-DWITH_BINDING_DOCS:BOOL=FALSE \
	%endif
	-DDEFAULT_PLUGIN_PATH:PATH=%{_libdir}/%{name}/plugins \
	-G Ninja
%ninja_build


%install
%ninja_install -C build
