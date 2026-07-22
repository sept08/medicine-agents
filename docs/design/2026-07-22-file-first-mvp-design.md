# File-First Medical Teaching Case MVP Design

## 1. Decision summary

The project will use a file-first, full-stack vertical-slice architecture. Its first objective is to let one operator run the complete business workflow and produce a medically reviewed teaching case and question-answer package. Scale, multi-user administration, and managed infrastructure are deferred until the core educational value is demonstrated.

The implementation will retain explicit interfaces around storage, model providers, retrieval, task execution, and observability so local components can be replaced without changing the domain workflow.

## 2. Frozen delivery scope

### 2.1 Quantitative baseline

| Delivery level | Disease coverage | Accepted output | Meaning |
|---|---:|---:|---|
| First runnable slice | 1 disease | 3 test packages | Technical validation only |
| MVP | 6 diseases | 5 medically approved packages per disease, 30 total | First usable teaching case library |
| Final project | 20 diseases | At least 100 medically approved packages | Formal project result |
| Final source corpus | 20 diseases | At least 500 de-identified source records | Formal knowledge-base target |

Generated drafts do not count toward accepted output. A case counts only after medical approval and publication.

### 2.2 MVP diseases

The MVP covers three renal and three cardiovascular disease categories:

- diabetic kidney disease;
- chronic kidney disease;
- acute kidney injury;
- chronic heart failure;
- acute myocardial infarction;
- hypertensive emergency.

### 2.3 MVP business workflow

1. Import approved textbook, guideline, and de-identified case materials.
2. Create a case order with disease, difficulty, audience, and teaching objectives.
3. Retrieve supporting evidence and generate a structured case draft.
4. Generate tiered teaching questions and an answer for every question.
5. Run deterministic checks and model-assisted quality review, with no more than three repair rounds.
6. Let the operator edit the package.
7. Submit the package for medical review.
8. Approve, publish, retire, and export the versioned package.

### 2.4 Included in the MVP

- local import and indexing of approved materials;
- structured case orders and case packages;
- case, question, answer, evidence, and quality-report generation;
- deterministic and model-assisted quality checks;
- edit, review, approve, publish, retire, and version workflows;
- JSON and Markdown export;
- a minimal browser interface for the complete workflow;
- local run records, cost records, and failure traces;
- synthetic fixtures and automated tests.

### 2.5 Deferred until after MVP validation

- multi-user authentication and advanced role management;
- PostgreSQL, Milvus, Redis, MinIO, managed object storage, and managed security services;
- GraphRAG and Neo4j;
- online A/B automation;
- concurrent task scheduling and batch generation;
- advanced dashboards;
- polished Word and PDF export;
- automated formal teaching-study statistics.

## 3. Architecture

### 3.1 Runtime components

- `apps/api`: FastAPI application and domain workflow.
- `apps/web`: React and Vite operator interface.
- local case repository: one directory per case, containing metadata, immutable versions, review records, and traces.
- local knowledge repository: normalized text chunks, manifests, embeddings, and retrieval metadata stored outside Git.
- model-provider adapters: OpenAI-compatible API clients behind a stable provider interface.
- in-process task runner: executes one generation workflow at a time and records progress events.
- local observability: structured JSON Lines logs and per-run cost summaries.

The domain layer must not depend directly on filesystem paths, a specific model vendor, or a particular retrieval engine.

### 3.2 Local case layout

```text
data/runtime/cases/<case-id>/
├─ order.json
├─ current.json
├─ versions/
│  ├─ v001.json
│  └─ v002.json
├─ reviews/
│  └─ review-001.json
├─ exports/
└─ trace.jsonl
```

Writes use a temporary file followed by an atomic replace. Published versions are immutable.

### 3.3 Publication state machine

```text
draft
  -> qc_passed
  -> awaiting_medical_review
  -> approved
  -> published
  -> retired
```

A rejected review returns the package to `draft` with a recorded reason. Editing an approved or published package creates a new draft version and invalidates prior approval for that new version. Publication requires a medical reviewer identifier and review timestamp. Every export carries an education-only disclaimer.

## 4. Planned technology replacement path

| MVP component | Stable boundary | Later replacement | Replacement trigger |
|---|---|---|---|
| JSON case directories | `CaseRepository` | PostgreSQL repositories | multi-user writes, complex queries, or file-lock contention |
| local source files and indexes | `KnowledgeRepository` / `Retriever` | Milvus or pgvector plus managed object storage | corpus size or retrieval latency exceeds agreed targets |
| in-process runner | `TaskRunner` | Redis plus Celery or another queue | concurrent generation or reliable background execution is required |
| local filesystem exports | `ArtifactStore` | MinIO or object storage | remote access, retention policies, or large artifacts are required |
| direct provider adapters | `ModelProvider` | LiteLLM gateway or approved internal gateway | centralized routing, quotas, or provider failover is required |
| JSONL traces | `TraceSink` | LangFuse or OpenTelemetry backend | shared monitoring and cross-run analysis become necessary |
| operator identity in local config | `IdentityContext` | authenticated users and role-based access | more than one operational user is introduced |
| in-memory retrieval coordination | `Retriever` | hybrid BM25/vector service and optional GraphRAG | measured quality gaps justify added complexity |

