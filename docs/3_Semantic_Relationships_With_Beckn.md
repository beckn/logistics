# Semantic Relationships with Beckn Core

## Introduction

This document maps every Beckn Logistics domain entity to its corresponding Beckn Core schema concept using OWL/RDFS/SKOS semantic predicates. These mappings enable interoperability across Beckn domains and allow logistics entities to be reasoned about in terms of the Beckn Core abstraction model.

## Predicate Legend

| Predicate | Description |
|-----------|-------------|
| `owl:equivalentClass` | Logistics entity is semantically equivalent to Beckn Core entity |
| `rdfs:subClassOf` | Logistics entity is a specialization of Beckn Core entity |
| `skos:exactMatch` | Near-identical meaning across schemas |
| `skos:closeMatch` | Similar meaning with minor differences |
| `skos:broadMatch` | Logistics entity is a narrower concept than the Beckn Core entity |

---

## Mapping Table

| Logistics Entity | Beckn Core Entity | Predicate | Notes |
|-----------------|-------------------|-----------|-------|
| `log:Shipment` | `beckn:Fulfillment` | `owl:equivalentClass` | Shipment is the logistics fulfillment |
| `log:Shipment` | `beckn:Order` | `skos:broadMatch` | Shipment is part of an order |
| `log:Package` | `beckn:Item` | `owl:equivalentClass` | Package is the logistics item |
| `log:Consignment` | `beckn:Order` | `owl:equivalentClass` | Consignment is the logistics order |
| `log:Courier` | `beckn:Agent` | `owl:equivalentClass` | Courier is a delivery agent |
| `log:Carrier` | `beckn:Provider` | `owl:equivalentClass` | Carrier is the logistics provider |
| `log:Driver` | `beckn:Agent` | `owl:equivalentClass` | Driver is an operational agent |
| `log:Vehicle` | `beckn:Asset` | `owl:equivalentClass` | Vehicle is a logistics asset |
| `log:Route` | `beckn:Journey` | `owl:equivalentClass` | Route defines the shipment journey |
| `log:Waypoint` | `beckn:Stop` | `owl:equivalentClass` | Waypoint is a logistics stop |
| `log:Hub` | `beckn:Location` | `rdfs:subClassOf` | Hub is a specialized location |
| `log:TrackingUpdate` | `beckn:Event` | `rdfs:subClassOf` | Tracking update is a lifecycle event |
| `log:DeliverySlot` | `beckn:TimeSlot` | `owl:equivalentClass` | Delivery slot is a time slot |
| `log:Proof` | `beckn:Document` | `rdfs:subClassOf` | Proof is a delivery document |
| `log:Place` | `beckn:Location` | `skos:exactMatch` | Direct location mapping |
| `log:Alert` | `beckn:Event` | `rdfs:subClassOf` | Alert is an exception event |
| `log:CancellationPolicy` | `beckn:Policy` | `owl:equivalentClass` | Direct policy mapping |
| `log:ReturnPolicy` | `beckn:Policy` | `owl:equivalentClass` | Return policy maps to Beckn policy |
| `log:Fare` | `beckn:Price` | `owl:equivalentClass` | Fare is the logistics price |
| `log:FareBreakup` | `beckn:Price` | `rdfs:subClassOf` | Breakup is a price sub-component |
| `log:Rating` | `beckn:Rating` | `skos:exactMatch` | Direct rating mapping |
| `log:Feedback` | `beckn:Feedback` | `owl:equivalentClass` | Direct feedback mapping |
| `log:SupportCase` | `beckn:Issue` | `owl:equivalentClass` | Support case is a Beckn issue |
| `log:Operator` | `beckn:Provider` | `owl:equivalentClass` | Operator is a logistics provider |
| `log:Contact` | `beckn:Contact` | `skos:exactMatch` | Direct contact mapping |
| `log:Receipt` | `beckn:Document` | `rdfs:subClassOf` | Receipt is a logistics document |

---

## JSON-LD Representation Example

```json
{
  "@context": "https://schema.beckn.org/logistics/context.jsonld",
  "@type": "Shipment",
  "@id": "log:SHP-2024-001234",
  "owl:equivalentClass": "beckn:Fulfillment",
  "status": "IN_TRANSIT",
  "origin": {
    "@type": "Place",
    "address": {
      "city": "Bengaluru",
      "pincode": "560038"
    }
  },
  "destination": {
    "@type": "Place",
    "address": {
      "city": "Mumbai",
      "pincode": "400001"
    }
  }
}
```

## Relationship with Mobility Ontology

The Logistics ontology is derived from and consistent with the Beckn Mobility ontology. Key parallel patterns:

| Mobility Entity | Logistics Equivalent | Relationship |
|----------------|---------------------|--------------|
| `mob:Trip` | `log:Shipment` | `skos:analogousTo` |
| `mob:Rider` | `log:Consignment` (shipper role) | `skos:broadMatch` |
| `mob:Driver` | `log:Driver` | `skos:exactMatch` |
| `mob:Vehicle` | `log:Vehicle` | `skos:exactMatch` |
| `mob:Route` | `log:Route` | `skos:exactMatch` |
| `mob:Stop` | `log:Waypoint` | `skos:closeMatch` |
| `mob:CancellationPolicy` | `log:CancellationPolicy` | `skos:exactMatch` |
| `mob:Rating` | `log:Rating` | `skos:exactMatch` |
| `mob:Feedback` | `log:Feedback` | `skos:exactMatch` |
