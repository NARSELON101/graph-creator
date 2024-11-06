from bokeh.io import curdoc
from bokeh.io.export import get_layout_html
from bokeh.layouts import layout
from bokeh.models import Spinner
from bokeh.models.widgets.inputs import ColorPicker
from bokeh.plotting import figure

from graphs.graph_constructor.base import BaseGraphConstructMethod


class LinearConstructMethod(BaseGraphConstructMethod):

    def construct(self, x_name, y_name, x_value, y_value, is_sorted, *args, **kwargs):
        curdoc().theme = 'dark_minimal'
        p = figure(title='Test', x_axis_label=x_name, y_axis_label=y_name)
        points = p.line(sorted(x_value) if is_sorted else x_value, sorted(y_value) if is_sorted else y_value,
                        line_width=2, color='black')
        spinner = Spinner(title='Толщина линии', low=1, high=10, step=1, value=points.glyph.line_width, width=200)
        palette = ColorPicker(title='Цвет линии')
        palette.js_link('color', points.glyph, 'line_color')
        spinner.js_link('value', points.glyph, 'line_width')
        layout_ = layout([[spinner, palette], [p]])
        diagram = get_layout_html(layout_, theme=curdoc().theme)

        return diagram


class ScatterConstructMethod(BaseGraphConstructMethod):

    def construct(self, x_name, y_name, x_value, y_value, is_sorted, *args, **kwargs):
        curdoc().theme = 'dark_minimal'
        p = figure(title='Test', x_axis_label=x_name, y_axis_label=y_name)
        points = p.scatter(sorted(x_value) if is_sorted else x_value, sorted(y_value) if is_sorted else y_value,
                           line_width=2, fill_color='white', size=20, line_color='black')
        circle_size = Spinner(title='Размер круга', low=1, high=30, step=1, value=points.glyph.size, width=190)
        border_size = Spinner(title='Размер границы круга', low=0, high=5, step=1, value=points.glyph.line_width, width=190)
        circle_palette = ColorPicker(title='Цвет круга', color='white')
        border_palette = ColorPicker(title='Цвет границы круга', color='black')
        border_palette.js_link('color', points.glyph, 'line_color')
        circle_palette.js_link('color', points.glyph, 'fill_color')
        circle_size.js_link('value', points.glyph, 'size')
        border_size.js_link('value', points.glyph, 'line_width')
        layout_ = layout([[circle_size, border_size, circle_palette, border_palette], [p]])
        diagram = get_layout_html(layout_, theme=curdoc().theme)

        return diagram
