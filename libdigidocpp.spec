#
# Conditional build:
%bcond_without	perl	# perl module
%bcond_without	php		# php module
%bcond_without	python	# python module
%bcond_with		bindings	# build bindings

%if %{without bindings}
%undefine	with_perl
%undefine	with_php
%undefine	with_python
%endif

Summary:	Library for creating and validating BDoc and DDoc containers
Name:		libdigidocpp
Version:	3.12.3
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://github.com/open-eid/libdigidocpp/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	deead245114c60c3afe7c4a3b3c81060
URL:		https://github.com/open-eid/libdigidocpp
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	libdigidoc-devel >= 3.9
BuildRequires:	libp11-devel
BuildRequires:	minizip-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.583
BuildRequires:	xml-security-c-devel
BuildRequires:	xsd
BuildRequires:	xxd
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

# missing -lpthread, -lxalan-c, etc
%define		skip_post_check_so	libdigidocpp.so.%{version}

%description
libdigidocpp is a C++ library for reading, validating, and creating
BDoc and DDoc containers. These file formats are widespread in Estonia
where they are used for storing legally binding digital signatures.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libdigidoc-devel
Requires:	libp11-devel
Requires:	openssl-devel
Requires:	xml-security-c-devel
Requires:	xsd

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n perl-digidoc
Summary:	Perl bindings for %{name}
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-perl = %{version}-%{release}
Obsoletes:	libdigidocpp-perl < 0.3.0-1

%description -n perl-digidoc
The perl-digidoc package contains Perl bindings for the %{name}
library.

%package -n php-digidoc
Summary:	PHP bindings for %{name}
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
%{?requires_php_extension}
Provides:	%{name}-php = %{version}-%{release}
Obsoletes:	libdigidocpp-php < 0.3.0-1

%description -n php-digidoc
The php-digidoc package contains PHP bindings for the %{name} library.

%package -n python-digidoc
Summary:	Python bindings for %{name}
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Provides:	%{name}-python = %{version}-%{release}
Obsoletes:	libdigidocpp-python < 0.3.0-1

%description -n python-digidoc
The python-digidoc package contains Python bindings for the %{name}
library.

%prep
%setup -q

# Remove bundled copy of minizip
rm -r src/minizip
# Remove bundled openssl
rm -r src/openssl

%build
install -d build
cd build
%cmake .. \
	%{!?with_bindings:-DENABLE_BINDINGS=NO}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md RELEASE-NOTES.txt
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
%{_libdir}/libdigidocpp.so
%{_includedir}/digidocpp
%{_pkgconfigdir}/libdigidocpp.pc

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
