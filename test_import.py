import sys
import os
sys.path.append(os.getcwd())
sys.path.append("/home/ubuntu/.cache/bazel/_bazel_ubuntu/239ae1ce73be6bae0635c62c3844b6fc/external/pypi_numpy/site-packages")
try:
    from pycoral.pybind import _pywrap_coral
    print("SUCCESS: _pywrap_coral imported correctly.")
except ImportError as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
