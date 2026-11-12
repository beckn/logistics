# Express Delivery (Same-Day Guaranteed) — End-to-End Example

## Overview

Time-critical express delivery with a guaranteed delivery window.

**Scenario:** Arvind needs to send a signed legal document from his office in Connaught Place, Delhi to a law firm in South Delhi, guaranteed within 3 hours.

**Schema packs used:** `Package`, `LogisticsFare`, `LogisticsFareBreakup`, `LogisticsOperator`, `Courier`, `Shipment`, `LogisticsPlace`, `DeliverySlot`, `LogisticsCancellationPolicy`, `TrackingUpdate`, `Proof`, `LogisticsAlert`, `LogisticsFeedback`, `LogisticsRating`

> Every payload on this page is checked in CI (`tools/validate.py examples`): the message against the core
> `beckn.yaml` action schema, and each typed logistics object against its schema pack. The message envelope
> follows the [hyperlocal implementation guide](../hyperlocal_delivery/Logistics_Implementation_Guide.md),
> which also explains the mapping of packs to core slots.

---

## Context values

| Field | Value |
|-------|-------|
| `version` | `2.0.0` |
| `bapId` | `dispatchnow.example.net` |
| `bppId` | `rapidline.example.net` |

---

## Discover

```json
{
  "context": {
    "version": "2.0.0",
    "action": "discover",
    "bapId": "dispatchnow.example.net",
    "bapUri": "https://dispatchnow.example.net/beckn",
    "transactionId": "exp-txn-001",
    "messageId": "exp-txn-001-msg-001",
    "timestamp": "2026-03-15T14:25:00.000Z"
  },
  "message": {
    "intent": {
      "spatial": [
        {
          "targets": [
            "$['serviceableArea'][*]['geo']"
          ],
          "op": "S_CONTAINS",
          "geometry": {
            "type": "LineString",
            "coordinates": [
              [
                77.2167,
                28.6315
              ],
              [
                77.209,
                28.5353
              ]
            ]
          }
        }
      ],
      "filters": {
        "type": "jsonpath",
        "expression": "$[?(@.serviceTypes anyof ['EXPRESS'] && @.deliveryWindowMinutes <= 180)]"
      }
    }
  }
}
```

