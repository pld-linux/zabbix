# TODO
# - systemd units for zabbix-agentd, zabbix-server and zabbix-java
# - initscript for zabbix-agentd, zabbix-server and zabbix-java
#
# Conditional build:
%bcond_with	pgsql 	# enable PostgreSQL support
%bcond_with	oracle 	# enable Oracle support
%bcond_with	sqlite3	# enable sqlite3 support
%bcond_without	mysql	# enable MySQL support

%bcond_without	java	# disable java support

%if %{with pgsql} || %{with oracle} || %{with sqlite3}
%undefine with_mysql
%endif

%if %{?with_pgsql:1}%{?with_oracle:1}%{?with_sqlite3:1}%{?with_mysql:1} != 1
ERROR: exactly one database must be selected
%endif

%define         php_min_version 5.4.0

Summary:	zabbix - network monitoring software
Summary(pl.UTF-8):	zabbix - oprogramowanie do monitorowania sieci
Name:		zabbix
Version:	3.2.0
Release:	0.1
License:	GPL v2+
Group:		Networking/Utilities
Source0:	http://dl.sourceforge.net/zabbix/%{name}-%{version}.tar.gz
# Source0-md5:	e2491b482868059f251902d5f636eacb
Source1:	%{name}-apache.conf
URL:		http://zabbix.sourceforge.net/
BuildRequires:	OpenIPMI-devel
BuildRequires:	curl-devel
BuildRequires:	iksemel-devel
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libxml2-devel
BuildRequires:	libssh2-devel
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	net-snmp-devel
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	openssl-devel >= 0.9.7d
%{?with_pgsql:BuildRequires:	postgresql-devel}
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
BuildRequires:	unixODBC-devel
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

%package agentd
Summary:	Standalone agent for zabbix
Summary(pl.UTF-8):	Wersja wolnostojąca agenta zabbiksa
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}
Obsoletes:	zabbix-agent-inetd
Obsoletes:	zabbix-agent-standalone

%description agentd
This package provides the zabbix agent.

%description agentd -l pl.UTF-8
Ten pakiet dostarcza agenta zabbiksa.

%package frontend-php
Summary:	PHP frontend for zabbix
Summary(pl.UTF-8):	Interfejs PHP dla zabbiksa
Group:		Applications/WWW
Requires:	php(bcmath)
Requires:	php(core) >= %{php_min_version}
Requires:	php(ctype)
Requires:	php(gd)
Requires:	php(gettext)
Requires:	php(mbstring)
Requires:	php(pcre)
Requires:	php(session)
Requires:	php(sockets)
Requires:	php(xml)
Requires:	php(xmlreader)
Requires:	php(xmlwriter)
%{?with_mysql:Requires:	php(mysql)}
%{?with_pgsql:Requires:	php(pgsql)}
Requires:	webapps
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

%package proxy
Summary:	Zabbix proxy
Summary(pl.UTF-8):	Proxy do zabbiksa
Group:		Networking/Utilities

%description proxy
This package provides the zabbix proxy.

%description proxy -l pl.UTF-8
Ten pakiet zawiera proxy zabbix.

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

%package java
Summary:	Zabbix Java Gateway
Group:		Networking/Utilities
Requires:	%{name} = %{version}-%{release}

%description java
This package provides the Zabbix Java Gateway.

%prep
%setup -q

