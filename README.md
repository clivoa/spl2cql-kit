# SPL → LogScale AI Kit (Automated)

This kit professionalizes SPL to CrowdStrike LogScale translation with Claude.

## Included
- `CLAUDE.md`: persistent project instructions
- `ai/prompts/`: structured prompt templates
- `ai/examples/`: validated examples
- `ai/snippets/`: reusable editor snippets (VS Code)
- `docs/`: project conventions and mappings
- `scripts/translate_workflow.py`: automation wrapper
- `scripts/run_examples.sh`: sample executions

## What the script does
- creates a translation prompt from a template
- optionally creates debug and review prompts
- stores run artifacts as markdown/json
- keeps each case organized under `runs/`

## Typical workflow
1. Save your SPL to a file
2. Run the translation command
3. Paste the generated prompt into Claude / Claude Code
4. Save the response to the run folder
5. If needed, run debug mode with the exact error
