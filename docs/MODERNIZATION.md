# PyCoral Modernization: Technical Documentation

This document details the architectural and code-level changes made to modernize the Google Coral Edge TPU Python bindings for modern systems (Ubuntu 24.04, Python 3.12, C++23).

For installation and usage instructions, please refer to the [Project Wiki](WIKI.md).

## 1. Build System Modernization

### Hermetic Python & NumPy
Legacy `pycoral` relied on `local_config_python`, which attempted to find Python headers and NumPy on the host system. This is notoriously brittle across different Linux distributions.
**New Approach**: We use `rules_python` and `pip_parse` to:
- Download a standalone Python 3.12 interpreter.
- Fetch NumPy as a Bazel-managed dependency.
- Generate a `cc_library` target for NumPy headers automatically.

### Workspace Stabilization
- **Cycle Resolution**: Fixed a circular dependency between `libedgetpu` and `pycoral` by reordering workspace declarations.
- **Static Linking**: The Python extension (`_pywrap_coral.so`) is now linked statically against `libedgetpu`. This eliminates the runtime dependency on `/usr/lib/libedgetpu.so.1`.

## 2. C++23 Standards & Best Practices

The codebase has been upgraded from C++17 to **C++23**. Key improvements include:

### Modern Abstractions
- **`std::span` (C++20)**: Replaced `absl::Span` and raw pointer/size pairs to provide safe, view-only access to contiguous memory.
- **`std::expected` (C++23)**: Replaced complex error-code-based logic with `std::expected<T, E>` for idiomatic error handling.
- **`std::format` (C++20/23)**: Replaced legacy string concatenation and `absl::Substitute` with type-safe, performant string formatting.
- **Ranges & Views**: Modernized loops and data processing using the `<ranges>` library.

### Memory Safety & RAII
- Removed manual `malloc`/`free` calls in quantization parameter copying.
- Replaced raw pointers with `std::unique_ptr` and `std::shared_ptr` where ownership is involved.
- Used `std::string_view` for efficient, non-owning string operations.

## 3. Portability (Windows & Linux)

The new build architecture is designed with cross-platform support in mind:
- **Abstracted I/O**: Switched to `std::filesystem` for all path manipulations.
- **Universal Drivers**: The move towards `libusb` as a primary communication layer (via `darwinn_portable`) improves consistency between Windows and Linux.
- **Hermeticity**: Because the build manages its own compilers and toolchains, the "it works on my machine" problem is virtually eliminated.

## 4. Why the legacy build was "hacky"?
The original build was created during the transition period of Bazel (0.x to 1.x) and TFLite. It relied on:
1.  **Global state**: Assumed fixed paths like `/usr/include/tensorflow`.
2.  **Exported internal tools**: Many build scripts were mirrors of internal Google tools that didn't translate perfectly to the public ecosystem.
3.  **Manual patching**: Frequently required `sed` hacks during the build process to fix version mismatches.

Our modernization removes these hacks in favor of **Declarative Architecture** and **Hermetic Sandboxing**.

## 5. Packaging & Distribution

The modernized project is designed for broad distribution:
- **Hermetic Wheels**: Self-contained wheels with static `libedgetpu`.
- **Debian/PPA**: Full support for `apt` distribution (COMING SOON).
- **RPM**: Support for `yum`/`dnf` based systems.
- **CI/CD**: Fully automated builds via GitHub Actions for multi-architecture (AMD64/ARM64) and multi-version Python (3.10-3.14+).
