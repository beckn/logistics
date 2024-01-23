# 1. Implementation Guide

This document contains the REQUIRED and RECOMMENDED standard functionality that must be implemented by any logistics service provider Platform a.k.a BPPs and logistics Consumer Platform a.k.a BAPs.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119 [RFC2119].

## 1.1 Discovery of logistics service providers

### 1.1.1 Recommendations for BPPs
The following recommendations need to be considered when implementing discovery functionality for a logistics BPP

- REQUIRED. The BPP MUST implement the `search` endpoint to receive an `Intent` object sent by BAPs
- REQUIRED. The BPP MUST return a catalog of logistics services on the `on_search` callback endpoint specified in the `context.bap_uri` field of the `search` request body.
- REQUIRED. The BPP MUST map its logistics services to the `Item` schema.
- REQUIRED. Any logistics service provider related information like name, logo, short description must be mapped to the `Provider.descriptor` schema
- REQUIRED. Any form that must be filled before receiving a quotation must be mapped to the `XInput` schema
- REQUIRED. If the platform wants to group its services under a specific category, it must map each category to the `Category` schema
- REQUIRED. Any order fulfillment-related information MUST be mapped to the `Fulfillment` schema.
- REQUIRED. If the BPP does not want to respond to a search request, it MUST return a `ack.status` value equal to `NACK`
- RECOMMENDED. Upon receiving a `search` request, the BPP SHOULD return a catalog that best matches the intent. This can be done by indexing the catalog against the various probable paths in the `Intent` schema relevant to typical logistics use cases

### 1.1.2 Recommendations for BAPs
- REQUIRED. The BAP MUST call the `search` endpoint of the BG to discover multiple BPPs on a network
- REQUIRED. The BAP MUST implement the `on_search` endpoint to consume the `Catalog` objects containing logistics services sent by BPPs.
- REQUIRED. The BAP MUST expect multiple catalogs sent by the respective logistics service providers on the network
- REQUIRED. The logistics services can be found in the `Catalog.providers[].items[]` array in the `on_search` request
- REQUIRED. If the `catalog.providers[].items[].xinput` object is present, then the BAP MUST redirect the user to, or natively render the form present on the link specified on the `items[].xinput.form.url` field.
- REQUIRED. If the `catalog.providers[].items[].xinput.required` field is set to `"true"` , then the BAP MUST NOT fire a `select`, `init` or `confirm` call until the form is submitted and a successful response is received
- RECOMMENDED. If the `catalog.providers[].items[].xinput.required` field is set to `"false"` , then the BAP SHOULD allow the user to skip filling the form


### Example
A search request for a logistics service provider may look like this
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "search",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "7a47a08d-69e0-4a14-9216-a95bfde08965",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "intent": {
            "category": {
                "descriptor": {
                    "name": "Fast delivery"
                }
            },
            "fulfillment": {
                "stops": [
                    {
                        "type": "Pickup",
                        "location": {
                            "gps": "14.785638,76.454553",
                            "address": {
                                "area_code": "320042"
                            }
                        }
                    },
                    {
                        "type": "Drop",
                        "location": {
                            "gps": "14.433424,77.928379",
                            "address": {
                                "area_code": "540045"
                            }
                        }
                    }
                ]
            }
        }
    }
}
```

An example catalog of a logistics service provider may look like this
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "on_search",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": { 
        "catalog": {
            "descriptor": { 
                "name":"XYZLogistics"
            },
            "providers": [ 
                { 
                    "id":"P1",
                    "descriptor": { 
                        "name":"Logistics",
                        "short_desc":"Logistics Org",
                        "long_desc":"Logistics Org"
                    },
                    "locations":[
                        {
                            "id": "L1",
                            "gps": "13.786587,76.872309",
                            "address": "Shubhash nagar, 3rd block",
                            "city": "Bengaluru",
                            "area_code": "560042",
                            "state": "KA"
                        }
                    ],
                    "categories": [
                        {
                            "id": "category1",
                            "descriptor": {
                                "name": "Fast delivery"
                            }
                        }
                    ],
                    "fulfillments": [
                        { 
                            "id":"1",
                            "type":"Road-Shipping"
                        },
                        {
                            "id":"2",
                            "type":"Rail-Shipping"
                        },
                        {
                            "id":"3",
                            "type":"Air-Shipping"
                        }
                    ],
                    "items": [
                        {
                            "id": "I1",
                            "descriptor": {
                                "Name": "Lightweight delivery",
                                "short_desc": "Delivery in just 1 hours",
                                "long_desc": "Delivery in just 1 hours"
                            },
                            "price": {
                                "currency": "INR",
                                "value": "starting from 50.0"
                            },
                            "category_ids": [
                                "category1"
                            ],
                            "fulfillment_ids": [
                                "1"
                            ],
                            "tags": [
                                {
                                    "descriptor": {
                                        "name": "charges"
                                    },
                                    "List": [
                                        {
                                            "descriptor": {
                                                "code": "Min-Chargable-Weight-in-KG"
                                            },
                                            "value": "10"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
}
```

