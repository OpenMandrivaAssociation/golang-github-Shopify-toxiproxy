# Run tests in check section
%bcond_without check

# https://github.com/Shopify/toxiproxy
%global goipath         github.com/Shopify/toxiproxy
Version:                2.1.3

%global common_description %{expand:
Toxiproxy is a framework for simulating network conditions. It's made 
specifically to work in testing, CI and development environments, supporting 
deterministic tampering with connections, but with support for randomized 
chaos and customization. Toxiproxy is the tool you need to prove with tests 
that your application doesn't have single points of failure.

Toxiproxy usage consists of two parts. A TCP proxy written in Go (what this 
repository contains) and a client communicating with the proxy over HTTP. You 
configure your application to make all test connections go through Toxiproxy 
and can then manipulate their health via HTTP. See Usage below on how to set 
up your project.}

%gometa

Name:           golang-github-Shopify-toxiproxy
Release:        1%{?dist}
Summary:        A proxy to simulate network and system conditions
# Detected licences
# - Expat License at 'LICENSE'
License:        MIT
URL:            %{gourl}
Source0:        %{gosource}
# Stolen from Debian:
Source1:        toxiproxy-server.1
Source2:        toxiproxy-cli.1
Source3:        toxiproxy.default
Source4:        toxiproxy.service
Source5:        toxiproxy.logrotate

Patch0:         https://github.com/Shopify/toxiproxy/commit/65bbb75e44c0368bcabbe2b1b428f1809993cdc0.patch#/0001-Fix-Fatalf-parameters.patch

%{?systemd_requires}
BuildRequires: systemd
BuildRequires: golang(github.com/gorilla/context)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/sirupsen/logrus)
BuildRequires: golang(github.com/urfave/cli)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(golang.org/x/sys/unix)
BuildRequires: golang(gopkg.in/tomb.v1)
Requires(pre): shadow-utils

%description
%{common_description}


%package -n toxiproxy
Summary:       %{summary}

%description -n toxiproxy
%{common_description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix


%package devel
Summary:       %{summary}
BuildArch:     noarch

%description devel
%{common_description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.


%prep
%forgeautosetup -p1

rm -rf vendor/


%build
%gobuildroot
export LDFLAGS="-X github.com/Shopify/toxiproxy.Version=%{version}"
%gobuild -o _bin/toxiproxy-cli %{goipath}/cli
%gobuild -o _bin/toxiproxy-server %{goipath}/cmd


%install
%goinstall
install -Dpm 0755 _bin/toxiproxy-cli %{buildroot}%{_bindir}/toxiproxy-cli
install -Dpm 0755 _bin/toxiproxy-server %{buildroot}%{_bindir}/toxiproxy-server

install -d -m 0755 %{buildroot}%{_mandir}/man1
install -p -m 0644 %{SOURCE1} %{buildroot}%{_mandir}/man1/toxiproxy-server.1
install -p -m 0644 %{SOURCE2} %{buildroot}%{_mandir}/man1/toxiproxy-cli.1

install -d -m 0755 %{buildroot}%{_sysconfdir}/default
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/default/toxiproxy

install -d -m 0755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}/toxiproxy.service

install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/toxiproxy

install -d -m 0755 %{buildroot}%{_sharedstatedir}/toxiproxy
install -d -m 0755 %{buildroot}%{_localstatedir}/log/toxiproxy


%if %{with check}
%check
%gochecks
%endif


%pre  -n toxiproxy
getent group toxiproxy >/dev/null || groupadd -r toxiproxy
getent passwd toxiproxy >/dev/null || \
    useradd -r -g toxiproxy -d %{_sharedstatedir}/toxiproxy -s /sbin/nologin \
    -c "Toxiproxy-server account" toxiproxy
exit 0


%post  -n toxiproxy
%systemd_post toxiproxy.service


%preun  -n toxiproxy
%systemd_preun toxiproxy.service


%postun  -n toxiproxy
%systemd_postun_with_restart toxiproxy.service


%files  -n toxiproxy
%license LICENSE
%doc README.md
%{_bindir}/toxiproxy-cli
%{_bindir}/toxiproxy-server
%config(noreplace) %{_sysconfdir}/default/toxiproxy
%config(noreplace) %{_sysconfdir}/logrotate.d/toxiproxy
%{_unitdir}/toxiproxy.service
%{_mandir}/man1/toxiproxy-server.1.*
%{_mandir}/man1/toxiproxy-cli.1.*
%attr(0775,root,toxiproxy) %dir %{_localstatedir}/log/toxiproxy
%attr(0750,toxiproxy,toxiproxy) %dir %{_sharedstatedir}/toxiproxy


%files devel -f devel.file-list
%license LICENSE
%doc README.md CREATING_TOXICS.md CHANGELOG.md


%changelog
* Mon Oct 29 2018 Robert-André Mauchin <zebob.m@gmail.com> - 2.1.3-1
- Release 2.1.3

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.7.rc2.gitfc5a9c0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.6.rc2.gitfc5a9c0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.5.rc2.gitfc5a9c0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.4.rc2.gitfc5a9c0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.3.rc2.gitfc5a9c0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-0.2.rc2.gitfc5a9c0
- https://fedoraproject.org/wiki/Changes/golang1.7

* Fri Apr 15 2016 jchaloup <jchaloup@redhat.com> - 2.0.0-0.1.rc2.gitfc5a9c0
- First package for Fedora
  resolves: #1327753

