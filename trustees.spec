#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace module
#
%define rel	1
Summary:	Trustees LSM
Summary(pl.UTF-8):	Moduł LSM Trustees
Name:		trustees
Version:	3.0
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/trustees/%{name}-%{version}.tar.bz2
# Source0-md5:	45b7e894f9fe2321d671a5272dac76c2
Patch0:		trustees-namespace.patch
URL:		http://trustees.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Trustees is an advanced Linux permission system inspired by Netware.

%description -l pl.UTF-8
Trustees jest zaawansowanym systemem linuksowych praw dostępu
zainspirowanym przez Netware.

%package -n kernel%{_alt_kernel}-misc-trustees
Summary:	Trustees kernel module
Summary(pl.UTF-8):	Moduł jądra Trustees
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Requires:	trustees

%description -n kernel%{_alt_kernel}-misc-trustees
Trustees is an advanced Linux permission system inspired by Netware.
This package contains Trustees kernel module.

%description -n kernel%{_alt_kernel}-misc-trustees -l pl.UTF-8
Trustees jest zaawansowanym systemem linuksowych praw dostępu
zainspirowanym przez Netware. Ten pakiet zawiera moduł jądra Trustees.

%prep
%setup -q
%patch0 -p1

%build
%if %{with userspace}
%{__make} -C src \
	CFLAGS="%{rpmcflags} -I$PWD/include"
%endif

%if %{with kernel}
%build_kernel_modules -C module -m %{name}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m module/trustees -d misc
%endif

%if %{with userspace}
install -d $RPM_BUILD_ROOT/sbin
install src/settrustees $RPM_BUILD_ROOT/sbin
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-trustees
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-trustees
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc README examples/*
%attr(755,root,root) /sbin/settrustees
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-trustees
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*
%endif
