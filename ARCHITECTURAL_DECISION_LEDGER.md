# MCP Details Readable Report Project - Architectural Decision Ledger

## Part 1 Architectural Decision Ledger Summary

| ID | Decision | Status |
|---|---|---|
| AD-001 | Keep readable reporting separate from MCP inspection | Accepted |
| AD-002 | Consume `ApplicationInspectionResult` as the initial structured reporting input | Accepted |
| AD-003 | Do not parse the existing detailed terminal report as the primary reporting input | Accepted |
| AD-004 | Preserve the existing MCP Details detailed report alongside the readable report | Accepted |
| AD-005 | Derive sibling detailed and readable reports from the same inspection result when generated together | Accepted |
| AD-006 | Preserve inspection semantics and do not mutate structured inspection evidence | Accepted |
| AD-007 | Use HTML as the initial rich readable-report format | Accepted |
| AD-008 | Do not modify MCP Details or introduce a separate interchange contract without demonstrated need | Accepted |


## AD-001 - Keep Readable Reporting Separate from MCP Inspection

**Status:** Accepted  
**Part:** Part 1A - Project Boundary and Upstream Integration Review  
**Date:** 2026-10-12

### Question

Should the MCP Details Readable Report Project perform MCP connection, initialization, discovery, pagination, and inspection itself, or should it remain a downstream reporting layer over the completed MCP Details project?

### Evidence

The completed MCP Details project already owns the MCP inspection lifecycle, including:

- connection profiles,
- STDIO and Streamable HTTP connection handling,
- MCP SDK client lifecycle,
- initialization,
- capability-aware discovery,
- pagination,
- partial and failed category semantics,
- and aggregation into structured inspection results.

The purpose of the new project is to improve presentation and readability, especially for large tool inventories and JSON schemas.

Duplicating MCP inspection behavior in the new project would create overlapping responsibility and duplicate already-tested inspection semantics.

### Decision

The MCP Details Readable Report Project will remain a reporting layer.

MCP Details continues to own MCP connection, protocol interaction, discovery, pagination, and inspection semantics.

The Readable Report Project owns human-oriented organization, transformation, and presentation of already-produced inspection evidence.

### Consequences

The new project will not independently implement MCP connection or discovery logic.

Readable-report development can focus on presentation without duplicating MCP behavior.

Future changes to MCP inspection semantics remain the responsibility of MCP Details.


## AD-002 - Use ApplicationInspectionResult as the Initial Structured Reporting Input

**Status:** Accepted  
**Part:** Part 1A - Project Boundary and Upstream Integration Review  
**Date:** 2026-10-12

### Question

What upstream representation should the Readable Report Project consume?

### Evidence

MCP Details already produces a project-owned `ApplicationInspectionResult` before presentation.

That result contains the configured target summary and the aggregate MCP inspection result, including server description and category inspection results for tools, resources, resource templates, and prompts.

The category inspection structures preserve explicit status, retrieved pages, and failures.

Using this structured result avoids reconstructing those relationships from rendered terminal text.

The MCP Details package does not currently expose this type through an explicit package-root public API, so the selected boundary is a tested module-level interface rather than a declared general-purpose external API.

### Decision

The initial reporting input contract will be the existing `ApplicationInspectionResult` from the known completed MCP Details baseline.

The Readable Report Project may consume the existing tested module-level interface directly.

### Consequences

The project is intentionally coupled to the known MCP Details structured-result model.

The initial integration also carries the MCP SDK types embedded within that model.

If this direct dependency later proves inadequate, an explicit interchange contract may be considered at that time.


## AD-003 - Do Not Parse the Existing Detailed Terminal Report as the Primary Input

**Status:** Accepted  
**Part:** Part 1A - Project Boundary and Upstream Integration Review  
**Date:** 2026-10-12

### Question

Should the new project consume the text produced by MCP Details `render_report()` and parse that text into a new readable representation?

### Evidence

The detailed report converts structured relationships into presentation conventions such as:

- section headings,
- labels,
- indentation,
- status wording,
- empty-inventory messages,
- failure sections,
- and formatted JSON blocks.

The structured `ApplicationInspectionResult` already exposes the underlying status, pages, failures, and MCP result objects directly.

Parsing terminal text would therefore require the new project to reconstruct information that already exists in structured form and would couple the project to presentation wording and layout.

### Decision

The existing detailed terminal report will not be parsed as the primary input for readable-report generation.

The Readable Report Project will consume structured inspection evidence instead.

### Consequences

Changes to MCP Details terminal wording or indentation should not determine readable-report correctness.

A future feature for importing previously captured report text, if ever required, would be a separate concern and would not replace the structured integration path.


## AD-004 - Preserve the Existing MCP Details Detailed Report

**Status:** Accepted  
**Part:** Part 1A - Project Boundary and Upstream Integration Review  
**Date:** 2026-10-12

### Question

Does the new readable report replace the existing MCP Details report, and what does the original requirement to retain the "raw output" mean?

### Evidence

The existing MCP Details `render_report()` output provides a detailed technical representation of the inspection result.

