Name:           scsi-target-utils
Version:        1.0.24
Release:        18%{?dist}
Summary:        The SCSI target daemon and utility programs

Group:          System Environment/Daemons
License:        GPLv2
URL:            http://stgt.sourceforge.net/
Source0:        https://github.com/fujita/tgt/tarball/v%{version}
Source1:        tgtd.init
Source2:        sysconfig.tgtd
Source3:        targets.conf
# Add Red Hat specific info to docs.
Patch0:         0001-redhatify-docs.patch
Patch1:         0002-remove-xsltproc.patch
Patch2:         0003-discovery-auth.patch
Patch3:         0004-iser-Fix-bidirectional-chap.patch
Patch4:         0005-bs_aio-use-64bit-to-read-eventfd-counter.patch
Patch5:         0006-iser-added-huge-pages-support.patch
Patch6:         0007-iser-added-parameter-for-pool-size.patch
Patch7:         0008-iser-limit-number-of-CQ-entries-requested.patch
Patch8:         0009-iser-add-CQ-vector-param.patch
Patch9:         0010-Rework-param_set_val-and-friends.patch
Patch10:        0011-return-Reject-in-iscsi-login-text-failure.patch
Patch11:        0012-Fix-leak-of-task-data.patch
Patch12:        0013-Fix-isns-to-handle-multiple-portals.patch
Patch13:        0014-iser-Don-t-wait-until-iser_ib_init-to-init-list_head.patch
Patch14:        0015-iser-cleaning-iser-ib-objects-on-lld-exit.patch
Patch15:        0016-iser-Don-t-release-IB-resources-if-were-not-allocate.patch
Patch16:        0017-Fix-possible-segfault-on-logicalunit-update.patch
Patch17:        0018-Fix-segfault-if-device_type-set-to-pt-but-bstype-not.patch
Patch18:        0019-Fix-race-on-thread-shutdown-causing-deadlock.patch
Patch19:        0020-workaround-for-pthreads-bug.patch
Patch20:        0021-DPO-Add-emulation-of-DPO-bit-for-READ-WRITE-VERIFY10.patch
Patch21:        0022-Add-support-for-WRITEVERIFY10-12-16.patch
Patch22:        0023-sbc-Add-residual-handling-for-WRITE6-10-12-16-and-WR.patch
Patch23:        0024-Handle-partial-reads-to-mgmt-responses-in-tgtadm.patch
Patch24:        0025-fix-checks-when-snprintf-output-is-truncated.patch
Patch25:        0026-iscsi-fix-leak-of-task-for-delayed-management-reques.patch
Patch26:        0027-Set-ExpCmdSn-and-MaxCmdSn-in-ISCSI_OP_R2T.patch
Patch27:        0028-targets.conf-manpage-should-not-refer-to-Wikipedia.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  pkgconfig libibverbs-devel librdmacm-devel libxslt docbook-style-xsl libaio-devel
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires: lsof sg3_utils libaio
ExcludeArch:    s390 s390x

%description
The SCSI target package contains the daemon and tools to setup a SCSI targets.
Currently, software iSCSI targets are supported.


%prep
%setup -q -n fujita-tgt-e039354
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1


%build
#pushd usr
%{__sed} -i -e 's|-Wall -g -O2|%{optflags}|' Makefile
%{__make} %{?_smp_mflags} ISCSI_RDMA=1
#popd


%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_mandir}/man5
%{__install} -d %{buildroot}%{_mandir}/man8
%{__install} -d %{buildroot}%{_initrddir}
%{__install} -d %{buildroot}/etc/tgt
%{__install} -d %{buildroot}/etc/sysconfig

