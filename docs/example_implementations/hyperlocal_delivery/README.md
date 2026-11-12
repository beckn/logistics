# Hyperlocal Delivery

Same-day delivery within a city, typically within two hours: groceries, food, pharmacy and small parcels.

The end-to-end example for this use case is the implementation guide:

**[Implementing Logistics Flows on a Value-exchange Fabric](./Logistics_Implementation_Guide.md)**

It covers the cascaded and parallel topologies, the mapping of schema packs to core slots, and a worked example with every message from discovery to confirmation. Its payloads are checked in CI (`tools/validate.py examples`).

## Schema references

- [Shipment](../../../schema/Shipment/)
- [Package](../../../schema/Package/)
- [Courier](../../../schema/Courier/)
- [DeliverySlot](../../../schema/DeliverySlot/)
- [LogisticsPlace](../../../schema/LogisticsPlace/)
- [LogisticsRoute](../../../schema/LogisticsRoute/)
- [LogisticsFare](../../../schema/LogisticsFare/)
- [LogisticsOperator](../../../schema/LogisticsOperator/)
- [LogisticsReceipt](../../../schema/LogisticsReceipt/)
- [TrackingUpdate](../../../schema/TrackingUpdate/)
- [Proof](../../../schema/Proof/)
