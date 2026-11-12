# ReturnPolicy — v2.0

Defines conditions for returning goods and reverse logistics workflows.

## Files

| File | Purpose |
|---|---|
| [https://schema.nfh.global/ReturnPolicy/v2.0/attributes.yaml](https://schema.nfh.global/ReturnPolicy/v2.0/attributes.yaml) | OpenAPI schema envelope (versioned path) |
| [https://schema.nfh.global/ReturnPolicy/v2.0/schema.json](https://schema.nfh.global/ReturnPolicy/v2.0/schema.json) | JSON Schema document (versioned path) |
| [https://schema.nfh.global/ReturnPolicy/v2.0/context.jsonld](https://schema.nfh.global/ReturnPolicy/v2.0/context.jsonld) | JSON-LD context (versioned path) |
| [https://schema.nfh.global/ReturnPolicy/v2.0/vocab.jsonld](https://schema.nfh.global/ReturnPolicy/v2.0/vocab.jsonld) | RDF vocabulary (versioned path) |

## Properties

| Property | Required | Type | Description |
|---|---|---|---|
| `id` | no | string | - |
| `returnsAccepted` | no | boolean | - |
| `returnWindow` | no | object | - |
| `returnReason` | no | array | - |
| `reversePickupCharge` | no | object | - |
| `refundOnReturn` | no | boolean | - |
| `returnHubAddress` | no | $ref: https://schema.nfh.global/LogisticsPlace/v2.0/attributes.yaml#/components/schemas/LogisticsPlace | - |