%{__install} -p -m 0755 scripts/tgt-setup-lun %{buildroot}%{_sbindir}
%{__install} -p -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/tgtd
%{__install} -p -m 0755 scripts/tgt-admin %{buildroot}/%{_sbindir}/tgt-admin
%{__install} -p -m 0644 doc/manpages/targets.conf.5 %{buildroot}/%{_mandir}/man5
%{__install} -p -m 0644 doc/manpages/tgtadm.8 %{buildroot}/%{_mandir}/man8
%{__install} -p -m 0644 doc/manpages/tgt-admin.8 %{buildroot}/%{_mandir}/man8
%{__install} -p -m 0644 doc/manpages/tgt-setup-lun.8 %{buildroot}/%{_mandir}/man8
%{__install} -p -m 0600 %{SOURCE2} %{buildroot}/etc/sysconfig/tgtd
%{__install} -p -m 0600 %{SOURCE3} %{buildroot}/etc/tgt

pushd usr
%{__make} install DESTDIR=%{buildroot} sbindir=%{_sbindir}


%post
/sbin/chkconfig --add tgtd

%postun
if [ "$1" = "1" ] ; then
     /sbin/service tgtd condrestart > /dev/null 2>&1 || :
fi

%preun
if [ "$1" = "0" ] ; then
     /sbin/chkconfig tgtd stop > /dev/null 2>&1
     /sbin/chkconfig --del tgtd
fi


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-, root, root, -)
%doc README doc/README.iscsi doc/README.iser doc/README.lu_configuration doc/README.mmc
%{_sbindir}/tgtd
%{_sbindir}/tgtadm
%{_sbindir}/tgt-setup-lun
%{_sbindir}/tgt-admin
%{_sbindir}/tgtimg
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_initrddir}/tgtd
%attr(0600,root,root) %config(noreplace) /etc/sysconfig/tgtd
%attr(0600,root,root) %config(noreplace) /etc/tgt/targets.conf


%changelog


* Tue Jan 19 2016 Andy Grover <agrover@redhat.com> - 1.0.24-18
- Add patch to fix #1038326
  * 0028-targets.conf-manpage-should-not-refer-to-Wikipedia.patch

* Mon Nov 2 2015 Andy Grover <agrover@redhat.com> - 1.0.24-17
- Add patches to fix #1186090, #852532, #1136405.
  * 0026-iscsi-fix-leak-of-task-for-delayed-management-reques.patch
  * 0027-Set-ExpCmdSn-and-MaxCmdSn-in-ISCSI_OP_R2T.patch

* Fri Jul 25 2014 Andy Grover <agrover@redhat.com> - 1.0.24-16
- Add patch 0025-fix-checks-when-snprintf-output-is-truncated.patch
  to resolve rhbz #1123438

* Thu Jul 17 2014 Andy Grover <agrover@redhat.com> - 1.0.24-15
- Add patch 0024-Handle-partial-reads-to-mgmt-responses-in-tgtadm.patch
  to resolve rhbz #865960.

* Thu Jul 10 2014 Andy Grover <agrover@redhat.com> - 1.0.24-14
- Add patches for write and verify support, rhbz #1094084
  * 0021-DPO-Add-emulation-of-DPO-bit-for-READ-WRITE-VERIFY10.patch
  * 0022-Add-support-for-WRITEVERIFY10-12-16.patch
  * 0023-sbc-Add-residual-handling-for-WRITE6-10-12-16-and-WR.patch

* Fri Jun 20 2014 Andy Grover <agrover@redhat.com> - 1.0.24-13
- Add patch 0020-workaround-for-pthreads-bug.patch
  for rhbz #848585.

* Wed Apr 30 2014 Andy Grover <agrover@redhat.com> - 1.0.24-12
- Add patch 0019-Fix-race-on-thread-shutdown-causing-deadlock.patch
  for rhbz #848585.

* Mon Mar 24 2014 Andy Grover <agrover@redhat.com> - 1.0.24-11
- Add patch 0018-Fix-segfault-if-device_type-set-to-pt-but-bstype-not.patch
  for rhbz #854123.

* Tue Sep 3 2013 Andy Grover <agrover@redhat.com> - 1.0.24-10
- Update sysconfig.tgtd with commented-out TGTD_OPTIONS

