Summary:	CUPS printer drivers for Casio USB label printers
Name:		cups-drivers-pegg
Version:	0.23
Release:	16
License:	GPLv2
Group:		System/Printing
URL:		http://www.tu-harburg.de/~soda0231/pegg/pegg.html
# the http://www.tu-harburg.de/~soda0231/pegg/files/ resource is gone
Source0:	pegg-0.23.tar.bz2
Source1:	xbm2crw-0.4.tar.bz2
Source2:	cups2pegg-0.21a.tar.bz2
Source3:	pegg_el-0.11.tar.bz2
Patch0:		cups-drivers-pegg-0.23-LDFLAGS.diff

BuildRequires:	pkgconfig(libusb)
Requires:	cups
Requires:	imagemagick

%description
CUPS printer drivers for  Casio USB label printers.

This package contains CUPS drivers (PPD) for the following printers:

 o CASIO Computer CO. LTD. EL-700 EL-5000W
 o CASIO Computer CO. LTD. KL-P1000 KL-E11
 o CASIO Computer CO. LTD. KP-C10 KP-C50

%prep
%setup -q -c -T -n %{name}-%{version} -a0 -a1 -a2 -a3
%patch0 -p1

# gunzip the man pages
find -name "*.1.gz" | xargs gunzip

%build
%make -C pegg-* CFLAGS="%{optflags}" LIB_PATH="%{_libdir}" LDFLAGS="%{ldflags}"

%make -C pegg_el-*/src CFLAGS="%{optflags}" LIB_PATH="%{_libdir}" LDFLAGS="%{ldflags}"

# Suppress logging in cups2pegg backend
sed -i -e "s:/var/log/cups/cups2pegg.log:/dev/null:" cups2pegg*/src/cups2pegg

# Fix PPD file
sed -i -e 's/^(\*ModelName:).*$/$1 "CASIO Computer CO. LTD. EL-700 EL-5000W"/' cups2pegg-*/src/ppd/casio_el.ppd
sed -i -e 's/^(\*ShortNickName:).*$/$1 "CASIO EL-700 EL-5000W"/' cups2pegg-*/src/ppd/casio_el.ppd
sed -i -e 's/^(\*ModelName:).*$/$1 "CASIO Computer CO. LTD. KL-P1000 KL-E11"/' cups2pegg-*/src/ppd/casio_kl.ppd
sed -i -e 's/^(\*ShortNickName:).*$/$1 "CASIO KL-P1000 KL-E11"/' cups2pegg-*/src/ppd/casio_kl.ppd
sed -i -e 's/: Letter/: 128_64/' cups2pegg-*/src/ppd/casio_kl.ppd
sed -i -e 's/^(\*ModelName:).*$/$1 "CASIO Computer CO. LTD. KP-C10 KP-C50"/' cups2pegg-*/src/ppd/casio_kp.ppd
sed -i -e 's/^(\*ShortNickName:).*$/$1 "CASIO KP-C10 KP-C50"/' cups2pegg-*/src/ppd/casio_kp.ppd
sed -i -e 's/: Letter/: 512_64/' cups2pegg-*/src/ppd/casio_kp.ppd

%install
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

%files
%doc pegg-*/CHANGELOG pegg-*/README pegg-*/LICENSE pegg-*/INSTALL installed_docs/*
%{_bindir}/pegg
%{_bindir}/pegg_el
%{_bindir}/xbm2crw
%{_prefix}/lib/cups/backend/cups2pegg
%dir %{_datadir}/cups/model/pegg
%{_datadir}/cups/model/pegg/*.ppd*
%{_mandir}/man1/pegg*.1*