## 1.2 Initiating an order for a logistics service
This section provides recommendations for implementing the APIs related to a logistics service.

### 1.2.1 Recommendations for BPPs

#### 1.2.1.1 Selecting a logistics service from the catalog
- REQUIRED. The BPP MUST implement the `select` endpoint on the url specified in the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry
- REQUIRED. The BPP MUST check for a form submission at the URL specified on the `xinput.form.url` before acknowledging a `select` request.
- REQUIRED. If the logistics service provider has successfully received the information submitted by the consumer, the BPP must return an acknowledgement with `ack.status` set to `ACK` in response to the `select` request
- REQUIRED. If the logistics service provider has returned a successful acknowledgement to a `select` request, it MUST send the offer encapsulated in an `Order` object

#### 1.2.1.2 Initializing a logistics service order
- REQUIRED. The BPP MUST implement the `init` endpoint on the url specified in  the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.2.1.3 Confirming the logistics service order
- REQUIRED. The BPP MUST implement the `confirm` endpoint on the url specified in URL specified in the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

### 1.2.2 Recommendations for BAPs

#### 1.2.1.1 Selecting a logistics service from the catalog
- REQUIRED. The BAP user MUST submit the form on the url received from  `on_search`  under `xinput.form.url`.
- REQUIRED. The BAP MUST implement the `on_select` endpoint on the url specified in the `context.bap_uri` field sent during `select`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.2.2.2  Initializing a logistics service order
- REQUIRED. The BAP MUST hit the `init` endpoint on the url specified in  the `context.bpp_uri` field sent during `on_search`. 
- REQUIRED. The BAP MUST implement the `on_init` endpoint on the url specified in  the `context.bap_uri` field sent during `init`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.2.2.3 Confirming the logistics service order
- REQUIRED. The BAP MUST hit the `confirm` endpoint on the url specified in  the `context.bpp_uri` field sent during `on_search`. 
- REQUIRED. The BAP MUST implement the `on_confirm` endpoint on the url specified in URL specified in the `context.bap_uri` field sent during `confirm`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

### 1.2.3 Example Workflow

### 1.2.3 Example Requests

Below is an example of a `select` request
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "select",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "order": {
            "provider": {
                "id": "P1"
            },
            "items":[
                {
                    "id": "I1",
                    "quantity": {
                        "selected": {
                            "count": "5",
                            "measure": {
                                "unit": "KG"
                            }
                        }
                    }
                }
            ],
            "fulfillments": [
                {
                    "id": "1",
                    "stops": [
                        {
                            "type": "Pickup",
                            "location": {
                                "gps": "14.785638,76.454553",
                                "address": {
                                    "area_code": "320042"
                                }
                            }
                        },
                        {
                            "type": "Drop",
                            "location": {
                                "gps": "14.433424,77.928379",
                                "address": {
                                    "area_code": "320042"
                                }
                            }
                        }
                    ]
                }
            ]
        }
    }
}
```

Below is an example of an `on_select` callback
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "on_select",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": { 
        "order": {
            "provider": { 
                "id":"P1",
                "descriptor": { 
                    "name":"Logistics",
                    "short_desc":"Logistics Org",
                    "long_desc":"Logistics Org"
                },
                "locations":[
                    {
                        "id": "L1",
                        "gps": "13.786587,76.872309",
                        "address": {
                            "street": "Shubhash nagar, 3rd block",
                            "city": "Bengaluru",
                            "area_code": "560042",
                            "state": "KA"
                        }
                    }
                ]
            },
            "items": [
                {
                    "id": "I1",
                    "descriptor": {
                        "Name": "Lightweight delivery",
                        "short_desc": "Delivery in just 1 hours",
                        "long_desc": "Delivery in just 1 hours"
                    },
                    "price": {
                        "currency": "INR",
                        "value": "starting from 50.0"
                    },
                    "category_ids": [
                        "category1"
                    ],
                    "tags": [
                        {
                            "descriptor": {
                                "name": "charges"
                            },
                            "List": [
                                {
                                    "descriptor": {
                                        "code": "Min-Chargable-Weight-in-KG"
                                    },
                                    "value": "10"
                                }
                            ]
                        }
                    ],
                    "quantity": {
                        "selected": {
                            "count": "5",
                            "measure": {
                                "unit": "KG"
                            }
                        }
                    }
                }
            ],
            "fulfillments": [
                { 
                    "id":"1",
                    "stops": [
                        {
                            "type": "Pickup",
                            "location": {
                                "gps": "14.785638,76.454553",
                                "address": {
                                    "area_code": "320042"
                                }
                            }
                        },
                        {
                            "type": "Drop",
                            "location": {
                                "gps": "14.433424,77.928379",
                                "address": {
                                    "area_code": "320042"
                                }
                            }
                        }
                    ]
                }
            ],
            "quote" :{
                "price": {
                    "currency": "INR",
                    "value": "50"
                },
                "breakup": [
                    {
                        "type": "item",
                        "item": {
                            "id": "I1"
                        },
                        "price": {
                            "currency": "INR",
                            "value": "50"
                        }
                    }
                ]
            }
        }
    }
}
```


