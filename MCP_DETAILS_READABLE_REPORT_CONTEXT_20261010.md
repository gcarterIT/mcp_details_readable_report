# MCP Details Readable Report Project — Initial Context

**Context date:** 2026-10-10

## 1. Project Identity

This is a new supporting project for the completed **MCP Details Learning Project**.

Provisional project name:

`mcp_details_readable_report`

This project is separate from:

1. `mcp_details_learning_project`
2. `mcp_details_real_world_validation`

The purpose of this project is to improve the human readability and usability of MCP inspection reports while preserving the existing raw MCP Details output.

This project must not casually modify the completed MCP Details application.

---

# 2. Upstream Project — MCP Details Learning Project

Repository:

`C:\AI_Projects\mcp_details_learning_project`

The MCP Details Learning Project is complete through Part 2.

Validated stable baseline:

* Branch: `main`
* Commit: `873d0d25f59af2e606ed57781648c8ee4380359b`
* Tag: `part-2-complete`
* Python: 3.12.7
* MCP Python SDK: 2.1.1
* pytest: 9.1.1
* anyio: 4.14.2
* Automated test baseline: 120 tests
* Supported transports:

  * STDIO
  * Streamable HTTP
* Terminal entry point:

  * `python -m mcp_details`
* Read-only discovery policy
* Real terminal acceptance previously completed for both transports

The stable application repository should remain unchanged unless this new project produces strong architectural evidence that an upstream change is justified.

---

# 3. Existing MCP Details Architecture

The completed MCP Details application has intentionally separated boundaries.

At a high level:

```text
Connection configuration
        |
        v
Connection profile
        |
        v
Connection boundary
        |
        v
MCP Python SDK Client
        |
        v
MCP initialization
        |
        v
transport-neutral inspect_mcp()
        |
        v
project-owned structured result DTOs
        |
        v
pure render_report()
        |
        v
terminal report
```

Important architectural properties include:

* explicit immutable connection profiles;
* separate STDIO and Streamable HTTP connection composition;
* MCP Python SDK v2 `Client`;
* transport-neutral inspection after connection;
* project-owned result DTOs;
* capability-aware primitive inspection;
* pagination handling;
* preservation of partial pagination results;
* a pure presentation boundary;
* synchronous process entry with asynchronous lower-level execution;
* strict read-only inspection.

The existing report renderer should not automatically be treated as the data source for the new readable-report project.

The new project must first investigate whether the correct integration point is the structured application/inspection result that exists before terminal rendering.

---

# 4. Existing Report Characteristics

The current MCP Details terminal report is designed to faithfully expose inspection information.

It can include:

* configured target;
* server identity;
* negotiated protocol version;
* server capabilities;
* server instructions;
* tools;
* resources;
* resource templates;
* prompts;
* category inspection status;
* pagination results;
* tool input schemas;
* prompt argument information;
* experimental/extension capabilities.

JSON-like structures such as tool input schemas can be large and difficult for a human to scan in terminal output.

A real-world Playwright MCP inspection, for example, produced a report of approximately 54 KB because of the substantial advertised tool surface and schemas.

The current report is useful as detailed/raw inspection evidence, but it is not necessarily the most convenient report for a human reader.

---

# 5. Real-World Validation Evidence

A separate project was created at:

`C:\AI_Projects\mcp_details_real_world_validation`

Its completed Git state is:

* Branch: `main`
* Commit: `160386effa4ff06aacfc06d7f56f5670d6799a98`
* Tag: `real-world-validation-complete`
* Core result: PASS

The validation project tested the completed MCP Details application without modifying it.

Two real-world experiments passed.

## STDIO-001 — Microsoft Playwright MCP

Configuration:

* MCP server: Microsoft Playwright MCP
* npm package: `@playwright/mcp@0.0.83`
* Transport: STDIO
* Windows launcher:

  * `C:\Program Files\nodejs\npx.cmd`
* Authentication: none

Observed server information included:

* Identity: `Playwright 1.64.0-alpha-1790635538000`
* Negotiated protocol version: `2025-11-25`
* Tools: advertised and successfully inspected
* Resources: NOT_ADVERTISED
* Resource Templates: NOT_ADVERTISED
* Prompts: NOT_ADVERTISED

The real report contains numerous substantial tool input schemas.

No Playwright tool was executed.