## On-discover

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_discover",
    "bapId": "dispatchnow.example.net",
    "bapUri": "https://dispatchnow.example.net/beckn",
    "bppId": "rapidline.example.net",
    "bppUri": "https://rapidline.example.net/beckn",
    "transactionId": "exp-txn-001",
    "messageId": "exp-txn-001-msg-001",
    "timestamp": "2026-03-15T14:25:00.500Z"
  },
  "message": {
    "catalogs": [
      {
        "id": "catalog-rapidline",
        "descriptor": {
          "name": "RapidLine express services"
        },
        "provider": {
          "id": "rapidline.example.net",
          "descriptor": {
            "name": "RapidLine Express"
          }
        },
        "offers": [
          {
            "id": "offer-express-3hr",
            "descriptor": {
              "name": "3-hour express",
              "shortDesc": "Guaranteed within 3 hours, full refund if late"
            },
            "offerAttributes": {
              "@context": "https://schema.nfh.global/LogisticsFare/v2.0/context.jsonld",
              "@type": "LogisticsFare",
              "currency": "INR",
              "totalAmount": 299,
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

The courier is a participant of the contract (`Courier` in `participantAttributes`). The guaranteed window is the `DeliverySlot` nested in the `Shipment`.

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_confirm",
    "bapId": "dispatchnow.example.net",
    "bapUri": "https://dispatchnow.example.net/beckn",
    "bppId": "rapidline.example.net",
    "bppUri": "https://rapidline.example.net/beckn",
    "transactionId": "exp-txn-001",
    "messageId": "exp-txn-001-msg-004",
    "timestamp": "2026-03-15T14:30:00.000Z"
  },
  "message": {
    "contract": {
      "id": "contract-exp-001",
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
                "description": "Signed legal documents",
                "weight": {
                  "value": 0.5,
                  "unit": "kg"
                },
                "packageType": "ENVELOPE"
              }
            }
          ],
          "offer": {
            "id": "offer-express-3hr",
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
            "id": "TRK-EXP-999",
            "trackingId": "TRK-EXP-999",
            "status": "PICKUP_PENDING",
            "serviceType": "EXPRESS",
            "origin": {
              "id": "place-cp-office",
              "name": "Arvind's office",
              "type": "PICKUP",
              "address": {
                "line1": "Block B, Connaught Place",
                "city": "Delhi",
                "pincode": "110001"
              },
              "gps": {
                "lat": 28.6315,
                "lng": 77.2167
              }
            },
            "destination": {
              "id": "place-saket-firm",
              "name": "Law firm",
              "type": "DELIVERY",
              "address": {
                "line1": "12 Press Enclave Road, Saket",
                "city": "Delhi",
                "pincode": "110017"
              },
              "gps": {
                "lat": 28.5353,
                "lng": 77.209
              }
            },
            "deliverySlot": {
              "id": "slot-3hr",
              "date": "2026-03-15",
              "startTime": "14:30",
              "endTime": "17:30",
              "label": "EXPRESS_2HR"
            },
            "scheduledPickup": "2026-03-15T14:42:00+05:30",
            "estimatedDelivery": "2026-03-15T17:30:00+05:30",
            "cancellationPolicy": {
              "id": "cp-express",
              "cancellableUntil": "BEFORE_PICKUP",
              "cancellationFee": {
                "type": "NIL",
                "value": 0,
                "currency": "INR"
              }
            }
          }
        }
      ],
      "participants": [
        {
          "id": "rapidline.example.net",
          "participantAttributes": {
            "@context": "https://schema.nfh.global/LogisticsOperator/v2.0/context.jsonld",
            "@type": "LogisticsOperator",
            "id": "rapidline.example.net",
            "name": "RapidLine Express"
          }
        },
        {
          "id": "courier-077",
          "participantAttributes": {
            "@context": "https://schema.nfh.global/Courier/v2.0/context.jsonld",
            "@type": "Courier",
            "id": "courier-077",
            "name": "Vikram Singh",
            "phone": "+911100000077",
            "rating": 4.9,
            "vehicleType": "MOTORCYCLE",
            "vehicleNumber": "DL05SA6789",
            "status": "ASSIGNED"
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
            "baseFreight": 250,
            "fuelSurcharge": 4,
            "gst": 45,
            "totalAmount": 299,
            "breakup": [
              {
                "title": "Express delivery fee",
                "amount": 250,
                "type": "ITEM"
              },
              {
                "title": "Fuel surcharge",
                "amount": 4,
                "type": "SURCHARGE"
              },
              {
                "title": "GST at 18%",
                "amount": 45,
                "type": "TAX"
              }
            ],
            "paymentMode": "PREPAID"
          }
        }
      ]
    }
  }
}
```

## On-status (delivered)

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_status",
    "bapId": "dispatchnow.example.net",
    "bapUri": "https://dispatchnow.example.net/beckn",
    "bppId": "rapidline.example.net",
    "bppUri": "https://rapidline.example.net/beckn",
    "transactionId": "exp-txn-001",
    "messageId": "exp-txn-001-msg-009",
    "timestamp": "2026-03-15T16:02:05.000Z"
  },
  "message": {
    "contract": {
      "id": "contract-exp-001",
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
                "description": "Signed legal documents",
                "weight": {
                  "value": 0.5,
                  "unit": "kg"
                },
                "packageType": "ENVELOPE"
              }
            }
          ],
          "offer": {
            "id": "offer-express-3hr",
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
            "id": "TRK-EXP-999",
            "trackingId": "TRK-EXP-999",
            "status": "DELIVERED",
            "serviceType": "EXPRESS",
            "origin": {
              "id": "place-cp-office",
              "name": "Arvind's office",
              "type": "PICKUP",
              "address": {
                "line1": "Block B, Connaught Place",
                "city": "Delhi",
                "pincode": "110001"
              },
              "gps": {
                "lat": 28.6315,
                "lng": 77.2167
              }
            },
            "destination": {
              "id": "place-saket-firm",
              "name": "Law firm",
              "type": "DELIVERY",
              "address": {
                "line1": "12 Press Enclave Road, Saket",
                "city": "Delhi",
                "pincode": "110017"
              },
              "gps": {
                "lat": 28.5353,
                "lng": 77.209
              }
            },
            "deliverySlot": {
              "id": "slot-3hr",
              "date": "2026-03-15",
              "startTime": "14:30",
              "endTime": "17:30",
              "label": "EXPRESS_2HR"
            },
            "scheduledPickup": "2026-03-15T14:42:00+05:30",
            "estimatedDelivery": "2026-03-15T17:30:00+05:30",
            "cancellationPolicy": {
              "id": "cp-express",
              "cancellableUntil": "BEFORE_PICKUP",
              "cancellationFee": {
                "type": "NIL",
                "value": 0,
                "currency": "INR"
              }
            },
            "actualDelivery": "2026-03-15T16:02:00+05:30",
            "proof": {
              "id": "pod-exp-001",
              "shipmentId": "TRK-EXP-999",
              "type": "OTP",
              "subType": "DELIVERED_TO_PERSON",
              "otpVerified": true,
              "recipientName": "Front desk",
              "location": {
                "lat": 28.5353,
                "lng": 77.209
              },
              "timestamp": "2026-03-15T16:02:00+05:30"
            },
            "trackingUpdates": [
              {
                "id": "tu-001",
                "shipmentId": "TRK-EXP-999",
                "status": "PICKED_UP",
                "timestamp": "2026-03-15T14:42:00+05:30"
              },
              {
                "id": "tu-002",
                "shipmentId": "TRK-EXP-999",
                "status": "OUT_FOR_DELIVERY",
                "timestamp": "2026-03-15T15:48:00+05:30"
              },
              {
                "id": "tu-003",
                "shipmentId": "TRK-EXP-999",
                "status": "DELIVERED",
                "timestamp": "2026-03-15T16:02:00+05:30"
              }
            ]
          }
        }
      ]
    }
  }
}
```

