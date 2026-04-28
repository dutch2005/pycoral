Name:           python3-pycoral
Version:        2.0.0
Release:        1%{?dist}
Summary:        Python API for Coral Edge TPU

License:        Apache-2.0
URL:            https://github.com/google-coral/pycoral
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  gcc-c++
BuildRequires:  libusb1-devel

Requires:       python3-numpy >= 1.16.0
Requires:       python3-tflite-runtime >= 2.14.0

%description
The PyCoral library is a set of Python APIs for the Coral Edge TPU.
It provides high-level abstractions for inference, model pipelining, and on-device training.

%prep
%autosetup

%build
# Note: Bazel build is expected to be done prior to rpmbuild or triggered here.
# For simplicity, we assume the wheel is already built or we use setup.py.
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.md
%{python3_sitearch}/pycoral/
%{python3_sitearch}/pycoral-*.egg-info/

%changelog
* Tue Apr 28 2026 Antigravity <antigravity@google.com> - 2.0.0-1
- Modernized for C++23 and Python 3.12.
- Static linking of libedgetpu.