Overall result:

`PASS`

## HTTP-001 — Context7

Configuration:

* Server: Context7
* Transport: Streamable HTTP
* Endpoint:

  * `https://mcp.context7.com/mcp`
* Authentication: none

Observed server information included:

* Identity: `Context7 4.3.0`
* Negotiated protocol version: `2026-07-28`
* Tools: advertised
* Resources: advertised
* Prompts: advertised
* Tools inspection: SUCCESS
* Resources inspection: SUCCESS with empty result
* Resource Templates inspection: SUCCESS with empty result
* Prompts inspection: SUCCESS with empty result

Context7 tools included:

* `resolve-library-id`
* `query-docs`

No Context7 tool was executed.

Overall result:

`PASS`

The real-world validation therefore demonstrated that the existing structured inspection/presentation architecture works across both supported transports and materially different server capability shapes.

---

# 6. Purpose of the New Readable Report Project

The new project should produce a more user-friendly representation of MCP Details inspection results.

The desired outcome is not merely cosmetic terminal formatting.

The project should investigate and design a reporting layer that makes large MCP inspection results easier to understand while retaining the full original/raw information.

Primary goals include:

1. improve human readability;
2. make large JSON schemas easier to understand;
3. provide clearer visual hierarchy;
4. make large tool inventories easier to scan;
5. preserve important inspection statuses and capability distinctions;
6. retain access to the original raw MCP Details output;
7. avoid losing technical detail;
8. avoid changing MCP inspection semantics;
9. keep reporting concerns separate from MCP transport and inspection concerns.

---

# 7. Raw Output Preservation Requirement

A central requirement is:

**The original/raw MCP Details report must remain available.**

The readable report is an additional representation, not a destructive replacement.

Conceptually:

```text
MCP inspection
      |
      v
structured inspection result
      |
      +--------------------------+
      |                          |
      v                          v
existing raw/detailed       readable report
representation             representation
      |                          |
      v                          v
preserved                   user-friendly
technical evidence          presentation
```

The exact architecture must be investigated rather than assumed.

In particular, determine what "raw output" should mean operationally.

Possible concepts that must be distinguished include:

* raw MCP protocol messages;
* project-owned structured inspection results;
* the existing detailed MCP Details terminal report;
* a captured text file containing that terminal report.

For this project, the user's immediate intent is to retain the existing detailed MCP Details report while also producing a friendlier report.

Do not silently redefine that requirement.

---

# 8. JSON and Schema Readability Problem

One major focus is reformatting structured JSON/schema information.

Current tool schemas may contain structures such as:

```text
object
  properties
    url
      type: string
    timeout
      type: number
    options
      type: object
      properties
        ...
```

or equivalent JSON Schema structures.

The project should investigate representations that improve comprehension without changing meaning.

Possible approaches to evaluate include:

* formatted/indented JSON;
* hierarchical sections;
* tables for properties;
* property/type/required/description columns;
* collapsible structures if a future output format supports them;
* summaries followed by full schemas;
* separate overview and technical-detail sections.

Do not choose a representation before examining actual MCP Details DTOs and real output.

---

# 9. Report Information Hierarchy

A user-friendly report may benefit from an information hierarchy such as:

```text
MCP Inspection Report
|
+-- Target Summary
|
+-- Server Summary
|
+-- Capabilities
|
+-- Tools
|    |
|    +-- tool summary
|    +-- description
|    +-- arguments
|    +-- schema/details
|
+-- Resources
|
+-- Resource Templates
|
+-- Prompts
|
+-- Technical Details
|
+-- Raw/Detailed Report
```

This is only an initial design concept.

It is not yet an architectural decision.

The project should derive the final representation from actual inspection data and user-readability goals.

---

# 10. Output Format Is Not Yet Decided

Do not assume the final readable report must be:

* terminal text;
* Markdown;
* HTML;
* PDF;
* JSON;
* DOCX; or
* another format.

The first architectural phase should compare appropriate formats.

Important considerations include:

* readability;
* preservation of structured detail;
* ability to handle large schemas;
* portability;
* ease of generation;
* ease of viewing;
* future GUI integration;
* testability;
* separation from MCP Details core logic.

A future GUI project is planned, so the report architecture should avoid unnecessary coupling to a single presentation surface.

---

# 11. Relationship to Planned GUI Project

