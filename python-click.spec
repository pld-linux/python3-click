#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	click
Summary:	A simple wrapper around optparse for powerful command line utilities
Name:		python-%{module}
Version:	6.7
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://github.com/pallets/click/archive/%{version}.tar.gz
# Source0-md5:	3cae45d064f341b3f373489d8f7745e9
URL:		http://click.pocoo.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-pytest
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-pytest
BuildRequires:	python3-setuptools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
click is a Python package for creating beautiful command line
interfaces in a composable way with as little amount of code as
necessary. It's the "Command Line Interface Creation Kit". It's highly
configurable but comes with good defaults out of the box.

%package -n python3-%{module}
Summary:	A simple wrapper around optparse for powerful command line utilities
Group:		Libraries/Python

%description -n python3-%{module}
click is a Python 3 package for creating beautiful command line
interfaces in a composable way with as little amount of code as
necessary. It's the "Command Line Interface Creation Kit". It's highly
configurable but comes with good defaults out of the box.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build
%if %{with tests}
PYTHONPATH=$(pwd) py.test-%{py_ver} tests --tb=long --verbose
%endif
%endif

%if %{with python3}
%py3_build
%if %{with tests}
LANG=en_GB.utf8 LC_ALL=en_GB.utf8 PYTHONPATH=$(pwd) py.test-%{py3_ver} tests --tb=long --verbose
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif
