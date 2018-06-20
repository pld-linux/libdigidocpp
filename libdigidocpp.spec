#
# Conditional build:
%bcond_without	perl		# Perl module
%bcond_without	php		# PHP module
%bcond_without	python		# Python module
%bcond_with	bindings	# build bindings (currently only C#/Win32 and Java/Android supported)

%if %{without bindings}
%undefine	with_perl
%undefine	with_php
%undefine	with_python
%endif

Summary:	Library for creating and validating BDoc and DDoc containers
Summary(pl.UTF-8):	Biblioteka do tworzenia i sprawdzania poprawności kontenerów BDoc i DDoc
Name:		libdigidocpp
Version:	3.13.2
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://github.com/open-eid/libdigidocpp/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	bc7b44fa9ff66669169337f330112ed4
Patch0:		%{name}-link.patch
URL:		https://github.com/open-eid/libdigidocpp
# for tests
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.0
BuildRequires:	doxygen
BuildRequires:	libdigidoc-devel >= 3.9
BuildRequires:	libstdc++-devel
BuildRequires:	minizip-devel
BuildRequires:	openssl-devel >= 1.0.1
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.734
BuildRequires:	xerces-c-devel
BuildRequires:	xml-security-c-devel
BuildRequires:	xsd >= 4.0
BuildRequires:	xxd
BuildRequires:	zlib-devel
%if %{with perl} || %{with php} || %{with python}
BuildRequires:	swig
%endif
%if %{with perl}
BuildRequires:	perl-devel
%endif
%if %{with php}
BuildRequires:	php-devel >= 4:5.0.4
%endif
%if %{with python}
BuildRequires:	python-devel
%endif
Requires:	libdigidoc >= 3.9
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

%package -n python-digidoc
Summary:	Python bindings for libdigidocpp library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libdigidocpp
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-python = %{version}-%{release}
Obsoletes:	libdigidocpp-python < 0.3.0-1

%description -n python-digidoc
Python bindings for libdigidocpp library.

%description -n python-digidoc -l pl.UTF-8
Wiązania Pythona do biblioteki libdigidocpp.

%prep
%setup -q
%patch0 -p1

# Remove bundled copy of minizip
%{__rm} -r src/minizip

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README.md RELEASE-NOTES.md
%dir %{_sysconfdir}/digidocpp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/digidocpp/digidocpp.conf
# XXX ?
%{_sysconfdir}/digidocpp/878252.p12
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
%files -n python-digidoc
%defattr(644,root,root,755)
%{py_sitedir}/*
%endif
