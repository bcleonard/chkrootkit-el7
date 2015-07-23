%define _hardened_build 1
Name:           chkrootkit
Version:        0.50
Release:        6%{?dist}
Summary:        Tool to locally check for signs of a rootkit
Group:          Applications/System
License:        BSD and GPLv2+ and Python
URL:            http://www.chkrootkit.org
Source0:        ftp://ftp.pangeia.com.br/pub/seg/pac/chkrootkit-%{version}.tar.gz
Source1:        chkrootkitX
Source2:        chkrootkit.png
Source3:        chkrootkit.desktop
Source4:        chkrootkit.console
Source5:        chkrootkit.pam
Source6:        README.false_positives
Patch1:         chkrootkit-0.44-getCMD.patch
Patch2:         chkrootkit-0.44-inetd.patch
#Patch3:         chkrootkit-0.45-includes.patch
#Patch4:         chkrootkit-0.49-warnings.patch
Patch6:         chkrootkit-0.47-chklastlog.patch
#Patch7:         chkrootkit-0.48-anomalies.patch
#Patch8:         chkrootkit-0.49-nophpcheck.patch
Patch9:         chkrootkit-0.49-chkproc-psver.patch
Patch10:	chkrootkit-0.49-chkutmp-outofbounds.patch
Patch11:	chkrootkit-0.49-CVE-2014-0476.patch
Patch12:	chkrootkit-suckit.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
Requires:	net-tools

%if 0%{?fedora} > 10
# as of glibc-2.9.90-7 in Rawhide
BuildRequires:  glibc-static
%endif

Requires:       %{_bindir}/consolehelper

%description
chkrootkit is a tool to locally check for signs of a rootkit.
It contains:

 * chkrootkit: shell script that checks system binaries for
   rootkit modification.
 * ifpromisc: checks if the network interface is in promiscuous mode.
 * chklastlog: checks for lastlog deletions.
 * chkwtmp: checks for wtmp deletions.
 * chkproc: checks for signs of LKM trojans.
 * chkdirs: checks for signs of LKM trojans.
 * strings: quick and dirty strings replacement.
 * chkutmp: checks for utmp deletions.


%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .getCMD
%patch2 -p1 -b .inetd
#%patch3 -p1 -b .includes
#%patch4 -p1 -b .warnings
%patch6 -p1 -b .chklastlog
#%patch7 -p1 -b .anomalies
#%patch8 -p0 -b .nophpcheck
%patch9 -p0 -b .chkproc-psver
%patch10 -p1
%patch11 -p1
%patch12 -p1
sed -i -e 's!\s\+@strip.*!!g' Makefile


%build
make sense CC="%{__cc} $RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"


%install
rm -rf ${RPM_BUILD_ROOT}

mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
cat << EOF > .tmp.chkrootkit.sbin
#! /bin/sh
cd %{_libdir}/%{name}-%{version}
exec ./chkrootkit "\$@"
EOF
install -p -D -m0755 .tmp.chkrootkit.sbin ${RPM_BUILD_ROOT}%{_sbindir}/chkrootkit

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
ln -s %{_bindir}/consolehelper ${RPM_BUILD_ROOT}%{_bindir}/chkrootkit

install -p -D -m0755 %{SOURCE1} ${RPM_BUILD_ROOT}%{_bindir}/chkrootkitX
perl -pi -e 's!/usr/bin!%{_bindir}!' ${RPM_BUILD_ROOT}%{_bindir}/chkrootkitX
install -p -D -m0644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_datadir}/pixmaps/chkrootkit.png
install -p -D -m0644 %{SOURCE4} ${RPM_BUILD_ROOT}%{_sysconfdir}/security/console.apps/chkrootkit
perl -pi -e 's!/usr/sbin!%{_sbindir}!' ${RPM_BUILD_ROOT}%{_sysconfdir}/security/console.apps/chkrootkit
install -p -D -m0644 %{SOURCE5} ${RPM_BUILD_ROOT}%{_sysconfdir}/pam.d/chkrootkit
for f in \
    check_wtmpx  \
    chkdirs  \
    chklastlog  \
    chkproc  \
    chkrootkit  \
    chkutmp \
    chkwtmp  \
    ifpromisc  \
    strings-static \
; do
    install -p -D -m0755 $f ${RPM_BUILD_ROOT}%{_libdir}/%{name}-%{version}/${f}
done
ln -s strings-static ${RPM_BUILD_ROOT}%{_libdir}/%{name}-%{version}/strings

