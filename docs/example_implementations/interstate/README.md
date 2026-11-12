# Interstate Freight (Less Than Truckload) — End-to-End Example

## Overview

Interstate road freight: a business ships a part-load consignment between two states.

**Scenario:** TechCorp ships 500 kg of electronic components from its Bengaluru warehouse to a distributor in Delhi. It uses the network to compare freight rates from several carriers.

**Schema packs used:** `Package`, `Carrier`, `LogisticsFare`, `LogisticsFareBreakup`, `Consignment`, `Shipment`, `LogisticsPlace`, `LogisticsRoute`, `Waypoint`, `LogisticsDriver`, `LogisticsVehicle`, `TrackingUpdate`

> Every payload on this page is checked in CI (`tools/validate.py examples`): the message against the core
> `beckn.yaml` action schema, and each typed logistics object against its schema pack. The message envelope
> follows the [hyperlocal implementation guide](../hyperlocal_delivery/Logistics_Implementation_Guide.md),
> which also explains the mapping of packs to core slots.

---

## Context values

| Field | Value |
|-------|-------|
| `version` | `2.0.0` |
| `bapId` | `freightdesk.example.net` |
| `bppId` | `roadlink.example.net` |

---

## Discover

The shipper's application looks for carriers that offer the service and cover both states.

