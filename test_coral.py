import sys
import os

# Add the directory containing the .so to sys.path
sys.path.append(os.path.join(os.getcwd(), 'bazel-bin', 'src'))
# Add hermetic numpy
sys.path.append('/home/ubuntu/.cache/bazel/_bazel_ubuntu/239ae1ce73be6bae0635c62c3844b6fc/external/pypi_numpy/site-packages')

try:
    import _pywrap_coral
    print("SUCCESS: _pywrap_coral imported successfully!")
    
    devices = _pywrap_coral.ListEdgeTpus()
    print(f"Detected Edge TPUs: {devices}")
    
    version = _pywrap_coral.GetRuntimeVersion()
    print(f"Runtime Version: {version}")

except Exception as e:
    print(f"FAILURE: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
