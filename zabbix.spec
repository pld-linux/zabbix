# TODO:
# - initscript for zabbix-agentd, zabbix-server, zabbix-proxy and zabbix-java
#
# Conditional build:
%bcond_without	pgsql 	# enable PostgreSQL support
%bcond_without	sqlite3	# enable sqlite3 support
%bcond_without	mysql	# enable MySQL support
%bcond_without	java	# disable java support

%define databases %{?with_pgsql:postgresql} %{?with_mysql:mysql} %{?with_sqlite3:sqlite3}
%define any_database %{with pgsql}%{with mysql}%{with sqlite3}

%define		php_min_version 5.4.0
Summary:	Zabbix - network monitoring software
Summary(pl.UTF-8):	Zabbix - oprogramowanie do monitorowania sieci
Name:		zabbix
Version:	3.2.6
Release:	1
License:	GPL v2+
Group:		Networking/Utilities
Source0:	http://downloads.sourceforge.net/zabbix/%{name}-%{version}.tar.gz
# Source0-md5:	87428256f7e48b8bf10a926df27a34c8
Source1:	%{name}-apache.conf
Source2:	%{name}_server.service
Source3:	%{name}_agentd.service
Source4:	%{name}_proxy.service
Source5:	%{name}_java.service
Source6:	%{name}.tmpfiles
Patch0:		config.patch
Patch1:		sqlite3_dbname.patch
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
Requires:	php(pcre)
Requires:	php(session)
Requires:	php(sockets)
Requires:	php(xml)
Requires:	php(xmlreader)
Requires:	php(xmlwriter)
Requires:	webapps
Requires:	webserver(alias)
Requires:	webserver(indexfile)
Requires:	webserver(php)
Suggests:	php(mysql)
Suggests:	php(pgsql)
Suggests:	php(sqlite3)
# used with sqlite3
Suggests:	php(sysvsem)
BuildArch:	noarch

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
Requires:	zabbix-proxy(db) = %{version}-%{release}

%description proxy
This package provides the Zabbix proxy.

%description proxy -l pl.UTF-8
Ten pakiet zawiera proxy Zabbix.

%package proxy-mysql
Summary:	MySQL support for Zabbix proxy
Summary(pl.UTF-8):	Obsługa MySQL dla proxy do Zabbiksa
Group:		Networking/Utilities
Provides:	%{name}-proxy(db) = %{version}-%{release}
Obsoletes:	zabbix-proxy-postgresql
Obsoletes:	zabbix-proxy-sqlite3

%description proxy-mysql
This package provides the Zabbix proxy binary with MySQL support.

%description proxy-mysql -l pl.UTF-8
Ten pakiet zawiera proxy Zabbix z obsługą MySQL.

%package proxy-postgresql
Summary:	PostgreSQL support for Zabbix proxy
Summary(pl.UTF-8):	Obsługa PostgreSQL dla proxy do Zabbiksa
Group:		Networking/Utilities
Provides:	%{name}-proxy(db) = %{version}-%{release}
Obsoletes:	zabbix-proxy-mysql
Obsoletes:	zabbix-proxy-sqlite3

%description proxy-postgresql
This package provides the Zabbix proxy binary with PostgreSQL support.

%description proxy-postgresql -l pl.UTF-8
Ten pakiet zawiera proxy Zabbix z obsługą PostgreSQL.

%package proxy-sqlite3
Summary:	SQLite 3 support for Zabbix proxy
Summary(pl.UTF-8):	Obsługa SQLite 3 dla proxy do Zabbiksa
Group:		Networking/Utilities
Provides:	%{name}-proxy(db) = %{version}-%{release}
Obsoletes:	zabbix-proxy-mysql
Obsoletes:	zabbix-proxy-postgresql

%description proxy-sqlite3
This package provides the Zabbix proxy binary with SQLite 3 support.

%description proxy-sqlite3 -l pl.UTF-8
Ten pakiet zawiera proxy Zabbix z obsługą SQLite 3.

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
Requires:	%{name}-server(db) = %{version}-%{release}
Requires:	systemd-units >= 38
Obsoletes:	zabbix-suckerd
Obsoletes:	zabbix-trapper-inetd
Obsoletes:	zabbix-trapper-standalone

%description server
This package provides the Zabbix server.

%description server -l pl.UTF-8
Ten pakiet zawiera serwer Zabbiksa.

%package server-mysql
Summary:	MySQL support for Zabbix server
Summary(pl.UTF-8):	Obsługa MySQL sla serwera Zabbiksa
Group:		Networking/Utilities
Provides:	%{name}-server(db) = %{version}-%{release}
Obsoletes:	zabbix-server-postgresql
Obsoletes:	zabbix-server-sqlite3

%description server-mysql
This package provides the Zabbix server binary for use with MySQL
database.

%description server-mysql -l pl.UTF-8
Ten pakiet zawiera serwer Zabbiksa z obsługą bazy danych MySQL.