Below is an example of a `init` request
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "init",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "order": {
            "provider": {
                "id": "P1"
            },
            "items":[
                {
                    "id": "I1",
                    "quantity": {
                        "selected": {
                            "count": "5",
                            "measure": {
                                "unit": "KG"
                            }
                        }
                    }
                }
            ],
            "fulfillments": [
                {
                    "id": "1",
                    "type": "Road-Shipping",
                    "stops": [
                        {
                            "type": "Pickup",
                            "location": {
                                "gps": "14.785638,76.454553",
                                "address": {
                                    "area_code": "320042"
                                }
                            },
                            "time": {
                                "timestamp": "2024-01-15T16:00:00.000Z"
                            }
                        },
                        {
                            "type": "Drop",
                            "location": {
                                "gps": "14.433424,77.928379",
                                "address": {
                                    "area_code": "320042"
                                }
                            }
                        }
                    ]
                }
            ],
            "billing": {
                "name": "Paul Sterling",
                "phone": "+919876345623",
                "email": "sample@gmail.com"
            }
        }
    }
}
```

Below is an example of an `on_init` callback
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "on_init",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": { 
        "order": {
            "provider": { 
                "id":"P1",
                "descriptor": { 
                    "name":"Logistics",
                    "short_desc":"Logistics Org",
                    "long_desc":"Logistics Org"
                },
                "locations":[
                    {
                        "id": "L1",
                        "gps": "13.786587,76.872309",
                        "address": {
                            "street": "Shubhash nagar, 3rd block",
                            "city": "Bengaluru",
                            "area_code": "560042",
                            "state": "KA"
                        }
                    }
                ]
            },
            "items": [
                {
                    "id": "I1",
                    "descriptor": {
                        "Name": "Lightweight delivery",
                        "short_desc": "Delivery in just 1 hours",
                        "long_desc": "Delivery in just 1 hours"
                    },
                    "price": {
                        "currency": "INR",
                        "value": "starting from 50.0"
                    },
                    "category_ids": [
                        "category1"
                    ],
                    "tags": [
                        {
                            "descriptor": {
                                "name": "charges"
                            },
                            "List": [
                                {
                                    "descriptor": {
                                        "code": "Min-Chargable-Weight-in-KG"
                                    },
                                    "value": "10"
                                }
                            ]
                        }
                    ],
                    "quantity": {
                        "selected": {
                            "count": "5",
                            "measure": {
                                "unit": "KG"
                            }
                        }
                    }
                }
            ],
            "quote" :{
                "price": {
                    "currency": "INR",
                    "value": "50"
                },
                "breakup": [
                    {
                        "type": "item",
                        "item": {
                            "id": "I1"
                        },
                        "price": {
                            "currency": "INR",
                            "value": "50"
                        }
                    }
                ]
            },
            "fulfillments": [
                {
                    "id": "1",
                    "type": "Road-Shipping",
                    "stops": [
                        {
                            "type": "Pickup",
                            "location": {
                                "gps": "14.785638,76.454553",
                                "address": {
                                    "area_code": "320042"
                                }
                            },
                            "time": {
                                "timestamp": "2024-01-15T16:00:00.000Z"
                            }
                        },
                        {
                            "type": "Drop",
                            "location": {
                                "gps": "14.433424,77.928379",
                                "address": {
                                    "area_code": "320042"
                                }
                            }
                        }
                    ]
                }
            ],
            "billing": {
                "name": "Paul Sterling",
                "phone": "+919876345623",
                "email": "sample@gmail.com"
            },
            "payment": {
                "status": "NOT-PAID",
                "type": "PRE-FULFILLMENT",
                "params": {
                  "amount": "1500",
                  "currency": "INR",
                  "bank_code": "INB0004321",
                  "bank_account_number": "1234002341"
                }
            }
        }
    }
}
```

