# Beckn Logistics Ontology

## Overview

The Beckn Logistics Ontology (BLO) is a formal semantic vocabulary for the logistics domain, expressed in JSON-LD and compatible with RDF/OWL. It covers all entity types, relationships, and controlled vocabularies needed to describe logistics transactions on the Beckn network.

**Ontology IRI**: `https://schema.beckn.org/logistics/`
**Version**: 2.0.0
**Namespace prefix**: `log:`

---

## 1. Core Foundation Classes

### 1.1 Shipment (`log:Shipment`)
The root fulfillment entity. A Shipment tracks the complete lifecycle of goods movement.

**JSON-LD Example:**
```json
{
  "@type": "Shipment",
  "id": "SHP-2024-001234",
  "status": "IN_TRANSIT",
  "serviceType": "EXPRESS",
  "estimatedDelivery": "2024-03-15T18:00:00+05:30"
}
```

### 1.2 Package (`log:Package`)
Physical unit of goods. Multiple packages constitute a shipment.

### 1.3 Consignment (`log:Consignment`)
Commercial grouping of shipments under a single transaction (AWB).

---

## 2. Actors

### 2.1 Carrier (`log:Carrier`)
Transport service provider. Carriers own fleets and operate hubs.

### 2.2 Operator (`log:Operator`)
Network manager. Operators coordinate carriers, drivers, and platform policies.

### 2.3 Driver (`log:Driver`)
Vehicle operator assigned to shipments.

### 2.4 Courier (`log:Courier`)
Last-mile delivery agent for urban hyperlocal contexts.

---

## 3. Transport & Network

### 3.1 Vehicle (`log:Vehicle`)
Transport asset ranging from bicycles to container trucks.

**Controlled Vocabulary — Vehicle Types:**
- `BICYCLE`, `ELECTRIC_SCOOTER`, `MOTORCYCLE`, `THREE_WHEELER`
- `CAR`, `VAN`, `MINI_TRUCK`, `TRUCK_LCV`, `TRUCK_HCV`
- `CONTAINER_TRUCK`, `TRAILER`

### 3.2 Route (`log:Route`)
Planned path with total distance, duration, and transport mode.

**Transport Modes:** `ROAD`, `AIR`, `RAIL`, `MULTIMODAL`

### 3.3 Waypoint (`log:Waypoint`)
Intermediate stop: `HUB`, `RELAY_POINT`, `CUSTOMS`, `PICKUP`, `DELIVERY`

### 3.4 Hub (`log:Hub`)
Logistics facility: `FULFILLMENT_CENTER`, `SORTING_HUB`, `DARK_STORE`, `LAST_MILE_HUB`

---

## 4. Tracking & Events

### 4.1 TrackingUpdate (`log:TrackingUpdate`)
Lifecycle event for shipments. Status progression:
```
BOOKED → PICKED_UP → IN_TRANSIT → AT_HUB → OUT_FOR_DELIVERY → DELIVERED
                                                              ↘ FAILED_DELIVERY → RETURNED
```

### 4.2 Alert (`log:Alert`)
Exception events: `DELAY`, `DAMAGE`, `LOSS`, `FAILED_DELIVERY`, `CUSTOMS_HOLD`, `SLA_BREACH`

---

## 5. Location

### 5.1 Place (`log:Place`)
Geographic location with structured address and GPS coordinates.

### 5.2 DeliverySlot (`log:DeliverySlot`)
Time windows: `EXPRESS_1HR`, `EXPRESS_2HR`, `MORNING`, `AFTERNOON`, `EVENING`, `NEXT_DAY`

---

## 6. Proof & Documents

### 6.1 Proof (`log:Proof`)
Delivery evidence types: `PHOTO`, `SIGNATURE`, `OTP`, `BIOMETRIC`, `DIGITAL_RECEIPT`

Subtypes: `DELIVERED_TO_PERSON`, `LEFT_AT_SAFE_PLACE`, `HANDED_TO_NEIGHBOUR`

### 6.2 Receipt (`log:Receipt`)
Transaction acknowledgment with fare details and payment confirmation.

---

## 7. Pricing

### 7.1 Fare (`log:Fare`)
Total cost = Base Freight + Fuel Surcharge + ODA + COD + Insurance + GST − Discount

### 7.2 FareBreakup (`log:FareBreakup`)
Individual line items: `ITEM`, `SURCHARGE`, `TAX`, `DISCOUNT`, `FEE`

**Payment Modes:** `PREPAID`, `COD`, `TO_PAY`, `CREDIT`

---

## 8. Policies

### 8.1 CancellationPolicy (`log:CancellationPolicy`)
Cancellable until: `BEFORE_PICKUP`, `BEFORE_DISPATCH`, `ANYTIME`, `NON_CANCELLABLE`

### 8.2 ReturnPolicy (`log:ReturnPolicy`)
Return reasons: `DAMAGED_IN_TRANSIT`, `WRONG_ITEM`, `CONSIGNEE_REFUSED`, `ADDRESS_NOT_FOUND`

---

## 9. Post-Delivery

### 9.1 Rating (`log:Rating`)
Categories: `DRIVER`, `CARRIER`, `SERVICE`, `PACKAGING`
Sub-dimensions: timeliness, packaging, handling, communication

### 9.2 Feedback (`log:Feedback`)
Free text + structured tags: `ON_TIME`, `PROFESSIONAL_DRIVER`, `GOOD_PACKAGING`

### 9.3 SupportCase (`log:SupportCase`)
Issue types: `SHIPMENT_LOST`, `SHIPMENT_DAMAGED`, `DELIVERY_DELAYED`, `BILLING_DISPUTE`, `DRIVER_MISCONDUCT`

---

## 10. Controlled Vocabularies

### Shipment Status
`CREATED` → `PICKUP_PENDING` → `PICKED_UP` → `IN_TRANSIT` → `AT_HUB` → `OUT_FOR_DELIVERY` → `DELIVERED`

### Service Types
`HYPERLOCAL`, `COURIER`, `INTERSTATE`, `LONG_HAUL`, `EXPRESS`

### Exception Reasons
`ADDRESS_NOT_FOUND`, `CONSIGNEE_UNAVAILABLE`, `ACCESS_DENIED`, `NATURAL_DISASTER`, `VEHICLE_BREAKDOWN`, `CUSTOMS_HOLD`
