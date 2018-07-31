# PositionMonitor

Note: This is a practice problem

Position Monitor sits inbetween the Firm and the Exchange

The Firm can make the following (outbound) actions for order:
* NEW
* CANCEL

The Exchange can make the following (inbound) actions for orders:
* ORDER_ACK
* ORDER_REJECT
* CANCEL_ACK
* CANCEL_REJECT
* FILL

An Order is defined as an object that has the following properties:
* id
* symbol
* type
* side
* quantity]
* filled
* cancelled

The caveats to this problem are in the way BUYS and SELLS are accounted for given that the **Exchange is the source of truth**:
* When buying: we make the assumption that the money that was sent to buy some security is gone until we hear back from the Exchange
* When selling: we make the assumption that the money that we are expecting is not in our wallet until we hear back from the Exchange
