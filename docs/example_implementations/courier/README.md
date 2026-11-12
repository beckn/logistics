# Courier (B2C Parcel) — End-to-End Example

## Overview

A standard B2C courier delivery: a shipper books a parcel for next-day delivery to a customer.

**Scenario:** Meera runs a small e-commerce business and ships a package of clothing from Delhi to Mumbai. She uses a courier aggregator on the network to find the best rate.

**Schema packs used:** `Package`, `Carrier`, `LogisticsFare`, `LogisticsFareBreakup`, `Consignment`, `Shipment`, `LogisticsPlace`, `TrackingUpdate`, `Proof`, `LogisticsReceipt`

> Every payload on this page is checked in CI (`tools/validate.py examples`): the message against the core
> `beckn.yaml` action schema, and each typed logistics object against its schema pack. The message envelope
> follows the [hyperlocal implementation guide](../hyperlocal_delivery/Logistics_Implementation_Guide.md),
> which also explains the mapping of packs to core slots.

---

## Context values

| Field | Value |
|-------|-------|
| `version` | `2.0.0` |
| `bapId` | `parcelhub.example.net` |
| `bppId` | `swiftpost.example.net` |

---

## Discover

The aggregator looks for carriers that offer courier service and cover both pincodes.

```json
{
  "context": {
    "version": "2.0.0",
    "action": "discover",
    "bapId": "parcelhub.example.net",
    "bapUri": "https://parcelhub.example.net/beckn",
    "transactionId": "cur-txn-001",
    "messageId": "cur-txn-001-msg-001",
    "timestamp": "2026-03-15T10:00:00.000Z"
  },
  "message": {
    "intent": {
      "filters": {
        "type": "jsonpath",
        "expression": "$[?(@.serviceTypes anyof ['COURIER'] && @.serviceCoverage[*].pincodes anyof ['110005'] && @.serviceCoverage[*].pincodes anyof ['400050'])]"
      }
    }
  }
}
```

## On-discover

