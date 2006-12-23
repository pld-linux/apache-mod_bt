%define		mod_name	bt
%define 	apxs		/usr/sbin/apxs
Summary:	Apache BitTorrent tracker
Summary(pl):	Tracker BitTorrenta w formie modu³u Apache'a
Name:		apache-mod_%{mod_name}
Version:	0.0.4
Release:	0.1
License:	GPL
Group:		Networking/Daemons
#Source0Download: http://www.crackerjack.net/mod_bt/download.html
Source0:	http://www.crackerjack.net/mod_bt/mod_%{mod_name}-%{version}.tgz
# Source0-md5:	dfb1f1a1aaae3313d8e1056a3d317740
Patch0:		%{name}-paths.patch
URL:		http://www.crackerjack.net/mod_bt/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	db-devel >= 4.2.52
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
Apache-based BitTorrent Tracker.

%description -l pl
Oparty na Apache'u tracker BitTorrenta.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
