from datetime import date
from itertools import cycle

import bokeh
import pandas as pd
from bokeh.io import curdoc, export_png, show
from bokeh.layouts import column, grid
from bokeh.models import DateRangeSlider, Span, tools
from bokeh.models.sources import ColumnDataSource
from bokeh.palettes import Dark2_8 as palette
from bokeh.plotting import figure


def chartFRED(df: pd.DataFrame) -> bokeh.layouts.layout:
    curdoc().theme = "dark_minimal"
    DateMinMax = (df["Date"].min(), df["Date"].max())
    DataCols = df.columns.drop(["Date"]).tolist()

    Date_Range_Slider = DateRangeSlider(
        start=pd.to_datetime(df["Date"].min()),
        end=pd.to_datetime(date.today()),
        step=(1 * 24 * 60 * 60 * 1000) * 30,  # 30 days in milliseconds
        value=DateMinMax,
    )
    source = ColumnDataSource(df)

    p1 = figure(
        x_range=DateMinMax,
        x_axis_type="datetime",
        toolbar_location=None,
        active_drag=None,
        active_scroll=None,
        active_tap=None,
        output_backend="webgl",
    )

    colors = cycle(palette)
    c = next(colors)
    plot1a = p1.line("Date", DataCols[0], source=source, legend_label=DataCols[0], color=c)
    for i, c in zip(range(1, len(DataCols)), colors):
        p1.line("Date", DataCols[i], source=source, legend_label=DataCols[i], color=c)

    Date_Range_Slider.js_link("value", p1.x_range, "start", attr_selector=0)
    Date_Range_Slider.js_link("value", p1.x_range, "end", attr_selector=1)
    p1.legend.location = "top_left"
    p1.legend.orientation = "horizontal"

    TooltipGuide = [(x, f"@{x}" + "{0.0a}") for x in DataCols]
    Format = {"@Date": "datetime"}
    Format.update({f"@{x}": "numeral" for x in DataCols})

    p1.renderers.extend([Span(location=0, dimension="width", line_color="gray", line_dash="dashed", line_width=3)])

    hover = tools.HoverTool(
        renderers=[plot1a],
        tooltips=[
            ("Date", "@Date{%F}"),
            *TooltipGuide,
        ],
        formatters=Format,
        mode="vline",
    )

    p1.add_tools(hover)

    layout = grid(
        [
            column(
                [Date_Range_Slider],
                # width=600,
                # height=50,
                sizing_mode="stretch_width",
            ),
            column(
                [p1],
                # width=600,
                # height=625,
                sizing_mode="stretch_width",
            ),
        ],
        sizing_mode="stretch_both",
    )
    # export_png(layout, filename="chartFRED.png")
    return layout
