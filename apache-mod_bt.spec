%define		mod_name	bt
%define 	apxs		/usr/sbin/apxs
Summary:	Apache BitTorrent tracker
Name:		apache-mod_%{mod_name}
Version:	0.0.4
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0: http://www.crackerjack.net/mod_%{mod_name}/mod_%{mod_name}-0.0.4.tgz
# Source0-md5:	dfb1f1a1aaae3313d8e1056a3d317740
Patch0:	%{name}-paths.patch
URL:		http://www.crackerjack.net/mod_bt/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	db-devel >= 4.2.52
Requires(post,preun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
Apache-based BitTorrent Tracker

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_pkglibdir}/*