* Tue Sep 3 2013 Andy Grover <agrover@redhat.com> - 1.0.24-9
- Redo patches to use 'git format-patch' naming
- Add more backported patches:
  * 0014-iser-Don-t-wait-until-iser_ib_init-to-init-list_head.patch
  * 0015-iser-cleaning-iser-ib-objects-on-lld-exit.patch
  * 0016-iser-Don-t-release-IB-resources-if-were-not-allocate.patch
  * 0017-Fix-possible-segfault-on-logicalunit-update.patch
  
* Thu Aug 29 2013 Andy Grover <agrover@redhat.com> - 1.0.24-8
- Add patch isns-regression.patch for #865739

* Mon Aug 19 2013 Andy Grover <agrover@redhat.com> - 1.0.24-7
- Fix logic error in fix-task-data-leak.patch

* Sun Aug 11 2013 Andy Grover <agrover@redhat.com> - 1.0.24-6
- Add patch fix-task-data-leak.patch for #813636

* Sat Aug 10 2013 Andy Grover <agrover@redhat.com> - 1.0.24-5
- Fix #922270 by adding TGTD_OPTIONS to daemon exec line in tgt.init

* Fri Aug 2 2013 Andy Grover <agrover@redhat.com> - 1.0.24-4
- Add patches
  * 0001-iser-Fix-bidirectional-chap.patch
  * 0002-bs_aio-use-64bit-to-read-eventfd-counter.patch
  * 0003-iser-added-huge-pages-support.patch
  * 0004-iser-added-parameter-for-pool-size.patch
  * 0005-iser-limit-number-of-CQ-entries-requested.patch
  * 0006-iser-add-CQ-vector-param.patch
  * 0007-Rework-param_set_val-and-friends.patch
  * 0008-return-Reject-in-iscsi-login-text-failure.patch

* Mon May 6 2013 Andy Grover <agrover@redhat.com> - 1.0.24-3
- Add libaio-devel as a BuildReq and libaio as a Req for #910638

* Tue Mar 20 2012 Andy Grover <agrover@redhat.com> - 1.0.24-2
- Add patch
  * scsi-target-utils-discovery-auth.patch

* Tue Mar 6 2012 Andy Grover <agrover@redhat.com> - 1.0.24-1
- Update to upstream 1.0.24 for bugfixes

* Tue Oct 4 2011 Andy Grover <agrover@redhat.com> - 1.0.14-4
- Add patches
  * scsi-target-utils-dont-reparse-conf.patch
  * scsi-target-utils-allow-guids.patch

* Thu Sep 29 2011 Andy Grover <agrover@redhat.com> - 1.0.14-3
- Add patch
  * scsi-target-utils-fix-segfault-on-exit.patch

* Thu Mar 17 2011 Andy Grover <agrover@redhat.com> - 1.0.14-2
- Rebuild for fudged cvs checkin

* Thu Mar 17 2011 Andy Grover <agrover@redhat.com> - 1.0.14-1
- Rebase to upstream 1.0.14
- Update git-sync patch to pull in add'l fixes to 9c1cd78.

* Mon Feb 28 2011 Andy Grover <agrover@redhat.com> - 1.0.13-2
- Resolves: rhbz #677475 Fix semkey and control socket clashes

* Thu Feb 3 2011 Mike Christie <mchristie@redhat.com> - 1.0.13-1
- Drop scsi-target-utils-dynamic-link-iser.patch patch. It turns out
in 6.0 this patch was broken and linked against rdma libs, so
the got brought in by yum. The new patch was not broken and did not
force linking but yum/iser users are not expecting the depencies
to be broken.

* Mon Jan 17 2011 Mike Christie <mchristie@redhat.com> - 1.0.13-0
- Rebase to upstream 1.0.13.
- Add upstream iser target. This requires setting the driver/lld
type to iser. See targets.conf for example or the README.iscsi for
a tgtadm example.
- 616402 read-only support

* Mon Jan 17 2011 Mike Christie <mchristie@redhat.com> - 1.0.4-4
- fix the buffer overflow bug before iscsi login (CVE-2011-0001)

