# Commit Message Template

## Main Commit Message

```
feat: enhance config diff tool with recursive scanning and consolidated output

- Add recursive directory scanning for nested structures (APP/server1/profiles/site.xml)
- Consolidate all differences into single "All Differences" sheet with file name column
- Preserve original key order from configuration files instead of alphabetical sorting
- Implement precise cell highlighting - only cells with actual differences highlighted orange
- Maintain full backward compatibility with existing flat directory structures
- Support file path identifiers for files with same names in different subdirectories

Breaking Changes: None
Tested: ✅ Nested directories, ✅ Flat directories, ✅ Mixed structures, ✅ Precise highlighting
```

## Alternative Shorter Version

```
feat: add recursive scanning and single-page output to config diff tool

- Recursive directory scanning for nested structures  
- Consolidated single-sheet output with file name column
- Preserve original key order from config files
- Full backward compatibility maintained
```

## PR Title Suggestion

```
Enhanced Config Diff Tool: Recursive Scanning + Consolidated Output
```

## PR Description Template

```
## Summary
Enhanced the configuration file diff tool with recursive directory scanning and consolidated Excel output for improved usability.

## Key Features Added
- 🔄 **Recursive Directory Scanning**: Now scans all nested subdirectories 
- 📊 **Single Consolidated Output**: All differences on one sheet with file name column
- 📋 **Preserved Key Order**: Keys appear in original file order (not alphabetical)
- 🎯 **Precise Cell Highlighting**: Only cells with actual differences highlighted orange
- ⚡ **Full Backward Compatibility**: Works with existing flat directory structures

## Testing
- ✅ Tested with nested directory structures (`APP/server1/profiles/site.xml`)
- ✅ Verified backward compatibility with existing flat structures  
- ✅ Confirmed key order preservation and file path handling
- ✅ Validated precise cell highlighting logic (majority vs minority values)

## Breaking Changes
None - fully backward compatible

Closes #[issue-number]