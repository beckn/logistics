# Express Delivery (Same-Day Guaranteed) — End-to-End Implementation Guide

## Overview

This guide covers time-critical express delivery with guaranteed SLA.

**Scenario:** Arvind needs to send a signed legal document from his office in Connaught Place, Delhi to a law firm in South Delhi — guaranteed within 3 hours.

**Key schema classes used:** `Shipment`, `Package`, `DeliverySlot`, `Courier`, `Vehicle`, `TrackingUpdate`, `Proof`, `Fare`, `Alert`, `Rating`, `Feedback`

---

## Context Values

| Field | Value |
|-------|-------|
| `domain` | `logistics` |
| `version` | `2.0` |
| `bap_id` | `porter.bap.io` |
| `bpp_id` | `bluedart.bpp.io` |

---

## Search Request

```json
{
  "context": { "domain": "logistics", "action": "search", "version": "2.0" },
  "message": {
    "intent": {
      "fulfillment": {
        "type": "EXPRESS",
        "start": {
          "location": { "gps": "28.6315,77.2167", "address": { "area": "Connaught Place", "city": "Delhi" } }
        },
        "end": {
          "location": { "gps": "28.5353,77.2090", "address": { "area": "Saket", "city": "Delhi" } }
        }
      },
      "tags": [
        { "code": "sla_hours", "value": "3" },
        { "code": "package_type", "value": "ENVELOPE" },
        { "code": "weight_kg", "value": "0.5" }
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
        "id": "bluedart-delhi",
        "descriptor": { "name": "Blue Dart Express", "short_desc": "India's No.1 Express Courier" },
        "items": [
          {
            "id": "bd-express-3hr",
            "descriptor": { "name": "Blue Dart 3-Hour Express", "short_desc": "Guaranteed in 3 hours" },
            "price": { "currency": "INR", "value": "299" },
            "tags": [
              { "code": "sla_hours", "value": "3" },
              { "code": "sla_guaranteed", "value": "true" },
              { "code": "sla_breach_refund_percent", "value": "100" }
            ]
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
      "id": "ORD-EXP-001",
      "state": "CONFIRMED",
      "fulfillments": [{
        "state": { "descriptor": { "code": "COURIER_ASSIGNED" } },
        "agent": {
          "name": "Vikram Singh",
          "phone": "+911122334455",
          "rating": "4.9",
          "vehicle": { "type": "MOTORCYCLE", "number": "DL05SA6789" }
        },
        "tags": [
          { "code": "tracking_id", "value": "TRK-EXP-BD-999" },
          { "code": "pickup_eta_minutes", "value": "12" },
          { "code": "delivery_sla_by", "value": "2024-03-15T17:30:00+05:30" },
          { "code": "sla_guaranteed", "value": "true" }
        ]
      }],
      "quote": {
        "price": { "currency": "INR", "value": "299" },
        "breakup": [
          { "title": "Express Delivery Fee", "price": { "value": "250" } },
          { "title": "GST @18%", "price": { "value": "45" } },
          { "title": "Fuel Surcharge", "price": { "value": "4" } }
        ]
      }
    }
  }
}
```

## Delivery Timeline

| Time | Event | Status |
|------|-------|--------|
| 2:30 PM | Order confirmed, Vikram assigned | CONFIRMED |
| 2:42 PM | Vikram picks up envelope from Connaught Place | PICKED_UP |
| 3:15 PM | En route, Delhi Ring Road | IN_TRANSIT |
| 3:48 PM | Out for delivery in Saket | OUT_FOR_DELIVERY |
| 4:02 PM | Delivered (OTP: 7823 confirmed) | DELIVERED |

**Total Time:** 1 hour 32 minutes (SLA: 3 hours ✅)

## SLA Breach Alert (Example)

If delivery is delayed beyond SLA:
```json
{
  "context": { "domain": "logistics", "action": "on_update" },
  "message": {
    "order": {
      "id": "ORD-EXP-001",
      "fulfillments": [{
        "tags": [{
          "code": "alert_type",
          "value": "SLA_BREACH"
        }, {
          "code": "refund_initiated",
          "value": "true"
        }, {
          "code": "refund_amount_inr",
          "value": "299"
        }]
      }]
    }
  }
}
```

## Rating

```json
{
  "context": { "domain": "logistics", "action": "rating" },
  "message": {
    "id": "ORD-EXP-001",
    "ratings": [{
      "id": "RTG-EXP-001",
      "rating_category": "Driver",
      "value": "5",
      "feedback_form": [{
        "question": "How was the express delivery?",
        "answer": "Excellent! Much faster than expected. Very professional."
      }]
    }]
  }
}
```

## Schema References

- [Shipment](../../../schema/Shipment/)
- [DeliverySlot](../../../schema/DeliverySlot/)
- [Courier](../../../schema/Courier/)
- [TrackingUpdate](../../../schema/TrackingUpdate/)
- [Alert](../../../schema/Alert/)
- [Proof](../../../schema/Proof/)
- [Fare](../../../schema/Fare/)
