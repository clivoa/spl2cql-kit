# Known Limitations

## SPL vs CQL Differences
### 1. Aggregation Model
- SPL uses stats
- CQL uses groupBy

### 2. Regex
- Syntax differences
- Flags handling differs

### 3. Joins
- SPL supports joins
- CQL often requires workaround

### 4. Eval
- No direct equivalent in some cases

## Strategy
- Simplify when needed
- Break queries into stages
- Prefer clarity over completeness
