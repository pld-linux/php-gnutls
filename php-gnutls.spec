%define		_modname	gnutls
Summary:	GnuTLS PHP Module
Name:		php-%{_modname}
Version:	0.3
%define	_pre	rc1
Release:	0.%{_pre}.1
License:	GPL
Group:		Development/Languages/PHP
Source0:	http://files.openvcp.org/modphp-%{_modname}-%{version}-%{_pre}.tar.gz
# Source0-md5:	2a52affb9b2a5271558ffc2baaf9aa56
URL:		http://www.openvcp.org/
BuildRequires:	autoconf
BuildRequires:	gnutls-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GnuTLS PHP Module.

%prep
%setup -q -n modphp-%{_modname}-%{version}-%{_pre}

%build
%{__autoconf}
%configure \
	--with-phpsrc=/usr/include/php

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_extensiondir},%{php_sysconfdir}/conf.d}

install %{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
