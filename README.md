# PositionMonitor

Note: This is a practice problem

Position Monitor sits inbetween the Firm and the Exchange

The Firm can make the following (outbound) actions for order:
* NEW - sends a request to exchange for a new order
* CANCEL - sends a request to the exchange to cancel and order

The Exchange can make the following (inbound) actions for orders:
* ORDER_ACK - exchange awknowledges an order
* ORDER_REJECT - exchange rejects an order
* CANCEL_ACK - exchange awknowledges a cancel of an order
* CANCEL_REJECT- exchange rejects a cancel of an order
* FILL - exchange notified that an order has been filled. It's possible to have partial fills.

An Order is defined as an object that has the following properties:
* id - the id of the order
* symbol - the security we are buying
* type - the type of action response see (outbound and inbound actions for firm and exchange)
* side - BUY or SELL
* quantity - the amount we want to buy or sell
* filled - how much of an order was filled
* cancelled - how much of an order was not filled if there were to be a cancel

The caveats to this problem are in the way BUYS and SELLS are accounted for given that the **Exchange is the source of truth**:
* When buying: we make the assumption that the money that was sent to buy some security is gone until we hear back from the Exchange
* When selling: we make the assumption that the money that we are expecting is not in our wallet until we hear back from the Exchange