## Delivery timeline

| Time | Event | Status |
|------|-------|--------|
| 2:30 PM | Order confirmed, courier assigned | PICKUP_PENDING |
| 2:42 PM | Courier picks up the envelope at Connaught Place | PICKED_UP |
| 3:48 PM | Out for delivery in Saket | OUT_FOR_DELIVERY |
| 4:02 PM | Delivered, OTP confirmed | DELIVERED |

**Total time:** 1 hour 32 minutes against a 3-hour guarantee.

## On-update (guarantee missed)

If the delivery is going to miss the guarantee, the provider declares it with a `LogisticsAlert` nested in the `Shipment`:

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_update",
    "bapId": "dispatchnow.example.net",
    "bapUri": "https://dispatchnow.example.net/beckn",
    "bppId": "rapidline.example.net",
    "bppUri": "https://rapidline.example.net/beckn",
    "transactionId": "exp-txn-001",
    "messageId": "exp-txn-001-msg-010",
    "timestamp": "2026-03-15T17:20:05.000Z"
  },
  "message": {
    "contract": {
      "id": "contract-exp-001",
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
                "description": "Signed legal documents",
                "weight": {
                  "value": 0.5,
                  "unit": "kg"
                },
                "packageType": "ENVELOPE"
              }
            }
          ],
          "offer": {
            "id": "offer-express-3hr",
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
            "id": "TRK-EXP-999",
            "trackingId": "TRK-EXP-999",
            "status": "OUT_FOR_DELIVERY",
            "serviceType": "EXPRESS",
            "origin": {
              "id": "place-cp-office",
              "name": "Arvind's office",
              "type": "PICKUP",
              "address": {
                "line1": "Block B, Connaught Place",
                "city": "Delhi",
                "pincode": "110001"
              },
              "gps": {
                "lat": 28.6315,
                "lng": 77.2167
              }
            },
            "destination": {
              "id": "place-saket-firm",
              "name": "Law firm",
              "type": "DELIVERY",
              "address": {
                "line1": "12 Press Enclave Road, Saket",
                "city": "Delhi",
                "pincode": "110017"
              },
              "gps": {
                "lat": 28.5353,
                "lng": 77.209
              }
            },
            "deliverySlot": {
              "id": "slot-3hr",
              "date": "2026-03-15",
              "startTime": "14:30",
              "endTime": "17:30",
              "label": "EXPRESS_2HR"
            },
            "scheduledPickup": "2026-03-15T14:42:00+05:30",
            "estimatedDelivery": "2026-03-15T17:30:00+05:30",
            "cancellationPolicy": {
              "id": "cp-express",
              "cancellableUntil": "BEFORE_PICKUP",
              "cancellationFee": {
                "type": "NIL",
                "value": 0,
                "currency": "INR"
              }
            },
            "alerts": [
              {
                "id": "alert-001",
                "shipmentId": "TRK-EXP-999",
                "type": "SLA_BREACH",
                "severity": "CRITICAL",
                "message": "Delivery will miss the 3-hour guarantee. The delivery fee of INR 299 is being refunded.",
                "cause": "Road closure on Ring Road",
                "impactedETA": "2026-03-15T17:55:00+05:30",
                "timestamp": "2026-03-15T17:20:00+05:30",
                "status": "OPEN",
                "actionRequired": false
              }
            ]
          }
        }
      ]
    }
  }
}
```

## Rate

The rating and the written feedback travel together as a `LogisticsFeedback` in `targetAttributes`:

```json
{
  "context": {
    "version": "2.0.0",
    "action": "rate",
    "bapId": "dispatchnow.example.net",
    "bapUri": "https://dispatchnow.example.net/beckn",
    "bppId": "rapidline.example.net",
    "bppUri": "https://rapidline.example.net/beckn",
    "transactionId": "exp-txn-001",
    "messageId": "exp-txn-001-msg-012",
    "timestamp": "2026-03-15T16:30:00.000Z"
  },
  "message": {
    "ratingInputs": [
      {
        "target": {
          "id": "courier-077",
          "descriptor": {
            "name": "Vikram Singh"
          },
          "targetAttributes": {
            "@context": "https://schema.nfh.global/LogisticsFeedback/v2.0/context.jsonld",
            "@type": "LogisticsFeedback",
            "id": "fb-001",
            "shipmentId": "TRK-EXP-999",
            "rating": {
              "value": 5,
              "ratingFor": "DRIVER",
              "categories": {
                "timeliness": 5,
                "handling": 5,
                "communication": 5
              }
            },
            "review": "Much faster than expected. Very professional.",
            "tags": [
              "fast",
              "professional"
            ],
            "wouldRecommend": true
          }
        },
        "range": {
          "min": 1,
          "max": 5
        }
      }
    ]
  }
}
```

## What the packs cannot express yet

- **Guarantee terms.** The guaranteed window and the refund on a miss have no property in `LogisticsFare` or `DeliverySlot`; the example states them in the offer's `descriptor.shortDesc` and in the alert message.
- **Slot labels.** `DeliverySlot.label` has `EXPRESS_1HR` and `EXPRESS_2HR` but nothing for a 3-hour window.
- **Refund.** A refund triggered by an alert belongs to settlement, which the implementation guide defers.

## Schema references

- [Shipment](../../../schema/Shipment/)
- [DeliverySlot](../../../schema/DeliverySlot/)
- [Courier](../../../schema/Courier/)
- [TrackingUpdate](../../../schema/TrackingUpdate/)
- [LogisticsAlert](../../../schema/LogisticsAlert/)
- [Proof](../../../schema/Proof/)
- [LogisticsFare](../../../schema/LogisticsFare/)
- [LogisticsFeedback](../../../schema/LogisticsFeedback/)
- [LogisticsRating](../../../schema/LogisticsRating/)
