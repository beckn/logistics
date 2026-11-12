# Shipment — v2.0

A Shipment represents the movement of one or more packages from an origin to a destination. It is the top-level fulfillment entity in a logistics transaction and maps to beckn:Fulfillment.

## Files

| File | Purpose |
|---|---|
| [https://schema.nfh.global/Shipment/v2.0/attributes.yaml](https://schema.nfh.global/Shipment/v2.0/attributes.yaml) | OpenAPI schema envelope (versioned path) |
| [https://schema.nfh.global/Shipment/v2.0/schema.json](https://schema.nfh.global/Shipment/v2.0/schema.json) | JSON Schema document (versioned path) |
| [https://schema.nfh.global/Shipment/v2.0/context.jsonld](https://schema.nfh.global/Shipment/v2.0/context.jsonld) | JSON-LD context (versioned path) |
| [https://schema.nfh.global/Shipment/v2.0/vocab.jsonld](https://schema.nfh.global/Shipment/v2.0/vocab.jsonld) | RDF vocabulary (versioned path) |

## Properties

| Property | Required | Type | Description |
|---|---|---|---|
| `id` | yes | string | Unique identifier for the shipment |
| `trackingId` | no | string | Public tracking identifier shared with sender/receiver |
| `status` | yes | string | Current status of the shipment |
| `origin` | yes | $ref: https://schema.nfh.global/LogisticsPlace/v2.0/attributes.yaml#/components/schemas/LogisticsPlace | - |
| `destination` | yes | $ref: https://schema.nfh.global/LogisticsPlace/v2.0/attributes.yaml#/components/schemas/LogisticsPlace | - |
| `packages` | no | array | List of packages in this shipment |
| `carrier` | no | $ref: https://schema.nfh.global/Carrier/v2.0/attributes.yaml#/components/schemas/Carrier | - |
| `driver` | no | $ref: https://schema.nfh.global/LogisticsDriver/v2.0/attributes.yaml#/components/schemas/LogisticsDriver | - |
| `vehicle` | no | $ref: https://schema.nfh.global/LogisticsVehicle/v2.0/attributes.yaml#/components/schemas/LogisticsVehicle | - |
| `route` | no | $ref: https://schema.nfh.global/LogisticsRoute/v2.0/attributes.yaml#/components/schemas/LogisticsRoute | - |
| `scheduledPickup` | no | string | Scheduled pickup time |
| `estimatedDelivery` | no | string | Estimated delivery date and time |
| `actualDelivery` | no | string | Actual delivery date and time |
| `deliverySlot` | no | $ref: https://schema.nfh.global/DeliverySlot/v2.0/attributes.yaml#/components/schemas/DeliverySlot | - |
| `serviceType` | no | string | Type of logistics service |
| `specialInstructions` | no | string | Special handling instructions for the shipment |
| `proof` | no | $ref: https://schema.nfh.global/Proof/v2.0/attributes.yaml#/components/schemas/Proof | - |
| `fare` | no | $ref: https://schema.nfh.global/LogisticsFare/v2.0/attributes.yaml#/components/schemas/LogisticsFare | - |
| `receipt` | no | $ref: https://schema.nfh.global/LogisticsReceipt/v2.0/attributes.yaml#/components/schemas/LogisticsReceipt | - |
| `cancellationPolicy` | no | $ref: https://schema.nfh.global/LogisticsCancellationPolicy/v2.0/attributes.yaml#/components/schemas/LogisticsCancellationPolicy | - |
| `returnPolicy` | no | $ref: https://schema.nfh.global/ReturnPolicy/v2.0/attributes.yaml#/components/schemas/ReturnPolicy | - |
| `alerts` | no | array | Alerts raised for this shipment |
| `trackingUpdates` | no | array | History of tracking updates |
| `createdAt` | no | string | Timestamp when shipment was created |
| `updatedAt` | no | string | Timestamp of last update |
