# TODO:
# - initscript for zabbix-server, zabbix-proxy and zabbix-java
# - unpackaged files:
#   /usr/bin/zabbix_js
#   /var/lib/zabbix/zabbix.db
#
# Conditional build:
%bcond_without	pgsql 	# enable PostgreSQL support
%bcond_without	sqlite3	# enable sqlite3 support
%bcond_without	mysql	# enable MySQL support
%bcond_without	java	# disable java support
%bcond_without	agent2	# disable bulding of Go based agent2

%define databases %{?with_sqlite3:sqlite3} %{?with_pgsql:postgresql} %{?with_mysql:mysql}
%define any_database %{with pgsql}%{with mysql}%{with sqlite3}

%ifnarch %{go_arches}
%undefine	with_agent2
%endif

%{?with_java:%{?use_default_jdk}}

%define		php_min_version 7.2.5
Summary:	Zabbix - network monitoring software
Summary(pl.UTF-8):	Zabbix - oprogramowanie do monitorowania sieci
Name:		zabbix
Version:	7.0.21
Release:	2
License:	GPL v2+
Group:		Networking/Utilities
# https://www.zabbix.com/download_sources
Source0:	https://cdn.zabbix.com/zabbix/sources/stable/7.0/%{name}-%{version}.tar.gz
# Source0-md5:	4a367338724ed926d8034121a333ada0
Source100:	go-vendor.tar.xz
# Source100-md5:	a562ca6399c811bf1d9f5dadb4978a79
Source1:	%{name}-apache.conf
Source2:	%{name}_server.service
Source3:	%{name}_agentd.service
Source4:	%{name}_proxy.service
Source5:	%{name}_java.service
Source6:	%{name}.tmpfiles
Source7:	%{name}_agentd.init
Source8:	%{name}_agent2.init
Source9:	%{name}_agent2.service
%if 0
cd src/go/
go mod vendor
tar -caf ~/go-vendor.tar.xz -C ../../ src/go/vendor
%endif
Patch0:		config.patch
Patch1:		sqlite3_dbname.patch
Patch2:		always_compile_ipc.patch
Patch3:		go-vendor.patch
Patch4:		builddir.patch
Patch5:		sha512-unaligned.patch
URL:		https://www.zabbix.com/
BuildRequires:	OpenIPMI-devel
BuildRequires:	autoconf
BuildRequires:	automake >= 1:1.15
BuildRequires:	c-ares-devel
BuildRequires:	curl-devel >= 7.19.1
BuildRequires:	iksemel-devel
%{?with_java:%buildrequires_jdk}
BuildRequires:	rpm-build >= 4.6
%{?with_java:BuildRequires:	rpm-pld-macros-javaprov}
%{?with_agent2:BuildRequires:	golang >= 1.23}
BuildRequires:	libevent-devel
BuildRequires:	libssh2-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	net-snmp-devel
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	openssl-devel >= 1.1.0
BuildRequires:	pcre-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 2.043
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
BuildRequires:	tar >= 1:1.22
BuildRequires:	unixODBC-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	%{name}-agentd = %{version}-%{release}
Requires:	%{name}-frontend-php = %{version}-%{release}
Requires:	%{name}-server = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}
%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}

%if %{defined __compress_doc}
%define		doc_cat		zcat
%define		doc_suffix	.gz
%else
%define		doc_cat		cat
%define		doc_suffix	%{nil}
%endif

# internal deps
%define		_noautoreq_pear		include/.* .*.inc.php vendor/autoload.php

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
Requires(pre):	/usr/sbin/usermod
Requires:	group(proc)
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
Requires(post,preun):	/sbin/chkconfig
Requires:	curl-libs >= 7.19.1
Requires:	rc-scripts

%description agentd
Zabbix agent collects data from the local system for a Zabbix server.

%description agentd -l pl.UTF-8
Agent zbiera dane z lokalnej maszyny dla serwera Zabbix.

%package agent2
Summary:	Zabbix Agent 2
Group:		Networking/Utilities
URL:		https://www.zabbix.com/documentation/current/manual/concepts/agent2
Requires:	%{name}-common = %{version}-%{release}
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description agent2
Zabbix agent 2 is a new generation of Zabbix agent and may be used in
place of Zabbix agent.

Zabbix agent 2 has been developed to:
- reduce the number of TCP connections
- have greater check concurrency
- be easily extendible with plugins.

A plugin should be able to:
- provide trivial checks consisting of only a few simple lines of code
- provide complex checks consisting of long-running scripts and
  standalone data gathering with periodic sending back of the data
