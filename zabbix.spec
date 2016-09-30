# TODO:
# - initscript for zabbix-agentd, zabbix-server, zabbix-proxy and zabbix-java
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

%define		php_min_version 5.4.0
Summary:	Zabbix - network monitoring software
Summary(pl.UTF-8):	Zabbix - oprogramowanie do monitorowania sieci
Name:		zabbix
Version:	3.2.0
Release:	0.2
License:	GPL v2+
Group:		Networking/Utilities
Source0:	http://downloads.sourceforge.net/zabbix/%{name}-%{version}.tar.gz
# Source0-md5:	e2491b482868059f251902d5f636eacb
Source1:	%{name}-apache.conf
Source2:	%{name}_server.service
Source3:	%{name}_agentd.service
Source4:	%{name}_proxy.service
Source5:	%{name}_java.service
Source6:	%{name}.tmpfiles
Patch0:		config.patch
URL:		http://zabbix.sourceforge.net/
BuildRequires:	OpenIPMI-devel
BuildRequires:	curl-devel
BuildRequires:	iksemel-devel
%{?with_java:BuildRequires:	jdk}
BuildRequires:	libssh2-devel
BuildRequires:	libxml2-devel
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	net-snmp-devel
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	openssl-devel >= 0.9.7d
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.671
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
BuildRequires:	unixODBC-devel
Requires:	%{name}-agentd = %{version}-%{release}
Requires:	%{name}-frontend-php = %{version}-%{release}
Requires:	%{name}-server = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}

%description
Zabbix is software that monitors numerous parameters of a network and
the servers on that network. It is a useful tool for monitoring the
health and integrity of servers. Zabbix uses a flexible notification
mechanism that allows users to configure email based alerts for
virtually any event. All monitored parameters are stored in a
database. Zabbix offers excellent reporting and data visualisation
features based on the stored data. Zabbix supports both polling and
trapping. All Zabbix reports and statistics, as well as configuration
parameters, are accessed through a web-based front end.

%description -l pl.UTF-8
Zabbix to oprogramowanie do monitorowania licznych parametrów sieci i
serwerów sieciowych. Jest przydatny przy monitorowaniu działania
serwerów. Jorzysta z elastycznego mechanizmu powiadamiania, który
pozwala użytkownikom konfigurować powiadamianie pocztą elektroniczną
dla praktycznie wszelkich zdarzeń. Monitorowane parametry są
przechowywane w bazie danych. W oparciu o przechowywane dane Zabbix
oferuje świetne raportowanie i funkcje wizualizacji. Wspiera zarówno
odpytywanie jak i pułapkowanie. Dostęp do wszystkich raportów i
statystyk Zabbiksa jest możliwy poprzez interfejs oparty o WWW.

%package common
Summary:	Common files for Zabbix monitoring software
Summary(pl.UTF-8):	Wspólne pliki dla oprogramowania monitorującego Zabbix
Group:		Networking/Utilities
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(zabbix)
Provides:	user(zabbix)

%description common
Common files for Zabbix monitoring software.

%description common -l pl.UTF-8
Wspólne pliki dla oprogramowania monitorującego Zabbix.

%package agentd
Summary:	Zabbix Agent
Summary(pl.UTF-8):	Agenta Zabbiksa
Group:		Networking/Utilities
Requires:	%{name}-common = %{version}-%{release}
Requires:	systemd-units >= 38
Obsoletes:	zabbix-agent-inetd
Obsoletes:	zabbix-agent-standalone

%description agentd
Zabbix agent collects data from the local system for a Zabbix server.

%description agentd -l pl.UTF-8
Agent zbiera dane z lokalnej maszyny dla serwera Zabbix.