Below is an example of a `confirm` request
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "confirm",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "order": {
            "provider": {
                "id": "P1"
            },
            "items": [
                {
                    "id": "I1",
                    "quantity": {
                        "selected": {
                            "count": "5",
                            "measure": {
                                "unit": "KG"
                            }
                        }
                    }
                }
            ],
            "fulfillments": [
                {
                    "id": "1",
                    "type": "Road-Shipping",
                    "stops": [
                        {
                            "type": "Pickup",
                            "location": {
                                "gps": "14.785638,76.454553",
                                "address": {
                                    "area_code": "320042"
                                }
                            },
                            "time": {
                                "timestamp": "2024-01-15T16:00:00.000Z"
                            }
                        },
                        {
                            "type": "Drop",
                            "location": {
                                "gps": "14.433424,77.928379",
                                "address": {
                                    "area_code": "320042"
                                }
                            }
                        }
                    ]
                }
            ],
            "billing": {
                "name": "Paul Sterling",
                "phone": "+919876345623",
                "email": "sample@gmail.com"
            },
            "payment": {
                "status": "PAID",
                "type": "PRE-FULFILLMENT",
                "params": {
                    "transaction_id": "tid/6737457",
                    "amount": "1500",
                    "currency": "INR",
                    "bank_code": "INB0004321",
                    "bank_account_number": "1234002341"
                }
            }
        }
    }
}
```
Below is an example of an `on_confirm` callback
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "on_confirm",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "order": {
            "id": "oid/12",
            "provider": {
                "id": "P1",
                "descriptor": {
                    "name": "Logistics",
                    "short_desc": "Logistics Org",
                    "long_desc": "Logistics Org"
                },
                "locations": [
                    {
                        "id": "L1",
                        "gps": "13.786587,76.872309",
                        "address": {
                            "street": "Shubhash nagar, 3rd block",
                            "city": "Bengaluru",
                            "area_code": "560042",
                            "state": "KA"
                        }
                    }
                ]
            },
            "items": [
                {
                    "id": "I1",
                    "descriptor": {
                        "Name": "Lightweight delivery",
                        "short_desc": "Delivery in just 1 hours",
                        "long_desc": "Delivery in just 1 hours"
                    },
                    "price": {
                        "currency": "INR",
                        "value": "50.0"
                    },
                    "category_ids": [
                        "category1"
                    ],
                    "tags": [
                        {
                            "descriptor": {
                                "name": "charges"
                            },
                            "List": [
                                {
                                    "descriptor": {
                                        "code": "Min-Chargable-Weight-in-KG"
                                    },
                                    "value": "10"
                                }
                            ]
                        }
                    ],
                    "quantity": {
                        "selected": {
                            "count": "5",
                            "measure": {
                                "unit": "KG"
                            }
                        }
                    }
                }
            ],
            "quote": {
                "price": {
                    "currency": "INR",
                    "value": "50"
                },
                "breakup": [
                    {
                        "type": "item",
                        "item": {
                            "id": "I1"
                        },
                        "price": {
                            "currency": "INR",
                            "value": "starting from 50.0"
                        }
                    }
                ]
            },
            "fulfillments": [
                {
                    "id": "1",
                    "type": "Road-Shipping",
                    "stops": [
                        {
                            "type": "Pickup",
                            "location": {
                                "gps": "14.785638,76.454553",
                                "address": {
                                    "area_code": "320042"
                                }
                            },
                            "time": {
                                "timestamp": "2024-01-15T16:00:00.000Z"
                            }
                        },
                        {
                            "type": "Drop",
                            "location": {
                                "gps": "14.433424,77.928379",
                                "address": {
                                    "area_code": "320042"
                                }
                            }
                        }
                    ],
                    "state": {
                        "descriptor": {
                            "code": "Pending-Fulfillment"
                        }
                    }
                }
            ],
            "billing": {
                "name": "Paul Sterling",
                "phone": "+919876345623",
                "email": "sample@gmail.com"
            },
            "payment": {
                "status": "PAID",
                "type": "PRE-FULFILLMENT",
                "params": {
                    "transaction_id": "tid/6737457",
                    "amount": "1500",
                    "currency": "INR",
                    "bank_code": "INB0004321",
                    "bank_account_number": "1234002341"
                }
            }
        }
    }
}
```

