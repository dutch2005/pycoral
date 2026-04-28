# PyCoral Modernization Wiki

Welcome to the modernized PyCoral project. This guide is designed to be **dummy-proof**. Whether you are a seasoned engineer or a hobbyist, follow these steps to get your Google Coral Edge TPU working with the latest C++23/Python 3.12 driver.

---

## 🚀 Quick Start (TL;DR)

If you just want it to work and don't care about the internals:
1. **Remove the old driver** (See [Uninstalling Legacy Drivers](#1-uninstalling-legacy-drivers)).
2. **Download the latest release** from the "Releases" page.
3. **Install the `.whl` file**: `pip install pycoral-2.0.0-cp312-cp312-linux_x86_64.whl`.
4. **Setup Permissions**: `sudo usermod -aG plugdev $USER` (Reboot after this).

---

## 1. Uninstalling Legacy Drivers

**CRITICAL**: The new driver is self-contained. If you have the old `libedgetpu1-std` or legacy `python3-pycoral` installed, they **WILL** conflict with the new version.

### Step-by-Step Removal:
```bash
# 1. Remove legacy Python package
sudo apt-get remove --purge python3-pycoral pycoral

# 2. Remove legacy system library
sudo apt-get remove --purge libedgetpu1-std libedgetpu1-max

# 3. Clean up package manager leftovers
sudo apt-get autoremove -y
```

---

## 2. Hardware Setup & Permissions

The Edge TPU requires specific permissions to be accessed by a non-root user.

### For USB Accelerators:
First, ensure your user is in the `plugdev` group:
```bash
sudo usermod -aG plugdev $USER
```

Second, ensure the USB udev rules exist on your system so the OS knows to hand the device to the `plugdev` group. Run this to generate the rule:
```bash
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="1a6e", ATTRS{idProduct}=="089a", MODE="0664", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-edgetpu-accelerator.rules > /dev/null
sudo udevadm control --reload-rules && sudo udevadm trigger
```
**You MUST log out and log back in (or reboot) for the group changes to take effect.**

### For PCIe Accelerators (M.2 / Mini PCIe):
The PCIe driver is part of the Linux kernel or provided by `apex-dkms`. Ensure it is loaded:
```bash
lsmod | grep apex
```
If nothing shows up, you may need to install the apex driver:
```bash
sudo apt-get install apex-dkms
```

---

## 3. Installation Guide

### Option A: Using Pre-built Wheels (Recommended)
1. Go to the **GitHub Releases** page.
2. Download the `.whl` file matching your architecture (AMD64 or ARM64) and Python version.
3. Install it directly into your virtual environment:
   ```bash
   pip3 install path/to/pycoral-2.0.0-cp312-cp312-linux_x86_64.whl
   ```

### Option B: Using Debian PPA (Ubuntu/Debian)
*(Note: PPA infrastructure is currently under construction. Please use Option A for now.)*
```bash
# COMING SOON
# sudo add-apt-repository ppa:dutch2005/pycoral-modernized
# sudo apt-get update
# sudo apt-get install python3-pycoral-modern
```

---

## 4. Verifying the Installation

We provide a specialized script to verify that the C++23 bindings are communicating with the hardware correctly.

```bash
# Clone the repo (if you haven't)
git clone https://github.com/dutch2005/pycoral.git
cd pycoral

# Run the validation
python3 verify_hardware.py --model test_data/mobilenet_v2_1.0_224_quant_edgetpu.tflite
```

**Success Message**: 
`SUCCESS: Inference completed in XX.X ms. Hardware is responding correctly.`

---

## 5. Troubleshooting (FAQ)

### Q: "ModuleNotFoundError: No module named 'pycoral.pybind._pywrap_coral'"
**A**: You likely installed the wrong wheel for your Python version. Run `python3 --version` and ensure it matches the `cp312` (for 3.12) or `cp311` (for 3.11) tag in the filename.

### Q: "ValueError: Failed to load delegate from libedgetpu.so.1"
**A**: The new version **DOES NOT** use `libedgetpu.so.1` (it's statically linked). This error usually means you have legacy code trying to load the library manually. Update your code to use `edgetpu.make_interpreter(model_path)`.

### Q: "RuntimeError: Node number 0 (EdgeTpuDelegateForCustomOp) failed to prepare."
**A**: This is almost always a permission issue. Ensure your user is in the `plugdev` group, the udev rules are installed (see Section 2), and you have rebooted.

---

## 6. Building from Source (For Developers)

If you want to modify the C++23 code and rebuild the hermetic wheel:

### Ensure dependencies are met:
You need `make`, `gcc`, `g++`, and Python 3.12 headers installed on your system.

### Run the Hermetic Build:
The modernized build system uses `rules_python` to handle the heavy lifting.
```bash
export TF_PYTHON_VERSION=3.12
bazel build //src:_pywrap_coral.so
```

### Locate the Wheel:
Once Bazel finishes compiling the static libraries, you can generate your `.whl` file using `setup.py`.
*(Note: Automated wheel generation via `bazel build //pycoral:wheel` is coming in a future update.)*

---

## 7. Bug Reports & Support

Since this is a public community-driven project, your feedback is vital.

- **Found a Bug?** Open an issue with the [BUG] prefix.
- **Hardware not detected?** Attach the output of `lsusb` or `lspci -v`.
- **Latency Issues?** Provide the logs from `verify_hardware.py`.

---

*Documentation maintained by the PyCoral Modernization Team.*
