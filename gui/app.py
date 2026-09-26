from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Button,
    Checkbox,
    DataTable,
    Footer,
    Header,
    Label,
)

from src.binance_client import BinanceWebSocketClient
import config


class BinanceApp(App[None]):

    def __init__(self):
        super().__init__()
        self.binance_client = BinanceWebSocketClient(config.BINANCE_URI)
        self.symbols = []

    CSS_PATH = "app.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit")
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        # WebSocket status
        with Horizontal(id="status_indicator"):
            yield Label("WebSocket Status:", id="status_label")
            yield Label("DISCONNECTED", id="status_state")

        # Connection controls
        with Horizontal(id="buttons"):
            yield Button("Connect", id="connect", variant="success")
            yield Button("Disconnect", id="disconnect", variant="error")

        # Subscriptions
        with Vertical(id="subscriptions_container"):
            yield Label("SUBSCRIPTIONS", classes="section_title")

            with Horizontal(id="subscriptions"):
                for symbol in config.SYMBOLS:
                    yield Checkbox(
                        symbol,
                        value=True,
                        id=f"checkbox_{symbol.lower()}"
                    )

        # Live market data
        with Vertical(id="table_container"):
            yield Label("LIVE MARKET DATA", classes="section_title")
            yield DataTable(id="market_table")

        # Activity
        with Vertical(id="activity_container"):
            yield Label("ACTIVITY", classes="section_title")
            yield Label("", id="activity_1")
            yield Label("", id="activity_2")
            yield Label("", id="activity_3")

        yield Footer()

    def update_activity(self, message: str) -> None:
        activity_1 = self.query_one("#activity_1", Label)
        activity_2 = self.query_one("#activity_2", Label)
        activity_3 = self.query_one("#activity_3", Label)

        activity_3.update(str(activity_2.render()))
        activity_2.update(str(activity_1.render()))
        activity_1.update(message)

    async def on_button_pressed(self, event: Button.Pressed):
        status = self.query_one("#status_state", Label)

        if event.button.id == "connect":
            status.update("CONNECTING...")
            self.update_activity("Connecting to Binance Websocket...")

            await self.binance_client.websocket_connect()

            status.update("CONNECTED")
            self.update_activity("Connected to Binance Websocket")

            self.symbols = []
            for checkbox in self.query(Checkbox):
                if checkbox.value:
                    self.symbols.append(str(checkbox.label))

            self.update_market_table()

            # Starts the background loop (no await, no create_task)
            self.receive_market_data()

        elif event.button.id == "disconnect":
            await self.binance_client.websocket_disconnect()

            status.update("DISCONNECTED")
            self.update_activity("Disconnected from Binance WebSocket")

    @work(exclusive=True)
    async def receive_market_data(self):
        table = self.query_one("#market_table", DataTable)

        await self.binance_client.websocket_subscribe(self.symbols)

        async for trade in self.binance_client.websocket_receive():
            symbol = trade["SYMBOL"]

            # A few updates can still arrive right after unsubscribing
            if symbol not in self.symbols:
                continue

            table.update_cell(symbol, "bid", trade["BID"])
            table.update_cell(symbol, "ask", trade["ASK"])
            table.update_cell(symbol, "last", trade["LAST"])
            table.update_cell(symbol, "volume", trade["VOLUME"])

    async def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        symbol = str(event.checkbox.label)
        table = self.query_one("#market_table", DataTable)

        if event.value:
            # Checked: add the row and subscribe
            if symbol not in self.symbols:
                self.symbols.append(symbol)
                table.add_row(symbol, "", "", "", "", key=symbol)
                await self.binance_client.websocket_subscribe([symbol])
                self.update_activity(f"Subscribed to {symbol}")
        else:
            # Unchecked: unsubscribe and remove the row
            if symbol in self.symbols:
                self.symbols.remove(symbol)
                await self.binance_client.websocket_unsubscribe([symbol])
                table.remove_row(symbol)
                self.update_activity(f"Unsubscribed from {symbol}")

    def update_market_table(self) -> None:
        table = self.query_one("#market_table", DataTable)
        table.clear()  # avoids duplicate rows when you reconnect

        for symbol in self.symbols:
            table.add_row(symbol, "", "", "", "", key=symbol)

    def on_mount(self) -> None:
        self.title = "Binance Market Watcher"

        table = self.query_one("#market_table", DataTable)
        table.add_column("Symbol", key="symbol", width=10)
        table.add_column("Bid", key="bid", width=14)
        table.add_column("Ask", key="ask", width=14)
        table.add_column("Last", key="last", width=14)
        table.add_column("Volume", key="volume", width=18)
