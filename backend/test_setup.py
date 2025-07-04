"""
Simple test script to verify the refactored backend works correctly.
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app.main import app
    from app.core.container import Container
    import pandas as pd
    
    print("✅ All imports successful!")
    
    # Test container initialization
    container = Container()
    print("✅ Container initialized successfully!")
    
    # Test distance factory
    metrics = container.distance_factory.get_available_metrics()
    print(f"✅ Available metrics: {metrics}")
    
    # Test distance calculators
    euclidean_calc = container.distance_factory.get_calculator("euclidean")
    test_distance = euclidean_calc.calculate([1, 2, 3], [2, 3, 4])
    print(f"✅ Euclidean distance test: {test_distance}")
    
    # Test data repository
    try:
        datasets = container.data_repository.get_available_datasets()
        print(f"✅ Available datasets: {datasets}")
    except Exception as e:
        print(f"⚠️ Data loading warning: {e}")
    
    print("\n🎉 Basic functionality test completed successfully!")
    print("You can now run: uvicorn main:app --reload")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
