# TODO
# - initscript for zabbix-agent-standalone
# - missing zabbix_agentd.conf, zabbix_trapperd.conf
#   see http://www.zabbix.com/manual_install_server.php
#
# Conditional build:
%bcond_with	pgsql 	# enable PostgreSQL support (by default use mysql)
%bcond_with	oracle 	# enable Oracle support (by default use mysql)

#
Summary:	zabbix - network monitoring software
Summary(pl.UTF-8):   zabbix - oprogramowanie do monitorowania sieci
Name:		zabbix
Version:	1.1
Release:	0.1
License:	GPL v2+
Group:		Networking/Admin
Source0:	http://dl.sourceforge.net/zabbix/%{name}-%{version}.tar.gz
# Source0-md5:	9697e5634547d9614963db04f6cd87d7
Source1:	%{name}-agent.inetd
Source2:	%{name}-trapper.inetd
URL:		http://zabbix.sourceforge.net/
%{!?with_pgsql:BuildRequires:	mysql-devel}
BuildRequires:	net-snmp-devel
BuildRequires:	openssl-devel >= 0.9.7d
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(zabbix)
Provides:	user(zabbix)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		htmldir		/home/services/httpd/html/%{name}

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

%description -l pl.UTF-8
zabbix to oprogramowanie do monitorowania licznych parametrów sieci i
serwerów sieciowych. zabbix jest przydatny przy monitorowaniu
działania serwerów. zabbix korzysta z elastycznego mechanizmu
powiadamiania, który pozwala użytkownikom konfigurować powiadamianie
pocztą elektroniczną dla praktycznie wszelkich zdarzeń. Monitorowane
parametry są przechowywane w bazie danych. zabbix oferuje, w oparciu o
przechowywane dane, świetne raportowanie i funkcje wizualizacji.
zabbix wspiera zarówno odpytywanie, jak i pułapkowanie. Dostęp do
wszystkich raportów i statystyk zabbiksa jest możliwy poprzez
interfejs oparty o WWW.

%package frontend-php
Summary:	PHP frontend for zabbix
Summary(pl.UTF-8):   Interfejs PHP dla zabbiksa
Group:		Networking/Admin
Requires:	php(gd)
%{!?with_pgsql:Requires:	php-mysql}
%{?with_pgsql:Requires:	php-pgsql}
Requires:	webserver = apache
Requires:	webserver(php)

%description frontend-php
This package provides web based (PHP) frontend for zabbix.

%description frontend-php -l pl.UTF-8
Ten pakiet dostarcza napisany w PHP frontend dla zabbiksa.

%package agent-inetd
Summary:	inetd agent for zabbix
Summary(pl.UTF-8):   Wersja inetd agenta zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}-%{release}
Requires:	inetdaemon
Obsoletes:	zabbix-agent-standalone

%description agent-inetd
This package provides inetd version of zabbix agent.

%description agent-inetd -l pl.UTF-8
Ten pakiet dostarcza agenta zabbiksa dla inetd.

%package agent-standalone
Summary:	Standalone agent for zabbix
Summary(pl.UTF-8):   Wersja wolnostojąca agenta zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}-%{release}
Obsoletes:	zabbix-agent-inetd

%description agent-standalone
This package provides standalone version of zabbix agent.

%description agent-standalone -l pl.UTF-8
Ten pakiet dostarcza wolnostojącej wersji agenta zabbiksa.

%package suckerd
Summary:	sucker daemon for zabbix
Summary(pl.UTF-8):   Demon sucker dla zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}-%{release}
%{!?with_pgsql:Requires:	mysql}
%{?with_pgsql:Requires:	postgresql}

%description suckerd
This package provides the sucker daemon for zabbix.

%description suckerd -l pl.UTF-8
Ten pakiet zawiera demona sucker dla zabbiksa.

%package trapper-inetd
Summary:	inetd trapper for zabbix
Summary(pl.UTF-8):   Wersja inetd programu pułapkującego zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}-%{release}
Requires:	inetdaemon
Obsoletes:	zabbix-trapper-standalone