%build
%configure \
	%{?with_mysql:--with-mysql} \
	%{?with_pgsql:--with-pgsql} \
	%{?with_oracle:--with-oracle} \
	%{?with_sqlite3:--with-sqlite3} \
	--enable-server \
	--enable-agent \
	--enable-proxy \
	--enable-ipv6 \
	%{__enable_disable java} \
	--with-jabber \
	--with-ldap \
	--with-libcurl \
	--with-libxml2 \
	--with-net-snmp \
	--with-openipmi \
	--with-openssl \
	--with-ssh2 \
	--with-unixodbc

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/webapps/%{_webapp},%{_appdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	ZJG_DEST=$RPM_BUILD_ROOT%{_datadir}/zabbix_java

cp -r frontends $RPM_BUILD_ROOT%{_appdir}
#mv -f $RPM_BUILD_ROOT%{_appdir}/frontends/php/include/db.inc.php $RPM_BUILD_ROOT%{_webapps}/%{_webapp}
#ln -s %{_webapps}/%{_webapp}/db.inc.php $RPM_BUILD_ROOT%{_appdir}/frontends/php/include
install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf

%if %{with java}
mv $RPM_BUILD_ROOT%{_datadir}/zabbix_java/settings.sh $RPM_BUILD_ROOT%{_sysconfdir}/zabbix_java.conf
ln -s %{_sysconfdir}/zabbix_java.conf $RPM_BUILD_ROOT%{_datadir}/zabbix_java/settings.sh

cat >$RPM_BUILD_ROOT%{_sbindir}/zabbix_java-start <<'EOF'
#!/bin/sh

exec %{_datadir}/zabbix_java/startup.sh "$@"
EOF

cat >$RPM_BUILD_ROOT%{_sbindir}/zabbix_java-stop <<'EOF'
#!/bin/sh

exec %{_datadir}/zabbix_java/shutdown.sh "$@"
EOF
%endif

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
	%banner -e %{name}-server <<-EOF
	You should create database for Zabbix.
%if %{with pgsql}
	Running these should be fine in most cases:
	psql -c 'create database zabbix'
	zcat %{_docdir}/%{name}-server-%{version}/postgresql/schema.sql.gz | psql zabbix
	zcat %{_docdir}/%{name}-server-%{version}/postgresql/data.sql.gz | psql zabbix
	zcat %{_docdir}/%{name}-server-%{version}/postgresql/images.sql.gz | psql zabbix
%else
%if %{with mysql}
	Running these should be fine in most cases:
	mysqladmin create zabbix
	zcat %{_docdir}/%{name}-server-%{version}/mysql/schema.sql.gz | mysql zabbix
	zcat %{_docdir}/%{name}-server-%{version}/mysql/images.sql.gz | mysql zabbix
	zcat %{_docdir}/%{name}-server-%{version}/mysql/data.sql.gz | mysql zabbix
%else
	Database template is available in %{_docdir}/%{name}-%{version}
%endif
%endif
	%{?TODO:You also need zabbix-agent. install zabbix-agentd.}
EOF
fi

%postun
if [ "$1" = "0" ]; then
	%userremove zabbix
	%groupremove zabbix
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(750,root,zabbix) %dir %{_sysconfdir}
%dir %{_appdir}
%dir %{_appdir}/frontends

%files agentd
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

%files proxy
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_proxy.conf
%attr(755,root,root) %{_sbindir}/zabbix_proxy
%{_mandir}/man8/zabbix_proxy*

%files sender
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_sender*

%files server
%defattr(644,root,root,755)
%doc upgrades/dbpatches
%if %{with mysql}
%doc database/mysql
%endif
%if %{with postgresql}
%doc database/postgresql
%endif
%if %{with oracle}
%doc database/oracle
%endif
%if %{with sqlite3}
%doc database/sqlite3
%endif
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_server.conf
%attr(755,root,root) %{_sbindir}/zabbix_server
%{_mandir}/man8/zabbix_server*

%if %{with java}
%files java
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/zabbix_java-start
%attr(755,root,root) %{_sbindir}/zabbix_java-stop
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_java.conf
%dir %{_datadir}/zabbix_java
%{_datadir}/zabbix_java/bin
%{_datadir}/zabbix_java/lib
%{_datadir}/zabbix_java/settings.sh
%attr(755,root,root) %{_datadir}/zabbix_java/shutdown.sh
%attr(755,root,root) %{_datadir}/zabbix_java/startup.sh
%endif
