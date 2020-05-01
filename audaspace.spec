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
Patch2:		python3.8.patch
BuildRequires:	cmake
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(fftw3)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(openal)
BuildRequires:	pkgconfig(python)
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

%package -n	python-%{name}
Summary:	Python3 bindings package for %{name}
Group:		Development/Python
Provides:	python3-%{name}
Requires:	pythonegg(3)(numpy)

%description -n	python-%{name}
This package contains Python3 bindings for %{name}.

#------------------------------------------------

%package -n	python-%{name}-devel
Summary:	Python3 development package for %{name}
Group:		Development/Python
Provides:	python3-%{name}-devel
Requires:	python-%{name} = %{version}-%{release}

%description -n	python-%{name}-devel
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

%files -n python-%{name}
%doc AUTHORS LICENSE README.md
#%{python_sitearch}/aud.cpython-3?m-*.so
%{python_sitearch}/%{name}-%{version}%{?prel}-py%{python_version}.egg-info

%files -n python-%{name}-devel
%doc AUTHORS LICENSE README.md
%{_includedir}/python*/%{name}/