- be a drop-in replacement for Zabbix agent (in that it supports all
  the previous functionality)

Passive checks work similarly to Zabbix agent. Active checks support
scheduled/flexible intervals and check concurrency within one active
server.

%package frontend-php
Summary:	PHP frontend for Zabbix
Summary(pl.UTF-8):	Interfejs PHP dla Zabbiksa
Group:		Applications/WWW
Requires:	php(bcmath)
Requires:	php(core) >= %{php_min_version}
Requires:	php(ctype)
Requires:	php(filter)
Requires:	php(gd)
Requires:	php(gettext)
Requires:	php(json)
Requires:	php(mbstring)
Requires:	php(openssl)
Requires:	php(pcre)
Requires:	php(session)
Requires:	php(simplexml)
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
Requires:	group(icmp)
Requires:	systemd-units >= 38
Requires:	zabbix-proxy(db) = %{version}-%{release}
Suggests:	fping

%description proxy
This package provides the Zabbix proxy.

%description proxy -l pl.UTF-8
Ten pakiet zawiera proxy Zabbix.

%package proxy-mysql
Summary:	MySQL support for Zabbix proxy
Summary(pl.UTF-8):	Obsługa MySQL dla proxy do Zabbiksa
Group:		Networking/Utilities
Requires:	curl-libs >= 7.19.1
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
Requires:	curl-libs >= 7.19.1
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
Requires:	curl-libs >= 7.19.1
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
Requires:	group(icmp)
Requires:	systemd-units >= 38
Suggests:	fping
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
Requires:	curl-libs >= 7.19.1
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
Requires:	curl-libs >= 7.19.1
Provides:	%{name}-server(db) = %{version}-%{release}
Obsoletes:	zabbix-server-mysql
Obsoletes:	zabbix-server-sqlite3

%description server-postgresql
This package provides the Zabbix server binary for use with PostgreSQL
database.

%description server-postgresql -l pl.UTF-8
Ten pakiet zawiera serwer Zabbiksa z obsługą bazy danych PostgreSQL.

%package java
Summary:	Zabbix Java Gateway
Group:		Networking/Utilities
Requires:	%{name}-common = %{version}-%{release}
Requires:	systemd-units >= 38

%description java
This package provides the Zabbix Java Gateway.

%prep
%setup -q -a100
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

%define		configuredir	..

configure() {
	%configure \
	--enable-ipv6 \
	--with-ares \
	--with-ldap \
	--with-libcurl \
	--with-libevent \
	--with-libpcre \
	--with-libxml2 \
	--with-net-snmp \
	--with-openipmi \
	--with-openssl \
	--with-ssh2 \
	--with-unixodbc \
	"$@"
}

install -d build-agents
cd build-agents
configure \
	%{?with_java:JAVAC=%{java_home}/bin/javac} \
	%{?with_java:JAR=%{java_home}/bin/jar} \
	--enable-agent \
	%{__enable_disable agent2} \
	%{__enable_disable java} \
	--disable-server \
	--disable-proxy

%{__make}
cd ..

for database in %{databases} ; do
	install -d build-$database
	cd build-$database
	if [ "$database" = "sqlite3" ] ; then
		enable_server=""
	else
		enable_server="--enable-server"
	fi
	configure \
		--with-$database \
		$enable_server \
		--enable-proxy \
		--disable-agent \
		--disable-agent2 \
		--disable-java

	%{__make}
	cd ..
done

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT/etc/webapps/%{_webapp} \
	$RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_appdir}/frontends/php} \
	$RPM_BUILD_ROOT{/var/run/zabbix,/var/log/zabbix,%{systemdunitdir},%{systemdtmpfilesdir}}

%{__make} -C build-agents install \
	DESTDIR=$RPM_BUILD_ROOT \
	ZJG_DEST=$RPM_BUILD_ROOT%{_datadir}/zabbix_java

for database in %{databases} ; do
	%{__make} -C build-$database install \
		DESTDIR=$RPM_BUILD_ROOT

	if [ "$database" != "sqlite3" ] ; then
		%{__mv} $RPM_BUILD_ROOT%{_sbindir}/zabbix_server{,-$database}
	fi
	%{__mv} $RPM_BUILD_ROOT%{_sbindir}/zabbix_proxy{,-$database}
done

