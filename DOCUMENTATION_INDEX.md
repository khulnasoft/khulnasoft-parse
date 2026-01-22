# Documentation Index

Welcome to the enhanced khulnasoft-parse documentation! This index helps you navigate all available resources.

## Start Here

### New to the Project?
1. Start with [README.md](README.md) - Project overview
2. Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick start guide
3. Try [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md) - Integration examples

### Want to Contribute?
1. Read [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
2. Reference [QUERY_PATTERNS.md](QUERY_PATTERNS.md) - Pattern documentation
3. Check [CODE_REVIEW.md](CODE_REVIEW.md) - Architecture overview

### Need Help?
1. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common tasks and debugging
2. [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md) - Troubleshooting section
3. [QUERY_PATTERNS.md](QUERY_PATTERNS.md) - Technical reference

---

## Documentation Files

### Core Documentation

#### [README.md](README.md)
Project overview, getting started, support status matrix.
- **Audience**: Everyone
- **Length**: ~200 lines
- **Contains**: Project description, examples, installation

#### [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
Fast lookup guide for common tasks and patterns.
- **Audience**: Users and developers
- **Length**: ~400 lines
- **Contains**: File structure, common tasks, query reference, language matrix

### Integration & Adoption

#### [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md)
How to integrate khulnasoft-parse into your tools and workflows.
- **Audience**: Tool developers, DevOps engineers
- **Length**: ~400 lines
- **Contains**: Use cases, integration examples, scripts, best practices

#### [CONTRIBUTING.md](CONTRIBUTING.md)
Complete guide for contributing queries and improvements.
- **Audience**: Contributors
- **Length**: ~400 lines
- **Contains**: Guidelines, query patterns, language notes, testing, checklist

### Technical Reference

#### [QUERY_PATTERNS.md](QUERY_PATTERNS.md)
Comprehensive reference for all query capture types and patterns.
- **Audience**: Query developers
- **Length**: ~600 lines
- **Contains**: Capture types, predicates, language patterns, examples

#### [CODE_REVIEW.md](CODE_REVIEW.md)
Professional code review and analysis of the project.
- **Audience**: Architects, senior developers
- **Length**: ~200 lines
- **Contains**: Strengths, weaknesses, recommendations, roadmap

### Project Enhancements

#### [ENHANCEMENTS.md](ENHANCEMENTS.md)
Summary of all improvements in this release.
- **Audience**: Project stakeholders
- **Length**: ~300 lines
- **Contains**: New features, statistics, capabilities matrix, usage examples

#### [REVIEW_COMPLETION_REPORT.md](REVIEW_COMPLETION_REPORT.md)
Final completion report with full details of review and enhancements.
- **Audience**: Project managers, stakeholders
- **Length**: ~400 lines
- **Contains**: Deliverables, metrics, validation, recommendations

---

## Documentation by Use Case

### I want to use khulnasoft-parse
→ Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md)  
→ Then [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md) for integration

### I want to understand the codebase
→ Read [README.md](README.md)  
→ Study [CODE_REVIEW.md](CODE_REVIEW.md)  
→ Reference [QUERY_PATTERNS.md](QUERY_PATTERNS.md)

### I want to add new queries
→ Follow [CONTRIBUTING.md](CONTRIBUTING.md)  
→ Reference [QUERY_PATTERNS.md](QUERY_PATTERNS.md)  
→ Use examples from [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md)

### I want to integrate with my tool
→ Study [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md)  
→ Review integration examples section  
→ Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for available captures

### I want project metrics and roadmap
→ Review [ENHANCEMENTS.md](ENHANCEMENTS.md)  
→ Study [REVIEW_COMPLETION_REPORT.md](REVIEW_COMPLETION_REPORT.md)  
→ Check [CODE_REVIEW.md](CODE_REVIEW.md) for recommendations

---

## Feature Overview by Language

