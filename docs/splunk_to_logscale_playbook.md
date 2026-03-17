# SPL to LogScale Playbook

## Objective
Standardize translation between SPL and CQL.

## Core Rules
1. Preserve intent over syntax
2. Avoid 1:1 pipeline assumptions
3. Validate fields explicitly
4. Keep queries readable

## Known Mappings
| SPL | CQL |
|-----|-----|
| stats count by X | groupBy(X, function=count()) |
| dc(field) | distinct count |
| where | filter |
| eval | transformation |
| rex | regex extraction |

## Common Pitfalls
- Wrong aggregation order
- Field mismatches
- Missing distinct logic
- Regex differences
- Unsupported functions

## Preferred Workflow
1. Understand intent
2. Translate
3. Validate
4. Test
5. Optimize