The carrier describes itself in `providerAttributes` (`Carrier`) and prices each service in `offerAttributes` (`LogisticsFare`).

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_discover",
    "bapId": "parcelhub.example.net",
    "bapUri": "https://parcelhub.example.net/beckn",
    "bppId": "swiftpost.example.net",
    "bppUri": "https://swiftpost.example.net/beckn",
    "transactionId": "cur-txn-001",
    "messageId": "cur-txn-001-msg-001",
    "timestamp": "2026-03-15T10:00:00.600Z"
  },
  "message": {
    "catalogs": [
      {
        "id": "catalog-swiftpost",
        "descriptor": {
          "name": "SwiftPost courier services"
        },
        "provider": {
          "id": "swiftpost.example.net",
          "descriptor": {
            "name": "SwiftPost Express",
            "shortDesc": "Door-to-door courier"
          },
          "providerAttributes": {
            "@context": "https://schema.nfh.global/Carrier/v2.0/context.jsonld",
            "@type": "Carrier",
            "id": "swiftpost.example.net",
            "name": "SwiftPost Express",
            "serviceTypes": [
              "COURIER",
              "EXPRESS"
            ]
          }
        },
        "offers": [
          {
            "id": "offer-next-day",
            "descriptor": {
              "name": "Next-day courier",
              "shortDesc": "Delivered the next day"
            },
            "offerAttributes": {
              "@context": "https://schema.nfh.global/LogisticsFare/v2.0/context.jsonld",
              "@type": "LogisticsFare",
              "currency": "INR",
              "totalAmount": 285,
              "estimatedFare": true
            }
          },
          {
            "id": "offer-standard",
            "descriptor": {
              "name": "Standard courier",
              "shortDesc": "Delivered in 3 days"
            },
            "offerAttributes": {
              "@context": "https://schema.nfh.global/LogisticsFare/v2.0/context.jsonld",
              "@type": "LogisticsFare",
              "currency": "INR",
              "totalAmount": 145,
              "estimatedFare": true
            }
          }
        ]
      }
    ]
  }
}
```

## On-confirm

The confirmed contract carries the parcel (`Package` in `resourceAttributes`), the booking (`Consignment` in `commitmentAttributes`), the agreed price (`LogisticsFare` in `considerationAttributes`), the shipment with its tracking number (`Shipment` in `performanceAttributes`) and the receipt (`LogisticsReceipt` in `contractAttributes`).

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_confirm",
    "bapId": "parcelhub.example.net",
    "bapUri": "https://parcelhub.example.net/beckn",
    "bppId": "swiftpost.example.net",
    "bppUri": "https://swiftpost.example.net/beckn",
    "transactionId": "cur-txn-001",
    "messageId": "cur-txn-001-msg-004",
    "timestamp": "2026-03-15T10:05:00.000Z"
  },
  "message": {
    "contract": {
      "id": "contract-cur-001",
      "status": {
        "code": "ACTIVE"
      },
      "commitments": [
        {
          "id": "commitment-001",
          "status": {
            "descriptor": {
              "code": "ACTIVE"
            }
          },
          "resources": [
            {
              "id": "pkg-001",
              "quantity": {
                "count": 1
              },
              "resourceAttributes": {
                "@context": "https://schema.nfh.global/Package/v2.0/context.jsonld",
                "@type": "Package",
                "id": "pkg-001",
                "description": "Clothing, 3 pieces",
                "weight": {
                  "value": 1.5,
                  "unit": "kg"
                },
                "dimensions": {
                  "length": 30,
                  "width": 25,
                  "height": 10,
                  "unit": "cm"
                },
                "packageType": "BOX",
                "declaredValue": {
                  "amount": 2000,
                  "currency": "INR"
                }
              }
            }
          ],
          "offer": {
            "id": "offer-next-day",
            "resourceIds": [
              "pkg-001"
            ]
          },
          "commitmentAttributes": {
            "@context": "https://schema.nfh.global/Consignment/v2.0/context.jsonld",
            "@type": "Consignment",
            "id": "CN-0001",
            "shipper": {
              "name": "Meera",
              "phone": "+911100000001"
            },
            "consignee": {
              "name": "R. Shah",
              "phone": "+912200000002"
            },
            "totalPackages": 1,
            "totalWeight": {
              "value": 1.5,
              "unit": "kg"
            },
            "serviceType": "COURIER",
            "paymentMode": "PREPAID",
            "status": "BOOKED"
          }
        }
      ],
      "consideration": [
        {
          "id": "consideration-001",
          "considerationAttributes": {
            "@context": "https://schema.nfh.global/LogisticsFare/v2.0/context.jsonld",
            "@type": "LogisticsFare",
            "currency": "INR",
            "baseFreight": 200,
            "fuelSurcharge": 20,
            "insuranceCharge": 26,
            "gst": 39,
            "totalAmount": 285,
            "breakup": [
              {
                "title": "Base freight",
                "amount": 200,
                "type": "ITEM"
              },
              {
                "title": "Fuel surcharge",
                "amount": 20,
                "type": "SURCHARGE"
              },
              {
                "title": "Insurance",
                "amount": 26,
                "type": "FEE"
              },
              {
                "title": "GST at 18%",
                "amount": 39,
                "type": "TAX"
              }
            ],
            "paymentMode": "PREPAID"
          }
        }
      ],
      "performance": [
        {
          "id": "performance-001",
          "commitmentIds": [
            "commitment-001"
          ],
          "performanceAttributes": {
            "@context": "https://schema.nfh.global/Shipment/v2.0/context.jsonld",
            "@type": "Shipment",
            "id": "SP123456789IN",
            "trackingId": "SP123456789IN",
            "status": "PICKUP_PENDING",
            "serviceType": "COURIER",
            "origin": {
              "id": "place-shipper",
              "name": "Meera's studio",
              "type": "PICKUP",
              "address": {
                "line1": "14 Karol Bagh Market",
                "city": "Delhi",
                "pincode": "110005",
                "state": "Delhi",
                "country": "IN"
              },
              "gps": {
                "lat": 28.6519,
                "lng": 77.1909
              }
            },
            "destination": {
              "id": "place-consignee",
              "name": "Customer address",
              "type": "DELIVERY",
              "address": {
                "line1": "22 Hill Road, Bandra West",
                "city": "Mumbai",
                "pincode": "400050",
                "state": "Maharashtra",
                "country": "IN"
              },
              "gps": {
                "lat": 19.0544,
                "lng": 72.8402
              }
            },
            "carrier": {
              "id": "swiftpost.example.net",
              "name": "SwiftPost Express",
              "serviceTypes": [
                "COURIER",
                "EXPRESS"
              ]
            },
            "scheduledPickup": "2026-03-15T16:00:00+05:30",
            "estimatedDelivery": "2026-03-16T19:00:00+05:30"
          }
        }
      ],
      "contractAttributes": {
        "@context": "https://schema.nfh.global/LogisticsReceipt/v2.0/context.jsonld",
        "@type": "LogisticsReceipt",
        "id": "rcpt-cur-001",
        "shipmentId": "SP123456789IN",
        "fare": {
          "currency": "INR",
          "baseFreight": 200,
          "fuelSurcharge": 20,
          "insuranceCharge": 26,
          "gst": 39,
          "totalAmount": 285
        },
        "paymentMode": "PREPAID"
      }
    }
  }
}
```

## On-status (delivered)

