#
# Conditional build:
%bcond_without	tests		# syntax check
%bcond_with	tests_kernel	# "make check" (requires seccomp aware kernel)
%bcond_with	gccgo		# use gcc-go instead of golang

%ifnarch %{ix86} %{x8664} %{arm} aarch64 mips64 mips64le ppc64 ppc64le s390x
%define	with_gccgo	1
%endif
%ifarch x32
# gcc-go.x32 supports 64 ABI, so won't go with libseccomp.x32
%undefine	with_tests
%endif
Summary:	Go language bindings for the libseccomp project
Summary(pl.UTF-8):	Wiązania języka Go do projektu libseccomp
Name:		golang-libseccomp
Version:	0.9.0
Release:	2
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/seccomp/libseccomp-golang/releases
Source0:	https://github.com/seccomp/libseccomp-golang/archive/v%{version}/libseccomp-golang-%{version}.tar.gz
# Source0-md5:	1395f1bf9534d28852f664daba703e83
URL:		https://github.com/seccomp/libseccomp-golang
%if %{with tests}
%{?with_gccgo:BuildRequires:	gcc-go >= 6:4.8.4}
%{!?with_gccgo:BuildRequires:	golang >= 1.2.1}
BuildRequires:	libseccomp-devel >= 2.2.1
%endif
%{?with_gccgo:Requires:	gcc-go >= 6:4.8.4}
%{!?with_gccgo:Requires:	golang >= 1.2.1}
Requires:	libseccomp-devel >= 2.2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libseccomp library provides and easy to use, platform independent,
interface to the Linux Kernel's syscall filtering mechanism: seccomp.
The libseccomp API is designed to abstract away the underlying BPF
based syscall filter language and present a more conventional
function-call based filtering interface that should be familiar to,
and easily adopted by application developers.

This package provides a Go based interface to the libseccomp library.

%description -l pl.UTF-8
Biblioteka libseccomp udostępnia łatwy w użyciu, niezależny od
platformy interfejs do mechanizmu filtrowania wywołań systemowych
jądra Linuksa - seccomp. API libseccomp jest zaprojektowane tak, żeby
wyabstrahować język filtrowania wywołań BPF niższego poziomu i
zaprezentować bardziej konwencjonalny interfejs filtrowania w oparciu
o wywołania funkcji, który powinien być bardziej przyjazny i łatwiej
adaptowalny dla programistów aplikacji.

Ten pakiet udostępnia interfejs języka Go do biblioteki libseccomp.

%prep
%setup -q -n libseccomp-golang-%{version}

%build
%if %{with tests}
# perform test-build to check syntax
%{__make}

%{?with_tests_kernel:%{__make} check}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/golang/src/github.com/seccomp/libseccomp-golang

cp -p *.go $RPM_BUILD_ROOT%{_libdir}/golang/src/github.com/seccomp/libseccomp-golang

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG LICENSE README
# XXX: github.com is shared
%dir %{_libdir}/golang/src/github.com
%dir %{_libdir}/golang/src/github.com/seccomp
%{_libdir}/golang/src/github.com/seccomp/libseccomp-golang
