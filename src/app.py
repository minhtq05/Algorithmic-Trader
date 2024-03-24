import dearpygui.dearpygui as dpg
import yfinance as yf
import pandas as pd
import time
import numpy as np
from components.menubar import MenuBar
from components.tabbar import TabBar
from components.stocktable import StocksTable


class App():
    def __init__(self):
        self.stock_ticker = {}
        self.stock_history = {}

    def visible_stocks(self):
        tab_ids = dpg.get_item_children('tab_bar')[1]
        for id in tab_ids:
            if dpg.get_item_configuration(id)['show'] == False:
                dpg.delete_item(id)
                tab_ids.remove(id)
        tab_labels = [dpg.get_item_label(id) for id in tab_ids]
        return tab_labels, tab_ids

    def load_stock_data(self, stock):
        ticker = yf.Ticker(stock)
        hist = ticker.history(period='5mo')
        hist.reset_index(inplace=True)
        self.stock_ticker[stock] = ticker
        self.stock_history[stock] = hist

    def show_stock_content(self, stock):
        def to_unix_date(tm):
            t = tm.astimezone('GMT-0')
            t = t.floor('D')
            unix_time = int(t.timestamp())
            return unix_time

        with dpg.plot(label=f'{stock} stock graph', tag=f'{stock}_candlestick', width=-1, height=-1):
            df = self.stock_history[stock]
            dates, opens, highs, lows, closes = df['Date'].tolist(), df['Open'].tolist(
            ), df['High'].tolist(), df['Low'].tolist(), df['Close'].tolist()

            dates = [to_unix_date(d) for d in dates]

            min_date, max_date = dates[0], dates[-1]

            # print(dates)
            # print(opens)
            # print(highs)
            # print(lows)
            # print(closes)

            dpg.add_plot_legend()
            xAxis = dpg.add_plot_axis(
                dpg.mvXAxis, label='Dates', time=True)
            # dpg.set_axis_limits(xAxis, min_date, max_date)
            with dpg.plot_axis(dpg.mvYAxis, label='Price') as yAxis:
                top, bot = max(highs), min(lows)
                diff = top - bot
                # dpg.set_axis_limits(yAxis, bot - diff / 10, top + diff / 10)
                dpg.add_candle_series(
                    dates, opens, closes, highs, lows, label=stock, time_unit=dpg.mvTimeUnit_Day)
                dpg.fit_axis_data(dpg.top_container_stack())
            dpg.fit_axis_data(xAxis)

    def show_stock(self, stock):
        stocks, tab_ids = self.visible_stocks()
        if stock not in self.stock_history.keys():
            self.load_stock_data(stock)
        if stock not in stocks:
            self.tab_bar.add_new_tab(
                stock=stock, content=self.show_stock_content)

            # self.load_stock_data(stock)
        stocks, tab_ids = self.visible_stocks()
        id = stocks.index(stock)
        dpg.set_value('tab_bar', tab_ids[id])

    def run(self):
        dpg.create_context()
        with dpg.window(label='Chart', width=1200, height=900, pos=(0, 0), no_move=True, tag='charts', no_title_bar=True):
            self.menu_bar = MenuBar(
                ['About', 'Help', 'Settings', 'Language', 'Keyboard shortcuts'], 'menu_bar')
            self.tab_bar = TabBar('tab_bar')

        with dpg.window(label='Stocks', width=400, height=900, pos=(1200, 0), no_move=True, tag='table'):
            self.stocks_table = StocksTable(callback_func=self.show_stock)

        dpg.create_viewport(title='Trading App', width=1600, height=900)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()


if __name__ == '__main__':
    App().run()
