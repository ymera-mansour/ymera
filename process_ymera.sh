#!/bin/bash

################################################################################
# YmeraRefactor Processing Script
# 
# This script automates the extraction, organization, review, and testing
# of the YmeraRefactor.zip file.
#
# Usage: ./process_ymera.sh
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZIP_FILE="$SCRIPT_DIR/YmeraRefactor.zip"
EXTRACT_DIR="$SCRIPT_DIR/ymera_extracted"
REPORT_FILE="$SCRIPT_DIR/PROCESSING_REPORT.md"

################################################################################
# Step 1: Validate Zip File
################################################################################
validate_zip() {
    log_info "Step 1: Validating zip file..."
    
    if [ ! -f "$ZIP_FILE" ]; then
        log_error "YmeraRefactor.zip not found!"
        exit 1
    fi
    
    # Check file size
    FILE_SIZE=$(stat -f%z "$ZIP_FILE" 2>/dev/null || stat -c%s "$ZIP_FILE" 2>/dev/null)
    
    if [ "$FILE_SIZE" -eq 0 ]; then
        log_error "YmeraRefactor.zip is empty (0 bytes)!"
        log_warning "Please upload a valid zip file before running this script."
        exit 1
    fi
    
    log_success "Zip file validated (${FILE_SIZE} bytes)"
    
    # Test zip integrity
    if ! unzip -t "$ZIP_FILE" > /dev/null 2>&1; then
        log_error "Zip file is corrupted or invalid!"
        exit 1
    fi
    
    log_success "Zip file integrity verified"
}

################################################################################
# Step 2: Extract Contents
################################################################################
extract_contents() {
    log_info "Step 2: Extracting contents..."
    
    # Create extraction directory
    if [ -d "$EXTRACT_DIR" ]; then
        log_warning "Extract directory already exists, removing..."
        rm -rf "$EXTRACT_DIR"
    fi
    
    mkdir -p "$EXTRACT_DIR"
    
    # Extract zip file
    unzip -q "$ZIP_FILE" -d "$EXTRACT_DIR"
    
    local FILE_COUNT=$(find "$EXTRACT_DIR" -type f | wc -l)
    log_success "Extracted $FILE_COUNT files to $EXTRACT_DIR"
}

