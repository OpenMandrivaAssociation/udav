Name:		udav
Version:	0.6
Release:	%mkrel 3
Summary:	Fast and interactive data plotting based on MathGL
Group:		Sciences/Mathematics
License:	GPLv2+
Url:		http://udav.sourceforge.net/
Source0:	http://downloads.sourceforge.net/udav/%{name}-%{version}.tgz
Patch0:		udav-0.6-mdv-fix-desktop-file.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	qt4-devel
BuildRequires:	mathgl-devel
BuildRequires:	hdf5-devel
BuildRequires:	imagemagick

%description
UDAV is cross-platform program for data arrays visualization based on
MathGL library. It support wide spectrum of graphics, simple script 
language and visual data handling and editing. It has window 
interface for data viewing, changing and plotting. Also it can 
execute MGL scripts, setup and rotate graphics and so on.

%files
%defattr(-,root,root,-)
%doc ChangeLog.txt TODO
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}*
%{_mandir}/man1/%{name}*

#-------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1

# fix paths in src.pro
sed -i	-e 's:\$(MGLDOCDIR):%{_defaultdocdir}/%{name}:' \
	-e 's:/usr/local:%{_prefix}:g' \
	-e 's:icon.path = %{_prefix}/share/udav/:icon.path = %{_iconsdir}/hicolor/64x64/apps/:' \
	src/src.pro

%build
# DEFINES+=H5_USE_16_API is needed to compile with HDF5 1.8
%qmake_qt4 DEFINES+=H5_USE_16_API
%make

%install
rm -rf %{buildroot}
make INSTALL_ROOT=%{buildroot} install

# convert and install icon in other sizes
for size in 16x16 32x32 48x48; do
  install -d %{buildroot}%{_iconsdir}/hicolor/$size/apps
  convert -resize $size src/%{name}.png %{buildroot}%{_iconsdir}/hicolor/$size/apps/%{name}.png
done

# install man page
install -d %{buildroot}%{_mandir}/man1
install -D -m 0644 %{name}.1 %{buildroot}%{_mandir}/man1

%clean
rm -rf %{buildroot}