Tracking events and the proof of delivery are nested in the `Shipment`.

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_status",
    "bapId": "parcelhub.example.net",
    "bapUri": "https://parcelhub.example.net/beckn",
    "bppId": "swiftpost.example.net",
    "bppUri": "https://swiftpost.example.net/beckn",
    "transactionId": "cur-txn-001",
    "messageId": "cur-txn-001-msg-009",
    "timestamp": "2026-03-16T14:00:05.000Z"
  },
  "message": {
    "contract": {
      "id": "contract-cur-001",
      "status": {
        "code": "COMPLETE"
      },
      "commitments": [
        {
          "id": "commitment-001",
          "status": {
            "descriptor": {
              "code": "CLOSED"
            }
          },
          "resources": [
            {
              "id": "pkg-001",
              "quantity": {
                "count": 1
              },
              "resourceAttributes": {
                "@context": "https://schema.nfh.global/Package/v2.0/context.jsonld",
                "@type": "Package",
                "id": "pkg-001",
                "description": "Clothing, 3 pieces",
                "weight": {
                  "value": 1.5,
                  "unit": "kg"
                },
                "dimensions": {
                  "length": 30,
                  "width": 25,
                  "height": 10,
                  "unit": "cm"
                },
                "packageType": "BOX",
                "declaredValue": {
                  "amount": 2000,
                  "currency": "INR"
                }
              }
            }
          ],
          "offer": {
            "id": "offer-next-day",
            "resourceIds": [
              "pkg-001"
            ]
          }
        }
      ],
      "performance": [
        {
          "id": "performance-001",
          "commitmentIds": [
            "commitment-001"
          ],
          "performanceAttributes": {
            "@context": "https://schema.nfh.global/Shipment/v2.0/context.jsonld",
            "@type": "Shipment",
            "id": "SP123456789IN",
            "trackingId": "SP123456789IN",
            "status": "DELIVERED",
            "serviceType": "COURIER",
            "origin": {
              "id": "place-shipper",
              "name": "Meera's studio",
              "type": "PICKUP",
              "address": {
                "line1": "14 Karol Bagh Market",
                "city": "Delhi",
                "pincode": "110005",
                "state": "Delhi",
                "country": "IN"
              },
              "gps": {
                "lat": 28.6519,
                "lng": 77.1909
              }
            },
            "destination": {
              "id": "place-consignee",
              "name": "Customer address",
              "type": "DELIVERY",
              "address": {
                "line1": "22 Hill Road, Bandra West",
                "city": "Mumbai",
                "pincode": "400050",
                "state": "Maharashtra",
                "country": "IN"
              },
              "gps": {
                "lat": 19.0544,
                "lng": 72.8402
              }
            },
            "carrier": {
              "id": "swiftpost.example.net",
              "name": "SwiftPost Express",
              "serviceTypes": [
                "COURIER",
                "EXPRESS"
              ]
            },
            "scheduledPickup": "2026-03-15T16:00:00+05:30",
            "estimatedDelivery": "2026-03-16T19:00:00+05:30",
            "actualDelivery": "2026-03-16T19:30:00+05:30",
            "trackingUpdates": [
              {
                "id": "tu-001",
                "shipmentId": "SP123456789IN",
                "status": "PICKED_UP",
                "timestamp": "2026-03-15T16:30:00+05:30",
                "location": {
                  "lat": 28.6519,
                  "lng": 77.1909,
                  "address": "Karol Bagh, Delhi"
                }
              },
              {
                "id": "tu-002",
                "shipmentId": "SP123456789IN",
                "status": "AT_HUB",
                "timestamp": "2026-03-15T23:00:00+05:30",
                "location": {
                  "lat": 28.5562,
                  "lng": 77.1,
                  "address": "Delhi gateway hub"
                }
              },
              {
                "id": "tu-003",
                "shipmentId": "SP123456789IN",
                "status": "OUT_FOR_DELIVERY",
                "timestamp": "2026-03-16T17:00:00+05:30",
                "location": {
                  "lat": 19.1136,
                  "lng": 72.8697,
                  "address": "Andheri, Mumbai"
                }
              }
            ],
            "proof": {
              "id": "pod-001",
              "shipmentId": "SP123456789IN",
              "type": "SIGNATURE",
              "subType": "DELIVERED_TO_PERSON",
              "recipientName": "R. Shah",
              "timestamp": "2026-03-16T19:30:00+05:30"
            }
          }
        }
      ]
    }
  }
}
```

## Tracking events

| Date/Time | Status | Location |
|-----------|--------|----------|
| Mar 15, 4:30 PM | PICKED_UP | Karol Bagh, Delhi |
| Mar 15, 11:00 PM | AT_HUB | Delhi gateway hub |
| Mar 16, 6:00 AM | IN_TRANSIT | En route to Mumbai |
| Mar 16, 2:00 PM | AT_HUB | Mumbai sorting hub |
| Mar 16, 5:00 PM | OUT_FOR_DELIVERY | Andheri, Mumbai |
| Mar 16, 7:30 PM | DELIVERED | Bandra, Mumbai |

## What the packs cannot express yet

- **Transit time on an offer.** `LogisticsFare` has no property for the promised transit time; the example states it in the offer's `descriptor.shortDesc`.
- **Shipping label.** No pack has a property for the label URL. `LogisticsReceipt.downloadUrl` is the receipt, not the label.

## Schema references

- [Shipment](../../../schema/Shipment/)
- [Consignment](../../../schema/Consignment/)
- [Carrier](../../../schema/Carrier/)
- [Package](../../../schema/Package/)
- [TrackingUpdate](../../../schema/TrackingUpdate/)
- [Proof](../../../schema/Proof/)
- [LogisticsFare](../../../schema/LogisticsFare/)
- [LogisticsReceipt](../../../schema/LogisticsReceipt/)
