# Long Haul (Full Truck Load) — End-to-End Implementation Guide

## Overview

This guide covers long haul full truck load (FTL) delivery — shipping bulk cargo across the country.

**Scenario:** ManuCorp ships a full truck load of industrial machinery (8 tonnes) from Mumbai to Chennai. They need real-time GPS tracking, driver contact details, and proof of delivery.

**Key schema classes used:** `Consignment`, `Shipment`, `Package`, `Carrier`, `Driver`, `Vehicle`, `Route`, `Waypoint`, `Hub`, `Fare`, `TrackingUpdate`, `Alert`, `Proof`, `Receipt`

---

## Context Values

| Field | Value |
|-------|-------|
| `domain` | `logistics` |
| `version` | `2.0` |
| `bap_id` | `trucksuvidha.bap.io` |
| `bpp_id` | `vrl.bpp.io` |

---

## Search Request

```json
{
  "context": { "domain": "logistics", "action": "search", "version": "2.0" },
  "message": {
    "intent": {
      "fulfillment": {
        "type": "LONG_HAUL",
        "start": {
          "location": { "address": { "city": "Mumbai", "state": "Maharashtra", "pincode": "400703" } }
        },
        "end": {
          "location": { "address": { "city": "Chennai", "state": "Tamil Nadu", "pincode": "600032" } }
        }
      },
      "tags": [
        { "code": "cargo_weight_tons", "value": "8" },
        { "code": "cargo_type", "value": "INDUSTRIAL_MACHINERY" },
        { "code": "service_type", "value": "FTL" },
        { "code": "vehicle_type", "value": "TRUCK_HCV" }
      ]
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
      "id": "ORD-LH-001",
      "state": "CONFIRMED",
      "tags": [
        { "code": "consignment_note", "value": "CN-VRL-2024-00456" },
        { "code": "vehicle_number", "value": "MH04FP5678" },
        { "code": "vehicle_type", "value": "TRUCK_HCV_32FT" },
        { "code": "driver_name", "value": "Suresh Yadav" },
        { "code": "driver_phone", "value": "+917654321098" },
        { "code": "gps_tracking_url", "value": "https://track.vrl.in/MH04FP5678" },
        { "code": "loading_date", "value": "2024-03-17T09:00:00+05:30" },
        { "code": "estimated_delivery", "value": "2024-03-20T14:00:00+05:30" }
      ],
      "quote": {
        "price": { "currency": "INR", "value": "54800" },
        "breakup": [
          { "title": "Base Freight (8T, 1350km)", "price": { "value": "40000" } },
          { "title": "Fuel Surcharge 12%", "price": { "value": "4800" } },
          { "title": "Toll Charges", "price": { "value": "3200" } },
          { "title": "Insurance (0.5% on ₹15L)", "price": { "value": "7500" } },
          { "title": "GST @5%", "price": { "value": "2400" } },
          { "title": "Loading/Unloading", "price": { "value": "3000" } },
          { "title": "Advance Paid (30%)", "price": { "value": "-16440" } }
        ]
      }
    }
  }
}
```

## Route Plan

| Waypoint | ETA | Distance from Previous |
|----------|-----|----------------------|
| Mumbai (Nhava Sheva) | Mar 17, 9:00 AM | — |
| Pune Bypass | Mar 17, 1:00 PM | 180 km |
| Solapur Hub | Mar 17, 7:00 PM | 250 km |
| Hyderabad Relay | Mar 18, 6:00 AM | 330 km |
| Bengaluru Hub | Mar 19, 4:00 AM | 560 km |
| Chennai (Destination) | Mar 20, 2:00 PM | 350 km |

**Total Distance:** 1,670 km | **Transit Time:** 77 hours

## Schema References

- [Consignment](../../../schema/Consignment/)
- [Route](../../../schema/Route/)
- [Waypoint](../../../schema/Waypoint/)
- [Vehicle](../../../schema/Vehicle/)
- [Fare](../../../schema/Fare/)
