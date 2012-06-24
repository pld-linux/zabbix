#
# Conditional build:
%bcond_with pgsql 	# enable postgresql support (by default use mysql)
#
%define	_beta	beta14
Summary:	zabbix - network monitoring software
Summary(pl):	zabbix - oprogramowanie do monitorowania sieci
Name:		zabbix
Version:	1.0
Release:	0.%{_beta}.1
License:	GPL v2+
Group:		Networking/Admin
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}%{_beta}.tar.gz
# Source0-md5:	0ac320c6cd99f801d8cb7923ca790419
Source1:	%{name}-agent.inetd
Source2:	%{name}-trapper.inetd
URL:		http://zabbix.sourceforge.net/
%{!?with_pgsql:BuildRequires:	mysql-devel}
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	ucd-snmp-devel
BuildRequires:	openssl-devel >= 0.9.6k
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		htmldir		/home/httpd/html/zabbix

%description
zabbix is software that monitors numerous parameters of a network and
the servers on that network. zabbix is a useful tool for monitoring
the health and integrity of servers. zabbix uses a flexible
notification mechanism that allows users to configure email based
alerts for virtually any event. All monitored parameters are stored in
a database. zabbix offers excellent reporting and data visualisation
features based on the stored data. zabbix supports both polling and
trapping. All zabbix reports and statistics, as well as configuration
parameters, are accessed through a web-based front end.

%description -l pl
zabbix to oprogramowanie do monitorowania licznych parametr�w sieci i
serwer�w sieciowych. zabbix jest przydatny przy monitorowaniu
dzia�ania serwer�w. zabbix korzysta z elastycznego mechanizmu
powiadamiania, kt�ry pozwala u�ytkownikom konfigurowa� powiadamianie
poczt� elektroniczn� dla praktycznie wszelkich zdarze�. Monitorowane
parametry s� przechowywane w bazie danych. zabbix oferuje, w oparciu o
przechowywane dane, �wietne raportowanie i funkcje wizualizacji.
zabbix wspiera zar�wno odpytywanie, jak i pu�apkowanie. Dost�p do
wszystkich raport�w i statystyk zabbiksa jest mo�liwy poprzez
interfejs oparty o WWW.

%package frontend-php
Summary:	PHP frontend for zabbix
Summary(pl):	Interfejs PHP dla zabbiksa
Group:		Networking/Admin
Requires:	apache
Requires:	php
%{!?with_pgsql:Requires:	php-mysql}
%{?with_pgsql:Requires:	php-pgsql}

%description frontend-php
This package provides web based (PHP) frontend for zabbix.

%description frontend-php -l pl
Ten pakiet dostarcza napisany w PHP frontend dla zabbiksa.

%package agent-inetd
Summary:	inetd agent for zabbix
Summary(pl):	Wersja inetd agenta zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}
Requires:	inetdaemon
Obsoletes:	%{name}-agent-standalone

%description agent-inetd
This package provides inetd version of zabbix agent.

%description agent-inetd -l pl
Ten pakiet dostarcza agenta zabbiksa dla inetd.

%package agent-standalone
Summary:	Standalone agent for zabbix
Summary(pl):	Wersja wolnostoj�ca agenta zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}
Obsoletes:	%{name}-agent-inetd

%description agent-standalone
This package provides standalone version of zabbix agent.

%description agent-standalone -l pl
Ten pakiet dostarcza wolnostoj�cej wersji agenta zabbiksa.

%package suckerd
Summary:	sucker daemon for zabbix
Summary(pl):	Demon sucker dla zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}
%{!?with_pgsql:Requires:	mysql}
%{?with_pgsql:Requires:	postgresql}

%description suckerd
This package provides the sucker daemon for zabbix.

%description suckerd -l pl
Ten pakiet zawiera demona sucker dla zabbiksa.

%package trapper-inetd
Summary:	inetd trapper for zabbix
Summary(pl):	Wersja inetd programu pu�apkuj�cego zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}
Requires:	inetdaemon
Obsoletes:	%{name}-trapper-standalone

%description trapper-inetd
This package provides inetd version of zabbix trapper.

%description trapper-inetd -l pl
Ten pakiet zawiera program pu�apkuj�cy zabbiksa dla inetd.

%package trapper-standalone
Summary:	Standalone trapper for zabbix
Summary(pl):	Wersja wolnostoj�ca programu pu�apkuj�cego zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}
Obsoletes:	%{name}-trapper-inetd

%description trapper-standalone
This package provides standalone version of zabbix trapper.

%description trapper-standalone -l pl
Ten pakiet zawiera wolnostoj�c� wersj� programu pu�apkuj�cego
zabbiksa.

%package sender
Summary:	zabbix's sender
Summary(pl):	Program zawiadamiaj�cy zabbiksa
Group:		Networking/Admin

%description sender
This package provides the zabbix sender.

%description sender -l pl
Ten pakiet zawiera program zawiadamiaj�cy zabbiksa.

%prep
%setup -q -n %{name}-%{version}%{_beta}

%build
%configure \
	%{!?with_pgsql:--with-mysql} \
	%{?with_pgsql:--with-pgsql} \
	--with-ucd-snmp

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/sysconfig/rc-inetd,%{_sbindir},%{htmldir}}

install bin/zabbix_* $RPM_BUILD_ROOT%{_sbindir}
install misc/conf/* $RPM_BUILD_ROOT%{_sysconfdir}
cp -r frontends/php/* $RPM_BUILD_ROOT%{htmldir}

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
%doc doc/Zabbix\ Manual.pdf AUTHORS ChangeLog FAQ TODO create bin/ZabbixW32.exe
%attr(750,root,zabbix) %dir %{_sysconfdir}

%files frontend-php
%defattr(644,root,root,755)
%{htmldir}

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