A second, separate supporting project is planned after this project.

Its purpose will be to provide:

1. user-friendly GUI entry of MCP connection parameters; and
2. report generation/viewing through the same GUI.

The readable-report project should therefore aim to produce a reporting boundary that could later be reused by a GUI.

However:

**Do not design or implement the GUI in this project.**

The reporting project should remain independently useful and independently testable.

Conceptually:

```text
                 future GUI
                    |
                    v
connection configuration
                    |
                    v
              MCP Details
                    |
                    v
         structured inspection
                    |
                    v
        readable-report layer
                    |
          +---------+---------+
          |                   |
          v                   v
     file/report          future GUI
       output               viewer
```

This is directional guidance, not a final architecture.

---

# 12. Important Architectural Question

The first major architectural question is:

**What should the readable-report project consume?**

Candidate boundaries include:

### Option A — Parse existing terminal output

```text
MCP Details
    |
    v
render_report()
    |
    v
text
    |
    v
new parser
    |
    v
readable report
```

This may introduce unnecessary text parsing and coupling to presentation syntax.

### Option B — Consume structured MCP Details results

```text
MCP Details
    |
    v
ApplicationInspectionResult
    |
    +-------------------+
    |                   |
    v                   v
render_report()    readable renderer
```

This may better preserve semantic structure and reuse the existing DTO boundary.

### Option C — Introduce some other explicit export/interchange boundary

This should be considered only if evidence demonstrates that neither existing boundary is appropriate.

Do not assume Option B automatically wins merely because it appears architecturally attractive.

Review the actual source code and DTO contracts first.

---

# 13. Separation of Responsibilities

The new project should not duplicate MCP responsibilities unnecessarily.

MCP Details should remain responsible for:

* connection configuration;
* transport handling;
* MCP SDK lifecycle;
* initialization;
* capability-aware discovery;
* pagination;
* inspection semantics;
* structured inspection results.

The readable-report project should focus on:

* information organization;
* human-readable formatting;
* report generation;
* presentation-specific transformation;
* preservation/linkage of detailed/raw output.

Any proposed responsibility shift must be explicitly justified.

---

# 14. Read-Only Policy

The supporting report project must preserve the read-only philosophy of MCP Details.

Generating a report must never require executing an advertised MCP tool.

The reporting layer should operate on inspection results, not perform MCP actions independently unless a future architecture explicitly establishes a safe and justified orchestration boundary.

---

# 15. Development Method

Use the same controlled learning style used throughout the MCP Details projects.

For each significant step:

1. inspect the actual current state;
2. distinguish verified facts from assumptions;
3. explain the architectural issue;
4. propose the smallest useful next step;
5. make one controlled change at a time;
6. run focused verification;
7. preserve regression safety;
8. record architectural decisions when appropriate;
9. stop at meaningful checkpoints before proceeding.

Do not generate a large implementation all at once.

The user wants to understand the architecture and reasoning, not merely receive completed code.

Use diagrams and concrete examples when they improve understanding.

---

# 16. Initial Project Boundary

The first phase is architectural investigation and planning.

Do not begin by implementing a report generator.

First determine:

* the exact current MCP Details result models;
* the exact application composition boundary;
* how `render_report()` currently consumes those models;
* whether the completed package exposes an appropriate reusable Python API;
* whether the new project should import MCP Details as a package;
* how the original detailed report can be preserved;
* candidate readable output formats;
* how report generation should remain reusable by the later GUI project;
* what should and should not be changed in the completed MCP Details repository.

Only after those questions are answered should implementation begin.

---

# 17. Initial Success Definition

The project will eventually be successful when a user can take a real MCP Details inspection and obtain:

1. the existing detailed/raw report, preserved without loss; and
2. an additional substantially more readable report that communicates the same inspection information accurately.

The readable report should make large schemas and tool inventories materially easier to understand.

The solution should also expose a clean enough reporting boundary that the later GUI project can reuse it without embedding report-generation logic directly into GUI widgets.

---

# 18. Initial Working Principle

Treat this as a **reporting and presentation architecture project**, not as a rewrite of MCP Details.

The existing MCP Details application has already passed controlled testing and real-world interoperability validation.

Changes to that stable application require evidence and architectural justification.

The first task is therefore to understand and reuse the strongest existing boundary rather than creating a parallel MCP client.