```json
{
  "context": {
    "version": "2.0.0",
    "action": "discover",
    "bapId": "freightdesk.example.net",
    "bapUri": "https://freightdesk.example.net/beckn",
    "transactionId": "int-txn-001",
    "messageId": "int-txn-001-msg-001",
    "timestamp": "2026-03-14T10:00:00.000Z"
  },
  "message": {
    "intent": {
      "filters": {
        "type": "jsonpath",
        "expression": "$[?(@.serviceTypes anyof ['INTERSTATE'] && @.serviceCoverage[*].states anyof ['Karnataka'] && @.serviceCoverage[*].states anyof ['Delhi'])]"
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
    "bapId": "freightdesk.example.net",
    "bapUri": "https://freightdesk.example.net/beckn",
    "bppId": "roadlink.example.net",
    "bppUri": "https://roadlink.example.net/beckn",
    "transactionId": "int-txn-001",
    "messageId": "int-txn-001-msg-001",
    "timestamp": "2026-03-14T10:00:00.700Z"
  },
  "message": {
    "catalogs": [
      {
        "id": "catalog-roadlink",
        "descriptor": {
          "name": "RoadLink Logistics freight services"
        },
        "provider": {
          "id": "roadlink.example.net",
          "descriptor": {
            "name": "RoadLink Logistics"
          },
          "providerAttributes": {
            "@context": "https://schema.nfh.global/Carrier/v2.0/context.jsonld",
            "@type": "Carrier",
            "id": "roadlink.example.net",
            "name": "RoadLink Logistics",
            "serviceTypes": [
              "INTERSTATE"
            ]
          }
        },
        "offers": [
          {
            "id": "offer-ltl-road",
            "descriptor": {
              "name": "Interstate Freight by road",
              "shortDesc": "Transit time 4 days"
            },
            "offerAttributes": {
              "@context": "https://schema.nfh.global/LogisticsFare/v2.0/context.jsonld",
              "@type": "LogisticsFare",
              "currency": "INR",
              "totalAmount": 9775,
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

The confirmed contract carries the cargo (`Package`), the booking (`Consignment` in `commitmentAttributes`), the agreed price with its breakup (`LogisticsFare`), and the `Shipment` with the assigned driver, vehicle and planned route.

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_confirm",
    "bapId": "freightdesk.example.net",
    "bapUri": "https://freightdesk.example.net/beckn",
    "bppId": "roadlink.example.net",
    "bppUri": "https://roadlink.example.net/beckn",
    "transactionId": "int-txn-001",
    "messageId": "int-txn-001-msg-004",
    "timestamp": "2026-03-14T10:20:00.000Z"
  },
  "message": {
    "contract": {
      "id": "contract-int-001",
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
                "description": "Electronic components, 20 cartons on 2 pallets",
                "weight": {
                  "value": 500,
                  "unit": "kg"
                },
                "packageType": "PALLET",
                "fragile": true,
                "declaredValue": {
                  "amount": 100000,
                  "currency": "INR"
                },
                "insuranceRequired": true
              }
            }
          ],
          "offer": {
            "id": "offer-ltl-road",
            "resourceIds": [
              "pkg-001"
            ]
          },
          "commitmentAttributes": {
            "@context": "https://schema.nfh.global/Consignment/v2.0/context.jsonld",
            "@type": "Consignment",
            "id": "LR-0001",
            "shipper": {
              "name": "Dispatch desk",
              "company": "TechCorp",
              "phone": "+918000000001"
            },
            "consignee": {
              "name": "Goods inward",
              "company": "Distributor",
              "phone": "+911100000002"
            },
            "totalWeight": {
              "value": 500,
              "unit": "kg"
            },
            "totalPackages": 2,
            "serviceType": "INTERSTATE",
            "paymentMode": "TO_PAY",
            "status": "BOOKED",
            "estimatedDelivery": "2026-03-19T14:00:00+05:30"
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
            "baseFreight": 7500,
            "fuelSurcharge": 750,
            "insuranceCharge": 500,
            "gst": 1476,
            "discount": 451,
            "totalAmount": 9775,
            "breakup": [
              {
                "title": "Base freight (500 kg)",
                "amount": 7500,
                "type": "ITEM"
              },
              {
                "title": "Fuel surcharge at 10%",
                "amount": 750,
                "type": "SURCHARGE"
              },
              {
                "title": "Insurance",
                "amount": 500,
                "type": "FEE"
              },
              {
                "title": "GST at 18%",
                "amount": 1476,
                "type": "TAX"
              },
              {
                "title": "Contract discount",
                "amount": 451,
                "type": "DISCOUNT"
              }
            ],
            "paymentMode": "TO_PAY"
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
            "id": "SHP-LR-0001",
            "trackingId": "SHP-LR-0001",
            "status": "PICKUP_PENDING",
            "serviceType": "INTERSTATE",
            "origin": {
              "id": "place-blr-wh",
              "name": "TechCorp warehouse",
              "type": "WAREHOUSE",
              "address": {
                "line1": "Plot 21, Peenya Industrial Area",
                "city": "Bengaluru",
                "pincode": "560058",
                "state": "Karnataka",
                "country": "IN"
              },
              "gps": {
                "lat": 13.0285,
                "lng": 77.5197
              }
            },
            "destination": {
              "id": "place-del-dist",
              "name": "Distributor warehouse",
              "type": "DELIVERY",
              "address": {
                "line1": "B-14 Okhla Phase II",
                "city": "Delhi",
                "pincode": "110044",
                "state": "Delhi",
                "country": "IN"
              },
              "gps": {
                "lat": 28.5355,
                "lng": 77.28
              }
            },
            "carrier": {
              "id": "roadlink.example.net",
              "name": "RoadLink Logistics",
              "serviceTypes": [
                "INTERSTATE"
              ]
            },
            "driver": {
              "id": "drv-001",
              "name": "Mohan Lal",
              "licenseNumber": "KA1920150012345",
              "phone": "+919800000003"
            },
            "vehicle": {
              "id": "veh-KA19C9876",
              "registrationNumber": "KA19C9876",
              "type": "TRUCK_LCV",
              "gpsEnabled": true
            },
            "route": {
              "id": "route-001",
              "origin": {
                "id": "place-blr-wh",
                "name": "TechCorp warehouse",
                "type": "WAREHOUSE",
                "address": {
                  "line1": "Plot 21, Peenya Industrial Area",
                  "city": "Bengaluru",
                  "pincode": "560058",
                  "state": "Karnataka",
                  "country": "IN"
                },
                "gps": {
                  "lat": 13.0285,
                  "lng": 77.5197
                }
              },
              "destination": {
                "id": "place-del-dist",
                "name": "Distributor warehouse",
                "type": "DELIVERY",
                "address": {
                  "line1": "B-14 Okhla Phase II",
                  "city": "Delhi",
                  "pincode": "110044",
                  "state": "Delhi",
                  "country": "IN"
                },
                "gps": {
                  "lat": 28.5355,
                  "lng": 77.28
                }
              },
              "transportMode": "ROAD",
              "routeType": "LINE_HAUL",
              "totalDistance": {
                "value": 2150,
                "unit": "km"
              },
              "waypoints": [
                {
                  "id": "wp-1",
                  "name": "Hyderabad hub",
                  "type": "HUB",
                  "sequenceNumber": 1,
                  "scheduledArrival": "2026-03-16T22:00:00+05:30",
                  "place": {
                    "id": "place-wp-1",
                    "name": "Hyderabad hub",
                    "type": "HUB",
                    "gps": {
                      "lat": 17.385,
                      "lng": 78.4867
                    }
                  }
                },
                {
                  "id": "wp-2",
                  "name": "Nagpur relay point",
                  "type": "RELAY_POINT",
                  "sequenceNumber": 2,
                  "scheduledArrival": "2026-03-17T14:00:00+05:30",
                  "place": {
                    "id": "place-wp-2",
                    "name": "Nagpur relay point",
                    "type": "WAYPOINT",
                    "gps": {
                      "lat": 21.1458,
                      "lng": 79.0882
                    }
                  }
                },
                {
                  "id": "wp-3",
                  "name": "Delhi gateway hub",
                  "type": "HUB",
                  "sequenceNumber": 3,
                  "scheduledArrival": "2026-03-19T06:00:00+05:30",
                  "place": {
                    "id": "place-wp-3",
                    "name": "Delhi gateway hub",
                    "type": "HUB",
                    "gps": {
                      "lat": 28.5562,
                      "lng": 77.1
                    }
                  }
                }
              ]
            },
            "scheduledPickup": "2026-03-16T08:00:00+05:30",
            "estimatedDelivery": "2026-03-19T14:00:00+05:30"
          }
        }
      ]
    }
  }
}
```

