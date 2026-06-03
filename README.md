---
title: "Beckn Logistics Specification"
metaTitle: "API Specification for Beckn Network Developers"
---

# Beckn Logistics Specification

A standardized, interoperable protocol for logistics services on the Beckn
network. It enables any logistics seeker (buyer application) to discover and
transact with logistics providers (seller applications) across use cases
including hyperlocal delivery, courier, interstate freight, long haul, and
express delivery.

## Repository Structure

| Path | Contents |
|------|----------|
| [api/](./api/) | OpenAPI specification ([logistics.yaml](./api/logistics.yaml)) |
| [docs/](./docs/) | Domain documentation — overview, concepts, ontology, API flows, and example implementations |
| [schema/](./schema/) | Entity schema definitions (attributes, JSON Schema, and JSON-LD context/vocab) |

## Documentation

Start with the [documentation index](./docs/README.md):

1. [Overview](./docs/1_Overview.md) — Introduction to Beckn Logistics
2. [Logistics Concepts](./docs/2_Logistics_Concepts.md) — Domain entity index with Beckn mappings
3. [Semantic Relationships with Beckn](./docs/3_Semantic_Relationships_With_Beckn.md) — OWL/SKOS mappings
4. [Logistics Ontology](./docs/Logistics_Ontology.md) — Full ontology documentation
5. [API Flows](./docs/API-Flows.md) — Beckn API transaction flows for logistics

## Example Implementations

| Use Case | Description |
|----------|-------------|
| [Hyperlocal Delivery](./docs/example_implementations/hyperlocal_delivery/) | Same-day sub-2-hour delivery |
| [Courier](./docs/example_implementations/courier/) | B2C/B2B parcel delivery |
| [Interstate](./docs/example_implementations/interstate/) | Multi-state freight and cargo |
| [Long Haul](./docs/example_implementations/long_haul/) | Cross-country heavy freight |
| [Express Delivery](./docs/example_implementations/express_delivery/) | Priority guaranteed delivery |

## Release History

| Version | Release Date | Notes |
|---------|--------------|-------|
| 2.0 | June 3, 2026 | Restructured spec with `docs/` and `schema/` directories; full entity ontology |
| 0.9.1 | August 23, 2022 | Hyperlocal delivery spec |
