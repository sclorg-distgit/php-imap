# centos/sclo spec file for php-imap
#
# Copyright (c) 2017-2019 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php71"
%global sub_prefix sclo-php71-
%else
%global sub_prefix %{scl_prefix}
%endif
%scl_package        php-imap
%else
%global pkg_name    %{name}
%endif

%global pecl_name  imap
%global ini_name   20-%{pecl_name}.ini

Name:           %{?sub_prefix}php-%{pecl_name}
Summary:        A module for PHP applications that use IMAP
Version:        7.1.30
Release:        1%{?dist}
Source0:        http://www.php.net/distributions/php-%{version}.tar.xz

License:        PHP
Group:          Development/Languages
URL:            http://php.net/%{pecl_name}

BuildRequires:  %{?scl_prefix}php-devel > 7.1
BuildRequires:  krb5-devel
BuildRequires:  openssl-devel
BuildRequires:  uw-imap-devel
BuildRequires:  uw-imap-static

%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}php-%{pecl_name}          = %{version}-%{release}
Provides:      %{?scl_prefix}php-%{pecl_name}%{?_isa}  = %{version}-%{release}
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}


%description
The %{name} package module will add IMAP (Internet Message Access Protocol)
support to PHP. IMAP is a protocol for retrieving and uploading e-mail messages
on mail servers. PHP is an HTML-embedded scripting language. If you need IMAP
support for PHP applications, you will need to install this package.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -n php-%{version}

# Fix reported version
sed -e '/PHP_IMAP_VERSION/s/PHP_VERSION/"%{version}"/' \
    -i ext/%{pecl_name}/php_imap.h

# Configuration file
cat << 'EOF' | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF


%build
cd ext/%{pecl_name}

%{_bindir}/phpize
%configure \
    --with-imap \
    --with-imap-ssl \
    --with-kerberos \
    --with-libdir=%{_lib} \
    --with-php-config=%{_bindir}/php-config

make %{?_smp_mflags}


%install
# Install the NTS stuff
make -C ext/%{pecl_name} install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}


%check
cd ext/%{pecl_name}

# can load the module
%{_bindir}/php -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -m | grep %{pecl_name}

# reported version from reflection
%{_bindir}/php -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --re %{pecl_name} | grep %{version}


%files
%license LICENSE
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so


%changelog
* Wed Aug 28 2019 Remi Collet <remi@remirepo.net> - 7.1.30-1
- rebase to 7.1.30

* Sat Dec  8 2018 Remi Collet <remi@remirepo.net> - 7.1.8-2
- Fix null pointer dereference in imap_mail CVE-2018-19935
- Fix imap_open allows to run arbitrary shell commands via
  mailbox parameter CVE-2018-19158

* Thu Aug 10 2017 Remi Collet <remi@remirepo.net> - 7.1.8-1
- update to 7.1.8 for sclo-php71

* Tue Mar  7 2017 Remi Collet <remi@remirepo.net> - 7.0.14-2
- add compatibility virtual provides

* Tue Mar  7 2017 Remi Collet <remi@remirepo.net> - 7.0.14-1
- initial package
- version 7.0.14 for security bugs fixed since 7.0.10

