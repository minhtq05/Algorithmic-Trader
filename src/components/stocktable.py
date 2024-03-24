import dearpygui.dearpygui as dpg


class StocksTable():
    def __init__(self, callback_func):
        self.stocks = ['AMZN', 'GOOG', 'MSFT', 'META', 'NFLX']
        self.create_table()
        self.callback_func = callback_func

    def filter_search(self, sender, filter_str):
        dpg.set_value('stock_table', filter_str)

    def create_table(self):
        dpg.add_input_text(
            label='Search stock', callback=self.filter_search)
        with dpg.filter_set(tag='stock_table'):
            def _selection_callback(sender):
                stock = dpg.get_item_label(sender)
                self.callback_func(stock)
                for item in items:
                    if item != sender:
                        dpg.set_value(item, False)

            items = tuple(
                dpg.add_selectable(label=stock, filter_key=stock, callback=_selection_callback) for stock in self.stocks
            )