Replacement is evidence-driven. No deferred component is introduced solely for architectural completeness.

## 5. Data and repository boundaries

- `wiki/`, private source data, knowledge indexes, runtime outputs, local deny lists, and secrets are never committed.
- Only synthetic fixtures may be versioned.
- The application treats de-identification as an input precondition and records the source approval status in the local manifest.
- Model calls may use approved de-identified content. The operator remains responsible for confirming provider and institutional rules before importing real material.
- Every generated package records source identifiers, model configuration, prompt version, knowledge-manifest version, and quality-rule version.

## 6. Error handling

- Pydantic schemas reject incomplete orders, cases, questions, reviews, and state transitions.
- Provider calls use bounded retries with exponential backoff and record the final failure.
- A failed workflow never produces a published or approved state.
- Partial run artifacts remain available for diagnosis but do not enter the accepted library.
- Quality repair stops after three rounds and routes the case to manual intervention.
- File writes are atomic, and state transitions verify the expected current version before replacement.
- User-facing errors contain an actionable summary and a local run identifier; secrets and raw sensitive inputs are excluded.

## 7. Quality and statistical evaluation

A separate quality plan will define four layers:

1. system quality: completion, schema validity, latency, cost, and repair rate;
2. medical-content quality: atomic-fact accuracy, unsupported-claim rate, logical self-consistency, and teaching-objective alignment;
3. AI-versus-human case equivalence: predefined equivalence margins and confidence-interval or TOST analysis;
4. teaching outcomes: OSCE as the primary endpoint, with satisfaction and qualitative feedback as secondary outcomes.

The production quality agent cannot be the sole evaluator of its own output. MVP publication requires human medical review. Formal evaluation uses a frozen, stratified sample and independent reviewers. Expected effect size is a study-planning assumption, not a product acceptance promise.

## 8. Testing strategy

- schema tests cover valid and invalid domain objects;
- state-machine tests cover every allowed and forbidden transition;
- repository tests verify atomic writes, immutable versions, and recovery from interrupted writes;
- provider contract tests use recorded synthetic responses and never require a real API key;
- retrieval tests use a small synthetic corpus with known expected evidence;
- workflow integration tests run the complete offline path from order to review-ready package;
- browser acceptance tests cover the single-user happy path and critical failure states;
- medical quality is validated separately with approved real inputs and reviewer forms outside Git.

Every implementation slice begins with an executable failing test and ends with a user-visible acceptance check.

## 9. Project and document structure

```text
medicine-agents/
├─ apps/                 # Executable product code
├─ config/               # Versioned non-sensitive schemas, prompts, and rules
├─ data/                 # Local data boundary; private/runtime content ignored
├─ docs/                 # Product, architecture, quality, governance, and guides
├─ project/              # Current status, roadmap, gates, inputs, risks, and decisions
├─ scripts/              # Setup, validation, import, backup, and maintenance tools
├─ tests/                # Cross-component tests and synthetic fixtures
└─ wiki/                 # Local source materials; completely ignored
```

`project/CURRENT_STATUS.md` will be the operational entry point. It will identify the current stage, current acceptance target, completed work, active blockers, medical-team inputs, next actions, and the latest runnable experience.

## 10. Incremental stages

| Stage | User-visible result | Medical input dependency |
|---|---|---|
| S0 Repository and project baseline | navigable project, scope, governance, and status | MVP disease confirmation; not blocking scaffolding |
| S1 Walking skeleton | synthetic order produces a fixed valid package | none |
| S2 One-disease generation | approved materials produce a generated case | one disease chapter/guideline and 3-5 de-identified cases; blocks medical validation only |
| S3 Question-answer package | tiered questions and grounded answers | example teaching objectives and 5-10 reviewed question-answer pairs |
| S4 Quality loop | checks, repair rounds, and a quality report | medical rules and representative error cases |
| S5 Publication governance | edit, review, approve, publish, retire, and version | reviewer assignment and minimal review form |
| S6 Web MVP | complete workflow in a browser | iterative usability feedback |
| S7 Six-disease MVP | 30 approved packages | six-disease source materials and case-by-case approval |
| S8 Formal evaluation | frozen 100-case evaluation and teaching-study inputs | reviewers, ethics, instruments, schedule, and participants |
| S9 Results | project report, registration material, and publication inputs | final analysis and domain review |

Medical preparation is tracked as a parallel workstream. An input blocks a stage only when the stage cannot reach its stated acceptance result without that input.

## 11. Acceptance of this design

This design is the baseline for the implementation plan. Changes to frozen scope, data boundaries, publication rules, or replacement interfaces require a recorded decision and change-log entry.