%description trapper-inetd
This package provides inetd version of zabbix trapper.

%description trapper-inetd -l pl.UTF-8
Ten pakiet zawiera program pułapkujący zabbiksa dla inetd.

%package trapper-standalone
Summary:	Standalone trapper for zabbix
Summary(pl.UTF-8):   Wersja wolnostojąca programu pułapkującego zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}-%{release}
Obsoletes:	zabbix-trapper-inetd

%description trapper-standalone
This package provides standalone version of zabbix trapper.

%description trapper-standalone -l pl.UTF-8
Ten pakiet zawiera wolnostojącą wersję programu pułapkującego
zabbiksa.

%package sender
Summary:	zabbix's sender
Summary(pl.UTF-8):   Program zawiadamiający zabbiksa
Group:		Networking/Admin

%description sender
This package provides the zabbix sender.

%description sender -l pl.UTF-8
Ten pakiet zawiera program zawiadamiający zabbiksa.

%prep
%setup -q

%build
%configure \
	%{!?with_pgsql:--with-mysql} \
	%{?with_pgsql:--with-pgsql} \
	%{?with_oracle:--with-oracle} \
	--enable-server \
	--enable-agent \
	--with-net-snmp \
#	--with-ldap=DIR \
#	--with-ucd-snmp=DIR \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

#install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/sysconfig/rc-inetd,%{_sbindir},%{htmldir}}
#install bin/zabbix_* $RPM_BUILD_ROOT%{_sbindir}
#install misc/conf/* $RPM_BUILD_ROOT%{_sysconfdir}
#cp -r frontends/php/* $RPM_BUILD_ROOT%{htmldir}
#install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/zabbix-agent
#install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/zabbix-trapper

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 111 zabbix
%useradd -d / -u 111 -g zabbix -c "Zabbix User" -s /bin/false zabbix

%post
if [ "$1" = 1 ]; then
	%banner -e %{name} <<-EOF
	You should create database for Zabbix.
	Running these should be fine in most cases:
%if %{with pgsql}
	psql -c 'create database zabbix'
	zcat %{_docdir}/%{name}-%{version}/create/pgsql/schema.sql.gz | psql zabbix
	zcat %{_docdir}/%{name}-%{version}/create/data/data.sql.gz | psql zabbix
%else
	mysqladmin create zabbix
	zcat %{_docdir}/%{name}-%{version}/create/mysql/schema.sql.gz | mysql zabbix
	zcat %{_docdir}/%{name}-%{version}/create/data/data.sql.gz | mysql zabbix
%endif
	%{?TODO:You also need zabbix-agent. install zabbix-agent-standalone %or zabbix-agent-inetd.}
EOF
fi

%postun
if [ "$1" = "0" ]; then
	%userremove zabbix
	%groupremove zabbix
fi

%post agent-inetd
%service -q rc-inetd reload

%postun agent-inetd
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%post trapper-inetd
%service -q rc-inetd reload

%postun trapper-inetd
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc doc/Zabbix\ Manual.pdf AUTHORS NEWS README ChangeLog create upgrades bin/ZabbixW32.exe
%attr(750,root,zabbix) %dir %{_sysconfdir}

%files frontend-php
%defattr(644,root,root,755)
%dir %{htmldir}
%{htmldir}/*.php
%{htmldir}/*.css
%{htmldir}/audio
%{htmldir}/images

%dir %{htmldir}/include
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{htmldir}/include/db.inc.php
%{htmldir}/include/.htaccess
%{htmldir}/include/classes.inc.php
%{htmldir}/include/config.inc.php
%{htmldir}/include/defines.inc.php

%files agent-inetd
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agent.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/zabbix-agent
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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/zabbix-trapper
%attr(755,root,root) %{_sbindir}/zabbix_trapper

%files trapper-standalone
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_trapperd.conf
%attr(755,root,root) %{_sbindir}/zabbix_trapperd

%files sender
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/zabbix_sender
