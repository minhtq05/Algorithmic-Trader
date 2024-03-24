import dearpygui.dearpygui as dpg


class MenuBar():
    def __init__(self, menu_items, tag: str | int = 'menu_bar'):
        self.menu_items = menu_items
        self.tag = tag
        self.create_menu_bar()

    def create_menu_bar(self):
        with dpg.menu_bar(tag=self.tag) as self.menu_bar:
            for item in self.menu_items:
                dpg.add_menu_item(label=item)
