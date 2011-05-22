# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
#define buildforkernels newest

Name:		rt2860-kmod
Version:	2.4.0.0
Release:	1%{?dist}.1.R
Summary:	Kernel module for RaLink 802.11 wireless devices rt2760/rt2790/rt2860/rt2890

Group:		System Environment/Kernel
License:	GPLv2+
URL:		http://www.ralinktech.com/support.php?s=2
# No direct downloads anymore. See the above link.
Source0:	2010_07_16_RT2860_Linux_STA_v2.4.0.0.tar.gz
Source11:	rt2860-kmodtool-excludekernel-filterfile

Patch1:		rt2860-dat-install-fixes.patch
Patch2:		rt2860-add-network-mgr-support.diff
Patch4:		rt2860-no2.4-in-kernelversion.patch
Patch6:		rt2860-suppress-flood.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	%{_bindir}/kmodtool

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the Ralink Driver for WiFi, a Linux device
driver for 802.11a/b/g universal NIC cards - either PCI, PCIe or
MiniPCI - that use Ralink chipsets (rt2760, rt2790, rt2860, rt2890).

%prep
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

pushd *RT2860*Linux*STA*
%patch1 -p1 -b .rpmbuild
%patch2 -p1 -b .NetworkManager
%patch4 -p1 -b .no24
%patch6 -p1 -b .messageflood
 for ext in c h; do
  find . -name "*.$ext" -exec chmod -x {} \;
 done
popd

for kernel_version in %{?kernel_versions} ; do
 cp -a *RT2860*Linux*STA* _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 make -C _kmod_build_${kernel_version%%___*} LINUX_SRC="${kernel_version##*___}"
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 make -C _kmod_build_${kernel_version%%___*} KERNELPATH="${kernel_version##*___}" KERNELRELEASE="${kernel_version%%___*}" INST_DIR=${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix} install
done

chmod 0755 $RPM_BUILD_ROOT/%{kmodinstdir_prefix}/*/%{kmodinstdir_postfix}/*
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Aug 29 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.4.0.0-1
- version update (2.4.0.0)

* Thu Apr 22 2010 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.3.0.0-1
- version update (2.3.0.0)

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.7
- rebuild for new kernel, disable i586 builds

* Tue Nov 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.6
- rebuild for F12 release kernel

* Mon Nov 09 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.5
- rebuild for new kernels

* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.4
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.3
- rebuild for new kernels

* Sat Oct 24 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.2
- rebuild for new kernels

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-3.1
- rebuild for new kernels

* Sat Aug 22 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-3
- Suppress a flood of system log messages

* Mon Aug 03 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-2
- Fix for kernels >= 2.6.31

* Fri Jun 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.3
- rebuild for final F11 kernel

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.2
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.2.0-1.1
- rebuild for new kernels

* Sat May 23 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.2.0-1
- version update (2.1.2.0)

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.4
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.3
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.2
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.1.0-1.1
- rebuild for new kernels

* Sun Apr 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.1.0-1
- version update (2.1.1.0)

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.1.0.0-1.1
- rebuild for new kernels

* Mon Apr 20 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 2.1.0.0-1
- version update (2.1.0.0)

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-4.7
- rebuild for new kernels

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-4.6
- rebuild for new F11 features

* Thu Mar 26 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.8.0.0-3.6
- Bugfix: kmod doesn't compile when the kernel version has a "2.4" substring

* Sun Mar 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-3.5
- rebuild for new kernels

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-3.4
- rebuild for latest Fedora kernel;

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-3.3
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-3.2
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-3.1
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 1.8.0.0-3
- Add a patch for compilation against kernels >= 2.6.29

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-2.5
- rebuild for latest Fedora kernel;

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-2.4
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-2.3
- rebuild for latest Fedora kernel;

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-2.2
- rebuild for latest Fedora kernel;

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-2.1
- rebuild for latest Fedora kernel;

* Sat Dec 06 2008 Orcan Ogetbil < orcanbahri [AT] yahoo [DOT] com > - 1.8.0.0-2
- removed the iwe-stream patch since it is not needed for 2.6.27+ kernels

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.8
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.7
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.6
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.5
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.4
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.3
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.8.0.0-1.2
- rebuild for latest rawhide kernel; enable ppc and ppc64 again

* Sun Oct 19 2008 Orcan Ogetbil <orcanbahri[at]yahoo[com]> 1.8.0.0-1.1
- update strip-tftpboot-copy.patch to match rt2860 sources with no fuzziness
- revert the patch names to the old versions

* Sun Oct 19 2008 Orcan Ogetbil <orcanbahri[at]yahoo[com]> 1.8.0.0-1
- version update (1.8.0.0)
- patches taken from rt2870-kmod directly

* Tue Oct 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-6.1
- disable ppc ppc64; both fail

* Tue Oct 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-5.1
- rebuild for RPM Fusion

* Sun Sep 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-4
- _default_patch_fuzz 2 for new rpm
- make some comments in install section not fail when building akmod package

* Fri Sep 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-3
- add rt2860-net-namespace-separation.patch to make it compile with 2.6.26.3
  from Fedora; patch provided by James as text in #2083
- License is GPLv2+

* Fri Sep 05 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.7.0-2
- some small fixes and cleanups

* Fri Aug 29 2008 James Bottomley <James.Bottomley [AT] hansenpartnership [DOT] com> 1.7.0-1
- Initial Version
- Applied patch to fix up around iwe_mark interface changes
