#
# Conditional build:
%bcond_without	java		# Java module
%bcond_with	perl		# Perl module
%bcond_with	php		# PHP module
%bcond_without	python		# Python 3 module
%bcond_without	bindings	# build bindings (currently only C#/Win32 and Java/Android supported)
# https://github.com/open-eid/libdigidocpp/issues/231
%bcond_with	podofo		# outdated PoDoFo support (disabled in sources)

%if %{without bindings}
%undefine	with_java
%undefine	with_perl
%undefine	with_php
%undefine	with_python
%endif

Summary:	Library for creating and validating BDoc and DDoc containers
Summary(pl.UTF-8):	Biblioteka do tworzenia i sprawdzania poprawności kontenerów BDoc i DDoc
Name:		libdigidocpp
Version:	3.16.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/open-eid/libdigidocpp/releases
Source0:	https://github.com/open-eid/libdigidocpp/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	879590bba8b236b128646871003593cd
Patch0:		%{name}-link.patch
Patch1:		%{name}-python.patch
URL:		https://github.com/open-eid/libdigidocpp
# for tests
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	doxygen
BuildRequires:	libstdc++-devel
BuildRequires:	minizip-devel >= 1
BuildRequires:	openssl-devel >= 1.1.1
%if %{with perl}
BuildRequires:	perl-devel
%endif
%if %{with php}
BuildRequires:	php-devel >= 4:5.0.4
%endif
BuildRequires:	pkgconfig
%{?with_podofo:BuildRequires:	podofo-devel}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.734
%if %{with perl} || %{with php} || %{with python}
BuildRequires:	swig
%endif
BuildRequires:	xerces-c-devel
BuildRequires:	xml-security-c-devel
BuildRequires:	xsd >= 4.0
BuildRequires:	xxd
BuildRequires:	zlib-devel
%if %{with python}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	swig-python >= 2
%endif
Requires:	opensc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libdigidocpp is a C++ library for reading, validating, and creating
BDoc and DDoc containers. These file formats are widespread in Estonia
where they are used for storing legally binding digital signatures.

%description -l pl.UTF-8
libdigidocpp to biblioteka C++ do odczytu, sprawdzania poprawności i
tworzenia kontenerów BDoc i DDoc. Te formaty plików są
rozpowszechnione w Estonii, gdzie służą do przechowywania umocowanych
prawnie podpisów cyfrowych.

%package devel
Summary:	Development files for libdigidocpp library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libdigidocpp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
This package contains the header files for developing applications
that use libdigidocpp library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę libdigidocpp.

%package apidocs
Summary:	API documentation for libdigidocpp library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libdigidocpp
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libdigidocpp library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libdigidocpp.

%package -n perl-digidoc
Summary:	Perl bindings for libdigidocpp library
Summary(pl.UTF-8):	Wiązania Perla do biblioteki libdigidocpp
Group:		Development/Languages/Perl
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-perl = %{version}-%{release}
Obsoletes:	libdigidocpp-perl < 0.3.0-1

%description -n perl-digidoc
Perl bindings for libdigidocpp library.

%description -n perl-digidoc -l pl.UTF-8
Wiązania Perla do biblioteki libdigidocpp.

%package -n php-digidoc
Summary:	PHP bindings for libdigidocpp library
Summary(pl.UTF-8):	Wiązania PHP do biblioteki libdigidocpp
Group:		Development/Languages/PHP
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}
Provides:	%{name}-php = %{version}-%{release}
Obsoletes:	libdigidocpp-php < 0.3.0-1

%description -n php-digidoc
PHP bindings for libdigidocpp library.

%description -n php-digidoc -l pl.UTF-8
Wiązania PHP do biblioteki libdigidocpp.

%package -n python3-digidoc
Summary:	Python bindings for libdigidocpp library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libdigidocpp
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-python = %{version}-%{release}
Obsoletes:	libdigidocpp-python < 0.3.0-1
Obsoletes:	python-digidoc < 0.3.0-2

%description -n python3-digidoc
Python bindings for libdigidocpp library.

%description -n python3-digidoc -l pl.UTF-8
Wiązania Pythona do biblioteki libdigidocpp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Remove bundled copy of minizip
%{__rm} -r src/minizip

%build
%cmake -B build \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
	-DPython3_SITELIB=%{py3_sitedir}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

# should be as dll not sources
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/digidocpp_csharp
# should be as jar not sources
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/ee/ria/libdigidocpp

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README.md RELEASE-NOTES.md
%dir %{_sysconfdir}/digidocpp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/digidocpp/digidocpp.conf
%{_sysconfdir}/digidocpp/schema
%attr(755,root,root) %{_libdir}/libdigidocpp.so.*.*.*
%ghost %attr(755,root,root) %{_libdir}/libdigidocpp.so.1
%attr(755,root,root) %{_bindir}/digidoc-tool
%{_mandir}/man1/digidoc-tool.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdigidocpp.so
%{_includedir}/digidocpp
%{_pkgconfigdir}/libdigidocpp.pc

%files apidocs
%defattr(644,root,root,755)
%doc build/doc/*

# TODO: csharp, java bindings?
#%attr(755,root,root) %{_libdir}/libdigidoc_csharp.so
#%attr(755,root,root) %{_libdir}/libdigidoc_java.so

%if %{with perl}
%files -n perl-digidoc
%defattr(644,root,root,755)
%{perl_vendorarch}/*
%{perl_vendorlib}/*
%endif

%if %{with php}
%files -n php-digidoc
%defattr(644,root,root,755)
%{php_extensiondir}/*
%{php_data_dir}/*
%{_sysconfdir}/php.d/digidoc.ini
%endif

%if %{with python}
%files -n python3-digidoc
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_digidoc_python.so
%{py3_sitedir}/digidoc.py
%{py3_sitedir}/__pycache__/digidoc.cpython-*.py[co]
%endif
