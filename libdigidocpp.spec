# TODO
# - use ca-certificates certs and drop /etc/digidocpp/certs
#
# Conditional build:
%bcond_without	perl	# perl module
%bcond_without	php		# php module
%bcond_without	python	# python module
%bcond_without	bindings	# build bindings

%if %{without bindings}
%undefine	with_perl
%undefine	with_php
%undefine	with_python
%endif

Summary:	Library for creating and validating BDoc and DDoc containers
Name:		libdigidocpp
Version:	0.3.0
Release:	0.1
License:	LGPL v2+
Group:		Libraries
URL:		http://code.google.com/p/esteid/
Source0:	http://esteid.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	a567fd16d2ce6205b179850e98c26971
BuildRequires:	cmake
BuildRequires:	libdigidoc-devel
BuildRequires:	libp11-devel
BuildRequires:	minizip-devel
BuildRequires:	openssl-devel
BuildRequires:	rpmbuild(macros) >= 1.519
BuildRequires:	xml-security-c-devel
BuildRequires:	xsd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
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
Requires:	libdigidoc
Requires:	opensc

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
rm -rf src/minizip

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
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libdigidocpp.so.*.*.*
%ghost %attr(755,root,root) %{_libdir}/libdigidocpp.so.0
%dir %{_sysconfdir}/digidocpp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/digidocpp/digidocpp.conf
%{_sysconfdir}/digidocpp/certs
%{_sysconfdir}/digidocpp/schema

%files devel
%defattr(644,root,root,755)
%{_libdir}/*.so
%{_includedir}/digidocpp
%{_pkgconfigdir}/lib*.pc

%if %{with perl}
%files -n perl-digidoc
%defattr(644,root,root,755)
%{perl_vendorarch}/*
%{perl_vendorlib}/*
%endif

%if %{with php}
%files -n php-digidoc
%defattr(644,root,root,755)
%{php_extdir}/*
%{php_data_dir}/*
%{_sysconfdir}/php.d/digidoc.ini
%endif

%if %{with python}
%files -n python-digidoc
%defattr(644,root,root,755)
%{py_sitedir}/*
%endif