%package server-postgresql
Summary:	PostgreSQL support for Zabbix server
Summary(pl.UTF-8):	Obsługa PostgreSQL sla serwera Zabbiksa
Group:		Networking/Utilities
Provides:	%{name}-server(db) = %{version}-%{release}
Obsoletes:	zabbix-server-mysql
Obsoletes:	zabbix-server-sqlite3

%description server-postgresql
This package provides the Zabbix server binary for use with PostgreSQL
database.

%description server-postgresql -l pl.UTF-8
Ten pakiet zawiera serwer Zabbiksa z obsługą bazy danych PostgreSQL.

%package server-sqlite3
Summary:	SQLite 3 support for Zabbix server
Summary(pl.UTF-8):	Obsługa SQLite 3 sla serwera Zabbiksa
Group:		Networking/Utilities
Requires(post):	/bin/zcat
Provides:	%{name}-server(db) = %{version}-%{release}
Obsoletes:	zabbix-server-mysql
Obsoletes:	zabbix-server-postgresql

%description server-sqlite3
This package provides the Zabbix server binary for use with SQLite 3
database.

NOTE: Support for SQLite 3 is EXPERIMENTAL and not recommended.

%description server-sqlite3 -l pl.UTF-8
Ten pakiet zawiera serwer Zabbiksa z obsługą bazy danych SQLite 3.

INFO: Wsparcie dla SQLite 3 jest EKSPERYMENTALNE i nie rekomendowane.

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
%patch1 -p1

%build

configure() {
	%configure \
	--enable-agent \
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
	--with-unixodbc \
	"$@"
}

configure \
	--disable-server \
	--disable-proxy

%{__make}

# keep timestamps to prevent unneccessary rebuilds
cp -a include/config.h include/config.h.old
cp -a include/stamp-h1 include/stamp-h1.old

