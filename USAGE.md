# AI-Assisted SPL → LogScale Workflow

## Usage Guide & Customization

## 0. Claude Skill Usage

This project now ships with a local Claude Skill:

`.claude/skills/spl2cql-detection/SKILL.md`

In Claude Code:
1. Open this repository as your working directory.
2. Ask naturally for SPL -> CQL translation, debug, or review (auto-trigger).
3. Or invoke directly with `/spl2cql-detection`.
4. Edit prompts/docs in `ai/` and `docs/` normally; no copy/sync into `.claude/skills` is required.

## 1. Overview

This project provides a structured, repeatable workflow to: - Translate
Splunk SPL → CrowdStrike LogScale (CQL) - Debug failing queries - Review
and optimize detections - Build a reusable knowledge base

Designed for Threat Hunters, Detection Engineers, and SOC teams.

## 2. Core Components

### CLAUDE.md

Defines model behavior, rules, and domain context.

### ai/prompts/

-   translate_query.md
-   debug_query.md
-   review_query.md

### ai/examples/

Real-world validated examples.

### docs/

Knowledge base and mappings.

### scripts/

Automation workflows.

### queries/

Lifecycle folders: spl, cql, failed, validated

## 3. Workflow

1.  Translate (use translate_query.md)
2.  Execute in LogScale
3.  Debug if needed
4.  Review query quality
5.  Store validated queries

## 4. Script Usage

### Translate

python3 scripts/translate_workflow.py translate ...

### Debug

python3 scripts/translate_workflow.py debug ...

### Review

python3 scripts/translate_workflow.py review ...

## 5. Customization

### Improve CLAUDE.md

Add: - Domain context - Detection patterns - Field mappings - Internal
standards

### Add Examples

Create structured cases in ai/examples/

### Extend Prompts

Add: - Validation rules - Performance constraints - SOC metadata (MITRE,
alert names)

## 6. Scaling

-   Build detection library
-   Store validated queries
-   Maintain golden dataset

## 7. Pitfalls

-   Blind translation
-   Field assumptions
-   Ignoring aggregation differences

## 8. Best Practices

-   Start with intent
-   Use structured prompts
-   Iterate continuously

## 9. Future Improvements

-   API integration
-   Auto-validation
-   Detection scoring

## 10. Final Notes

This is a Detection Engineering assistant workflow, not just prompting.

## 11. VS Code Snippet: SPL to CQL

This project includes a reusable VS Code snippet at:

`ai/snippets/spl_to_cql.code-snippets`

### Install

1. Open VS Code.
2. Run `Preferences: Configure User Snippets`.
3. Select `New Global Snippets file...` (or an existing `.code-snippets` file).
4. Copy the content from `ai/snippets/spl_to_cql.code-snippets` into that file.
5. Save.

### Use

1. Open any Markdown or text file where you draft prompts.
2. Type `spl2cql`.
3. Press `Tab` (or `Enter`) to expand the snippet.
4. Fill placeholders:
   - `$1`: SPL query
   - `$2`: data source
   - `$3`: relevant fields
   - `$4`: detection goal

### Snippet Content

```json
{
  "SPL to CQL Translate": {
    "prefix": "spl2cql",
    "body": [
      "Translate the following Splunk SPL into CrowdStrike LogScale CQL.",
      "",
      "Requirements:",
      "- Preserve detection logic",
      "- Do not invent fields",
      "- If unsure, explicitly state assumptions",
      "",
      "### SPL",
      "```spl",
      "$1",
      "```",
      "",
      "### Context",
      "- Source: $2",
      "- Fields: $3",
      "- Goal: $4"
    ]
  }
}
```
