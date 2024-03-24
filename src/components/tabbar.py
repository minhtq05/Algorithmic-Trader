import dearpygui.dearpygui as dpg


class TabBar():
    def __init__(self, tag: str | int = 'tab_bar'):
        self.tag = tag
        self.create_tab_bar()

    def create_tab_bar(self):
        with dpg.tab_bar(tag=self.tag, reorderable=True) as self.tab_bar:
            pass
            # for item in self.tab_items:
            #     with dpg.tab(label=item, closable=True):
            #         dpg.add_text(f'Tab stock: {item}')

            # dpg.add_tab_button(
            # label='+', callback=self.add_new_tab, tag='new_tab_button')

    def add_new_tab(self, stock, content):
        # dpg.delete_item('new_tab_button')
        with dpg.tab(label=stock, closable=True, parent=self.tab_bar) as new_tab:
            content(stock)
            # dpg.add_plot_()
        # dpg.add_tab_button(label='+', callback=self.add_new_tab,
            #    tag='new_tab_button', parent=self.tab_bar)
