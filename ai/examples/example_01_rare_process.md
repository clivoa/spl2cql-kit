# Rare Process Execution

## SPL
```spl
index=win EventCode=1
| stats dc(host) as hosts by process_name
| where hosts=1
```

## Intent
Detect processes executed on only one host.

## Good CQL
```cql
groupBy(process_name, function=distinct_count(host))
| filter hosts == 1
```
