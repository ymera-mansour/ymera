#!/usr/bin/env python3
"""
Unit tests for the Cloud Agent Delegation Framework
"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloud_agent_delegate import CloudAgentDelegate, TaskType


class TestCloudAgentDelegate(unittest.TestCase):
    """Test cases for CloudAgentDelegate class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.delegate = CloudAgentDelegate()
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_delegate_initialization(self):
        """Test that CloudAgentDelegate can be initialized."""
        self.assertIsInstance(self.delegate, CloudAgentDelegate)
        self.assertIsNotNone(self.delegate.config_path)
        self.assertTrue(os.path.exists(self.delegate.reports_dir))
    
    def test_unzip_nonexistent_file(self):
        """Test unzip with non-existent file."""
        result = self.delegate.delegate_task(
            TaskType.UNZIP,
            "nonexistent.zip"
        )
        self.assertEqual(result['status'], 'error')
        self.assertIn('not found', result['message'].lower())
    
    def test_unzip_empty_file(self):
        """Test unzip with empty file."""
        empty_zip = os.path.join(self.test_dir, "empty.zip")
        Path(empty_zip).touch()
        
        result = self.delegate.delegate_task(
            TaskType.UNZIP,
            empty_zip
        )
        self.assertEqual(result['status'], 'error')
        self.assertIn('empty', result['message'].lower())
        self.assertIn('recommendation', result)
    
    def test_organize_nonexistent_path(self):
        """Test organize with non-existent path."""
        result = self.delegate.delegate_task(
            TaskType.ORGANIZE,
            "/nonexistent/path"
        )
        self.assertEqual(result['status'], 'error')
        self.assertIn('not found', result['message'].lower())
    
    def test_organize_empty_directory(self):
        """Test organize with empty directory."""
        result = self.delegate.delegate_task(
            TaskType.ORGANIZE,
            self.test_dir
        )
        self.assertEqual(result['status'], 'success')
        self.assertIn('categories', result)
        self.assertEqual(sum(result['categories'].values()), 0)
    
    def test_organize_with_files(self):
        """Test organize with various file types."""
        # Create test files
        test_files = [
            "test.py",
            "readme.md",
            "config.yaml",
            "data.txt"
        ]
        for filename in test_files:
            Path(os.path.join(self.test_dir, filename)).touch()
        
        result = self.delegate.delegate_task(
            TaskType.ORGANIZE,
            self.test_dir
        )
        self.assertEqual(result['status'], 'success')
        self.assertIn('categories', result)
        self.assertGreater(sum(result['categories'].values()), 0)
        
        # Check that files were categorized
        categories = result['categories']
        self.assertGreater(categories['source_code'], 0)
        self.assertGreater(categories['documentation'], 0)
        self.assertGreater(categories['configs'], 0)
    
    def test_review_nonexistent_path(self):
        """Test review with non-existent path."""
        result = self.delegate.delegate_task(
            TaskType.REVIEW,
            "/nonexistent/path"
        )
        self.assertEqual(result['status'], 'error')
        self.assertIn('not found', result['message'].lower())
    
    def test_review_empty_directory(self):
        """Test review with empty directory."""
        result = self.delegate.delegate_task(
            TaskType.REVIEW,
            self.test_dir
        )
        self.assertEqual(result['status'], 'success')
        self.assertIn('review', result)
        self.assertEqual(result['review']['files_reviewed'], 0)
    
    def test_review_with_code_files(self):
        """Test review with code files."""
        # Create test code files
        py_file = os.path.join(self.test_dir, "test.py")
        with open(py_file, 'w') as f:
            f.write("def hello():\n    print('Hello')\n")
        
        result = self.delegate.delegate_task(
            TaskType.REVIEW,
            self.test_dir
        )
        self.assertEqual(result['status'], 'success')
        self.assertIn('review', result)
        self.assertGreater(result['review']['files_reviewed'], 0)
        self.assertIn('suggestions', result['review'])
    
    def test_test_nonexistent_path(self):
        """Test test execution with non-existent path."""
        result = self.delegate.delegate_task(
            TaskType.TEST,
            "/nonexistent/path"
        )
        self.assertEqual(result['status'], 'error')
        self.assertIn('not found', result['message'].lower())
    
    def test_test_task(self):
        """Test test execution."""
        result = self.delegate.delegate_task(
            TaskType.TEST,
            self.test_dir
        )
        self.assertEqual(result['status'], 'success')
        self.assertIn('test_results', result)
    
    def test_report_generation(self):
        """Test report generation."""
        result = self.delegate.delegate_task(
            TaskType.REPORT,
            self.test_dir,
            format="detailed"
        )
        self.assertEqual(result['status'], 'success')
        self.assertIn('report_path', result)
        self.assertTrue(os.path.exists(result['report_path']))
    
    def test_report_basic_format(self):
        """Test report generation with basic format."""
        result = self.delegate.delegate_task(
            TaskType.REPORT,
            self.test_dir,
            format="basic"
        )
        self.assertEqual(result['status'], 'success')
        self.assertIn('report_data', result)
        self.assertEqual(result['report_data']['format'], 'basic')


class TestTaskTypes(unittest.TestCase):
    """Test cases for TaskType enum."""
    
    def test_task_type_values(self):
        """Test that all expected task types exist."""
        expected_types = ['unzip', 'organize', 'review', 'test', 'report']
        actual_types = [t.value for t in TaskType]
        
        for expected in expected_types:
            self.assertIn(expected, actual_types)
    
    def test_task_type_from_string(self):
        """Test converting string to TaskType."""
        self.assertEqual(TaskType('unzip'), TaskType.UNZIP)
        self.assertEqual(TaskType('organize'), TaskType.ORGANIZE)
        self.assertEqual(TaskType('review'), TaskType.REVIEW)
        self.assertEqual(TaskType('test'), TaskType.TEST)
        self.assertEqual(TaskType('report'), TaskType.REPORT)


def run_tests():
    """Run all tests and print results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestCloudAgentDelegate))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskTypes))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