## On-status (in transit)

```json
{
  "context": {
    "version": "2.0.0",
    "action": "on_status",
    "bapId": "freightdesk.example.net",
    "bapUri": "https://freightdesk.example.net/beckn",
    "bppId": "roadlink.example.net",
    "bppUri": "https://roadlink.example.net/beckn",
    "transactionId": "int-txn-001",
    "messageId": "int-txn-001-msg-008",
    "timestamp": "2026-03-16T22:00:00.000+05:30"
  },
  "message": {
    "contract": {
      "id": "contract-int-001",
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
                "description": "Electronic components, 20 cartons on 2 pallets",
                "weight": {
                  "value": 500,
                  "unit": "kg"
                },
                "packageType": "PALLET",
                "fragile": true,
                "declaredValue": {
                  "amount": 100000,
                  "currency": "INR"
                },
                "insuranceRequired": true
              }
            }
          ],
          "offer": {
            "id": "offer-ltl-road",
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
            "id": "SHP-LR-0001",
            "trackingId": "SHP-LR-0001",
            "status": "IN_TRANSIT",
            "serviceType": "INTERSTATE",
            "origin": {
              "id": "place-blr-wh",
              "name": "TechCorp warehouse",
              "type": "WAREHOUSE",
              "address": {
                "line1": "Plot 21, Peenya Industrial Area",
                "city": "Bengaluru",
                "pincode": "560058",
                "state": "Karnataka",
                "country": "IN"
              },
              "gps": {
                "lat": 13.0285,
                "lng": 77.5197
              }
            },
            "destination": {
              "id": "place-del-dist",
              "name": "Distributor warehouse",
              "type": "DELIVERY",
              "address": {
                "line1": "B-14 Okhla Phase II",
                "city": "Delhi",
                "pincode": "110044",
                "state": "Delhi",
                "country": "IN"
              },
              "gps": {
                "lat": 28.5355,
                "lng": 77.28
              }
            },
            "carrier": {
              "id": "roadlink.example.net",
              "name": "RoadLink Logistics",
              "serviceTypes": [
                "INTERSTATE"
              ]
            },
            "driver": {
              "id": "drv-001",
              "name": "Mohan Lal",
              "licenseNumber": "KA1920150012345",
              "phone": "+919800000003"
            },
            "vehicle": {
              "id": "veh-KA19C9876",
              "registrationNumber": "KA19C9876",
              "type": "TRUCK_LCV",
              "gpsEnabled": true
            },
            "route": {
              "id": "route-001",
              "origin": {
                "id": "place-blr-wh",
                "name": "TechCorp warehouse",
                "type": "WAREHOUSE",
                "address": {
                  "line1": "Plot 21, Peenya Industrial Area",
                  "city": "Bengaluru",
                  "pincode": "560058",
                  "state": "Karnataka",
                  "country": "IN"
                },
                "gps": {
                  "lat": 13.0285,
                  "lng": 77.5197
                }
              },
              "destination": {
                "id": "place-del-dist",
                "name": "Distributor warehouse",
                "type": "DELIVERY",
                "address": {
                  "line1": "B-14 Okhla Phase II",
                  "city": "Delhi",
                  "pincode": "110044",
                  "state": "Delhi",
                  "country": "IN"
                },
                "gps": {
                  "lat": 28.5355,
                  "lng": 77.28
                }
              },
              "transportMode": "ROAD",
              "routeType": "LINE_HAUL",
              "totalDistance": {
                "value": 2150,
                "unit": "km"
              },
              "waypoints": [
                {
                  "id": "wp-1",
                  "name": "Hyderabad hub",
                  "type": "HUB",
                  "sequenceNumber": 1,
                  "scheduledArrival": "2026-03-16T22:00:00+05:30",
                  "place": {
                    "id": "place-wp-1",
                    "name": "Hyderabad hub",
                    "type": "HUB",
                    "gps": {
                      "lat": 17.385,
                      "lng": 78.4867
                    }
                  }
                },
                {
                  "id": "wp-2",
                  "name": "Nagpur relay point",
                  "type": "RELAY_POINT",
                  "sequenceNumber": 2,
                  "scheduledArrival": "2026-03-17T14:00:00+05:30",
                  "place": {
                    "id": "place-wp-2",
                    "name": "Nagpur relay point",
                    "type": "WAYPOINT",
                    "gps": {
                      "lat": 21.1458,
                      "lng": 79.0882
                    }
                  }
                },
                {
                  "id": "wp-3",
                  "name": "Delhi gateway hub",
                  "type": "HUB",
                  "sequenceNumber": 3,
                  "scheduledArrival": "2026-03-19T06:00:00+05:30",
                  "place": {
                    "id": "place-wp-3",
                    "name": "Delhi gateway hub",
                    "type": "HUB",
                    "gps": {
                      "lat": 28.5562,
                      "lng": 77.1
                    }
                  }
                }
              ]
            },
            "scheduledPickup": "2026-03-16T08:00:00+05:30",
            "estimatedDelivery": "2026-03-19T14:00:00+05:30",
            "trackingUpdates": [
              {
                "id": "tu-001",
                "shipmentId": "SHP-LR-0001",
                "status": "PICKED_UP",
                "timestamp": "2026-03-16T08:00:00+05:30",
                "vehicle": {
                  "id": "veh-KA19C9876",
                  "registrationNumber": "KA19C9876",
                  "type": "TRUCK_LCV",
                  "gpsEnabled": true
                }
              },
              {
                "id": "tu-002",
                "shipmentId": "SHP-LR-0001",
                "status": "AT_HUB",
                "timestamp": "2026-03-16T22:00:00+05:30",
                "location": {
                  "lat": 17.385,
                  "lng": 78.4867,
                  "address": "Hyderabad hub"
                },
                "message": "Reached Hyderabad hub"
              }
            ]
          }
        }
      ]
    }
  }
}
```