## 1.3 Fulfillment of a logistics order
This section contains recommendations for implementing the APIs related to fulfilling a logistics order

### 1.3.1 Recommendations for BPPs

#### 1.3.1.1 Sending status updates
- REQUIRED. The BPP MUST implement the `status` endpoint on the url specified in URL specified in the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.3.1.2 Updating a logistics order
- REQUIRED. The BPP MUST implement the `update` endpoint on the url specified in URL specified in the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.3.1.3 Cancelling a logistics order
- REQUIRED. The BPP MUST implement the `cancel` endpoint on the url specified in URL specified in the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry
- REQUIRED. The BPP MUST implement the `get_cancellation_reasons` endpoint on the url specified in URL specified in the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.3.1.4 Real-time tracking
- REQUIRED. The BPP MUST implement the `track` endpoint on the url specified in URL specified in the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

### 1.3.2 Recommendations for BAPs

#### 1.3.2.1 Receiving status updates
- REQUIRED. The BAP MUST implement the `on_status` endpoint on the url specified in URL specified in the `context.bap_uri` field sent during `status`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.3.2.2 Updating a logistics order
- REQUIRED. The BAP MUST implement the `on_update` endpoint on the url specified in URL specified in the `context.bap_uri` field sent during `update`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.3.2.3 Cancelling a logistics order
- REQUIRED. The BAP MUST implement the `on_cancel` endpoint on the url specified in URL specified in the `context.bap_uri` field sent during `cancel`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry
- REQUIRED. The BAP MUST implement the `cancellation_reasons` endpoint on the url specified in URL specified in the `context.bap_uri` field sent during `get_cancellation_reasons`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.3.2.4 Real-time tracking
- REQUIRED. The BAP MUST implement the `on_track` endpoint on the url specified in URL specified in the `context.bap_uri` field sent during `track`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

### 1.3.3 Example Workflow

### 1.3.4 Example Requests

Below is an example of a `status` request
```

{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "status",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "order_id": "oid/12"
    }
}
```

