import argparse
import time
import numpy as np
from PIL import Image
from pycoral.adapters import classify
from pycoral.adapters import common
from pycoral.utils import edgetpu

def main():
    parser = argparse.ArgumentParser(description='Verify Coral TPU Hardware Inference')
    parser.add_argument('--model', help='Path to TFLite model file', 
                        default='test_data/mobilenet_v2_1.0_224_quant_edgetpu.tflite')
    parser.add_argument('--image', help='Path to image file', 
                        default='test_data/cat.bmp')
    parser.add_argument('--count', type=int, help='Number of inferences', default=100)
    args = parser.parse_args()

    import os
    if not os.path.exists(args.model):
        print(f'Error: Model file {args.model} not found.')
        exit(1)
    if not os.path.exists(args.image):
        print(f'Error: Image file {args.image} not found.')
        exit(1)

    try:
        # 1. Load the Edge TPU Delegate and create interpreter
        interpreter = edgetpu.make_interpreter(args.model)
        interpreter.allocate_tensors()
        
        # 2. Prepare the input image
        size = common.input_size(interpreter)
        # Use Image.Resampling.LANCZOS or NEAREST for modern Pillow
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.ANTIALIAS
            
        image = Image.open(args.image).convert('RGB').resize(size, resample)
        common.set_input(interpreter, image)
        
        print('Initial inference to warm up...')
        interpreter.invoke()
        
        # 3. Benchmark loop
        print(f'Running {args.count} inferences...')
        latencies = []
        for _ in range(args.count):
            start = time.perf_counter()
            interpreter.invoke()
            latencies.append(time.perf_counter() - start)
            
        # 4. Process results
        classes = classify.get_classes(interpreter, top_k=1)
        for c in classes:
            print(f'Top Result: ID={c.id}, Score={c.score:.2f}')
            
        avg_latency = np.mean(latencies) * 1000
        std_latency = np.std(latencies) * 1000
        print(f'Average Latency: {avg_latency:.2f} ms')
        print(f'Std Dev Latency: {std_latency:.2f} ms')
        print('--- Hardware Validation Success ---')
        
    except Exception as e:
        print(f'--- Hardware Validation FAILED ---')
        print(f'Error: {e}')
        exit(1)

if __name__ == '__main__':
    main()
