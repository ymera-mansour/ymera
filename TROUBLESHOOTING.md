# Troubleshooting Guide

## Common Issues and Solutions

### Issue 1: Empty Zip File (Current Issue)

**Problem:** YmeraRefactor.zip is 0 bytes and cannot be extracted.

**Symptoms:**
```bash
$ unzip -l YmeraRefactor.zip
Archive:  YmeraRefactor.zip
End-of-central-directory signature not found.
```

**Solutions:**

#### Option A: Replace the Zip File
1. Find the correct zip file on your local machine
2. Verify it's not empty: `ls -lh YmeraRefactor.zip`
3. Test extraction: `unzip -t YmeraRefactor.zip`
4. Replace in repository:
   ```bash
   git rm YmeraRefactor.zip
   cp /path/to/correct/YmeraRefactor.zip .
   git add YmeraRefactor.zip
   git commit -m "Replace empty zip with correct file"
   git push
   ```

#### Option B: Upload Files Directly
Instead of using a zip file, upload your project files directly:
```bash
# Extract locally
unzip YmeraRefactor.zip -d ymera-project

# Push to repository
git rm YmeraRefactor.zip
cp -r ymera-project/* .
git add .
git commit -m "Add project files directly"
git push
```

#### Option C: Use Git LFS (for large files)
If your zip file is very large (>100MB):
```bash
# Install Git LFS
git lfs install

# Track the specific zip file (recommended to avoid tracking all zips)
git lfs track "YmeraRefactor.zip"
git add .gitattributes

# Add your file
git add YmeraRefactor.zip
git commit -m "Add large zip file via LFS"
git push
```

### Issue 2: Corrupted Zip File

**Problem:** Zip file exists but cannot be extracted.

**Diagnosis:**
```bash
# Check file type
file YmeraRefactor.zip

# Verify zip integrity
unzip -t YmeraRefactor.zip

# Check for corruption
zip -T YmeraRefactor.zip
```

**Solutions:**
1. Re-download the original file
2. Use `zip -FF` to attempt repair
3. Use alternative tools like 7-zip
4. Re-create the archive from source files

### Issue 3: Partial Upload

**Problem:** Upload was interrupted, file is incomplete.

**Symptoms:**
- File size smaller than expected
- Extraction fails partway through
- Missing end-of-archive marker

**Solutions:**
1. Delete the partial file
2. Re-upload the complete file
3. Verify file hash/checksum matches original

### Issue 4: Git File Size Limits

**Problem:** GitHub rejects files larger than 100MB.

**Error:**
```
remote: error: File YmeraRefactor.zip is 123.45 MB; this exceeds GitHub's file size limit of 100.00 MB
```

**Solutions:**

#### Use Git LFS
```bash
git lfs install
git lfs track "YmeraRefactor.zip"
git add .gitattributes YmeraRefactor.zip
git commit -m "Add large file via LFS"
git push
```

#### Split the Archive
```bash
# Split into 50MB chunks
zip -s 50m YmeraRefactor.zip --out YmeraRefactor-split.zip

# This creates: YmeraRefactor-split.z01, YmeraRefactor-split.z02, etc.
```

#### Use External Storage
- Upload to Google Drive, Dropbox, or similar
- Add download link to README
- Include instructions for setup

### Issue 5: Permission Denied

**Problem:** Cannot extract files due to permissions.

**Solutions:**
```bash
# Add execute permissions
chmod +x YmeraRefactor.zip

# Extract with permissions
unzip -o YmeraRefactor.zip

# Fix permissions after extraction
chmod -R u+rwX extracted-folder/
```

## Verification Checklist

Before uploading a zip file, verify:

- [ ] File size is greater than 0 bytes
- [ ] File can be extracted locally
- [ ] All expected files are present in the archive
- [ ] No corrupted files in the archive
- [ ] File size is under GitHub's 100MB limit (or use LFS)
- [ ] No sensitive data in the archive (passwords, API keys, etc.)

## Testing Your Zip File

### Basic Tests
```bash
# Check file exists and has size
ls -lh YmeraRefactor.zip

# Check file type
file YmeraRefactor.zip

# List contents without extracting
unzip -l YmeraRefactor.zip

# Test integrity
unzip -t YmeraRefactor.zip

# Count files
unzip -l YmeraRefactor.zip | wc -l
```

### Advanced Tests
```bash
# Check for specific files
unzip -l YmeraRefactor.zip | grep -i "package.json"
unzip -l YmeraRefactor.zip | grep -i "readme"

# Verify checksums
md5sum YmeraRefactor.zip
sha256sum YmeraRefactor.zip

# Check compression ratio
unzip -l YmeraRefactor.zip | tail -1
```

## Getting Help

If you continue to experience issues:

1. **Check File Locally First**
   - Verify you can extract it on your machine
   - Check the file isn't corrupted
   - Confirm it contains the expected files

2. **Provide Details**
   - File size
   - Error messages
   - Output of `file YmeraRefactor.zip`
   - Output of `unzip -t YmeraRefactor.zip`

3. **Consider Alternatives**
   - Upload files directly (no zip)
   - Use external file hosting
   - Split into smaller archives

## Additional Resources

- [GitHub Large File Storage](https://git-lfs.github.com/)
- [ZIP file format specification](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT)
- [Git documentation](https://git-scm.com/doc)

---

**Last Updated:** December 3, 2025