## Route plan

| Waypoint | ETA | Type |
|----------|-----|------|
| Bengaluru (origin) | Mar 16, 8:00 AM | PICKUP |
| Hyderabad hub | Mar 16, 10:00 PM | HUB |
| Nagpur relay point | Mar 17, 2:00 PM | RELAY_POINT |
| Delhi gateway hub | Mar 19, 6:00 AM | HUB |
| Delhi (destination) | Mar 19, 2:00 PM | DELIVERY |

## What the packs cannot express yet

- **Lorry receipt number.** No pack has a property for the consignment note or lorry receipt number; the example uses it as the `Consignment.id`.
- **Load type.** `LTL` versus `FTL` is not an attribute of `Consignment` or `Shipment`.
- **Cargo category.** `Package` has no category or commodity code.

## Schema references

- [Consignment](../../../schema/Consignment/)
- [Shipment](../../../schema/Shipment/)
- [LogisticsRoute](../../../schema/LogisticsRoute/)
- [Waypoint](../../../schema/Waypoint/)
- [LogisticsDriver](../../../schema/LogisticsDriver/)
- [LogisticsVehicle](../../../schema/LogisticsVehicle/)
- [LogisticsFare](../../../schema/LogisticsFare/)
- [TrackingUpdate](../../../schema/TrackingUpdate/)
