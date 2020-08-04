%undefine __cmake_in_source_build

Name:           svt-hevc
Version:        1.5.0
Release:        1%{?dist}
Summary:        Scalable Video Technology for HEVC Encoder

License:        BSD-2-Clause-Patent
URL:            https://github.com/OpenVisualCloud/SVT-HEVC
Source0:        %url/archive/v%{version}/SVT-HEVC-%{version}.tar.gz
# Correct build flags and gstreamer plugin
Patch0:         svt-hevc-build.patch

BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  yasm
BuildRequires:  meson
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

ExclusiveArch:  x86_64

%description
The Scalable Video Technology for HEVC Encoder (SVT-HEVC Encoder) is an
HEVC-compliant encoder library core that achieves excellent density-quality
tradeoffs, and is highly optimized for Intel® Xeon™ Scalable Processor and
Xeon™ D processors.

%package        libs
Summary:        Libraries for svt-hevc

%description    libs
Libraries for development svt-hevc.

%package        devel
Summary:        Include files and mandatory libraries for development svt-hevc
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
Include files and mandatory libraries for development svt-hevc.

%package -n     gstreamer1-%{name}
Summary:        GStreamer 1.0 %{name}-based plug-in
Requires:       gstreamer1-plugins-base%{?_isa}

%description -n gstreamer1-%{name}
This package provides %{name}-based GStreamer plug-in.

%prep
%autosetup -p1 -n SVT-HEVC-%{version}


%build
%cmake -G Ninja \
%if 0%{?rhel} && 0%{?rhel} > 7
 -B %{_target_platform} -S .
%endif

%ninja_build -C %{_target_platform}

pushd gstreamer-plugin
    export LIBRARY_PATH="$PWD/../Bin/Release:$LIBRARY_PATH"
    %meson
    %meson_build
popd


%install
%ninja_install -C %{_target_platform}
pushd gstreamer-plugin
    %meson_install
popd

%files
%{_bindir}/SvtHevcEncApp

%files libs
%license LICENSE.md
%doc README.md Docs/svt-hevc_encoder_user_guide.md
%{_libdir}/libSvtHevcEnc.so.1*

%files devel
%{_includedir}/%{name}
%{_libdir}/libSvtHevcEnc.so
%{_libdir}/pkgconfig/*.pc

%files -n gstreamer1-%{name}
%{_libdir}/gstreamer-1.0/libgstsvthevcenc.so

%changelog
* Tue Aug 04 2020 Vasiliy Glazov <vascom2@gmail.com> - 1.5.0-1
- Update to 1.5.0

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Vasiliy Glazov <vascom2@gmail.com> - 1.4.3-1
- Update to 1.4.3

* Tue Sep 17 2019 Vasiliy Glazov <vascom2@gmail.com> - 1.4.1-2
- Correct build gstreamer plugin

* Tue Sep 17 2019 Vasiliy Glazov <vascom2@gmail.com> - 1.4.1-1
- Initial release
