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
Summary(pl.UTF-8):	zabbix - oprogramowanie do monitorowania sieci
Name:		zabbix
Version:	1.1.7
Release:	1
License:	GPL v2+
Group:		Networking/Admin
Source0:	http://dl.sourceforge.net/zabbix/%{name}-%{version}.tar.gz
# Source0-md5:	ac24ab58ef1a985c1e2a5217386d5dba
Source1:	%{name}-agent.inetd
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
Summary(pl.UTF-8):	Wersja wolnostojąca agenta zabbiksa
Group:		Networking/Admin
Requires:	%{name} = %{version}-%{release}
Obsoletes:	zabbix-agent-inetd

%description agent-standalone
This package provides standalone version of zabbix agent.

%description agent-standalone -l pl.UTF-8
Ten pakiet dostarcza wolnostojącej wersji agenta zabbiksa.

%package sender
Summary:	zabbix's sender
Summary(pl.UTF-8):	Program zawiadamiający zabbiksa
Group:		Networking/Admin

%description sender
This package provides the zabbix sender.

%description sender -l pl.UTF-8
Ten pakiet zawiera program zawiadamiający zabbiksa.

%package get
Summary:        zabbix's get
#Summary(pl.UTF-8):      Program zawiadamiajÄy zabbiksa
Group:          Networking/Admin

%description get
This package provides the zabbix get.

#%description get -l pl.UTF-8
#Ten pakiet zawiera program zawiadamiajÄy zabbiksa.

%package server
Summary:        zabbix's server
Summary(pl.UTF-8):      Serwer zabbiksa
Group:          Networking/Admin
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

%files
%defattr(644,root,root,755)
#%doc doc/Zabbix\ Manual.pdf AUTHORS NEWS README ChangeLog create upgrades bin/ZabbixW32.exe
#%attr(750,root,zabbix) %dir %{_sysconfdir}
%{_libdir}/*.a

%files agent-inetd
%defattr(644,root,root,755)
#%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agent.conf
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/zabbix-agent
%attr(755,root,root) %{_bindir}/zabbix_agent

%files agent-standalone
%defattr(644,root,root,755)
#%attr(640,root,zabbix) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/zabbix_agentd.conf
%attr(755,root,root) %{_bindir}/zabbix_agentd

%files sender
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_sender

%files get
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_get

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/zabbix_server
