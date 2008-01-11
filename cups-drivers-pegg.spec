Summary:	CUPS printer drivers for Casio USB label printers
Name:		cups-drivers-pegg
Version:	0.23
Release:	%mkrel 4
License:	GPL
Group:		System/Printing
URL:		http://www.tu-harburg.de/~soda0231/pegg/pegg.html
# the http://www.tu-harburg.de/~soda0231/pegg/files/ resource is gone
Source0:	pegg-0.23.tar.bz2
Source1:	xbm2crw-0.4.tar.bz2
Source2:	cups2pegg-0.21a.tar.bz2
Source3:	pegg_el-0.11.tar.bz2
Requires:	ImageMagick
Requires:	cups
BuildRequires:	libusb-devel
Conflicts:	cups-drivers = 2007
Conflicts:	printer-utils = 2007
Conflicts:	printer-filters = 2007
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
CUPS printer drivers for  Casio USB label printers.

This package contains CUPS drivers (PPD) for the following printers:

 o CASIO Computer CO. LTD. EL-700 EL-5000W
 o CASIO Computer CO. LTD. KL-P1000 KL-E11
 o CASIO Computer CO. LTD. KP-C10 KP-C50

%prep

%setup -q -c -T -n %{name}-%{version} -a0 -a1 -a2 -a3

# gunzip the man pages
find -name "*.1.gz" | xargs gunzip

%build

%make -C pegg-* CFLAGS="%{optflags}" LIB_PATH="%{_libdir}"

%make -C pegg_el-*/src CFLAGS="%{optflags}" LIB_PATH="%{_libdir}"

# Suppress logging in cups2pegg backend
perl -p -i -e "s:/var/log/cups/cups2pegg.log:/dev/null:" cups2pegg*/src/cups2pegg

# Fix PPD file
perl -p -i -e 's/^(\*ModelName:).*$/$1 "CASIO Computer CO. LTD. EL-700 EL-5000W"/' cups2pegg-*/src/ppd/casio_el.ppd
perl -p -i -e 's/^(\*ShortNickName:).*$/$1 "CASIO EL-700 EL-5000W"/' cups2pegg-*/src/ppd/casio_el.ppd
perl -p -i -e 's/^(\*ModelName:).*$/$1 "CASIO Computer CO. LTD. KL-P1000 KL-E11"/' cups2pegg-*/src/ppd/casio_kl.ppd
perl -p -i -e 's/^(\*ShortNickName:).*$/$1 "CASIO KL-P1000 KL-E11"/' cups2pegg-*/src/ppd/casio_kl.ppd
perl -p -i -e 's/: Letter/: 128_64/' cups2pegg-*/src/ppd/casio_kl.ppd
perl -p -i -e 's/^(\*ModelName:).*$/$1 "CASIO Computer CO. LTD. KP-C10 KP-C50"/' cups2pegg-*/src/ppd/casio_kp.ppd
perl -p -i -e 's/^(\*ShortNickName:).*$/$1 "CASIO KP-C10 KP-C50"/' cups2pegg-*/src/ppd/casio_kp.ppd
perl -p -i -e 's/: Letter/: 512_64/' cups2pegg-*/src/ppd/casio_kp.ppd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_prefix}/lib/cups/backend
install -d %{buildroot}%{_datadir}/cups/model/pegg
install -d %{buildroot}%{_mandir}/man1

install -m0755 pegg-*/pegg %{buildroot}%{_bindir}/
install -m0755 pegg_el-*/src/pegg_el %{buildroot}%{_bindir}/
install -m0755 xbm2crw*/xbm2crw %{buildroot}%{_bindir}/
install -m0755 cups2pegg*/src/cups2pegg %{buildroot}%{_prefix}/lib/cups/backend/
install -m0644 pegg-*/pegg.1 %{buildroot}%{_mandir}/man1/
install -m0644 pegg_el-*/src/pegg_el.1 %{buildroot}%{_mandir}/man1/
install -m0644 cups2pegg-*/src/ppd/*.ppd* %{buildroot}%{_datadir}/cups/model/pegg/

rm -rf installed_docs
mkdir -p installed_docs/{pegg_el,xbm2crw,cups2pegg}
cp pegg_el-*/README pegg_el-*/TODO pegg_el-*/INSTALL installed_docs/pegg_el/
cp xbm2crw-*/README installed_docs/xbm2crw/
cp cups2pegg-*/*.png cups2pegg-*/*.html installed_docs/cups2pegg/

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc pegg-*/CHANGELOG pegg-*/README pegg-*/LICENSE pegg-*/INSTALL installed_docs/*
%attr(0755,root,root) %{_bindir}/pegg
%attr(0755,root,root) %{_bindir}/pegg_el
%attr(0755,root,root) %{_bindir}/xbm2crw
%attr(0755,root,root) %{_prefix}/lib/cups/backend/cups2pegg
%attr(0755,root,root) %dir %{_datadir}/cups/model/pegg
%attr(0644,root,root) %{_datadir}/cups/model/pegg/*.ppd*
%attr(0644,root,root) %{_mandir}/man1/pegg*.1*
