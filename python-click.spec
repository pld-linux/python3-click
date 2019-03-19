#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# py.test tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	click
Summary:	A simple wrapper around optparse for powerful command line utilities
Summary(pl.UTF-8):	Proste obudowanie optparse do tworzenia potężnych narzędzi linii poleceń
Name:		python-%{module}
Version:	7.0
Release:	1.1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/pallets/click/releases
# TODO: use:
#Source0:	https://github.com/pallets/click/archive/click-%{version}.tar.gz
Source0:	https://github.com/pallets/click/archive/%{version}.tar.gz
# Source0-md5:	1c000f4357bd04e49af568b51bc03c6a
URL:		http://click.pocoo.org/
%if %{with tests} && %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-modules >= 2
BuildRequires:	python-pytest
BuildRequires:	python-setuptools
%{?with_doc:BuildRequires:	python-pallets-sphinx-themes}
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-pytest
BuildRequires:	python3-setuptools
%{?with_doc:BuildRequires:	python3-pallets-sphinx-themes}
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
click is a Python package for creating beautiful command line
interfaces in a composable way with as little amount of code as
necessary. It's the "Command Line Interface Creation Kit". It's highly
configurable but comes with good defaults out of the box.

%description -l pl.UTF-8
click to pakiet Pythona do tworzenia ładnych interfejsów linii poleceń
w uporządkowany sposób, przy użyciu jak najmniejszej ilości kodu.
Nazwa "click" pochodzi od "Command Line Interface Creation Kit"
(zestaw do tworzenia interfejsu linii poleceń). Jest wysoce
konfigurowalny, ale ma dobre ustawienia domyślne.

%package -n python3-%{module}
Summary:	A simple wrapper around optparse for powerful command line utilities
Summary(pl.UTF-8):	Proste obudowanie optparse do tworzenia potężnych narzędzi linii poleceń
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
click is a Python 3 package for creating beautiful command line
interfaces in a composable way with as little amount of code as
necessary. It's the "Command Line Interface Creation Kit". It's highly
configurable but comes with good defaults out of the box.

%description -n python3-%{module} -l pl.UTF-8
click to pakiet Pythona do tworzenia ładnych interfejsów linii poleceń
w uporządkowany sposób, przy użyciu jak najmniejszej ilości kodu.
Nazwa "click" pochodzi od "Command Line Interface Creation Kit"
(zestaw do tworzenia interfejsu linii poleceń). Jest wysoce
konfigurowalny, ale ma dobre ustawienia domyślne.

%package apidocs
Summary:	Documentation for Python click module
Summary(pl.UTF-8):	Dokumentacja do modułu Pythona click
Group:		Documentation

%description apidocs
Documentation for Python click module.

%description apidocs -l pl.UTF-8
Dokumentacja do modułu Pythona click.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build
%if %{with tests}
PYTHONPATH=$(pwd) %{__python} -m pytest tests --tb=long --verbose
%endif
%endif

%if %{with python3}
%py3_build
%if %{with tests}
LC_ALL=C.UTF-8 PYTHONPATH=$(pwd) %{__python3} -m pytest tests --tb=long --verbose
%endif
%endif

%if %{with doc}
# click-specific code is not python3 ready
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
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
%doc CHANGES.rst LICENSE.rst README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/Click-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/Click-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