### Python
- **Tags**: Classes, functions, methods, imports
- **Variables** (NEW): Module/class/annotated variables
- **Decorators** (NEW): Function/class decorators
- **Exceptions** (NEW): Try-except-finally blocks
- **Docs**: [QUERY_PATTERNS.md](QUERY_PATTERNS.md#python-patterns)

### TypeScript/JavaScript
- **Tags**: Classes, functions, methods, imports, JSX
- **Class Fields**: Class members and properties
- **Constructors**: Constructor definitions
- **Functions**: Function declarations and patterns
- **Types** (NEW): Type aliases, interfaces, enums
- **Generics** (NEW): Generic type parameters
- **Exceptions** (NEW): Try-catch-finally blocks
- **Docs**: [QUERY_PATTERNS.md](QUERY_PATTERNS.md#typescriptjavascript-patterns)

### Java
- **Tags**: Classes, methods, imports
- **Class Fields**: Field declarations
- **Enums/Annotations** (NEW): Enums, annotations, annotation types
- **Exceptions** (NEW): Try-catch, throws, custom exceptions
- **Docs**: [QUERY_PATTERNS.md](QUERY_PATTERNS.md#java-patterns)

### Go
- **Tags**: Functions, methods, imports, packages
- **Class Fields**: Struct fields
- **Types/Enums** (NEW): Type aliases, const blocks, iota
- **Exceptions** (NEW): Error returns, panic, error checking
- **Docs**: [QUERY_PATTERNS.md](QUERY_PATTERNS.md#go-patterns)

### C/C++
- **Tags**: Functions, methods, classes
- **Class Fields**: Class members
- **Enums** (NEW): Enum declarations, scoped enums
- **Exceptions** (NEW): Try-catch, throw, exception specs
- **Docs**: [QUERY_PATTERNS.md](QUERY_PATTERNS.md#cc-patterns)

### Other Languages
See [README.md](README.md#support-status) for coverage matrix of remaining languages.

---

## Quick Access to Patterns

### Capture Types
For all capture types (`@definition.*`, `@reference.*`, etc.):
→ [QUERY_PATTERNS.md - Capture Types](QUERY_PATTERNS.md#standard-capture-types)

### Predicates
For all predicates (`#has-type?`, `#match?`, etc.):
→ [QUERY_PATTERNS.md - Predicates](QUERY_PATTERNS.md#common-predicates-reference)

### Language Examples
For language-specific patterns:
→ [QUERY_PATTERNS.md - Language Patterns](QUERY_PATTERNS.md#language-specific-patterns)

### Common Patterns
For repeated query patterns:
→ [CONTRIBUTING.md - Common Query Patterns](CONTRIBUTING.md#common-query-patterns)

---

## Tools & Scripts

### Scripts in this Repository

#### [./test.sh](test.sh) (ENHANCED)
Run regression tests against golden files.
```bash
./test.sh              # Test all
./test.sh python       # Test Python only
./test.sh "java|go"    # Test with pattern
```

#### [./download_parse.sh](download_parse.sh) (ENHANCED)
Download the parse binary for your platform.
```bash
./download_parse.sh               # Latest version
./download_parse.sh v0.0.17       # Specific version
```

#### [./validate_queries.sh](validate_queries.sh) (NEW)
Validate query files for correctness.
```bash
./validate_queries.sh            # Validate all
./validate_queries.sh python     # Python only
```

#### [./goldens.sh](goldens.sh)
Regenerate golden test files.
```bash
./goldens.sh
```

For script documentation:
→ [QUICK_REFERENCE.md - Common Tasks](QUICK_REFERENCE.md#common-tasks)

---

## File Organization

### Query Files
Located in `queries/`:
- `{language}_tags.scm` - Main definitions
- `{language}_class_fields.scm` - Class members
- `{language}_imports.scm` - Imports
- `{language}_functions.scm` - Functions
- `{language}_constructors.scm` - Constructors
- `{language}_variables.scm` - Variables (NEW)
- `{language}_enums.scm` - Enums (NEW)
- `{language}_types.scm` - Types (NEW)
- `{language}_exceptions.scm` - Exceptions (NEW)
- `{language}_decorators.scm` - Decorators (NEW)
- `{language}_generics.scm` - Generics (NEW)
- `{language}_injections.scm` - Injections

### Test Files
Located in `test_files/`:
- `test.{language}` - Sample code for testing

### Golden References
Located in `goldens/`:
- `test.{language}.golden` - Expected test output

---

## Getting Help

### Troubleshooting
→ [ADOPTION_GUIDE.md - Troubleshooting](ADOPTION_GUIDE.md#troubleshooting)  
→ [QUICK_REFERENCE.md - Debugging Tips](QUICK_REFERENCE.md#debugging-tips)

### Common Issues
→ [CONTRIBUTING.md - Common Issues](CONTRIBUTING.md#common-issues)

### Performance Tips
→ [QUICK_REFERENCE.md - Performance Tips](QUICK_REFERENCE.md#performance-tips)  
→ [ADOPTION_GUIDE.md - Best Practices](ADOPTION_GUIDE.md#best-practices)

### Code Examples
→ [ADOPTION_GUIDE.md - Use Cases](ADOPTION_GUIDE.md#use-cases)  
→ [ADOPTION_GUIDE.md - Integration Examples](ADOPTION_GUIDE.md#integration-examples)

---

## Release Information

**Version**: Enhanced Release (v0.0.17+)  
**Date**: January 22, 2026  
**Status**: Ready for Production  

### What's New
- 12 new query files
- 10 new capture types
- 3 enhanced scripts
- 6 documentation files
- 100% backward compatible

For details:
→ [ENHANCEMENTS.md](ENHANCEMENTS.md)  
→ [REVIEW_COMPLETION_REPORT.md](REVIEW_COMPLETION_REPORT.md)

---

## Resources

### External Links
- [Tree-sitter Documentation](https://tree-sitter.github.io/tree-sitter/)
- [Query Syntax Guide](https://tree-sitter.github.io/tree-sitter/query-syntax)
- [Language Grammars](https://github.com/tree-sitter)
- [GitHub Repository](https://github.com/KhulnaSoft/khulnasoft-parse)

### Internal Resources
All documentation files are in the root directory and start with:
- `README.md` - Main project file
- `*.md` files starting with capital letters

---

## Document Statistics

| Document | Lines | Audience | Type |
|----------|-------|----------|------|
| README.md | ~200 | Everyone | Overview |
| QUICK_REFERENCE.md | ~400 | Users | Guide |
| ADOPTION_GUIDE.md | ~400 | Developers | Guide |
| CONTRIBUTING.md | ~400 | Contributors | Guide |
| QUERY_PATTERNS.md | ~600 | Query Devs | Reference |
| CODE_REVIEW.md | ~200 | Architects | Analysis |
| ENHANCEMENTS.md | ~300 | Stakeholders | Summary |
| REVIEW_COMPLETION_REPORT.md | ~400 | Stakeholders | Report |
| **TOTAL** | **~2,900** | - | - |

---

## Navigation Tips

1. **First Time?** → Start with [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. **Need to Contribute?** → Read [CONTRIBUTING.md](CONTRIBUTING.md)
3. **Want Full Details?** → Study [QUERY_PATTERNS.md](QUERY_PATTERNS.md)
4. **Building a Tool?** → See [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md)
5. **Check Project Status?** → Review [REVIEW_COMPLETION_REPORT.md](REVIEW_COMPLETION_REPORT.md)

---

## Support Channels

- 📚 **Documentation**: All `.md` files in root directory
- 🔧 **Scripts**: `test.sh`, `download_parse.sh`, `validate_queries.sh`
- 📝 **Examples**: See [ADOPTION_GUIDE.md](ADOPTION_GUIDE.md#examples-repository)
- 🐛 **Issues**: GitHub Issues (link in README)
- 💬 **Discussions**: GitHub Discussions

---

**Last Updated**: January 22, 2026  
**Version**: Enhanced Release  
**Status**: Complete ✅
