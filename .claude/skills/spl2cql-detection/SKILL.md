---
name: spl2cql-detection
description: Translate Splunk SPL to CrowdStrike LogScale CQL, debug failing CQL queries, and review/optimize detection queries. Use whenever the user asks to migrate SPL to CQL, fix LogScale query errors, validate translation fidelity, or improve query performance/readability for SOC detection workflows.
---

# SPL to CQL Detection Engineering

Use this skill to convert SPL into production-ready LogScale CQL while preserving detection intent.

## What this skill does

- Translate SPL to CQL with semantic fidelity
- Debug failing CQL queries
- Review and optimize query quality (correctness, performance, readability)
- Keep outputs structured for SOC workflows

## Core rules

1. Preserve intent over syntax.
2. Never invent fields/functions/pipelines.
3. If a mapping is uncertain, state assumptions explicitly.
4. Keep filter -> transform -> aggregate logic order unless a documented reason requires change.
5. Prefer readable, operational CQL over compressed syntax.

## Mode selection

Choose the mode that matches the request:

1. **Translate**: SPL -> CQL conversion.
2. **Debug**: Existing CQL fails or returns wrong result.
3. **Review**: Existing SPL + CQL pair needs quality assessment and optimization.

## Output contract

### Translate mode (always use this structure)

1. SPL Intent
2. Proposed CQL (fenced `cql` block)
3. Mapping Notes
4. Validation Checklist
5. Risks / Limitations

### Debug mode (always use this structure)

1. Issue Classification (`syntax`, `unsupported function`, `wrong field`, `aggregation`, `pipeline`)
2. Root Cause
3. Fixed Query (fenced `cql` block)
4. Simplified Debug Query (fenced `cql` block)
5. Validation Checklist

### Review mode (always use this structure)

1. Verdict
2. Issues Found
3. Improved Query (fenced `cql` block)
4. Why It Is Better
5. Validation Checklist

## Workflow

1. Identify user goal and mode (translate/debug/review).
2. Read the relevant canonical template in:
   - `ai/prompts/translate_query.md`
   - `ai/prompts/debug_query.md`
   - `ai/prompts/review_query.md`
3. Load references only as needed:
   - `docs/field_mappings.md`
   - `docs/known_limitations.md`
   - `docs/splunk_to_logscale_playbook.md`
4. If field mapping is uncertain, add a **Field Mapping to Validate** section.
5. Return structured output using the mode contract.

## Optional run scaffolding

If the user wants reproducible run artifacts, use the bundled wrapper:

```bash
${CLAUDE_SKILL_DIR}/scripts/run_workflow.sh --help
```

Example:

```bash
${CLAUDE_SKILL_DIR}/scripts/run_workflow.sh translate \
  --title "rare process" \
  --spl-file queries/spl/rare_user_exe.spl \
  --source "CrowdStrike LogScale" \
  --goal "Detect process seen on one host" \
  --fields "process_name,host"
```

## Supporting files

This skill intentionally uses project files as the single source of truth:

- Prompts: `ai/prompts/`
- References: `docs/`
- Examples: `ai/examples/`
- Workflow automation: `scripts/translate_workflow.py`
