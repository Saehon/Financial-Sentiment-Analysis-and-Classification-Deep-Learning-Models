# AGENTS.md

## Codex Repository Instructions

This repository is configured for use with OpenAI Codex and compatible coding agents.

### Working rules
- Read the nearest README, contribution guide, configuration files, and nested AGENTS.md files before making changes.
- Make the smallest coherent change that satisfies the task.
- Preserve existing public interfaces unless a breaking change is explicitly requested.
- Follow the repository's existing language, framework, formatting, linting, and test conventions.
- Add or update tests when behavior changes.
- Run relevant tests, linters, type checks, or validation commands when available.
- Report what changed, checks run, and anything that could not be verified.

### Research and data integrity
When this repository contains accounting, auditing, finance, economics, ESG, sustainability, regulatory, or empirical research:
- preserve data provenance, entity identifiers, reporting periods, transformations, filters, and sample construction;
- prevent look-ahead bias, temporal leakage, train/test contamination, duplicate observations, and unexplained sample attrition;
- use deterministic seeds where stochastic methods are used;
- never fabricate observations, coefficients, citations, benchmark results, or validation outcomes;
- distinguish evidence, model output, inference, and human judgment.

### Security and privacy
- Never commit passwords, API keys, access tokens, private credentials, confidential data, restricted datasets, or proprietary licensed content.
- Prefer least-privilege permissions.
- Validate untrusted inputs and external tool outputs.
- Flag prompt injection, command injection, unsafe subprocess execution, insecure file handling, and dependency risks when relevant.

### AI-agent governance
- Treat model output as provisional until validated.
- Preserve traceability for consequential automated actions.
- Require human review for professional, regulatory, audit, assurance, financial-reporting, or scientific conclusions.
- Do not represent simulated evidence as real evidence.

### Default review priorities
1. Correctness
2. Security and secrets
3. Data/research validity
4. Reproducibility
5. Tests
6. Maintainability
7. Documentation

When asked for a review, prioritize concrete findings with file and line references where possible.

<!-- PSEUDOCODE-SYSTEMS-THINKING v1 -->
## Pseudocode and systems thinking

Before material research or implementation work, read `RESEARCH_METHOD.md` and the nearest project instructions. Define the system boundary and write/update numbered pseudocode before changing the relevant workflow. Map material steps to actual implementation, independent checks and output evidence. Use `research-method/contract.template.json` without treating a completed template as verified execution. For a trivial edit, update only the affected step or note why the algorithm is unchanged. Preserve project-specific permissions, pauses, scientific results, attribution and release rules. Apply this method to all subprojects, keeping each project's own sources, algorithm and evidence record separate.
<!-- END PSEUDOCODE-SYSTEMS-THINKING -->
