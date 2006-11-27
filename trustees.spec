#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_without	userspace	# don't build userspace module
#
%define rel	0.1
Summary:	Trustees LSM
Summary(pl):	Modu³ LSM Trustees
Name:		trustees
Version:	3.0
Release:	%{rel}
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/trustees/%{name}-%{version}.tar.bz2
# Source0-md5:	45b7e894f9fe2321d671a5272dac76c2
URL:		http://trustees.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 3:2.6.0}
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Trustees is an advanced Linux permission system inspired by Netware.

%description -l pl
Trustees jest zaawansowanym systemem linuksowych praw dostêpu
zainspirowanym przez Netware.

%package -n kernel-misc-trustees
Summary:	Trustees kernel module
Summary(pl):	Modu³ j±dra Trustees
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Requires:	trustees

%description -n kernel-misc-trustees
Trustees is an advanced Linux permission system inspired by Netware.
This package contains Trustees kernel module.

%description -n kernel-misc-trustees -l pl
Trustees jest zaawansowanym systemem linuksowych praw dostêpu
zainspirowanym przez Netware. Ten pakiet zawiera modu³ j±dra Trustees.

%package -n kernel-smp-misc-trustees
Summary:	Trustees SMP kernel module
Summary(pl):	Modu³ SMP j±dra Trustees
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Requires:	trustees

%description -n kernel-smp-misc-trustees
Trustees is an advanced Linux permission system inspired by Netware.
This package contains Trustees kernel module.

%description -n kernel-smp-misc-trustees -l pl
Trustees jest zaawansowanym systemem linuksowych praw dostêpu
zainspirowanym przez Netware. Ten pakiet zawiera modu³ j±dra Trustees.

%prep
%setup -q

%build
%if %{with userspace}
%{__make} -C src
%endif

%if %{with kernel}
cd module
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	mkdir -p modules/$cfg
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	rm -rf include
	chmod 000 modules
	install -d include/{linux,config}
	%{__make} -C %{_kernelsrcdir} clean \
		SUBDIRS=$PWD \
		O=$PWD \
		%{?with_verbose:V=1}
	install -d include/config
	chmod 700 modules
	ln -sf %{_kernelsrcdir}/config-$cfg .config
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-${cfg}.h include/linux/autoconf.h
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
	cp ../include/*.h include/
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} modules \
		SUBDIRS=$PWD \
		O=$PWD \
		%{?with_verbose:V=1}
	mv *.ko modules/$cfg/
done
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install module/modules/%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}/*.ko \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
%if %{with smp} && %{with dist_kernel}
install module/modules/smp/*.ko \
		$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
%endif
%endif

%if %{with userspace}
install -d $RPM_BUILD_ROOT/sbin
install src/settrustees $RPM_BUILD_ROOT/sbin
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-misc-trustees
%depmod %{_kernel_ver}

%postun	-n kernel-misc-trustees
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-trustees
%depmod %{_kernel_ver}smp

%postun	-n kernel-smp-misc-trustees
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc README examples/*
%attr(755,root,root) /sbin/settrustees
%endif

%if %{with kernel}
%files -n kernel-misc-trustees
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-misc-trustees
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
%endif
%endif
