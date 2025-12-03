#!/usr/bin/env python3
"""
Basic Usage Example for Cloud Agent Delegation Framework

This example demonstrates how to use the CloudAgentDelegate class
to perform various tasks programmatically.
"""

import sys
import os

# Add parent directory to path to import cloud_agent_delegate
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cloud_agent_delegate import CloudAgentDelegate, TaskType


def example_unzip_task():
    """Example: Unzip a file using the cloud agent."""
    print("\n" + "="*60)
    print("Example 1: Unzip Task")
    print("="*60)
    
    delegate = CloudAgentDelegate()
    result = delegate.delegate_task(
        TaskType.UNZIP,
        "YmeraRefactor.zip",
        output_dir="extracted"
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    if 'recommendation' in result:
        print(f"Recommendation: {result.get('recommendation')}")
    print()


def example_organize_task():
    """Example: Organize files in a directory."""
    print("\n" + "="*60)
    print("Example 2: Organize Task")
    print("="*60)
    
    delegate = CloudAgentDelegate()
    result = delegate.delegate_task(
        TaskType.ORGANIZE,
        "."  # Current directory
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    if 'categories' in result:
        print("\nFile Categories:")
        for category, count in result['categories'].items():
            print(f"  {category}: {count} files")
    print()


def example_review_task():
    """Example: Review code in a directory."""
    print("\n" + "="*60)
    print("Example 3: Review Task")
    print("="*60)
    
    delegate = CloudAgentDelegate()
    result = delegate.delegate_task(
        TaskType.REVIEW,
        "."
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    if 'review' in result:
        review = result['review']
        print(f"\nFiles Reviewed: {review.get('files_reviewed', 0)}")
        if review.get('suggestions'):
            print("\nSuggestions:")
            for suggestion in review['suggestions']:
                print(f"  • {suggestion}")
    print()


def example_test_task():
    """Example: Run tests in a directory."""
    print("\n" + "="*60)
    print("Example 4: Test Task")
    print("="*60)
    
    delegate = CloudAgentDelegate()
    result = delegate.delegate_task(
        TaskType.TEST,
        "."
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    if 'test_results' in result:
        tests = result['test_results']
        print(f"\nTest Results:")
        print(f"  Total: {tests.get('total_tests', 0)}")
        print(f"  Passed: {tests.get('passed', 0)}")
        print(f"  Failed: {tests.get('failed', 0)}")
        print(f"  Skipped: {tests.get('skipped', 0)}")
    if 'note' in result:
        print(f"\nNote: {result['note']}")
    print()


def example_report_task():
    """Example: Generate a detailed report."""
    print("\n" + "="*60)
    print("Example 5: Report Task")
    print("="*60)
    
    delegate = CloudAgentDelegate()
    result = delegate.delegate_task(
        TaskType.REPORT,
        ".",
        format="detailed"
    )
    
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    if 'report_path' in result:
        print(f"Report Path: {result['report_path']}")
    print()


def example_workflow():
    """Example: Complete workflow with multiple tasks."""
    print("\n" + "="*60)
    print("Example 6: Complete Workflow")
    print("="*60)
    print("This demonstrates a complete workflow that would typically")
    print("process a project from start to finish.\n")
    
    delegate = CloudAgentDelegate()
    workflow_results = []
    
    # Step 1: Unzip
    print("Step 1: Attempting to unzip project files...")
    result = delegate.delegate_task(TaskType.UNZIP, "YmeraRefactor.zip")
    workflow_results.append(("Unzip", result['status']))
    
    # If unzip succeeds, continue with other tasks
    if result['status'] == 'success':
        extract_dir = result.get('output_dir', 'extracted')
        
        # Step 2: Organize
        print(f"Step 2: Organizing files in {extract_dir}...")
        result = delegate.delegate_task(TaskType.ORGANIZE, extract_dir)
        workflow_results.append(("Organize", result['status']))
        
        # Step 3: Review
        print(f"Step 3: Reviewing code in {extract_dir}...")
        result = delegate.delegate_task(TaskType.REVIEW, extract_dir)
        workflow_results.append(("Review", result['status']))
        
        # Step 4: Test
        print(f"Step 4: Running tests in {extract_dir}...")
        result = delegate.delegate_task(TaskType.TEST, extract_dir)
        workflow_results.append(("Test", result['status']))
        
        # Step 5: Generate Report
        print("Step 5: Generating final report...")
        result = delegate.delegate_task(TaskType.REPORT, extract_dir, format="detailed")
        workflow_results.append(("Report", result['status']))
    else:
        print(f"⚠ Workflow stopped: {result.get('message')}")
        print(f"   {result.get('recommendation', '')}")
    
    # Print workflow summary
    print("\nWorkflow Summary:")
    print("-" * 40)
    for task, status in workflow_results:
        status_symbol = "✓" if status == "success" else "✗"
        print(f"  {status_symbol} {task}: {status}")
    print()


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print(" Cloud Agent Delegation Framework - Usage Examples")
    print("="*70)
    
    # Run individual task examples
    example_unzip_task()
    example_organize_task()
    example_review_task()
    example_test_task()
    example_report_task()
    
    # Run complete workflow example
    example_workflow()
    
    print("="*70)
    print(" All examples completed!")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
