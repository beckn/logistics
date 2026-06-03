# Logistics Domain Concepts

## Introduction

This document provides a comprehensive index of core logistics domain entities used in the Beckn Logistics specification. Each concept includes a description, relevant use cases, applicable industry standards, and Beckn IRI mappings.

---

## Core Entities

### 1. Shipment
**Description**: The top-level fulfillment object representing the movement of goods from origin to destination.
**Use Cases**: All (Hyperlocal, Courier, Interstate, Long Haul, Express)
**Standards**: GS1 EPCIS, UN/CEFACT
**IRI**: `https://schema.beckn.org/logistics/Shipment`
**Beckn Mapping**: `beckn:Fulfillment` (equivalentClass)

---

### 2. Package
**Description**: A physical unit of goods packaged for transport, with defined dimensions, weight, and handling requirements.
**Use Cases**: All
**Standards**: GS1, IATA ULD
**IRI**: `https://schema.beckn.org/logistics/Package`
**Beckn Mapping**: `beckn:Item` (equivalentClass)

---

### 3. Consignment
**Description**: A collection of packages grouped under a single commercial transaction, typically identified by an AWB number.
**Use Cases**: Courier, Interstate, Long Haul
**Standards**: IATA AWB, UN/CEFACT
**IRI**: `https://schema.beckn.org/logistics/Consignment`
**Beckn Mapping**: `beckn:Order` (equivalentClass)

---

### 4. Courier
**Description**: A last-mile delivery agent responsible for pickup and delivery of packages in urban contexts.
**Use Cases**: Hyperlocal, Courier, Express
**Standards**: Beckn Logistics Ontology
**IRI**: `https://schema.beckn.org/logistics/Courier`
**Beckn Mapping**: `beckn:Agent` (equivalentClass)

---

### 5. Carrier
**Description**: A transport service provider operating a fleet and logistics network.
**Use Cases**: Courier, Interstate, Long Haul, Express
**Standards**: Beckn Logistics Ontology
**IRI**: `https://schema.beckn.org/logistics/Carrier`
**Beckn Mapping**: `beckn:Provider` (equivalentClass)

---

### 6. Driver
**Description**: The individual operating a vehicle for logistics delivery.
**Use Cases**: All
**Standards**: Beckn Logistics Ontology
**IRI**: `https://schema.beckn.org/logistics/Driver`
**Beckn Mapping**: `beckn:Agent` (equivalentClass)

---

### 7. Vehicle
**Description**: Transport asset used for logistics — bicycle to heavy truck.
**Use Cases**: All
**Standards**: Beckn Logistics Ontology
**IRI**: `https://schema.beckn.org/logistics/Vehicle`
**Beckn Mapping**: `beckn:Asset` (equivalentClass)

---

### 8. Route
**Description**: Planned path from origin to destination with waypoints and transport modes.
**Use Cases**: All
**Standards**: GeoJSON, OpenRoute
**IRI**: `https://schema.beckn.org/logistics/Route`
**Beckn Mapping**: `beckn:Journey` (equivalentClass)

---

### 9. Waypoint
**Description**: An intermediate stop on a logistics route — hub, relay point, or customs checkpoint.
**Use Cases**: Interstate, Long Haul
**Standards**: Beckn Logistics Ontology
**IRI**: `https://schema.beckn.org/logistics/Waypoint`
**Beckn Mapping**: `beckn:Stop` (equivalentClass)

---

### 10. Hub
**Description**: A logistics fulfillment center or sorting facility.
**Use Cases**: Courier, Interstate, Long Haul
**Standards**: Beckn Logistics Ontology
**IRI**: `https://schema.beckn.org/logistics/Hub`
**Beckn Mapping**: `beckn:Location` (equivalentClass)

---

### 11. TrackingUpdate
**Description**: Real-time or periodic status update on a shipment during transit.
**Use Cases**: All
**Standards**: GS1 EPCIS, Beckn Logistics Ontology
**IRI**: `https://schema.beckn.org/logistics/TrackingUpdate`
**Beckn Mapping**: `beckn:Event` (equivalentClass)

---

