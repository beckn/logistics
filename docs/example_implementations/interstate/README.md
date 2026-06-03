# Interstate Freight — End-to-End Implementation Guide

## Overview

This guide covers interstate freight delivery — a business ships a cargo consignment from Bengaluru to Delhi via road.

**Scenario:** TechCorp ships 500 kg of electronic components from their Bengaluru warehouse to a distributor in Delhi. They use the Beckn network to compare freight rates from multiple carriers.

**Key schema classes used:** `Consignment`, `Shipment`, `Package`, `Carrier`, `Driver`, `Vehicle`, `Route`, `Waypoint`, `Hub`, `Fare`, `FareBreakup`, `TrackingUpdate`, `Alert`, `Proof`, `Receipt`

---

## Context Values

| Field | Value |
|-------|-------|
| `domain` | `logistics` |
| `version` | `2.0` |
| `bap_id` | `freighttiger.bap.io` |
| `bpp_id` | `safexpress.bpp.io` |

---

## Search Request

```json
{
  "context": { "domain": "logistics", "action": "search", "version": "2.0" },
  "message": {
    "intent": {
      "fulfillment": {
        "type": "INTERSTATE",
        "start": {
          "location": { "address": { "city": "Bengaluru", "state": "Karnataka", "pincode": "560058" } }
        },
        "end": {
          "location": { "address": { "city": "Delhi", "state": "Delhi", "pincode": "110044" } }
        }
      },
      "tags": [
        { "code": "cargo_weight_kg", "value": "500" },
        { "code": "cargo_type", "value": "ELECTRONICS" },
        { "code": "service_type", "value": "LTL" }
      ]
    }
  }
}
```

## On-Search Response (Freight Options)

```json
{
  "context": { "domain": "logistics", "action": "on_search" },
  "message": {
    "catalog": {
      "providers": [{
        "id": "safexpress",
        "descriptor": { "name": "Safexpress Pvt Ltd", "short_desc": "Pan India Logistics" },
        "items": [{
          "id": "safe-ltl-road",
          "descriptor": { "name": "LTL Road Freight", "short_desc": "Bengaluru to Delhi LTL, 4-5 days" },
          "price": { "currency": "INR", "value": "8500" },
          "tags": [
            { "code": "transit_days", "value": "4" },
            { "code": "vehicle_type", "value": "TRUCK_HCV" }
          ]
        }]
      }]
    }
  }
}
```

## On-Confirm Response

```json
{
  "context": { "domain": "logistics", "action": "on_confirm" },
  "message": {
    "order": {
      "id": "ORD-INT-001",
      "state": "CONFIRMED",
      "tags": [
        { "code": "lorry_receipt_number", "value": "LR-SAFE-2024-00123" },
        { "code": "vehicle_number", "value": "KA19C9876" },
        { "code": "driver_name", "value": "Mohan Lal" },
        { "code": "driver_phone", "value": "+919845001234" },
        { "code": "loading_date", "value": "2024-03-16T08:00:00+05:30" }
      ],
      "quote": {
        "price": { "currency": "INR", "value": "9775" },
        "breakup": [
          { "title": "Base Freight (500kg)", "price": { "value": "7500" } },
          { "title": "Fuel Surcharge 10%", "price": { "value": "750" } },
          { "title": "GST @18%", "price": { "value": "1476" } },
          { "title": "Insurance (0.5% on ₹1L)", "price": { "value": "500" } },
          { "title": "Toll Charges", "price": { "value": "-451" } }
        ]
      }
    }
  }
}
```

## Route Plan

| Waypoint | ETA | Type |
|----------|-----|------|
| Bengaluru (Origin) | Mar 16, 8:00 AM | PICKUP |
| Hyderabad Hub | Mar 16, 10:00 PM | HUB |
| Nagpur Relay | Mar 17, 2:00 PM | RELAY_POINT |
| Delhi Gateway Hub | Mar 19, 6:00 AM | HUB |
| Delhi (Destination) | Mar 19, 2:00 PM | DELIVERY |

## Schema References

- [Consignment](../../../schema/Consignment/)
- [Route](../../../schema/Route/)
- [Waypoint](../../../schema/Waypoint/)
- [Hub](../../../schema/Hub/)
- [Fare](../../../schema/Fare/)
