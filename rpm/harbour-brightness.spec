Name:       harbour-brightness

Summary:    Brightness fix for Xperia 10 III
Version:    1.0
Release:    1
Group:      System
License:    GPLv2
BuildArch:  noarch
URL:        http://github.com/direc85/harbour-brightness
Source0:    %{name}-%{version}.tar.bz2

%description
Short description of my Sailfish OS Application

%prep
%setup -q -n %{name}-%{version}

%build

%pre
if ! rpm -qi droid-config-xqbt52 >/dev/null
then
  echo "Error: Device is not Sony Xperia 10 III"
  exit 1
fi

%install
rm -rf %{buildroot}
install -Dm 755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dm 644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%posttrans
systemctl daemon-reload
systemctl enable %{name}.service
systemctl stop %{name}.service
systemctl start %{name}.service
exit 0

%postun
# Run on uninstall, not on upgrade
if [ $1 -eq 0 ]; then
  systemctl stop %{name}.service
  systemctl disable %{name}.service
  systemctl daemon-reload
  systemctl reset-failed
fi
exit 0
