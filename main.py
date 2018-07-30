# Implement the class below, keeping the constructor's signature unchanged; it should take no arguments.
import json
from itertools import zip_longest

class MarkingPositionMonitor:
    def __init__(self):
        self.func_map = {
            "NEW": self.handle_new,
            "ORDER_ACK": self.handle_order_ack,
            "ORDER_REJECT": self.handle_order_reject,
            "CANCEL": self.handle_cancel,
            "CANCEL_ACK": self.handle_cancel_ack,
            "CANCEL_REJECT": self.handle_cancel,
            "FILL": self.handle_fill
        }

        self.order_list = {}  # will contain a order number to order mapping
        self.position_list = {}  # will contain a symbol to position mapping

    def on_event(self, message):
        # check if the type exists, otherwise error
        message_json = json.loads(message)
        return self.func_map[message_json["type"]](message_json)

    def handle_new(self, message):

        id = message["order_id"]
        symbol = message["symbol"]
        side = message["side"]
        quantity = message["quantity"]

        position = 0
        # check if it exists within the table - get it
        if symbol in self.position_list.keys():
            position = self.position_list[symbol]

        # update position value on sell only
        if side == "SELL":
            position = position - quantity

        # set position in map
        self.position_list[symbol] = position

        # save order
        self.order_list[id] = Order(message)

        return position

    def handle_order_ack(self, message):
        order_id = message["order_id"]
        return self.get_position_by_order_id(order_id)

    def handle_order_reject(self, message):
        # get order
        order = self.order_list[message["order_id"]]
        # determine if its buy/sell
        if order.side == "SELL":
            # if sell then we update position
            self.position_list[order.symbol] += order.quantity
        # if buy we do nothing since position is still unmodified for order
        return self.position_list[order.symbol]

    def handle_cancel(self, message):
        order_id = message["order_id"]
        return self.get_position_by_order_id(order_id)

    def handle_cancel_ack(self, message):
        # only changes state for sell because you want to see your money back
        order = self.order_list[message["order_id"]]

        # get the sysmbol , get the position
        position = self.position_list[order.symbol]
        cancelled_amnt = order.quantity - order.filled
        if order.side == "SELL":
            position += cancelled_amnt
            self.position_list[order.symbol] = position

            # update order - not necessary, but good to track state
        order.cancelled = cancelled_amnt

        return position

    def handle_cancel_reject(self, message):
        # yo... this isn't used in a meaningful way
        order_id = message["order_id"]
        return self.get_position_by_order_id(order_id)

    def handle_fill(self, message):
        # update order - partial/full
        # update position from order
        # return position
        order = self.order_list[message["order_id"]]
        filled_quant = message["filled_quantity"]
        order.filled += filled_quant

        #validate , remaining amount
        remaining_order_quantity = order.quantity - order.filled
        assert(remaining_order_quantity == message["remaining_quantity"])

        position = self.position_list[order.symbol]
        if order.side == "BUY":
            position += filled_quant
            self.position_list[order.symbol] = position

        return position

    def get_position_by_order_id(self, order_id):
        assert(self.order_list[order_id] is not None)
        order = self.order_list[order_id]

        assert(self.position_list[order.symbol] is not None)
        return self.position_list[order.symbol]


class Order:
    def __init__(self, order_json):
        self.id = order_json["order_id"]
        self.symbol = order_json["symbol"]
        self.type = order_json["type"]
        self.side = order_json["side"]
        self.quantity = order_json["quantity"]
        self.filled = 0
        self.cancelled = 0

if __name__ == '__main__':

    filenames = ["input000.txt", "input001.txt"]

    positionMonitor = MarkingPositionMonitor()

    for file in filenames:
        # open the input file

        print("File: %s" % file)
        for f_line, expected_line in zip_longest(open(file, "r"), open("expected_" + file, "r")):
                # print the file name we're looking at
                input = f_line.strip("\n")
                print(input)
                output = str(positionMonitor.on_event(input))
                print(output)
                assert(output == expected_line.strip("\n"))