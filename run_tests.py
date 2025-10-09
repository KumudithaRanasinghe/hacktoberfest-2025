# Test runner script for the Hacktoberfest Project Tracker

import os
import sys
import subprocess

def main():
    """Run all tests for the project."""
    print("🧪 Running Hacktoberfest 2025 Project Tracker Tests")
    print("=" * 60)
    
    # Add src directory to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(project_root, "src")
    sys.path.insert(0, src_path)
    
    try:
        # Try to import pytest
        import pytest
        
        # Run pytest with verbose output
        print("Running tests with pytest...")
        test_dir = os.path.join(project_root, "tests")
        exit_code = pytest.main([test_dir, "-v", "--tb=short"])
        
        if exit_code == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Some tests failed (exit code: {exit_code})")
        
        return exit_code
        
    except ImportError:
        print("⚠️  pytest not found. Running basic tests manually...")
        return run_basic_tests()

def run_basic_tests():
    """Run basic tests without pytest."""
    try:
        # Import test module
        from tests.test_project_tracker import TestContributor, TestProjectTracker
        
        # Run basic tests manually
        test_contributor = TestContributor()
        test_tracker = TestProjectTracker()
        
        print("\n🧪 Running Contributor tests...")
        test_methods = [method for method in dir(test_contributor) if method.startswith('test_')]
        
        for method_name in test_methods:
            try:
                print(f"  Running {method_name}...")
                getattr(test_contributor, method_name)()
                print(f"  ✅ {method_name} passed")
            except Exception as e:
                print(f"  ❌ {method_name} failed: {e}")
                return 1
        
        print("\n🧪 Running ProjectTracker tests...")
        tracker_methods = [method for method in dir(test_tracker) if method.startswith('test_')]
        
        for method_name in tracker_methods:
            try:
                print(f"  Running {method_name}...")
                # Set up method if it exists
                if hasattr(test_tracker, 'setup_method'):
                    test_tracker.setup_method()
                
                getattr(test_tracker, method_name)()
                print(f"  ✅ {method_name} passed")
                
                # Tear down method if it exists
                if hasattr(test_tracker, 'teardown_method'):
                    test_tracker.teardown_method()
                    
            except Exception as e:
                print(f"  ❌ {method_name} failed: {e}")
                if hasattr(test_tracker, 'teardown_method'):
                    test_tracker.teardown_method()
                return 1
        
        print("\n✅ All basic tests passed!")
        return 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)