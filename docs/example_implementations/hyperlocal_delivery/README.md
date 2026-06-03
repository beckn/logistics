# Hyperlocal Delivery — End-to-End Implementation Guide

## Overview

This guide provides complete Beckn protocol v2.0 JSON request and response payloads for a hyperlocal delivery transaction covering `search` through `rating`.

**Scenario:** Riya orders groceries from a dark store in Bengaluru's Koramangala area for delivery to her home in HSR Layout — 5 km away, 45-minute delivery promised.

**Key logistics schema classes used:** `Shipment`, `Package`, `DeliverySlot`, `Courier`, `Vehicle`, `TrackingUpdate`, `Proof`, `Fare`, `FareBreakup`, `CancellationPolicy`, `Rating`, `Feedback`, `Place`, `Contact`

---

## Context Values

| Field | Value |
|-------|-------|
| `domain` | `logistics` |
| `version` | `2.0` |
| `bap_id` | `swiggy-instamart.bap.io` |
| `bpp_id` | `dunzo.bpp.io` |

---

## API Flow

### 1. Search

```json
{
  "context": {
    "domain": "logistics",
    "action": "search",
    "version": "2.0",
    "transaction_id": "hyp-txn-001",
    "bap_id": "swiggy-instamart.bap.io"
  },
  "message": {
    "intent": {
      "fulfillment": {
        "type": "HYPERLOCAL",
        "start": {
          "location": {
            "gps": "12.9352,77.6244",
            "address": { "city": "Bengaluru", "area": "Koramangala", "pincode": "560095" }
          }
        },
        "end": {
          "location": {
            "gps": "12.9116,77.6389",
            "address": { "city": "Bengaluru", "area": "HSR Layout", "pincode": "560102" }
          }
        }
      },
      "tags": [
        { "code": "package_weight_kg", "value": "2.5" },
        { "code": "express_delivery", "value": "true" }
      ]
    }
  }
}
```

### 2. On-Search Response

```json
{
  "context": { "domain": "logistics", "action": "on_search" },
  "message": {
    "catalog": {
      "providers": [{
        "id": "dunzo-blr",
        "descriptor": { "name": "Dunzo Hyperlocal", "short_desc": "Fast city delivery" },
        "fulfillments": [{
          "id": "hyp-slot-45min",
          "type": "HYPERLOCAL",
          "tags": [{ "code": "sla_minutes", "value": "45" }]
        }],
        "items": [{
          "id": "hyperlocal-standard",
          "descriptor": { "name": "45-Minute Delivery", "short_desc": "Guaranteed delivery in 45 mins" },
          "price": { "currency": "INR", "value": "29" },
          "fulfillment_id": "hyp-slot-45min"
        }]
      }]
    }
  }
}
```

### 3. Confirm Response

```json
{
  "context": { "domain": "logistics", "action": "on_confirm" },
  "message": {
    "order": {
      "id": "ORD-HYP-001",
      "state": "CONFIRMED",
      "fulfillments": [{
        "id": "HYP-FUL-001",
        "type": "HYPERLOCAL",
        "state": { "descriptor": { "code": "COURIER_ASSIGNED" } },
        "agent": {
          "name": "Ravi Kumar",
          "phone": "+919900112233",
          "rating": "4.8",
          "vehicle": { "type": "ELECTRIC_SCOOTER", "number": "KA01EV2345" }
        },
        "tracking": true,
        "tags": [
          { "code": "tracking_id", "value": "TRK-HYP-001234" },
          { "code": "estimated_delivery", "value": "2024-03-15T15:15:00+05:30" }
        ]
      }],
      "quote": {
        "price": { "currency": "INR", "value": "29" },
        "breakup": [
          { "title": "Delivery Charge", "price": { "currency": "INR", "value": "29" } }
        ]
      }
    }
  }
}
```

### 4. Tracking Update (On-Update)

```json
{
  "context": { "domain": "logistics", "action": "on_update" },
  "message": {
    "order": {
      "id": "ORD-HYP-001",
      "fulfillments": [{
        "state": { "descriptor": { "code": "OUT_FOR_DELIVERY", "name": "Courier is nearby" } },
        "agent": {
          "name": "Ravi Kumar",
          "location": { "gps": "12.9200,77.6300", "updated_at": "2024-03-15T15:05:00+05:30" }
        },
        "tags": [{ "code": "eta_minutes", "value": "8" }]
      }]
    }
  }
}
```

### 5. Delivery Confirmed (On-Update)

```json
{
  "context": { "domain": "logistics", "action": "on_update" },
  "message": {
    "order": {
      "id": "ORD-HYP-001",
      "state": "COMPLETED",
      "fulfillments": [{
        "state": { "descriptor": { "code": "DELIVERED" } },
        "tags": [
          { "code": "delivered_at", "value": "2024-03-15T15:12:00+05:30" },
          { "code": "proof_type", "value": "PHOTO" },
          { "code": "proof_url", "value": "https://cdn.dunzo.com/pod/ORD-HYP-001.jpg" }
        ]
      }]
    }
  }
}
```

### 6. Rating

```json
{
  "context": { "domain": "logistics", "action": "rating" },
  "message": {
    "id": "ORD-HYP-001",
    "ratings": [
      {
        "id": "RTG-DRIVER-001",
        "rating_category": "Driver",
        "value": "5",
        "feedback_form": [{
          "question": "How was the delivery experience?",
          "answer": "Excellent! Very fast and professional."
        }]
      }
    ]
  }
}
```

---

## Delivery Timeline

| Time | Event |
|------|-------|
| 14:30 | Order confirmed, Ravi Kumar assigned |
| 14:35 | Courier picked up package from dark store |
| 14:55 | Out for delivery, 8 minutes away |
| 15:12 | Delivered to Riya at HSR Layout (42 min total) |

---

## Schema References

- [Shipment](../../../schema/Shipment/)
- [Courier](../../../schema/Courier/)
- [DeliverySlot](../../../schema/DeliverySlot/)
- [TrackingUpdate](../../../schema/TrackingUpdate/)
- [Proof](../../../schema/Proof/)