desktop-file-install                   \
  --dir ${RPM_BUILD_ROOT}%{_datadir}/applications      \
  %{SOURCE3}

install -p -m0644 %{SOURCE6} .


%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr(-,root,root,-)
%doc ACKNOWLEDGMENTS COPYRIGHT README README.chklastlog README.chkwtmp chkrootkit.lsm README.false_positives
%{_sbindir}/chkrootkit
%{_bindir}/chkrootkit
%{_bindir}/chkrootkitX
%config(noreplace) %{_sysconfdir}/pam.d/chkrootkit
%config(noreplace) %{_sysconfdir}/security/console.apps/chkrootkit
%{_libdir}/%{name}-%{version}
%{_datadir}/applications/chkrootkit.desktop
%{_datadir}/pixmaps/chkrootkit.png


%changelog
* Thu Jul 23 2015 Bradley Leonard <bradley@stygianresearch.com> - 0.50-6
- Rebuilt for centos/el7

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 21 2014 Jon Ciesla <limburgher@gmail.com> - 0.50-4
- Patch for suckit false positive, BZ 636231.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 05 2014 Jon Ciesla <limburgher@gmail.com> - 0.50-1
- Latest upstream, BZ 1104775.
- Dropped upstreamed patch.
- Fixed bad changelog date.

* Wed Jun 04 2014 Jon Ciesla <limburgher@gmail.com> - 0.49-9
- Patch for CVE-2014-0476, BZ 1104456, 11044567.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 11 2013 Jon Ciesla <limburgher@gmail.com> - 0.49-7
- Drop desktop vendor tag.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Jon Ciesla <limburgher@gmail.com> - 0.49-5
- Add hardened build.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 19 2010 Jon Ciesla <limb@jcomserv.net> 0.49-2
- Updated outofbounds patch, BZ 577979 and 626067.

* Thu Mar 18 2010 Jon Ciesla <limb@jcomserv.net> 0.49-1
- New upstream, including upstreamed patches.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Jon Ciesla <limb@jcomserv.net> 0.48-13
- Additional items in chkutmp patch.

* Tue Jul 21 2009 Jon Ciesla <limb@jcomserv.net> 0.48-12
- Patch to fix crash in chkutmp on x86_64.

* Tue Feb 24 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 0.48-11
- update .desktop file for Icon Theme Specification
- no longer add X-Fedora category to .desktop file
- Fedora > 10: conditional BR glibc-static as needed for strings-static

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.48-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.48-9
- fix license tag

* Fri May 30 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.48-8
- Let chkproc default to procps version 3.