%package frontend-php
Summary:	PHP frontend for Zabbix
Summary(pl.UTF-8):	Interfejs PHP dla Zabbiksa
Group:		Applications/WWW
Requires:	php(bcmath)
Requires:	php(core) >= %{php_min_version}
Requires:	php(ctype)
Requires:	php(gd)
Requires:	php(gettext)
Requires:	php(json)
Requires:	php(mbstring)
%{?with_mysql:Requires: php(mysql)}
Requires:	php(pcre)
%{?with_pgsql:Requires: php(pgsql)}
Requires:	php(session)
Requires:	php(sockets)
Requires:	php(xml)
Requires:	php(xmlreader)
Requires:	php(xmlwriter)
Requires:	webapps
Requires:	webserver(php)

%description frontend-php
This package provides web based (PHP) frontend for Zabbix.

%description frontend-php -l pl.UTF-8
Ten pakiet dostarcza napisany w PHP frontend dla Zabbiksa.

%package get
Summary:	Program retrieving data from Zabbix agent
Summary(pl.UTF-8):	Program odpytujÄcy agenta Zabbiksa
Group:		Networking/Utilities

%description get
This package provides a program retrieving data from Zabbix agent.

%description get -l pl.UTF-8
Ten pakiet zawiera program odpytujÄcy agenta Zabbiksa.

%package proxy
Summary:	Zabbix proxy
Summary(pl.UTF-8):	Proxy do Zabbiksa
Group:		Networking/Utilities
Requires:	%{name}-common = %{version}-%{release}
Requires:	systemd-units >= 38

%description proxy
This package provides the Zabbix proxy.

%description proxy -l pl.UTF-8
Ten pakiet zawiera proxy Zabbix.

%package sender
Summary:	Zabbix sender
Summary(pl.UTF-8):	Program zawiadamiający Zabbiksa
Group:		Networking/Utilities

%description sender
This package provides the Zabbix sender.

%description sender -l pl.UTF-8
Ten pakiet zawiera program zawiadamiający Zabbiksa.

%package server
Summary:	Zabbix server
Summary(pl.UTF-8):	Serwer Zabbiksa
Group:		Networking/Utilities
Requires:	%{name}-common = %{version}-%{release}
Requires:	systemd-units >= 38
Obsoletes:	zabbix-suckerd
Obsoletes:	zabbix-trapper-inetd
Obsoletes:	zabbix-trapper-standalone

%description server
This package provides the Zabbix server.

%description server -l pl.UTF-8
Ten pakiet zawiera serwer Zabbiksa.

%package java
Summary:	Zabbix Java Gateway
Group:		Networking/Utilities
Requires:	%{name}-common = %{version}-%{release}
Requires:	systemd-units >= 38

%description java
This package provides the Zabbix Java Gateway.

%prep
%setup -q

%patch0 -p1

