#
# Conditional build:
# _with_pgsql - enable postgresql support (by default use mysql)
#
%define	_beta	beta8
Summary:	zabbix
Summary(pl):	zabbix
Name:		zabbix
Version:	1.0
Release:	0.%{_beta}.0.1
License:	GPL v2+
Group:		Networking/Admin
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}%{_beta}.tar.gz
Source1:	%{name}-agent.inetd
Source2:	%{name}-trapper.inetd
URL:		http://zabbix.sourceforge.net/
%{!?_with_pgsql:BuildRequires:   mysql-devel}
%{?_with_pgsql:BuildRequires:   postgresql-devel}
BuildRequires:	ucd-snmp-devel
BuildRequires:	openssl-devel >= 0.9.6j
#PreReq:	-
#Requires	-
#Requires(pre,post):	-
#Requires(preun):	-
#Requires(postun):	-
#Provides:	-
#Obsoletes:	-
#Conflicts:	-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_sysconfdir	/etc/%{name}

%description
none yet

%package frontend-php
Summary:	PHP frontend for zabbix
Group:		Networking/Admin
Requires:	apache
Requires:	php

%description frontend-php
blah

%package agent-inetd
Summary:	inetd agent for zabbix
Group:		Networking/Admin
Requires:	%{name}
Requires:	inetdaemon
Obsoletes:	%{name}-agent-standalone

%description agent-inetd
blah

%package agent-standalone
Summary:	standalone agent for zabbix
Group:		Networking/Admin
Requires:	%{name}
Obsoletes:	%{name}-agent-inetd

%description agent-standalone
blah

%package suckerd
Summary:	sucker daemon for zabbix
Group:		Networking/Admin
Requires:	%{name}
%{!?_with_pgsql:Requires:   mysql}
%{?_with_pgsql:Requires:   postgresql}

%description suckerd
blah

%package trapper-inetd
Summary:	inetd trapper for zabbix
Group:		Networking/Admin
Requires:	%{name}
Requires:	inetdaemon
Obsoletes:	%{name}-trapper-standalone

%description trapper-inetd
blah

%package trapper-standalone
Summary:	standalone trapper for zabbix
Group:		Networking/Admin
Requires:	%{name}
Obsoletes:	%{name}-trapper-inetd

%description trapper-standalone
blah

%package sender
Summary:	zabbix's sender
Group:		Networking/Admin

%description sender
blah

%prep
%setup -q -n %{name}-%{version}%{_beta}

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%configure \
	%{!?_with_pgsql:--with-mysql} \
	%{?_with_pgsql:--with-pgsql}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/sysconfig/rc-inetd,%{_sbindir},/home/services/html/zabbix}

install bin/zabbix_* $RPM_BUILD_ROOT%{_sbindir}
install misc/conf/* $RPM_BUILD_ROOT%{_sysconfdir}
cp -r frontends/php/* $RPM_BUILD_ROOT/home/services/html/zabbix

install %SOURCE1 $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/zabbix-agent
install %SOURCE2 $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/zabbix-trapper

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -z "`/usr/bin/getgid zabbix`" ]; then
	/usr/sbin/groupadd zabbix
fi
if [ -z "`/bin/id -u zabbix 2>/dev/null`" ]; then
	/usr/sbin/useradd -d / -g zabbix -c "Zabbix User" -s /bin/false zabbix
fi

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/userdel zabbix
	/usr/sbin/groupdel zabbix
fi

%post agent-inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun agent-inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%post trapper-inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun trapper-inetd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc doc/manual.pdf AUTHORS ChangeLog FAQ TODO create bin/ZabbixW32.exe
%attr(750,root,zabbix) %dir %{_sysconfdir}

%files frontend-php
%defattr(644,root,root,755)
/home/services/html/zabbix

%files agent-inetd
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agent.conf
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/sysconfig/rc-inetd/zabbix-agent
%attr(755,root,root) %{_sbindir}/zabbix_agent

%files agent-standalone
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agentd.conf
%attr(755,root,root) %{_sbindir}/zabbix_agentd

%files suckerd
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_suckerd.conf
%attr(755,root,root) %{_sbindir}/zabbix_suckerd

%files trapper-inetd
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_trapper.conf
%attr(640,root,root) %config(noreplace) %verify(not mtime md5 size) /etc/sysconfig/rc-inetd/zabbix-trapper
%attr(755,root,root) %{_sbindir}/zabbix_trapper

%files trapper-standalone
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_trapperd.conf
%attr(755,root,root) %{_sbindir}/zabbix_trapperd

%files sender
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/zabbix_sender