* Wed Apr  9 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.48-7
- Build with large file API (#441638).

* Tue Mar 18 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.48-6
- Delete the "suspect PHP files" check. Not only does it trigger
  SIGPIPE for file names which contain special unescaped characters,
  the second half is doubtful (it doesn't print any filenames and
  gets confused by binary file contents).

* Tue Feb 12 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.48-5
- Fix the empty warning of the shell history files anomalies check.
- Initialise two variables in chkdirs.c to silence compiler.

* Fri Feb 08 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.48-3
- rebuilt for GCC 4.3 as requested by Fedora Release Engineering
  (only in devel)

* Sat Jan 12 2008 Michael Schwendt <mschwendt@fedoraproject.org> - 0.48-2
- Install README with mode 0644.

* Sat Dec 22 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 0.48-1
- Update to 0.48 (new tests, enhanced tests, minor bug-fixes).

* Tue Aug 21 2007 Michael Schwendt <mschwendt@fedoraproject.org>
- rebuilt

* Wed May 23 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 0.47-7
- Fix obsolete PAM pam_stack usage (#241038) to make desktop menu
  and consolehelper work again.

* Sun Feb 11 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 0.47-6
- Make chklastlog default to /var/log/lastlog and /var/log/wtmp,
  which can be set with options -l and -f, too, however.

* Wed Jan 31 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 0.47-5
- Upstream wants to disable the OBSD rk v1 check on Linux with
  next release.

* Tue Jan 30 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 0.47-4
- Don't like the previous patch yet, since it is unsafe and
  makes -p more difficult, so removed it again.

* Tue Jan 30 2007 Michael Schwendt <mschwendt@fedoraproject.org> - 0.47-3
- Patch OpenBSD rootkit check to not report libgcj file
  /usr/lib/security/classpath.security without querying the RPM
  database about that file
- Add README.false_positives

* Thu Jan 04 2007 Michael Schwendt <mschwendt@fedoraproject.org>
- rebuilt

* Fri Oct 20 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 0.47-1
- Update to 0.47.
- mark PAM and consolehelper files in /etc as config

* Mon Aug 28 2006 Michael Schwendt <mschwendt@fedoraproject.org>
- rebuilt

* Sat Feb 25 2006 Michael Schwendt <mschwendt@fedoraproject.org> - 0.46a-2
- rebuilt for FC5

* Thu Nov 10 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 0.46a-1
- Update to 0.46a.

* Fri Aug 19 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 0.45-4
- Pass on command-line arguments to main program (#166321).

* Mon May  9 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 0.45-3
- Create debuginfo package, remove stripping from Makefile in %%prep,
  build with optflags.

* Thu Mar 17 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 0.45-2
- Make GCC4 shut up by including more C headers in chkproc.c/chkwtmp.c

* Thu Feb 24 2005 Michael Schwendt <mschwendt@fedoraproject.org> - 0:0.45-1
- Update to 0.45, trim description.

* Mon Oct  4 2004 Michael Schwendt <mschwendt@fedoraproject.org> - 0:0.44-0.fdr.2
- Fix inetd/sshd checks.

* Sat Sep 11 2004 Michael Schwendt <mschwendt@fedoraproject.org> - 0:0.44-0.fdr.1
- Update to 0.44.

* Wed Aug 18 2004 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.43-0.fdr.5
- License COPYRIGHTED -> BSD-like (#1746).

* Sat Mar 13 2004 Michael Schwendt <mschwendt@fedoraproject.org> - 0:0.43-0.fdr.4
- rh80 doesn't have sed -i, use perl instead (#1326).
- Obsolete chkrootkit-strings patch due to soft-link since 0.43-0.fdr.1.

* Fri Feb 27 2004 Michael Schwendt <mschwendt@fedoraproject.org> - 0:0.43-0.fdr.3
- Make in %%build section (#1326).

* Fri Feb 27 2004 Michael Schwendt <mschwendt@fedoraproject.org> - 0:0.43-0.fdr.2
- Substitute a few hardcoded paths (#1326).

* Thu Feb 26 2004 Michael Schwendt <mschwendt@fedoraproject.org> - 0:0.43-0.fdr.1
- Update to 0.43.
- Add dependency on consolehelper binary.
- Drop patched chkrootkit script due to change in 0.42-0.fdr.3.b.
- Make available "strings-static" as "strings", too.

* Wed Dec 10 2003 Michael Schwendt <mschwendt@fedoraproject.org> - 0:0.42-0.fdr.3.b
- Make /usr/bin/chkrootkit enter chkrootkit home directory.
  This puts its own helper tools into its search path.

* Thu Dec 04 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.42-0.fdr.2.b
- Move binaries out of %%{_datadir}.

* Sun Sep 21 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.42-0.fdr.1.b
- Updated to 0.42b.

* Mon Sep 15 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.42-0.fdr.1
- Updated to 0.42.
- Moved pam and console entries into seperate files.
- Install into %%{_datadir} not %%{_libdir}.

* Fri Jun 27 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.41-0.fdr.3
- Moved chkrootkit.lsm into docs.
- Explicitly set file permissions for icon and desktop entry on install.
- No longer include backup of original chkrootkit script.

* Fri Jun 27 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.41-0.fdr.2
- Removed unnecessary files.

* Sat Jun 21 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.41-0.fdr.1
- Updated to 0.41.

* Fri Apr 04 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.40-0.fdr.3
- Modified the chkrootkit scrip to execute the other sub programs correctly when called from the menu entry.

* Fri Apr 04 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.40-0.fdr.2
- Removed hardcoded path.

* Thu Apr 03 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.40-0.fdr.1
- Updated to 0.40

* Tue Apr 01 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0:0.39a-0.fdr.4
- Added Epoch:0.
- Added desktop-file-utils to BuildRequires.
- Changed category to X-Fedora-Extra.
- Moved desktop entry into seperate file.

* Wed Mar 26 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.39a-0.fdr.3
- Added Icon.
- Added desktop entry.
- Added pam entry.

* Sat Mar 22 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.39a-0.fdr.2
- Spec Cleanup.

* Sat Mar 08 2003 Phillip Compton <pcompton[AT]proteinmedia.com> - 0.39a-0.fdr.1
- Initial RPM release.
