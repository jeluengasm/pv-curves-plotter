import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import itertools
from dataclasses import dataclass


@dataclass
class PVPlotly():
    figure: go = None

    def __post_init__(self):
        self.setup()

    def setup(self):
        # Create figure
        self.figure = make_subplots(
            specs=[[{"secondary_y": True}]],
        )

        # Add figure title
        self.figure.update_layout(
            title_text="<b>Trazado de curvas I-V</b>",
            title_x=0.5
        )

        # Set x-axis title
        self.figure.update_xaxes(title_text="Tensión eléctrica (V)")

        # Set y-axes titles
        self.figure.update_yaxes(
            title_text="<b>Corriente eléctrica</b> (A)",
            secondary_y=False
        )

        self.figure.update_yaxes(
            title_text="<b>Potencia eléctrica</b> (W)",
            secondary_y=True
        )

    def add_layout(self, data: list):
        col_pal = px.colors.sequential.Rainbow
        col_pal_iterator = itertools.cycle(col_pal)

        for measures in data:
            next(col_pal_iterator)
            new_colour = next(col_pal_iterator)

            # Add traces
            self.figure.add_trace(
                go.Scatter(
                    x=measures['voltage_data'],
                    y=measures['current_data'],
                    name=f"[I] - {measures['temperature']} ºC",
                    # mode='lines',
                    line=dict(
                        color=new_colour,
                        dash='solid'
                    )
                ),
                secondary_y=False,
            )

            self.figure.add_trace(
                go.Scatter(
                    x=measures['voltage_data'],
                    y=measures['power_data'],
                    name=f"[P] - {measures['temperature']} ºC",
                    # mode='lines',
                    line=dict(
                        color=new_colour,
                        dash="dash"
                    )
                ),
                secondary_y=True,
            )

    def render_layout(self):
        return self.figure.to_html(full_html=False)