%build
%configure \
	%{?with_mysql:--with-mysql} \
	%{?with_pgsql:--with-postgresql} \
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
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/webapps/%{_webapp},%{_appdir}} \
	$RPM_BUILD_ROOT{/run/zabbix,/var/log/zabbix,%{systemdunitdir},%{tmpfilesdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	ZJG_DEST=$RPM_BUILD_ROOT%{_datadir}/zabbix_java

cp -r frontends $RPM_BUILD_ROOT%{_appdir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf

install	%{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_server.service
install	%{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_agentd.service
install	%{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_proxy.service
install	%{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_java.service

cp -p %{SOURCE6} $RPM_BUILD_ROOT%{tmpfilesdir}/zabbix.conf

mv $RPM_BUILD_ROOT%{_appdir}/frontends/php/conf $RPM_BUILD_ROOT%{_sysconfdir}/frontend
ln -s %{_sysconfdir}/frontend $RPM_BUILD_ROOT%{_appdir}/frontends/php/conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/frontend/zabbix.conf.php

%if %{with java}
mv $RPM_BUILD_ROOT%{_datadir}/zabbix_java/settings.sh $RPM_BUILD_ROOT%{_sysconfdir}/zabbix_java.conf
ln -s %{_sysconfdir}/zabbix_java.conf $RPM_BUILD_ROOT%{_datadir}/zabbix_java/settings.sh
mv $RPM_BUILD_ROOT%{_datadir}/zabbix_java/lib/logback.xml $RPM_BUILD_ROOT%{_sysconfdir}/java-logback.xml
ln -s %{_sysconfdir}/java-logback.xml $RPM_BUILD_ROOT%{_datadir}/zabbix_java/lib/logback.xml
mv $RPM_BUILD_ROOT%{_datadir}/zabbix_java/lib/logback-console.xml $RPM_BUILD_ROOT%{_sysconfdir}/java-logback-console.xml
ln -s %{_sysconfdir}/java-logback-console.xml $RPM_BUILD_ROOT%{_datadir}/zabbix_java/lib/logback-console.xml

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

%pre common
%groupadd -g 111 zabbix
%useradd -d / -u 111 -g zabbix -c "Zabbix User" -s /bin/false zabbix

%postun common
if [ "$1" = "0" ]; then
	%userremove zabbix
	%groupremove zabbix
fi

%post server
if [ "$1" = 1 ]; then
	%banner -e %{name}-server <<-EOF
	You should create database for Zabbix.
%if %{with pgsql}
	Running these should be fine in most cases:
	psql -c 'create database zabbix'
	zcat %{_docdir}/%{name}-server-%{version}/postgresql/schema.sql.gz | psql zabbix
	zcat %{_docdir}/%{name}-server-%{version}/postgresql/images.sql.gz | psql zabbix
	zcat %{_docdir}/%{name}-server-%{version}/postgresql/data.sql.gz | psql zabbix
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
%systemd_post zabbix_server.service

%preun server
%systemd_preun zabbix_server.service

%postun server
%systemd_reload

%post agentd
%systemd_post zabbix_agentd.service

%preun agentd
%systemd_preun zabbix_agentd.service

%postun agentd
%systemd_reload

%post proxy
%systemd_post zabbix_proxy.service

%preun proxy
%systemd_preun zabbix_proxy.service

%postun proxy
%systemd_reload

%post java
%systemd_post zabbix_java.service

%preun java
%systemd_preun zabbix_java.service

%postun java
%systemd_reload

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README

%files common
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(751,root,zabbix) %dir %{_sysconfdir}
%attr(751,root,http) %dir %{_sysconfdir}/frontend
%dir %{_appdir}
%dir %{_appdir}/frontends
%dir %attr(770,root,zabbix) /run/zabbix
%dir %attr(775,root,zabbix) /var/log/zabbix

%files agentd
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agentd.conf
%attr(755,root,root) %{_sbindir}/zabbix_agentd
%{_mandir}/man8/zabbix_agentd*
%{systemdunitdir}/zabbix_agentd.service

%files frontend-php
%defattr(644,root,root,755)
%attr(750,root,http) %dir %{_webapps}/%{_webapp}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/*
%{_appdir}/frontends/php
%ghost %attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/frontend/zabbix.conf.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/frontend/.htaccess
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/frontend/maintenance.inc.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/frontend/zabbix.conf.php.example

%files get
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_get
%{_mandir}/man1/zabbix_get*

%files proxy
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_proxy.conf
%attr(755,root,root) %{_sbindir}/zabbix_proxy
%{_mandir}/man8/zabbix_proxy*
%{systemdunitdir}/zabbix_proxy.service

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
%if %{with pgsql}
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
%{systemdunitdir}/zabbix_server.service

%if %{with java}
%files java
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/zabbix_java-start
%attr(755,root,root) %{_sbindir}/zabbix_java-stop
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_java.conf
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/java-logback.xml
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/java-logback-console.xml
%dir %{_datadir}/zabbix_java
%{_datadir}/zabbix_java/bin
%{_datadir}/zabbix_java/lib
%{_datadir}/zabbix_java/settings.sh
%attr(755,root,root) %{_datadir}/zabbix_java/shutdown.sh
%attr(755,root,root) %{_datadir}/zabbix_java/startup.sh
%{systemdunitdir}/zabbix_java.service
%endif
