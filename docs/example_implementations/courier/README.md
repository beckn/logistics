# Courier (B2C Parcel) — End-to-End Implementation Guide

## Overview

This guide covers a standard B2C courier delivery transaction — a shipper books a parcel for next-day delivery to a customer.

**Scenario:** Meera runs a small e-commerce business and ships a package of clothing from Delhi to Mumbai. She uses a courier aggregator on the Beckn network to find the best rate.

**Key schema classes used:** `Shipment`, `Package`, `Consignment`, `Carrier`, `Driver`, `Vehicle`, `Fare`, `FareBreakup`, `TrackingUpdate`, `Proof`, `Alert`, `Receipt`

---

## Context Values

| Field | Value |
|-------|-------|
| `domain` | `logistics` |
| `version` | `2.0` |
| `bap_id` | `shiprocket.bap.io` |
| `bpp_id` | `dtdc.bpp.io` |

---

## Search Request

```json
{
  "context": { "domain": "logistics", "action": "search", "version": "2.0" },
  "message": {
    "intent": {
      "fulfillment": {
        "type": "COURIER",
        "start": {
          "location": { "address": { "city": "Delhi", "pincode": "110001" } }
        },
        "end": {
          "location": { "address": { "city": "Mumbai", "pincode": "400001" } }
        }
      },
      "tags": [
        { "code": "weight_kg", "value": "1.5" },
        { "code": "declared_value_inr", "value": "2000" }
      ]
    }
  }
}
```

## On-Search Response

```json
{
  "context": { "domain": "logistics", "action": "on_search" },
  "message": {
    "catalog": {
      "providers": [{
        "id": "dtdc",
        "descriptor": { "name": "DTDC Express", "short_desc": "Reliable Courier Service" },
        "items": [
          {
            "id": "dtdc-express-1day",
            "descriptor": { "name": "DTDC Express (1 Day)", "short_desc": "Next-day guaranteed" },
            "price": { "currency": "INR", "value": "285" },
            "tags": [{ "code": "transit_days", "value": "1" }]
          },
          {
            "id": "dtdc-standard-3day",
            "descriptor": { "name": "DTDC Standard (3 Days)", "short_desc": "Economy delivery" },
            "price": { "currency": "INR", "value": "145" },
            "tags": [{ "code": "transit_days", "value": "3" }]
          }
        ]
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
      "id": "ORD-CUR-001",
      "state": "CONFIRMED",
      "tags": [
        { "code": "awb_number", "value": "DTDC123456789IN" },
        { "code": "label_url", "value": "https://dtdc.in/labels/DTDC123456789IN.pdf" },
        { "code": "pickup_scheduled", "value": "2024-03-15T16:00:00+05:30" }
      ],
      "quote": {
        "price": { "currency": "INR", "value": "285" },
        "breakup": [
          { "title": "Base Freight", "price": { "value": "200" } },
          { "title": "Fuel Surcharge", "price": { "value": "20" } },
          { "title": "GST @18%", "price": { "value": "39" } },
          { "title": "Insurance", "price": { "value": "26" } }
        ]
      }
    }
  }
}
```

## Tracking Events

| Date/Time | Status | Location |
|-----------|--------|----------|
| Mar 15, 4:30 PM | PICKED_UP | Karol Bagh, Delhi |
| Mar 15, 11:00 PM | AT_HUB | Delhi Gateway Hub |
| Mar 16, 6:00 AM | IN_TRANSIT | En route to Mumbai |
| Mar 16, 2:00 PM | AT_HUB | Mumbai Sorting Hub |
| Mar 16, 5:00 PM | OUT_FOR_DELIVERY | Andheri, Mumbai |
| Mar 16, 7:30 PM | DELIVERED | Bandra, Mumbai |

## Schema References

- [Shipment](../../../schema/Shipment/)
- [Consignment](../../../schema/Consignment/)
- [Carrier](../../../schema/Carrier/)
- [TrackingUpdate](../../../schema/TrackingUpdate/)
- [Fare](../../../schema/Fare/)
