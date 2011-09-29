# TODO
# - initscript for zabbix-agent-standalone and zabbix-server
#
# Conditional build:
%bcond_with	pgsql 	# enable PostgreSQL support (by default use mysql)
%bcond_with	oracle 	# enable Oracle support (by default use mysql)

Summary:	zabbix - network monitoring software
Summary(pl.UTF-8):	zabbix - oprogramowanie do monitorowania sieci
Name:		zabbix
Version:	1.8.8
Release:	0.1
License:	GPL v2+
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/zabbix/%{name}-%{version}.tar.gz
# Source0-md5:	8e38079640cf50c215f36dfd3125a6d3
Source1:	%{name}-agent.inetd
Source2:	%{name}-apache.conf
URL:		http://zabbix.sourceforge.net/
%{!?with_pgsql:BuildRequires:	mysql-devel}
BuildRequires:	curl-devel
BuildRequires:	iksemel-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openldap-devel >= 2.4.6
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
%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}

# FIXME
%define filterout_ld -Wl,--as-needed

%description
zabbix is software that monitors numerous parameters of a network and
the servers on that network. It is a useful tool for monitoring
the health and integrity of servers. zabbix uses a flexible
notification mechanism that allows users to configure email based
alerts for virtually any event. All monitored parameters are stored in
a database. zabbix offers excellent reporting and data visualisation
features based on the stored data. zabbix supports both polling and
trapping. All zabbix reports and statistics, as well as configuration
parameters, are accessed through a web-based front end.

%description -l pl.UTF-8
zabbix to oprogramowanie do monitorowania licznych parametrów sieci i
serwerów sieciowych. Jest przydatny przy monitorowaniu działania
serwerów. Jorzysta z elastycznego mechanizmu powiadamiania, który
pozwala użytkownikom konfigurować powiadamianie pocztą elektroniczną
dla praktycznie wszelkich zdarzeń. Monitorowane parametry są
przechowywane w bazie danych. W oparciu o przechowywane dane zabbix
oferuje świetne raportowanie i funkcje wizualizacji. Wspiera zarówno
odpytywanie jak i pułapkowanie. Dostęp do wszystkich raportów i
statystyk zabbiksa jest możliwy poprzez interfejs oparty o WWW.

%package agent-inetd
Summary:	inetd agent for zabbix
Summary(pl.UTF-8):	Wersja inetd agenta zabbiksa
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}
Requires:	inetdaemon
Obsoletes:	zabbix-agent-standalone

%description agent-inetd
This package provides inetd version of zabbix agent.

%description agent-inetd -l pl.UTF-8
Ten pakiet dostarcza agenta zabbiksa dla inetd.

%package agent-standalone
Summary:	Standalone agent for zabbix
Summary(pl.UTF-8):	Wersja wolnostojąca agenta zabbiksa
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}
Obsoletes:	zabbix-agent-inetd

%description agent-standalone
This package provides standalone (recommended) version of zabbix agent.

%description agent-standalone -l pl.UTF-8
Ten pakiet dostarcza wolnostojącej (zalecanej) wersji agenta zabbiksa.

%package frontend-php
Summary:	PHP frontend for zabbix
Summary(pl.UTF-8):	Interfejs PHP dla zabbiksa
Group:		Applications/WWW
Requires:	php(gd)
Requires:	php-bcmath
Requires:	php-ctype
Requires:	php-mbstring
Requires:	php-pcre
Requires:	php-sockets
Requires:	php-session
%{!?with_pgsql:Requires:	php-mysql}
%{?with_pgsql:Requires:	php-pgsql}
Requires:	webapps
Requires:	webserver = apache
Requires:	webserver(php)

%description frontend-php
This package provides web based (PHP) frontend for zabbix.

%description frontend-php -l pl.UTF-8
Ten pakiet dostarcza napisany w PHP frontend dla zabbiksa.

%package get
Summary:	Program retrieving data from zabbix agent
Summary(pl.UTF-8):	Program odpytujÄcy agenta zabbiksa
Group:		Networking/Utilities

%description get
This package provides a program retrieving data from zabbix agent.

%description get -l pl.UTF-8
Ten pakiet zawiera program odpytujÄcy agenta zabbiksa.

%package sender
Summary:	Zabbix sender
Summary(pl.UTF-8):	Program zawiadamiający zabbiksa
Group:		Networking/Utilities

%description sender
This package provides the zabbix sender.

%description sender -l pl.UTF-8
Ten pakiet zawiera program zawiadamiający zabbiksa.

%package server
Summary:	Zabbix server
Summary(pl.UTF-8):	Serwer zabbiksa
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{name}-suckerd
Obsoletes:	%{name}-trapper-inetd
Obsoletes:	%{name}-trapper-standalone

%description server
This package provides the zabbix server.

%description server -l pl.UTF-8
Ten pakiet zawiera serwer zabbiksa.

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
	--with-ldap \
	--with-jabber \
	--with-libcurl
#	--with-ucd-snmp=DIR \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{sysconfig/rc-inetd,webapps/%{_webapp}},%{_appdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install misc/conf/zabbix_{a*,s*}.conf $RPM_BUILD_ROOT%{_sysconfdir}
cp -r frontends $RPM_BUILD_ROOT%{_appdir}
#mv -f $RPM_BUILD_ROOT%{_appdir}/frontends/php/include/db.inc.php $RPM_BUILD_ROOT%{_webapps}/%{_webapp}
#ln -s %{_webapps}/%{_webapp}/db.inc.php $RPM_BUILD_ROOT%{_appdir}/frontends/php/include
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/zabbix-agent
install %{SOURCE2} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin frontend-php -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun frontend-php -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin frontend-php -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun frontend-php -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%pre
%groupadd -g 111 zabbix
%useradd -d / -u 111 -g zabbix -c "Zabbix User" -s /bin/false zabbix

%post server
if [ "$1" = 1 ]; then
	%banner -e %{name} <<-EOF
	You should create database for Zabbix.
	Running these should be fine in most cases:
%if %{with pgsql}
	psql -c 'create database zabbix'
	zcat %{_docdir}/%{name}-%{version}/create/postgresql/schema.sql.gz | psql zabbix
	zcat %{_docdir}/%{name}-%{version}/create/data/data.sql.gz | psql zabbix
	zcat %{_docdir}/%{name}-%{version}/create/data/images_pgsql.sql.gz | psql zabbix
%else
	mysqladmin create zabbix
	zcat %{_docdir}/%{name}-%{version}/create/mysql/schema.sql.gz | mysql zabbix
	zcat %{_docdir}/%{name}-%{version}/create/data/data.sql.gz | mysql zabbix
	zcat %{_docdir}/%{name}-%{version}/create/data/images.sql.gz | mysql zabbix
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

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README ChangeLog
%attr(750,root,zabbix) %dir %{_sysconfdir}
%dir %{_appdir}
%dir %{_appdir}/frontends

%files agent-inetd
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agent.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/zabbix-agent
%attr(755,root,root) %{_sbindir}/zabbix_agent

%files agent-standalone
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agentd.conf
%attr(755,root,root) %{_sbindir}/zabbix_agentd
%{_mandir}/man8/zabbix_agentd*

%files frontend-php
%defattr(644,root,root,755)
%attr(750,root,http) %dir %{_webapps}/%{_webapp}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/*
%{_appdir}/frontends/php

%files get
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_get
%{_mandir}/man1/zabbix_get*

%files sender
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_sender*

%files server
%defattr(644,root,root,755)
%doc create upgrades
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_server.conf
%attr(755,root,root) %{_sbindir}/zabbix_server
%{_mandir}/man8/zabbix_server*
