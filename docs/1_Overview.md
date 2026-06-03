# Beckn Logistics — Overview

## Introduction

The Beckn Logistics domain specification defines a standardized, interoperable protocol for logistics services on the Beckn network. It enables any logistics seeker (buyer application) to discover and transact with logistics providers (seller applications) across use cases including hyperlocal delivery, courier, interstate freight, long haul, and express delivery.

## Vision

To democratize logistics by enabling any shipper — from an individual sending a parcel to a large enterprise managing complex supply chains — to access a competitive, open, and interoperable logistics network.

## Scope of the Specification

### Use Cases

| Use Case | Description | Typical Distance | Time Sensitivity |
|----------|-------------|-----------------|-----------------|
| **Hyperlocal Delivery** | Last-mile delivery within a city, often same-hour | < 10 km | Very High (< 2 hrs) |
| **Courier** | B2C and B2B parcel delivery, typically next-day | 10 km – 2000 km | Medium (1-5 days) |
| **Interstate** | Freight and cargo moving across state boundaries | 500 km – 3000 km | Medium-Low (2-7 days) |
| **Long Haul** | Heavy freight, full truck load, cross-country | > 1000 km | Low (3-10 days) |
| **Express** | Priority, time-guaranteed delivery (same-day, next-hour) | Any | Very High |

## How Beckn Logistics Works

Beckn Logistics uses the standard Beckn protocol transaction model:

1. **Search**: Buyer Application (BAP) searches for logistics services
2. **On-Search**: Provider Application (BPP) returns available services with fare estimates
3. **Select**: BAP selects a specific service/carrier/slot
4. **On-Select**: BPP returns detailed quote
5. **Init**: BAP initializes order with shipment and contact details
6. **On-Init**: BPP returns draft order with payment terms
7. **Confirm**: BAP confirms the order and payment
8. **On-Confirm**: BPP confirms booking and assigns carrier/driver
9. **Status / On-Status**: Real-time tracking updates
10. **Update / On-Update**: Modify delivery slot or address
11. **Cancel / On-Cancel**: Cancel booking
12. **Track / On-Track**: Live location tracking
13. **Support / On-Support**: Raise support cases
14. **Rating / On-Rating**: Post-delivery ratings

## Key Design Principles

- **Interoperability**: Any BAP can connect to any BPP through the Beckn Gateway
- **Transparency**: All fare components, policies, and terms are machine-readable
- **Real-time Tracking**: Standardized TrackingUpdate events for all shipment lifecycle stages
- **Trust**: Proof of delivery (POD) with photos, signatures, and OTP verification
- **Inclusivity**: Supports individual couriers, local carriers, and large 3PL operators

## Relationship with Mobility

The Logistics specification is a cousin of the Beckn Mobility specification. Both share:
- Core entity patterns (Provider → Carrier, Driver, Vehicle)
- Fulfillment lifecycle (Order → Shipment)
- Location entities (Place, Waypoint/Stop)
- Policy entities (CancellationPolicy, ReturnPolicy/DropPolicy)
- Rating and Feedback entities

Key differences:
- Logistics adds: Package, Consignment, Hub, TrackingUpdate, Proof, DeliverySlot, ReturnPolicy
- Logistics focuses on goods movement; Mobility focuses on people movement

## IRI Namespace

All logistics schema entities use the IRI prefix: `https://schema.beckn.org/logistics/`

## Version

This specification is version **2.0**. See [schema/](../schema/) for all entity definitions.
