#
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# don't build SMP module
#
Summary:	Trustees LSM
Summary(pl):	Modu³ LSM Trustees
Name:		trustees2.6
Version:	0
%define pre 20041113
Release:	0.%{pre}.1
License:	GPL
Group:		Base/Kernel
Source0:	%{name}-%{pre}.tar.gz
# Source0-md5:	dd789d54dc735e622843ad23dcd6d0fd
URL:		http://trustees.sourceforge.net/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.0}
BuildRequires:	rpmbuild(macros) >= 1.153
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Trustees LSM.

%description -l pl
Modu³ LSM Trustees.

%define buildconfigs %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}

%prep
%setup -q -n trustees

%build
#%{__make} prereq \
#	CC="%{__cc}"

cd module

for cfg in %{buildconfigs}; do
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
	ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm #FIXME
	cp ../include/*.h include/
	touch include/config/MARKER
	%{__make} -C %{_kernelsrcdir} modules \
		SUBDIRS=$PWD \
		O=$PWD \
		%{?with_verbose:V=1}
	mv *.ko modules/$cfg/
done

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
for cfg in %{buildconfigs}; do
	cfgdest=''
	if [ "$cfg" = "smp" ]; then
		install modules/$cfg/*.ko \
			$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}$cfg/misc
	else
		install modules/$cfg/*.ko \
			$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
	fi
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%attr(600,root,root) %config(noreplace) /etc/trustees2.6.conf
%attr(755,root,root) /sbin/*
%attr(755,root,root) %{_libdir}/*.so.*