for database in %{databases} ; do
	configure \
		--with-$database \
		--enable-server \
		--enable-proxy

	# restore timestamps
	touch --reference=include/config.h.old include/config.h
	touch --reference=include/stamp-h1.old include/stamp-h1

	# clean what needs rebuilding
	for dir in src/libs/zbxdb* src/libs/zbxserver ; do
		%{__make} -C $dir clean
	done

	touch include/zbxdb.h

	%{__make}

	%{__make} install \
		-C src/zabbix_server \
		DESTDIR=$PWD/install-${database}
	%{__make} install \
		-C src/zabbix_proxy \
		DESTDIR=$PWD/install-${database}

	# prepare dirs for %%doc
	for dir in upgrades/dbpatches/* ; do
		[ -d $dir/${database} ] || continue
		mkdir -p install-${database}/upgrade/$(basename $dir)
		cp -a $dir/${databases}/* install-${database}/upgrade/$(basename $dir)
	done
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/webapps/%{_webapp},%{_appdir}} \
	$RPM_BUILD_ROOT{/run/zabbix,/var/log/zabbix,%{systemdunitdir},%{systemdtmpfilesdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	ZJG_DEST=$RPM_BUILD_ROOT%{_datadir}/zabbix_java

for database in %{databases} ; do
	cp -p install-$database/%{_sbindir}/zabbix_server \
		$RPM_BUILD_ROOT%{_sbindir}/zabbix_server-$database
	cp -p install-$database/%{_sbindir}/zabbix_proxy \
		$RPM_BUILD_ROOT%{_sbindir}/zabbix_proxy-$database
done

if [ -n "$database" ] ; then
	ln -sf %{_sbindir}/zabbix_server-$database $RPM_BUILD_ROOT%{_sbindir}/zabbix_server
	ln -sf %{_sbindir}/zabbix_proxy-$database $RPM_BUILD_ROOT%{_sbindir}/zabbix_proxy
fi

%if %{with sqlite3}
install -d $RPM_BUILD_ROOT/var/lib/zabbix
touch $RPM_BUILD_ROOT/var/lib/zabbix/zabbix.db
%endif

cp -r frontends $RPM_BUILD_ROOT%{_appdir}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf

install	%{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_server.service
install	%{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_agentd.service
install	%{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_proxy.service
install	%{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_java.service

cp -p %{SOURCE6} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/zabbix.conf

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
%addusertogroup -q zabbix proc

%postun common
if [ "$1" = "0" ]; then
	%userremove zabbix
	%groupremove zabbix
fi

%post server-mysql
if [ "$1" = 1 ]; then
	%banner -e %{name}-server <<-EOF
	You should create database for Zabbix.

	Running these should be fine in most cases:
	mysqladmin create zabbix
	zcat %{_docdir}/%{name}-server-mysql-%{version}/schema.sql.gz | mysql zabbix
	zcat %{_docdir}/%{name}-server-mysql-%{version}/images.sql.gz | mysql zabbix
	zcat %{_docdir}/%{name}-server-mysql-%{version}/data.sql.gz | mysql zabbix
EOF
fi
ln -sf %{_sbindir}/zabbix_server-mysql %{_sbindir}/zabbix_server || :

%post server-postgresql
if [ "$1" = 1 ]; then
	%banner -e %{name}-server <<-EOF
	You should create database for Zabbix.

	Running these should be fine in most cases:

	createuser zabbix
	createdb -O zabbix zabbix
	zcat %{_docdir}/%{name}-server-postgresql-%{version}/schema.sql.gz | psql -u zabbix zabbix
	zcat %{_docdir}/%{name}-server-postgresql-%{version}/images.sql.gz | psql -u zabbix zabbix
	zcat %{_docdir}/%{name}-server-postgresql-%{version}/data.sql.gz | psql -u zabbix zabbix
EOF
fi
ln -sf %{_sbindir}/zabbix_server-postgresql %{_sbindir}/zabbix_server || :

%post server-sqlite3
if [ "$1" = 1 ]; then
	if [ ! -f /var/lib/zabbix/zabbix.db ] ; then
		%banner -e %{name}-server <<-EOF
		Creating sqlite3 database for Zabbix in /var/lib/zabbix/zabbix.db
EOF
		zcat %{_docdir}/%{name}-server-sqlite3-%{version}/schema.sql.gz | sqlite3 /var/lib/zabbix/zabbix.db && \
		zcat %{_docdir}/%{name}-server-sqlite3-%{version}/images.sql.gz | sqlite3 /var/lib/zabbix/zabbix.db && \
		zcat %{_docdir}/%{name}-server-sqlite3-%{version}/data.sql.gz | sqlite3 /var/lib/zabbix/zabbix.db && \
		chown zabbix:zabbix /var/lib/zabbix/zabbix.db && \
		chmod 644 /var/lib/zabbix/zabbix.db || :
	fi
fi
ln -sf %{_sbindir}/zabbix_server-sqlite3 %{_sbindir}/zabbix_server || :

%post server
%systemd_post zabbix_server.service

%preun server
%systemd_preun zabbix_server.service

%postun server
if [ "$1" = "0" ]; then
	if [ -L %{_sbindir}/zabbix_server ] ; then
		rm -f %{_sbindir}/zabbix_server || :
	fi
fi
%systemd_reload

%post agentd
%systemd_post zabbix_agentd.service

%preun agentd
%systemd_preun zabbix_agentd.service

%postun agentd
%systemd_reload

%post proxy-mysql
ln -sf %{_sbindir}/zabbix_proxy-mysql %{_sbindir}/zabbix_proxy || :

%post proxy-postgresql
ln -sf %{_sbindir}/zabbix_proxy-postgresql %{_sbindir}/zabbix_proxy || :

%post proxy-sqlite3
ln -sf %{_sbindir}/zabbix_proxy-sqlite3 %{_sbindir}/zabbix_proxy || :

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
%{systemdtmpfilesdir}/zabbix.conf

%files agentd
%defattr(644,root,root,755)
%doc conf/zabbix_agentd/*.conf
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agentd.conf
%dir %attr(751,root,zabbix) %{_sysconfdir}/zabbix_agentd.conf.d
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

%if %{any_database}
%files proxy
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_proxy.conf
%dir %attr(751,root,zabbix) %{_sysconfdir}/zabbix_proxy.conf.d
%ghost %attr(755,root,root) %{_sbindir}/zabbix_proxy
%{_mandir}/man8/zabbix_proxy*
%{systemdunitdir}/zabbix_proxy.service
%endif

%if %{with mysql}
%files proxy-mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/zabbix_proxy-mysql
%endif

%if %{with pgsql}
%files proxy-postgresql
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/zabbix_proxy-postgresql
%endif

%if %{with sqlite3}
%files proxy-sqlite3
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/zabbix_proxy-sqlite3
%endif

%files sender
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_sender*

%if %{any_database}
%files server
%defattr(644,root,root,755)
%doc upgrades/dbpatches
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_server.conf
%dir %attr(751,root,zabbix) %{_sysconfdir}/zabbix_server.conf.d
%ghost %attr(755,root,root) %{_sbindir}/zabbix_server
%{_mandir}/man8/zabbix_server*
%{systemdunitdir}/zabbix_server.service
%endif

%if %{with mysql}
%files server-mysql
%defattr(644,root,root,755)
%doc database/mysql/*.sql install-mysql/upgrade
%attr(755,root,root) %{_sbindir}/zabbix_server-mysql
%endif

%if %{with pgsql}
%files server-postgresql
%defattr(644,root,root,755)
%doc database/postgresql/*.sql install-postgresql/upgrade
%attr(755,root,root) %{_sbindir}/zabbix_server-postgresql
%endif

%if %{with sqlite3}
%files server-sqlite3
%defattr(644,root,root,755)
%doc database/sqlite3/*.sql
%attr(755,root,root) %{_sbindir}/zabbix_server-sqlite3
%dir %attr(771,root,zabbix) /var/lib/zabbix
%ghost %attr(644,zabbix,zabbix) /var/lib/zabbix/zabbix.db
%endif

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