################################################################################
# Step 3: Organize Structure
################################################################################
organize_structure() {
    log_info "Step 3: Analyzing project structure..."
    
    # Detect project type
    cd "$EXTRACT_DIR"
    
    local PROJECT_TYPE="unknown"
    
    if [ -f "package.json" ]; then
        PROJECT_TYPE="Node.js/JavaScript"
    elif [ -f "pom.xml" ]; then
        PROJECT_TYPE="Maven/Java"
    elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
        PROJECT_TYPE="Gradle/Java"
    elif [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
        PROJECT_TYPE="Python"
    elif [ -f "Cargo.toml" ]; then
        PROJECT_TYPE="Rust"
    elif [ -f "go.mod" ]; then
        PROJECT_TYPE="Go"
    elif [ -f "*.csproj" ]; then
        PROJECT_TYPE=".NET/C#"
    fi
    
    log_success "Detected project type: $PROJECT_TYPE"
    
    # Create directory tree
    log_info "Generating directory structure..."
    tree -L 3 "$EXTRACT_DIR" > "$SCRIPT_DIR/directory_structure.txt" 2>/dev/null || \
        find "$EXTRACT_DIR" -maxdepth 3 -print | sed 's|[^/]*/| |g' > "$SCRIPT_DIR/directory_structure.txt"
    
    log_success "Directory structure saved to directory_structure.txt"
}

################################################################################
# Step 4: Code Review
################################################################################
review_code() {
    log_info "Step 4: Performing code review..."
    
    cd "$EXTRACT_DIR"
    
    # Count lines of code
    log_info "Counting lines of code..."
    local TOTAL_LINES=$(find . -type f \( -name "*.js" -o -name "*.ts" -o -name "*.java" -o -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.cs" \) -exec wc -l {} + 2>/dev/null | tail -1 | awk '{print $1}' || echo "N/A")
    
    log_success "Total lines of code: $TOTAL_LINES"
    
    # Find potential issues
    log_info "Scanning for common issues..."
    
    # Check for TODO/FIXME comments
    local TODO_COUNT=$(grep -r "TODO\|FIXME" --include="*.js" --include="*.ts" --include="*.java" --include="*.py" . 2>/dev/null | wc -l || echo "0")
    log_info "Found $TODO_COUNT TODO/FIXME comments"
    
    # Check for console.log statements (if JavaScript/TypeScript)
    if [ -f "package.json" ]; then
        local CONSOLE_COUNT=$(grep -r "console.log" --include="*.js" --include="*.ts" . 2>/dev/null | wc -l || echo "0")
        log_info "Found $CONSOLE_COUNT console.log statements"
    fi
    
    log_success "Code review completed"
}

################################################################################
# Step 5: Run Tests
################################################################################
run_tests() {
    log_info "Step 5: Running end-to-end tests..."
    
    cd "$EXTRACT_DIR"
    
    # Detect and run tests based on project type
    if [ -f "package.json" ]; then
        log_info "Detected Node.js project, checking for test scripts..."
        
        if grep -q "\"test\"" package.json; then
            log_info "Installing dependencies..."
            npm install --silent
            
            log_info "Running tests..."
            npm test || log_warning "Some tests failed"
        else
            log_warning "No test script found in package.json"
        fi
        
    elif [ -f "pom.xml" ]; then
        log_info "Detected Maven project..."
        mvn test || log_warning "Some tests failed"
        
    elif [ -f "requirements.txt" ]; then
        log_info "Detected Python project..."
        pip install -r requirements.txt
        python -m pytest || python -m unittest discover || log_warning "No tests found or tests failed"
        
    else
        log_warning "Could not detect test framework, skipping automated tests"
    fi
    
    log_success "Test execution completed"
}

################################################################################
# Step 6: Generate Report
################################################################################
generate_report() {
    log_info "Step 6: Generating detailed report..."
    
    cat > "$REPORT_FILE" << 'EOF'
# YmeraRefactor Processing Report

## Processing Summary

**Date**: $(date)
**Status**: ✅ Processing Completed

## Extraction Results

- **Zip File**: YmeraRefactor.zip
- **Extract Location**: ymera_extracted/
- **Files Extracted**: [See directory structure]

## Project Analysis

### Project Structure
```
[See directory_structure.txt for full tree]
```

### Code Metrics
- **Total Lines of Code**: [See review output]
- **TODO/FIXME Items**: [See review output]

### Test Results
[See test execution output above]

## Recommendations

1. Review any TODO/FIXME comments found during code review
2. Address any failed tests
3. Consider adding CI/CD pipeline for automated testing
4. Update documentation as needed

## Files Generated

- `PROCESSING_REPORT.md` - This report
- `directory_structure.txt` - Full directory tree
- `ymera_extracted/` - Extracted project files

## Next Steps

1. Review the extracted code in `ymera_extracted/`
2. Address any issues found during code review
3. Re-run tests to ensure all pass
4. Begin development or refactoring work

---

**Report Generated by**: YmeraRefactor Processing Script
EOF

    log_success "Report generated: $REPORT_FILE"
}

################################################################################
# Main Execution
################################################################################
main() {
    log_info "Starting YmeraRefactor processing..."
    echo ""
    
    validate_zip
    echo ""
    
    extract_contents
    echo ""
    
    organize_structure
    echo ""
    
    review_code
    echo ""
    
    run_tests
    echo ""
    
    generate_report
    echo ""
    
    log_success "All processing steps completed successfully!"
    log_info "Check the following files for details:"
    log_info "  - PROCESSING_REPORT.md (detailed report)"
    log_info "  - directory_structure.txt (project structure)"
    log_info "  - ymera_extracted/ (extracted files)"
}

# Run main function
main "$@"