### 12. DeliverySlot
**Description**: Time window for delivery — from 1-hour express to next-day slots.
**Use Cases**: Hyperlocal, Courier, Express
**Standards**: Beckn Logistics Ontology
**IRI**: `https://schema.beckn.org/logistics/DeliverySlot`
**Beckn Mapping**: `beckn:TimeSlot` (equivalentClass)

---

### 13. Proof
**Description**: Evidence of delivery — photo, signature, OTP, or digital receipt.
**Use Cases**: All
**Standards**: GS1 EPCIS (Disposition)
**IRI**: `https://schema.beckn.org/logistics/Proof`
**Beckn Mapping**: `beckn:Document` (equivalentClass)

---

### 14. Place
**Description**: Any geographic location — origin, destination, hub, or waypoint.
**Use Cases**: All
**Standards**: schema.org/Place, GeoJSON
**IRI**: `https://schema.beckn.org/logistics/Place`
**Beckn Mapping**: `beckn:Location` (exactMatch)

---

### 15. Alert
**Description**: Notification for shipment exceptions — delays, damage, customs holds.
**Use Cases**: All
**Standards**: Beckn Logistics Ontology
**IRI**: `https://schema.beckn.org/logistics/Alert`
**Beckn Mapping**: `beckn:Event` (subClassOf)

---

### 16. CancellationPolicy
**Description**: Terms and charges for cancelling a shipment booking.
**Use Cases**: All
**Standards**: Beckn Core
**IRI**: `https://schema.beckn.org/logistics/CancellationPolicy`
**Beckn Mapping**: `beckn:Policy` (equivalentClass)

---

### 17. ReturnPolicy
**Description**: Conditions for return and reverse logistics.
**Use Cases**: Courier, Express
**Standards**: Beckn Core
**IRI**: `https://schema.beckn.org/logistics/ReturnPolicy`
**Beckn Mapping**: `beckn:Policy` (equivalentClass)

---

### 18. Fare
**Description**: Total cost for logistics service including freight, surcharges, and taxes.
**Use Cases**: All
**Standards**: Beckn Core
**IRI**: `https://schema.beckn.org/logistics/Fare`
**Beckn Mapping**: `beckn:Price` (equivalentClass)

---

### 19. FareBreakup
**Description**: Line-item breakdown of fare components.
**Use Cases**: All
**Standards**: Beckn Core
**IRI**: `https://schema.beckn.org/logistics/FareBreakup`
**Beckn Mapping**: `beckn:Price` (subClassOf)

---

### 20. Rating
**Description**: Numeric score for service, driver, or carrier.
**Use Cases**: All
**Standards**: schema.org/Rating
**IRI**: `https://schema.beckn.org/logistics/Rating`
**Beckn Mapping**: `beckn:Rating` (exactMatch)

---

### 21. Feedback
**Description**: Qualitative post-delivery feedback from sender or receiver.
**Use Cases**: All
**Standards**: schema.org/Review
**IRI**: `https://schema.beckn.org/logistics/Feedback`
**Beckn Mapping**: `beckn:Feedback` (equivalentClass)

---

### 22. SupportCase
**Description**: Customer support ticket for shipment issues.
**Use Cases**: All
**Standards**: Beckn IGMT (Issue Management)
**IRI**: `https://schema.beckn.org/logistics/SupportCase`
**Beckn Mapping**: `beckn:Issue` (equivalentClass)

---

### 23. Operator
**Description**: Logistics network operator managing carriers and drivers.
**Use Cases**: All
**Standards**: Beckn Core
**IRI**: `https://schema.beckn.org/logistics/Operator`
**Beckn Mapping**: `beckn:Provider` (equivalentClass)

---

### 24. Contact
**Description**: Contact information for any party in a logistics transaction.
**Use Cases**: All
**Standards**: schema.org/ContactPoint
**IRI**: `https://schema.beckn.org/logistics/Contact`
**Beckn Mapping**: `beckn:Contact` (exactMatch)

---

### 25. Receipt
**Description**: Payment and delivery acknowledgment document.
**Use Cases**: All
**Standards**: Peppol, UN/CEFACT Invoice
**IRI**: `https://schema.beckn.org/logistics/Receipt`
**Beckn Mapping**: `beckn:Document` (subClassOf)
