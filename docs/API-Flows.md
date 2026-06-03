# Beckn Logistics — API Flows

## Overview

This document describes the standard Beckn protocol API flows for logistics use cases. All logistics transactions follow the Beckn Core API specification with domain-specific context and catalog structures.

## Common Context Values

```json
{
  "context": {
    "domain": "logistics",
    "version": "2.0",
    "bap_id": "logistics-bap.example.io",
    "bpp_id": "delhivery.bpp.io"
  }
}
```

---

## Flow 1: Hyperlocal Delivery (Express 2-Hour)

```
BAP                    BPP (Carrier/Aggregator)
 |------ search ------->|   {pickup, dropoff, package details}
 |<----- on_search -----|   {available services, fare estimates, slots}
 |------ select ------->|   {selected service + slot}
 |<----- on_select -----|   {confirmed quote, T&Cs}
 |------ init --------->|   {sender/receiver contact, payment intent}
 |<----- on_init -------|   {order draft, payment link}
 |------ confirm ------>|   {payment confirmation}
 |<----- on_confirm ----|   {booking confirmed, tracking ID, courier assigned}
 |------ track -------->|   {shipment ID}
 |<----- on_track ------|   {live courier location}
 |<----- on_update -----|   {tracking events: PICKED_UP, OUT_FOR_DELIVERY, DELIVERED}
 |------ rating ------->|   {driver rating, feedback}
 |<----- on_rating -----|   {rating acknowledged}
```

---

## Flow 2: Courier (B2C Next-Day Parcel)

```
BAP                    BPP (Courier Service)
 |------ search ------->|   {origin pincode, dest pincode, weight, dimensions}
 |<----- on_search -----|   {courier services with TAT and fare}
 |------ select ------->|   {selected courier service}
 |<----- on_select -----|   {detailed quote + cancellation policy}
 |------ init --------->|   {package details, sender/receiver}
 |<----- on_init -------|   {AWB number, pickup scheduled}
 |------ confirm ------>|
 |<----- on_confirm ----|   {booking confirmed, AWB label URL}
 |------ status ------->|   {AWB number}
 |<----- on_status -----|   {PICKED_UP → IN_TRANSIT → AT_HUB → DELIVERED}
 |------ support ------>|   {issue: DELIVERY_DELAYED}
 |<----- on_support ----|   {ticket ID, resolution ETA}
```

---

## Flow 3: Interstate Freight

```
BAP                    BPP (Freight Carrier)
 |------ search ------->|   {origin city, dest city, cargo type, weight/volume}
 |<----- on_search -----|   {freight options: FTL, LTL, with transit time}
 |------ select ------->|   {selected freight type}
 |<----- on_select -----|   {quote with breakup: freight + fuel + GST}
 |------ init --------->|   {consignment details, commercial invoice}
 |<----- on_init -------|   {consignment ID, vehicle assignment}
 |------ confirm ------>|
 |<----- on_confirm ----|   {loading date confirmed, driver assigned}
 |<----- on_update -----|   {waypoint updates: city1 → hub → city2}
 |------ track -------->|
 |<----- on_track ------|   {truck GPS location}
 |<----- on_update -----|   {DELIVERED, POD uploaded}
```

---

## Flow 4: Long Haul (FTL)

```
BAP                    BPP (Long Haul Operator)
 |------ search ------->|   {source, destination, cargo specs, FTL requirement}
 |<----- on_search -----|   {truck options: LCV/HCV/Container, fare + transit days}
 |------ select ------->|   {selected truck type}
 |<----- on_select -----|   {detailed quote, route plan with hubs}
 |------ init --------->|   {loading address, unloading address, goods declaration}
 |<----- on_init -------|   {lorry receipt, advance payment terms}
 |------ confirm ------>|
 |<----- on_confirm ----|   {truck assigned, driver details, loading date}
 |<----- on_update -----|   {hub checkpoints: LOADING → IN_TRANSIT → AT_HUB → DELIVERY}
 |------ support ------->|  {issue: DELAY due to highway closure}
 |<----- on_support ----|   {revised ETA confirmed}
```

---

## Flow 5: Express Delivery (Same-Day Guaranteed)

```
BAP                    BPP (Express Carrier)
 |------ search ------->|   {pickup, delivery, SLA: 4-hour}
 |<----- on_search -----|   {express slots available, premium fare}
 |------ select ------->|   {EXPRESS_4HR slot selected}
 |<----- on_select -----|   {confirmed fare with SLA guarantee}
 |------ init --------->|   {sender/receiver, package}
 |<----- on_init -------|   {booking draft}
 |------ confirm ------>|
 |<----- on_confirm ----|   {confirmed, courier assigned immediately}
 |<----- on_update -----|   {real-time: PICKED_UP → EN_ROUTE → DELIVERED}
 |------ rating ------->|
 |<----- on_rating -----|
```

---

## Status Lifecycle

```
CREATED
   ↓
PICKUP_PENDING
   ↓
PICKED_UP
   ↓
IN_TRANSIT ←→ AT_HUB (may repeat for multi-hub routes)
   ↓
OUT_FOR_DELIVERY
   ↓
DELIVERED ──────────── (success)
   ↓
FAILED_DELIVERY ──→ RETURNED (if undeliverable)
```

---

## Search Request Example (Hyperlocal)

```json
{
  "context": {
    "domain": "logistics",
    "action": "search",
    "version": "2.0",
    "transaction_id": "txn-uuid-001",
    "bap_id": "swiggy-instamart.bap.io",
    "bap_uri": "https://api.swiggy.com/beckn"
  },
  "message": {
    "intent": {
      "fulfillment": {
        "start": {
          "location": {
            "gps": "12.9352,77.6244",
            "address": { "city": "Bengaluru", "pincode": "560095" }
          },
          "time": { "range": { "start": "2024-03-15T14:00:00+05:30", "end": "2024-03-15T14:30:00+05:30" } }
        },
        "end": {
          "location": {
            "gps": "12.9716,77.5946",
            "address": { "city": "Bengaluru", "pincode": "560038" }
          }
        },
        "tags": [{ "code": "package_details", "list": [{ "code": "weight_kg", "value": "2.5" }, { "code": "fragile", "value": "false" }] }]
      }
    }
  }
}
```
