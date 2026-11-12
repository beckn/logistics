# Long Haul (Full Truck Load) — End-to-End Example

## Overview

Long-haul full truck load: bulk cargo shipped across the country on a dedicated vehicle.

**Scenario:** ManuCorp ships a full truck load of industrial machinery (8 tonnes) from Mumbai to Chennai. It needs live tracking, the driver's contact details and proof of delivery.

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
| `bapId` | `truckdesk.example.net` |
| `bppId` | `highwayfleet.example.net` |

---

## Discover

The shipper's application looks for carriers that offer the service and cover both states.

```json
{
  "context": {
    "version": "2.0.0",
    "action": "discover",
    "bapId": "truckdesk.example.net",
    "bapUri": "https://truckdesk.example.net/beckn",
    "transactionId": "lh-txn-001",
    "messageId": "lh-txn-001-msg-001",
    "timestamp": "2026-03-14T10:00:00.000Z"
  },
  "message": {
    "intent": {
      "filters": {
        "type": "jsonpath",
        "expression": "$[?(@.serviceTypes anyof ['LONG_HAUL'] && @.serviceCoverage[*].states anyof ['Maharashtra'] && @.serviceCoverage[*].states anyof ['Tamil Nadu'])]"
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
    "bapId": "truckdesk.example.net",
    "bapUri": "https://truckdesk.example.net/beckn",
    "bppId": "highwayfleet.example.net",
    "bppUri": "https://highwayfleet.example.net/beckn",
    "transactionId": "lh-txn-001",
    "messageId": "lh-txn-001-msg-001",
    "timestamp": "2026-03-14T10:00:00.700Z"
  },
  "message": {
    "catalogs": [
      {
        "id": "catalog-highwayfleet",
        "descriptor": {
          "name": "Highway Fleet Carriers freight services"
        },
        "provider": {
          "id": "highwayfleet.example.net",
          "descriptor": {
            "name": "Highway Fleet Carriers"
          },
          "providerAttributes": {
            "@context": "https://schema.nfh.global/Carrier/v2.0/context.jsonld",
            "@type": "Carrier",
            "id": "highwayfleet.example.net",
            "name": "Highway Fleet Carriers",
            "serviceTypes": [
              "LONG_HAUL"
            ]
          }
        },
        "offers": [
          {
            "id": "offer-ftl-32ft",
            "descriptor": {
              "name": "Long Haul by road",
              "shortDesc": "Transit time 4 days"
            },
            "offerAttributes": {
              "@context": "https://schema.nfh.global/LogisticsFare/v2.0/context.jsonld",
              "@type": "LogisticsFare",
              "currency": "INR",
              "totalAmount": 60900,
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
    "bapId": "truckdesk.example.net",
    "bapUri": "https://truckdesk.example.net/beckn",
    "bppId": "highwayfleet.example.net",
    "bppUri": "https://highwayfleet.example.net/beckn",
    "transactionId": "lh-txn-001",
    "messageId": "lh-txn-001-msg-004",
    "timestamp": "2026-03-14T10:20:00.000Z"
  },
  "message": {
    "contract": {
      "id": "contract-lh-001",
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
                "description": "Industrial machinery, 3 crated units",
                "weight": {
                  "value": 8000,
                  "unit": "kg"
                },
                "packageType": "PALLET",
                "declaredValue": {
                  "amount": 1500000,
                  "currency": "INR"
                },
                "insuranceRequired": true
              }
            }
          ],
          "offer": {
            "id": "offer-ftl-32ft",
            "resourceIds": [
              "pkg-001"
            ]
          },
          "commitmentAttributes": {
            "@context": "https://schema.nfh.global/Consignment/v2.0/context.jsonld",
            "@type": "Consignment",
            "id": "CN-0456",
            "shipper": {
              "name": "Dispatch desk",
              "company": "ManuCorp",
              "phone": "+918000000001"
            },
            "consignee": {
              "name": "Goods inward",
              "company": "Customer plant",
              "phone": "+911100000002"
            },
            "totalWeight": {
              "value": 8,
              "unit": "ton"
            },
            "totalPackages": 3,
            "serviceType": "LONG_HAUL",
            "paymentMode": "PREPAID",
            "status": "BOOKED",
            "estimatedDelivery": "2026-03-20T14:00:00+05:30"
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
            "baseFreight": 40000,
            "fuelSurcharge": 4800,
            "insuranceCharge": 7500,
            "gst": 2400,
            "otherCharges": 6200,
            "totalAmount": 60900,
            "breakup": [
              {
                "title": "Base freight (8 t, 1,350 km)",
                "amount": 40000,
                "type": "ITEM"
              },
              {
                "title": "Fuel surcharge at 12%",
                "amount": 4800,
                "type": "SURCHARGE"
              },
              {
                "title": "Toll charges",
                "amount": 3200,
                "type": "FEE"
              },
              {
                "title": "Loading and unloading",
                "amount": 3000,
                "type": "FEE"
              },
              {
                "title": "Insurance",
                "amount": 7500,
                "type": "FEE"
              },
              {
                "title": "GST at 5%",
                "amount": 2400,
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
            "id": "SHP-CN-0456",
            "trackingId": "SHP-CN-0456",
            "status": "PICKUP_PENDING",
            "serviceType": "LONG_HAUL",
            "origin": {
              "id": "place-mum-yard",
              "name": "ManuCorp yard, Nhava Sheva",
              "type": "WAREHOUSE",
              "address": {
                "line1": "Plot 7, JNPT Road",
                "city": "Navi Mumbai",
                "pincode": "400703",
                "state": "Maharashtra",
                "country": "IN"
              },
              "gps": {
                "lat": 18.949,
                "lng": 72.951
              }
            },
            "destination": {
              "id": "place-chn-plant",
              "name": "Customer plant, Guindy",
              "type": "DELIVERY",
              "address": {
                "line1": "45 Industrial Estate",
                "city": "Chennai",
                "pincode": "600032",
                "state": "Tamil Nadu",
                "country": "IN"
              },
              "gps": {
                "lat": 13.0067,
                "lng": 80.2206
              }
            },
            "carrier": {
              "id": "highwayfleet.example.net",
              "name": "Highway Fleet Carriers",
              "serviceTypes": [
                "LONG_HAUL"
              ]
            },
            "driver": {
              "id": "drv-001",
              "name": "Suresh Yadav",
              "licenseNumber": "MH0420120067890",
              "phone": "+919800000003"
            },
            "vehicle": {
              "id": "veh-MH04FP5678",
              "registrationNumber": "MH04FP5678",
              "type": "TRUCK_HCV",
              "gpsEnabled": true
            },
            "route": {
              "id": "route-001",
              "origin": {
                "id": "place-mum-yard",
                "name": "ManuCorp yard, Nhava Sheva",
                "type": "WAREHOUSE",
                "address": {
                  "line1": "Plot 7, JNPT Road",
                  "city": "Navi Mumbai",
                  "pincode": "400703",
                  "state": "Maharashtra",
                  "country": "IN"
                },
                "gps": {
                  "lat": 18.949,
                  "lng": 72.951
                }
              },
              "destination": {
                "id": "place-chn-plant",
                "name": "Customer plant, Guindy",
                "type": "DELIVERY",
                "address": {
                  "line1": "45 Industrial Estate",
                  "city": "Chennai",
                  "pincode": "600032",
                  "state": "Tamil Nadu",
                  "country": "IN"
                },
                "gps": {
                  "lat": 13.0067,
                  "lng": 80.2206
                }
              },
              "transportMode": "ROAD",
              "routeType": "LINE_HAUL",
              "totalDistance": {
                "value": 1670,
                "unit": "km"
              },
              "waypoints": [
                {
                  "id": "wp-1",
                  "name": "Pune bypass",
                  "type": "RELAY_POINT",
                  "sequenceNumber": 1,
                  "scheduledArrival": "2026-03-17T13:00:00+05:30",
                  "place": {
                    "id": "place-wp-1",
                    "name": "Pune bypass",
                    "type": "WAYPOINT",
                    "gps": {
                      "lat": 18.5204,
                      "lng": 73.8567
                    }
                  }
                },
                {
                  "id": "wp-2",
                  "name": "Solapur hub",
                  "type": "HUB",
                  "sequenceNumber": 2,
                  "scheduledArrival": "2026-03-17T19:00:00+05:30",
                  "place": {
                    "id": "place-wp-2",
                    "name": "Solapur hub",
                    "type": "HUB",
                    "gps": {
                      "lat": 17.6599,
                      "lng": 75.9064
                    }
                  }
                },
                {
                  "id": "wp-3",
                  "name": "Hyderabad relay point",
                  "type": "RELAY_POINT",
                  "sequenceNumber": 3,
                  "scheduledArrival": "2026-03-18T06:00:00+05:30",
                  "place": {
                    "id": "place-wp-3",
                    "name": "Hyderabad relay point",
                    "type": "WAYPOINT",
                    "gps": {
                      "lat": 17.385,
                      "lng": 78.4867
                    }
                  }
                },
                {
                  "id": "wp-4",
                  "name": "Bengaluru hub",
                  "type": "HUB",
                  "sequenceNumber": 4,
                  "scheduledArrival": "2026-03-19T04:00:00+05:30",
                  "place": {
                    "id": "place-wp-4",
                    "name": "Bengaluru hub",
                    "type": "HUB",
                    "gps": {
                      "lat": 12.9716,
                      "lng": 77.5946
                    }
                  }
                }
              ]
            },
            "scheduledPickup": "2026-03-17T09:00:00+05:30",
            "estimatedDelivery": "2026-03-20T14:00:00+05:30"
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
    "bapId": "truckdesk.example.net",
    "bapUri": "https://truckdesk.example.net/beckn",
    "bppId": "highwayfleet.example.net",
    "bppUri": "https://highwayfleet.example.net/beckn",
    "transactionId": "lh-txn-001",
    "messageId": "lh-txn-001-msg-008",
    "timestamp": "2026-03-17T13:00:00.000+05:30"
  },
  "message": {
    "contract": {
      "id": "contract-lh-001",
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
                "description": "Industrial machinery, 3 crated units",
                "weight": {
                  "value": 8000,
                  "unit": "kg"
                },
                "packageType": "PALLET",
                "declaredValue": {
                  "amount": 1500000,
                  "currency": "INR"
                },
                "insuranceRequired": true
              }
            }
          ],
          "offer": {
            "id": "offer-ftl-32ft",
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
            "id": "SHP-CN-0456",
            "trackingId": "SHP-CN-0456",
            "status": "IN_TRANSIT",
            "serviceType": "LONG_HAUL",
            "origin": {
              "id": "place-mum-yard",
              "name": "ManuCorp yard, Nhava Sheva",
              "type": "WAREHOUSE",
              "address": {
                "line1": "Plot 7, JNPT Road",
                "city": "Navi Mumbai",
                "pincode": "400703",
                "state": "Maharashtra",
                "country": "IN"
              },
              "gps": {
                "lat": 18.949,
                "lng": 72.951
              }
            },
            "destination": {
              "id": "place-chn-plant",
              "name": "Customer plant, Guindy",
              "type": "DELIVERY",
              "address": {
                "line1": "45 Industrial Estate",
                "city": "Chennai",
                "pincode": "600032",
                "state": "Tamil Nadu",
                "country": "IN"
              },
              "gps": {
                "lat": 13.0067,
                "lng": 80.2206
              }
            },
            "carrier": {
              "id": "highwayfleet.example.net",
              "name": "Highway Fleet Carriers",
              "serviceTypes": [
                "LONG_HAUL"
              ]
            },
            "driver": {
              "id": "drv-001",
              "name": "Suresh Yadav",
              "licenseNumber": "MH0420120067890",
              "phone": "+919800000003"
            },
            "vehicle": {
              "id": "veh-MH04FP5678",
              "registrationNumber": "MH04FP5678",
              "type": "TRUCK_HCV",
              "gpsEnabled": true
            },
            "route": {
              "id": "route-001",
              "origin": {
                "id": "place-mum-yard",
                "name": "ManuCorp yard, Nhava Sheva",
                "type": "WAREHOUSE",
                "address": {
                  "line1": "Plot 7, JNPT Road",
                  "city": "Navi Mumbai",
                  "pincode": "400703",
                  "state": "Maharashtra",
                  "country": "IN"
                },
                "gps": {
                  "lat": 18.949,
                  "lng": 72.951
                }
              },
              "destination": {
                "id": "place-chn-plant",
                "name": "Customer plant, Guindy",
                "type": "DELIVERY",
                "address": {
                  "line1": "45 Industrial Estate",
                  "city": "Chennai",
                  "pincode": "600032",
                  "state": "Tamil Nadu",
                  "country": "IN"
                },
                "gps": {
                  "lat": 13.0067,
                  "lng": 80.2206
                }
              },
              "transportMode": "ROAD",
              "routeType": "LINE_HAUL",
              "totalDistance": {
                "value": 1670,
                "unit": "km"
              },
              "waypoints": [
                {
                  "id": "wp-1",
                  "name": "Pune bypass",
                  "type": "RELAY_POINT",
                  "sequenceNumber": 1,
                  "scheduledArrival": "2026-03-17T13:00:00+05:30",
                  "place": {
                    "id": "place-wp-1",
                    "name": "Pune bypass",
                    "type": "WAYPOINT",
                    "gps": {
                      "lat": 18.5204,
                      "lng": 73.8567
                    }
                  }
                },
                {
                  "id": "wp-2",
                  "name": "Solapur hub",
                  "type": "HUB",
                  "sequenceNumber": 2,
                  "scheduledArrival": "2026-03-17T19:00:00+05:30",
                  "place": {
                    "id": "place-wp-2",
                    "name": "Solapur hub",
                    "type": "HUB",
                    "gps": {
                      "lat": 17.6599,
                      "lng": 75.9064
                    }
                  }
                },
                {
                  "id": "wp-3",
                  "name": "Hyderabad relay point",
                  "type": "RELAY_POINT",
                  "sequenceNumber": 3,
                  "scheduledArrival": "2026-03-18T06:00:00+05:30",
                  "place": {
                    "id": "place-wp-3",
                    "name": "Hyderabad relay point",
                    "type": "WAYPOINT",
                    "gps": {
                      "lat": 17.385,
                      "lng": 78.4867
                    }
                  }
                },
                {
                  "id": "wp-4",
                  "name": "Bengaluru hub",
                  "type": "HUB",
                  "sequenceNumber": 4,
                  "scheduledArrival": "2026-03-19T04:00:00+05:30",
                  "place": {
                    "id": "place-wp-4",
                    "name": "Bengaluru hub",
                    "type": "HUB",
                    "gps": {
                      "lat": 12.9716,
                      "lng": 77.5946
                    }
                  }
                }
              ]
            },
            "scheduledPickup": "2026-03-17T09:00:00+05:30",
            "estimatedDelivery": "2026-03-20T14:00:00+05:30",
            "trackingUpdates": [
              {
                "id": "tu-001",
                "shipmentId": "SHP-CN-0456",
                "status": "PICKED_UP",
                "timestamp": "2026-03-17T09:00:00+05:30",
                "vehicle": {
                  "id": "veh-MH04FP5678",
                  "registrationNumber": "MH04FP5678",
                  "type": "TRUCK_HCV",
                  "gpsEnabled": true
                }
              },
              {
                "id": "tu-002",
                "shipmentId": "SHP-CN-0456",
                "status": "AT_HUB",
                "timestamp": "2026-03-17T13:00:00+05:30",
                "location": {
                  "lat": 18.5204,
                  "lng": 73.8567,
                  "address": "Pune bypass"
                },
                "message": "Reached Pune bypass"
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

| Waypoint | ETA | Distance from previous |
|----------|-----|----------------------|
| Mumbai (Nhava Sheva) | Mar 17, 9:00 AM | — |
| Pune bypass | Mar 17, 1:00 PM | 180 km |
| Solapur hub | Mar 17, 7:00 PM | 250 km |
| Hyderabad relay point | Mar 18, 6:00 AM | 330 km |
| Bengaluru hub | Mar 19, 4:00 AM | 560 km |
| Chennai (destination) | Mar 20, 2:00 PM | 350 km |

**Total distance:** 1,670 km | **Transit time:** 77 hours

## What the packs cannot express yet

- **Advance and balance payment.** A part payment before loading belongs to settlement, which the implementation guide defers. `LogisticsFare` has no property for it.
- **Live tracking link.** `Shipment` has no tracking URL; the core `/track` and `/on_track` messages carry it.
- **Vehicle size.** `LogisticsVehicle.type` distinguishes `TRUCK_HCV` but not body length (for example 32 ft).
- **Load type.** `LTL` versus `FTL` is not an attribute of `Consignment` or `Shipment`.

## Schema references

- [Consignment](../../../schema/Consignment/)
- [Shipment](../../../schema/Shipment/)
- [LogisticsRoute](../../../schema/LogisticsRoute/)
- [Waypoint](../../../schema/Waypoint/)
- [LogisticsDriver](../../../schema/LogisticsDriver/)
- [LogisticsVehicle](../../../schema/LogisticsVehicle/)
- [LogisticsFare](../../../schema/LogisticsFare/)
- [TrackingUpdate](../../../schema/TrackingUpdate/)