* Thu Jul 8 2010 Mike Christie <mchristie@redhat.com> - 1.0.4-3
- 584426 Make init scripts LSB-compilant

* Tue Jun 29 2010 Mike Christie <mchristie@redhat.com> - 1.0.4-2
- Fix iSNS scn pdu overflows (CVE-2010-2221).

* Fri May 7 2010 Mike Christie <mchristie@redhat.com> - 1.0.4-1
- 589803 Fix iser rpm dependencies

* Wed May 5 2010 Mike Christie <mchristie@redhat.com> - 1.0.4-0
- 587072 Fix tgt-admin logic error with shared accounts in targets.conf 
- Rebase to 1.0.4 to sync fixes.

* Thu Apr 8 2010 Mike Christie <mchristie@redhat.com> - 1.0.1-3
- 576359 Fix format string vulnerability  (CVE-2010-0743)

* Wed Mar 31 2010 Mike Christie <mchristie@redhat.com> - 1.0.1-2
- 578274 - Support iSNS settings in targets.conf

* Mon Feb 8 2010 Mike Christie <mchristie@redhat.com> - 1.0.1-1
- Add spec patch comments.

* Thu Feb 4 2010 Mike Christie <mchristie@redhat.com> - 1.0.1-0
- Rebase to 1.0.1 release, and update spec http references to reflect
project moved to sourceforge.

* Wed Jan 13 2010 Mike Christie <mchristie@redhat.com> - 0.9.11-1.20091205snap
- 549683 Rebuild for RHEL-6

* Mon Dec 21 2009 Hans de Goede <hdegoede@redhat.com> - 0.9.11-1.20091205snap
- Rebase to 0.9.11 + some fixes from git (git id
  97832d8dcd00202a493290b5d134b581ce20885c)
- Rewrite initscript, make it follow:
  http://fedoraproject.org/wiki/Packaging/SysVInitScript
  And merge in RHEL-5 initscript improvements:
  - Parse /etc/tgt/targets.conf, which allows easy configuration of targets
  - Better initiator status checking in stop
  - Add force-stop, to stop even when initiators are still connected
  - Make reload reload configuration from /etc/tgt/targets.conf without
    stopping tgtd (but only for unused targets)
  - Add force-reload (reloads configs for all targets including busy ones)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.5-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 16 2009 Terje Rosten <terje.rosten@ntnu.no> - 0.9.5-1
- 0.9.5
- remove patch now upstream
- add patch to fix mising destdir in usr/Makefile
- mktape and dump_tape has moved to tgtimg
- add more docs

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.9.2-2
- rebuild with new openssl

* Tue Dec 16 2008 Jarod Wilson <jarod@redhat.com> - 0.9.2-1
- update to 0.9.2 release

* Tue Oct 21 2008 Terje Rosten <terje.rosten@ntnu.no> - 0.0-6.20080805snap
- add tgt-admin man page, tgt-admin and tgt-core-test

* Fri Aug 22 2008 Terje Rosten <terje.rosten@ntnu.no> - 0.0-5.20080805snap
- update to 20080805 snapshot

* Sun Feb 10 2008 Terje Rosten <terje.rosten@ntnu.no> - 0.0-4.20071227snap
- update to 20071227 snapshot
- add patch to compile with newer glibc

* Sat Feb  9 2008 Terje Rosten <terje.rosten@ntnu.no> - 0.0-3.20070803snap
- rebuild

* Sun Dec 9 2007 Alex Lancaster <alexlan[AT]fedoraproject.org> - 0.0-2.20070803snap
- rebuild for new openssl soname bump

* Wed Sep 26 2007 Terje Rosten <terje.rosten@ntnu.no> - 0.0-1.20070803snap
- random cleanup

* Wed Sep 26 2007 Terje Rosten <terje.rosten@ntnu.no> - 0.0-0.20070803snap
- update to 20070803
- fix license tag
- use date macro
- build with correct flags (%%optflags)

* Tue Jul 10 2007 Mike Christie <mchristie@redhat.com> - 0.0-0.20070620snap
- first build
