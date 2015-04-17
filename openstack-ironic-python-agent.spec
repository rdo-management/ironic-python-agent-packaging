%{?!_licensedir:%global license %%doc}

Name:       openstack-ironic-python-agent
Summary:    A python agent for provisioning and deprovisioning Bare Metal servers.
Version:    0.1
Release:    1
License:    ASL 2.0
Group:      System Environment/Base
URL:        https://github.com/openstack/ironic-python-agent

Source0:    https://github.com/openstack/ironic-python-agent
Source1:    openstack-ironic-python-agent.service

BuildArch:  noarch
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires: python-babel
Requires: python-eventlet
Requires: python-iso8601
Requires: python-netifaces
Requires: python-ordereddict
Requires: python-oslo-config
Requires: python-oslo-concurrency
Requires: python-oslo-i18n
Requires: python-oslo-log
Requires: python-oslo-serialization
Requires: python-oslo-utils
Requires: python-pecan
Requires: python-psutil
Requires: python-pyudev
Requires: python-requests
Requires: python-six
Requires: python-stevedore
Requires: python-wsme

%prep
%autosetup -v -p 1 -n ironic-python-agent-%{upstream_version}
rm -rf *.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

# install systemd scripts
mkdir -p %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}

install -p -D -m 644 etc/ironic_python_agent/ironic_python_agent.conf.sample %{buildroot}/%{_sysconfdir}/ironic-python-agent/agent.conf

%description
An agent for controlling and deploying Ironic controlled baremetal nodes.

The ironic-python-agent works with the agent driver in Ironic to provision the
node. Starting with ironic-python-agent running on a ramdisk on the
unprovisioned node, Ironic makes API calls to ironic-python-agent to provision
the machine. This allows for greater control and flexibility of the entire
deployment process.

The ironic-python-agent may also be used with the original Ironic pxe drivers
as of the Kilo OpenStack release.

%files
%doc README.rst
%license LICENSE
%config(noreplace) %attr(-,root,root) %{_sysconfdir}/ironic-python-agent
%{_bindir}/ironic-python-agent
%{_unitdir}/openstack-ironic-python-agent.service
%{python_sitelib}/ironic_python_agent*

%post
%systemd_post openstack-ironic-python-agent.service

%preun
%systemd_preun openstack-ironic-python-agent.service

%postun
%systemd_postun_with_restart openstack-ironic-python-agent.service


%changelog

* Thu May 21 2015 John Trowbridge <trown@redhat.com> - 0.1.0-1
- Initial package build