The Readable Report Project exists to add a more human-friendly representation, not to remove that technical representation.

The phrase "raw output" is ambiguous because it could also refer to MCP protocol traffic, DTO serialization, or a captured output file.

### Decision

For this project, the original preservation requirement means that the existing MCP Details detailed report remains independently obtainable alongside the new readable report.

The project will use the term "detailed report" for the existing `render_report()` representation.

Preserving raw MCP protocol traffic is not part of this requirement.

### Consequences

The readable report is an additional representation rather than a replacement.

The readable report does not need to physically embed the detailed report.

Whether reports are automatically persisted to files is a separate output-delivery decision.


## AD-005 - Use the Same Inspection Result for Sibling Reports

**Status:** Accepted  
**Part:** Part 1A - Project Boundary and Upstream Integration Review  
**Date:** 2026-10-12

### Question

When a detailed report and readable report are generated for the same inspection operation, should each report perform a separate MCP inspection?

### Evidence

Separate inspections could observe different server state and could therefore produce reports containing different evidence.

Repeated inspection would also duplicate connection and discovery work unnecessarily.

A single `ApplicationInspectionResult` can serve as the source for multiple presentation representations.

### Decision

When the detailed and readable reports are generated together for one inspection operation, both should derive from the same `ApplicationInspectionResult`.

### Consequences

Detailed and readable reports can share common provenance.

Generating an additional representation does not require a second MCP inspection.

This decision does not require every workflow to generate both reports.


## AD-006 - Preserve Inspection Semantics and Do Not Mutate Evidence

**Status:** Accepted  
**Part:** Part 1A - Project Boundary and Upstream Integration Review  
**Date:** 2026-10-12

### Question

How much may the readable-report transformation simplify or reorganize the structured inspection result?

### Evidence

MCP Details intentionally distinguishes category states including:

- `NOT_ADVERTISED`,
- `SUCCESS`,
- `PARTIAL`,
- and `FAILED`.

A successful empty inventory is not equivalent to an unadvertised category.

A partial inspection may contain successfully retrieved evidence together with a later failure.

Human-oriented presentation can reorganize this evidence, but collapsing these distinctions would change its meaning.

The existing presentation boundary is observational rather than a mechanism for modifying inspection results.

### Decision

Readable reporting may summarize, reorganize, label, count, tabulate, and visually restructure inspection evidence, but it must not collapse semantically distinct inspection states or discard successfully preserved evidence.

Readable rendering must not mutate the supplied `ApplicationInspectionResult` or its preserved inspection evidence.

### Consequences

Readable-report tests must protect semantic distinctions in addition to checking visual output.

Partial results must remain visibly partial.

Unknown or open-ended structures require a generic fallback rather than silent omission.


## AD-007 - Use HTML as the Initial Rich Readable-Report Format

**Status:** Accepted  
**Part:** Part 1A - Project Boundary and Upstream Integration Review  
**Date:** 2026-10-12

### Question

Which output format should initially serve as the rich human-readable report representation?

### Evidence

The project must handle potentially large hierarchical inspection results, including large tool inventories and nested JSON schemas.

HTML supports:

- hierarchy,
- tables,
- code blocks,
- anchors,
- browser search,
- progressive disclosure,
- collapsible detail,
- and potential future GUI viewing.

Markdown is a strong alternative but provides less consistent support for rich progressive disclosure.

PDF and DOCX introduce fixed-document complexity not currently required.

JSON is useful for machine interchange but does not solve the project's human-readability problem.

### Decision

HTML will be the initial rich readable-report target.

The structured inspection result remains authoritative; HTML is a presentation representation and not an interchange or inspection-data contract.

### Consequences

Initial implementation will focus on one rich output format rather than building multiple renderers.

Markdown remains a possible future secondary format.

PDF, DOCX, and JSON output are deferred until demonstrated requirements justify them.

Exact HTML structure, styling, and interactivity remain later design decisions.


## AD-008 - Do Not Modify MCP Details or Introduce an Interchange Layer Without Demonstrated Need

**Status:** Accepted  
**Part:** Part 1A - Project Boundary and Upstream Integration Review  
**Date:** 2026-10-12

### Question

Should the completed MCP Details project be modified now to expose a new public reporting API or serialized interchange representation for the Readable Report Project?

### Evidence

The existing MCP Details application layer already returns `ApplicationInspectionResult` before presentation.

That existing structured boundary is sufficient to begin controlled integration.

Creating a new interchange layer would introduce additional serialization, versioning, testing, and upstream maintenance work before a concrete limitation has been demonstrated.

The MCP Details project has already reached a completed and validated Part 2 baseline.

### Decision

The Readable Report Project will initially consume the existing tested module-level structured boundary without modifying the completed MCP Details project.

A new explicit interchange contract will be considered only if future evidence demonstrates that direct structured integration is inadequate.

### Consequences

The completed MCP Details baseline remains unchanged.

The new project can begin independently.

Any future proposal to change the upstream integration contract must be justified by an observed limitation rather than architectural speculation.