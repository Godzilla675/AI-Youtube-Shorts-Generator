#!/usr/bin/env python3
"""
Comprehensive test runner for AI Youtube Shorts Generator
Runs all test suites and generates a summary report
"""
import unittest
import sys
import os
from io import StringIO

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def run_all_tests():
    """Run all test suites and generate a summary"""
    
    # Test modules to run
    test_modules = [
        'tests.test_youtube_downloader',
        'tests.test_edit',
        'tests.test_transcription',
        'tests.test_language_tasks',
        'tests.test_gemini_vision',
        'tests.test_face_crop',
        'tests.test_speaker',
        'tests.test_main',
    ]
    
    print("=" * 70)
    print("AI YouTube Shorts Generator - Comprehensive Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Load all test modules
    for module_name in test_modules:
        try:
            module_tests = loader.loadTestsFromName(module_name)
            suite.addTests(module_tests)
            print(f"✓ Loaded tests from {module_name}")
        except Exception as e:
            print(f"✗ Failed to load {module_name}: {e}")
    
    print()
    print("=" * 70)
    print("Running Tests...")
    print("=" * 70)
    print()
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)
    
    # Return exit code
    if result.wasSuccessful():
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1


def run_specific_module(module_name):
    """Run tests for a specific module"""
    print(f"Running tests for: {module_name}")
    print("=" * 70)
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(f'tests.{module_name}')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific test module
        module_name = sys.argv[1]
        exit_code = run_specific_module(module_name)
    else:
        # Run all tests
        exit_code = run_all_tests()
    
    sys.exit(exit_code)
