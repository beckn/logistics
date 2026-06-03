# Global Logistics Standards Landscape

## Introduction

This document provides an objective overview of prominent **logistics standards** used across last-mile delivery, courier services, freight, supply chain, and parcel tracking. The standards listed below are ordered approximately by **real-world adoption and ecosystem visibility**, and includes a **JSON-LD support** column indicating whether published JSON-LD or RDF/OWL artifacts exist.

**JSON-LD support legend**

* **Yes (JSON-LD)**: a project publishes JSON-LD outputs or an `@context`.
* **Yes (RDF/OWL)**: RDF/OWL exists; JSON-LD is a compatible serialization.
* **Partial**: limited/experimental mappings exist, not widely used.
* **No known**: no notable JSON-LD/RDF/OWL schema publication found.

---

## Global Logistics Standards (Ordered by Adoption)

| Rank | Standard | Sub-industry | Has Schema? | Has API Specs? | Global / Regional | Community Support | JSON-LD Support |
|------|----------|-------------|-------------|----------------|------------------|-------------------|-----------------|
| 1 | **GS1** | Supply Chain, Parcel | Yes (EPCIS) | Yes | Global | Very High | Yes (JSON-LD) |
| 2 | **EDIFACT** | Freight, Customs | Yes | Yes | Global | High | No known |
| 3 | **OpenAPI/Swagger (carrier APIs)** | All logistics | Yes | Yes | Global | Very High | Partial |
| 4 | **GS1 EPCIS 2.0** | Track & Trace | Yes | Yes | Global | High | Yes (JSON-LD) |
| 5 | **UN/CEFACT** | Trade, Customs | Yes | Yes | Global | High | Partial |
| 6 | **OpenShipment** | Parcel, LTL | Yes | Yes | Regional | Medium | No known |
| 7 | **IATA Cargo-XML** | Air Freight | Yes | Yes | Global | High | No known |
| 8 | **Beckn Protocol (Logistics)** | All logistics | Yes | Yes | Global | Growing | Yes (JSON-LD) |
| 9 | **ANSI X12** | EDI, Freight | Yes | No | North America | High | No known |
| 10 | **Peppol** | e-Commerce Logistics | Yes | Yes | Global | Medium | Partial |

---

## Schema Organization

This folder contains the canonical logistics domain schemas for the Beckn protocol. Each schema is versioned and follows the OpenAPI 3.1.0 specification for attribute definitions.

### Use Cases Covered
- **Hyperlocal Delivery**: Same-day, sub-2-hour delivery within a city
- **Courier**: B2C and B2B parcel delivery
- **Interstate**: Multi-state freight and cargo
- **Long Haul**: Cross-country or multi-hub heavy freight
- **Express**: Priority, time-guaranteed delivery

### Schema Entities

| Schema | Description | Use Cases |
|--------|-------------|-----------|
| [Shipment](./Shipment/) | Core delivery fulfillment entity | All |
| [Package](./Package/) | Physical goods unit for transport | All |
| [Consignment](./Consignment/) | Grouped shipment for one commercial transaction | Courier, Interstate, Long Haul |
| [Courier](./Courier/) | Last-mile delivery person | Hyperlocal, Courier, Express |
| [Carrier](./Carrier/) | Transport service provider | Interstate, Long Haul, Express |
| [Driver](./Driver/) | Vehicle operator | All |
| [Vehicle](./Vehicle/) | Transport vehicle | All |
| [Route](./Route/) | Planned path for shipment | All |
| [Waypoint](./Waypoint/) | Intermediate stop on route | Interstate, Long Haul |
| [Hub](./Hub/) | Logistics fulfillment center | Courier, Interstate, Long Haul |
| [TrackingUpdate](./TrackingUpdate/) | Real-time shipment status | All |
| [DeliverySlot](./DeliverySlot/) | Time window for delivery | Hyperlocal, Courier, Express |
| [Proof](./Proof/) | Delivery proof (photo, signature, OTP) | All |
| [Place](./Place/) | Geographic location | All |
| [Alert](./Alert/) | Exception/delay notification | All |
| [CancellationPolicy](./CancellationPolicy/) | Cancellation terms | All |
| [ReturnPolicy](./ReturnPolicy/) | Return/reverse logistics terms | Courier, Express |
| [Fare](./Fare/) | Total delivery cost | All |
| [FareBreakup](./FareBreakup/) | Itemized fare components | All |
| [Rating](./Rating/) | Service/driver rating | All |
| [Feedback](./Feedback/) | Qualitative service feedback | All |
| [SupportCase](./SupportCase/) | Customer issue ticket | All |
| [Operator](./Operator/) | Logistics network operator | All |
| [Contact](./Contact/) | Contact information entity | All |
| [Receipt](./Receipt/) | Payment and delivery acknowledgment | All |