if [ -n "$database" ] ; then
	ln -sf zabbix_server-$database $RPM_BUILD_ROOT%{_sbindir}/zabbix_server
	ln -sf zabbix_proxy-$database $RPM_BUILD_ROOT%{_sbindir}/zabbix_proxy
fi

%if %{with sqlite3}
install -d $RPM_BUILD_ROOT/var/lib/zabbix
touch $RPM_BUILD_ROOT/var/lib/zabbix/zabbix.db
%endif

cp -r ui/* $RPM_BUILD_ROOT%{_appdir}/frontends/php

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/apache.conf
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_webapps}/%{_webapp}/httpd.conf

install	%{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_server.service
install	%{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_agentd.service
install	%{SOURCE9} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_agent2.service
install	%{SOURCE7} $RPM_BUILD_ROOT/etc/rc.d/init.d/zabbix_agentd
install	%{SOURCE8} $RPM_BUILD_ROOT/etc/rc.d/init.d/zabbix_agent2
install	%{SOURCE4} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_proxy.service
%{?with_java:install	%{SOURCE5} $RPM_BUILD_ROOT%{systemdunitdir}/zabbix_java.service}

cp -p %{SOURCE6} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/zabbix.conf

mv $RPM_BUILD_ROOT%{_appdir}/frontends/php/conf $RPM_BUILD_ROOT%{_sysconfdir}/frontend
ln -s --relative $RPM_BUILD_ROOT{%{_sysconfdir}/frontend,%{_appdir}/frontends/php/conf}
touch $RPM_BUILD_ROOT%{_sysconfdir}/frontend/zabbix.conf.php

%if %{with java}
mv $RPM_BUILD_ROOT%{_datadir}/zabbix_java/settings.sh $RPM_BUILD_ROOT%{_sysconfdir}/zabbix_java.conf
ln -s --relative $RPM_BUILD_ROOT{%{_sysconfdir}/zabbix_java.conf,%{_datadir}/zabbix_java/settings.sh}
mv $RPM_BUILD_ROOT%{_datadir}/zabbix_java/lib/logback.xml $RPM_BUILD_ROOT%{_sysconfdir}/java-logback.xml
ln -s --relative $RPM_BUILD_ROOT{%{_sysconfdir}/java-logback.xml,%{_datadir}/zabbix_java/lib/logback.xml}
mv $RPM_BUILD_ROOT%{_datadir}/zabbix_java/lib/logback-console.xml $RPM_BUILD_ROOT%{_sysconfdir}/java-logback-console.xml
ln -s --relative $RPM_BUILD_ROOT{%{_sysconfdir}/java-logback-console.xml,%{_datadir}/zabbix_java/lib/logback-console.xml}

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

%triggerpostun agent2 -- zabbix-agent2 < 6.0.15
%systemd_trigger zabbix_agent2.service

%triggerun proxy -- zabbix-proxy < 7.0.21-2
%addusertogroup -q zabbix icmp

%triggerun server -- zabbix-server < 7.0.21-2
%addusertogroup -q zabbix icmp

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
	%doc_cat %{_docdir}/%{name}-server-mysql-%{version}/schema.sql%{doc_suffix} | mysql zabbix
	%doc_cat %{_docdir}/%{name}-server-mysql-%{version}/images.sql%{doc_suffix} | mysql zabbix
	%doc_cat %{_docdir}/%{name}-server-mysql-%{version}/data.sql%{doc_suffix} | mysql zabbix
EOF
fi
ln -sf zabbix_server-mysql %{_sbindir}/zabbix_server || :

%post server-postgresql
if [ "$1" = 1 ]; then
	%banner -e %{name}-server <<-EOF
	You should create database for Zabbix.

	Running these should be fine in most cases:

	createuser zabbix
	createdb -O zabbix -E utf8 -T template0 zabbix
	%doc_cat %{_docdir}/%{name}-server-postgresql-%{version}/schema.sql%{doc_suffix} | psql -U zabbix zabbix
	%doc_cat %{_docdir}/%{name}-server-postgresql-%{version}/images.sql%{doc_suffix} | psql -U zabbix zabbix
	%doc_cat %{_docdir}/%{name}-server-postgresql-%{version}/data.sql%{doc_suffix} | psql -U zabbix zabbix
EOF
fi
ln -sf zabbix_server-postgresql %{_sbindir}/zabbix_server || :

%post server
if [ "$1" = 1 ]; then
	%addusertogroup -q zabbix icmp
fi
%systemd_post zabbix_server.service

%preun server
%systemd_preun zabbix_server.service

%postun server
if [ "$1" = "0" ]; then
	if [ -L %{_sbindir}/zabbix_server ] ; then
		rm -f %{_sbindir}/zabbix_server || :
	fi
	if [ ! -e /usr/sbin/zabbix_proxy ]; then
		/usr/sbin/usermod -r -G icmp zabbix
	fi
fi
%systemd_reload

%post agentd
/sbin/chkconfig --add zabbix_agentd
%service zabbix_agentd restart
%systemd_post zabbix_agentd.service

%preun agentd
if [ "$1" = "0" ]; then
	%service -q zabbix_agentd stop
	/sbin/chkconfig --del zabbix_agentd
fi
%systemd_preun zabbix_agentd.service

%postun agentd
%systemd_reload

%post agent2
/sbin/chkconfig --add zabbix_agent2
%service zabbix_agent2 restart
%systemd_post zabbix_agent2.service

%preun agent2
if [ "$1" = "0" ]; then
	%service -q zabbix_agent2 stop
	/sbin/chkconfig --del zabbix_agent2
fi
%systemd_preun zabbix_agent2.service

%post proxy-mysql
ln -sf zabbix_proxy-mysql %{_sbindir}/zabbix_proxy || :

%post proxy-postgresql
ln -sf zabbix_proxy-postgresql %{_sbindir}/zabbix_proxy || :

%post proxy-sqlite3
ln -sf zabbix_proxy-sqlite3 %{_sbindir}/zabbix_proxy || :

%post proxy
if [ "$1" = 1 ]; then
	%addusertogroup -q zabbix icmp
fi
%systemd_post zabbix_proxy.service

%preun proxy
%systemd_preun zabbix_proxy.service

%postun proxy
if [ "$1" = 0 ]; then
	if [ ! -e /usr/sbin/zabbix_server ]; then
		/usr/sbin/usermod -r -G icmp zabbix
	fi
fi
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
%dir %attr(770,root,zabbix) /var/run/zabbix
%dir %attr(775,root,zabbix) /var/log/zabbix
%{systemdtmpfilesdir}/zabbix.conf

%files agentd
%defattr(644,root,root,755)
%doc conf/zabbix_agentd/*.conf
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agentd.conf
%dir %attr(751,root,zabbix) %{_sysconfdir}/zabbix_agentd.conf.d
%attr(754,root,root) /etc/rc.d/init.d/zabbix_agentd
%attr(755,root,root) %{_sbindir}/zabbix_agentd
%{_mandir}/man8/zabbix_agentd*
%{systemdunitdir}/zabbix_agentd.service

%if %{with agent2}
%files agent2
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agent2.conf
%dir %attr(751,root,zabbix) %{_sysconfdir}/zabbix_agent2.d
%dir %attr(751,root,zabbix) %{_sysconfdir}/zabbix_agent2.d/plugins.d
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agent2.d/plugins.d/*.conf
%attr(754,root,root) /etc/rc.d/init.d/zabbix_agent2
%attr(755,root,root) %{_sbindir}/zabbix_agent2
%{_mandir}/man8/zabbix_agent2.8*
%{systemdunitdir}/zabbix_agent2.service
%endif

%files frontend-php
%defattr(644,root,root,755)
%attr(750,root,http) %dir %{_webapps}/%{_webapp}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_webapps}/%{_webapp}/httpd.conf
%ghost %attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/frontend/zabbix.conf.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/frontend/.htaccess
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/frontend/maintenance.inc.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/frontend/zabbix.conf.php.example
%{_appdir}/frontends/php

%files get
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_get
%{_mandir}/man1/zabbix_get*

%if %{any_database}
%files proxy
%defattr(644,root,root,755)
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_proxy.conf
%dir %attr(751,root,zabbix) %{_sysconfdir}/zabbix_proxy.conf.d
%ghost %{_sbindir}/zabbix_proxy
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
%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_server.conf
%dir %attr(751,root,zabbix) %{_sysconfdir}/zabbix_server.conf.d
%ghost %{_sbindir}/zabbix_server
%{_mandir}/man8/zabbix_server*
%{systemdunitdir}/zabbix_server.service
%endif

%if %{with mysql}
%files server-mysql
%defattr(644,root,root,755)
%doc database/mysql/*.sql
%attr(755,root,root) %{_sbindir}/zabbix_server-mysql
%endif

%if %{with pgsql}
%files server-postgresql
%defattr(644,root,root,755)
%doc database/postgresql/*.sql
%attr(755,root,root) %{_sbindir}/zabbix_server-postgresql
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