Below is an example of an `on_status` callback
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "on_status",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "order": {
            "id": "oid/12",
            "provider": {
                "id": "P1",
                "descriptor": {
                    "name": "Logistics",
                    "short_desc": "Logistics Org",
                    "long_desc": "Logistics Org"
                },
                "locations": [
                    {
                        "id": "L1",
                        "gps": "13.786587,76.872309",
                        "address": {
                            "street": "Shubhash nagar, 3rd block",
                            "city": "Bengaluru",
                            "area_code": "560042",
                            "state": "KA"
                        }
                    }
                ]
            },
            "items": [
                {
                    "id": "I1",
                    "descriptor": {
                        "Name": "Lightweight delivery",
                        "short_desc": "Delivery in just 1 hours",
                        "long_desc": "Delivery in just 1 hours"
                    },
                    "price": {
                        "currency": "INR",
                        "value": "starting from 50.0"
                    },
                    "category_ids": [
                        "category1"
                    ],
                    "tags": [
                        {
                            "descriptor": {
                                "name": "charges"
                            },
                            "List": [
                                {
                                    "descriptor": {
                                        "code": "Min-Chargable-Weight-in-KG"
                                    },
                                    "value": "10"
                                }
                            ]
                        }
                    ],
                    "quantity": {
                        "selected": {
                            "count": "5",
                            "measure": {
                                "unit": "KG"
                            }
                        }
                    }
                }
            ],
            "quote": {
                "price": {
                    "currency": "INR",
                    "value": "50"
                },
                "breakup": [
                    {
                        "type": "item",
                        "item": {
                            "id": "I1"
                        },
                        "price": {
                            "currency": "INR",
                            "value": "50"
                        }
                    }
                ]
            },
            "fulfillments": [
                {
                    "id": "1",
                    "type": "Road-Shipping",
                    "stops": [
                        {
                            "type": "Pickup",
                            "location": {
                                "gps": "14.785638,76.454553",
                                "address": {
                                    "area_code": "320042"
                                }
                            },
                            "time": {
                                "timestamp": "2024-01-15T16:00:00.000Z"
                            }
                        },
                        {
                            "type": "Drop",
                            "location": {
                                "gps": "14.433424,77.928379",
                                "address": {
                                    "area_code": "320042"
                                }
                            }
                        }
                    ],
                    "state": {
                        "descriptor": {
                            "code": "Shipped"
                        }
                    }
                }
            ],
            "billing": {
                "name": "Paul Sterling",
                "phone": "+919876345623",
                "email": "sample@gmail.com"
            },
            "payment": {
                "status": "PAID",
                "type": "PRE-FULFILLMENT",
                "params": {
                    "transaction_id": "tid/6737457",
                    "amount": "1500",
                    "currency": "INR",
                    "bank_code": "INB0004321",
                    "bank_account_number": "1234002341"
                }
            }
        }
    }
}
```

## 1.4 Post-fulfillment of logistics order
This section contains recommendations for implementing the APIs after fulfilling a logistics order

### 1.4.1 Recommendations for BPPs

#### 1.4.1.1 Rating and Feedback
- REQUIRED. The BPP MUST implement the `rating` endpoint on the url specified in URL specified in the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry
- REQUIRED. The BPP MUST implement the `get_rating_categories` endpoint on the url specified in URL specified in the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.4.1.2 Providing Support
- REQUIRED. The BPP MUST implement the `support` endpoint on the url specified in URL specified in the `context.bpp_uri` field sent during `on_search`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

### 1.4.2 Recommendations for BAPs

#### 1.4.2.1 Rating and Feedback
- REQUIRED. The BAP MUST implement the `on_rating` endpoint on the url specified in URL specified in the `context.bap_uri` field sent during `rating`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry
- REQUIRED. The BAP MUST implement the `rating_categories` endpoint on the url specified in URL specified in the `context.bap_uri` field sent during `get_rating_categories`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

#### 1.4.2.2 Providing Support
- REQUIRED. The BAP MUST implement the `on_support` endpoint on the url specified in URL specified in the `context.bap_uri` field sent during `support`. In case of permissioned networks, this URL MUST match the `Subscriber.url` present on the respective entry in the Network Registry

### 1.4.3 Example Workflow

### 1.4.4 Example Requests

Below is an example of a `get_rating_categories` request
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "get_rating_categories",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    }
}
```

Below is an example of an `rating_categories` callback
```
{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "rating_categories",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "rating_categories" : [
            "Item",
            "Order",
            "Fulfillment",
            "provider",
            "Agent",
            "SUpport"
        ]
    }
}
```

Below is an example of a `rating` request

```

{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "rating",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "ratings": [
            {
                "rating_category": "Order",
                "id": "oid/12",
                "value": "4"
            }
        ]
    }
}
```
Below is an example of an `on_rating` callback
```

{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "on_rating",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "feedback_form": {
            "form": {
                "url": "https://form/url"
            }
        }
    }
}
```

Below is an example of a `support` request
```

{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "support",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "support": {
            "type": "Order",
            "ref_id": "oid/12",
            "callback_phone": "+919876564534"
        }
    }
}
```

Below is an example of an `on_support` callback
```

{
    "context": {
        "domain": "logistics",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:0806"
            }
        },
        "action": "on_support",
        "version": "1.1.0",
        "bap_id": "logistics_bap",
        "bap_uri": "https://logistics_bap.com",
        "bpp_id": "logistics_bpp",
        "bpp_uri": "https://logistics_bpp.com",
        "transaction_id": "aa77b78e-66b0-47a5-9560-527a36cf0d9f",
        "message_id": "9d498536-4dba-4c69-a47e-bed245623ecc",
        "timestamp": "2024-01-15T16:00:00.000Z",
        "ttl": "PT30S"
    },
    "message": {
        "support": {
            "phone": "+918675453298",
            "email": "helpline@logistics.com"
        }
    }
}
```
