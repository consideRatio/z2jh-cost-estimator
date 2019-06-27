from abc import ABC, abstractmethod


class InputForm(ABC):
    @abstractmethod
    def get_input_form(self):
        """Presents something that can receive input from the user."""
        pass

    @abstractmethod
    def get_data(self):
        """Return processed results from the input form."""
        pass


import numpy as np
import bqplot
import bqplot.interacts


class InteractiveInputForm(InputForm):
    """
    Presents an interactive input form allowing the user to draw a line graph representing hourly usage of some kind.
    """

    fig = None

    def get_input_form(self, figure_title):
        if self.fig:
            return self.fig
        self.figure_title = figure_title
        max_hours = 24 + 1
        max_users = 10

        # Define scales
        x_scale = bqplot.LinearScale(min=0, max=max_hours)
        y_scale = bqplot.LinearScale(min=0, max=max_users)

        # Initialize data for our line
        line = bqplot.Lines(
            x=np.arange(0, max_hours),
            y=np.zeros(max_hours),
            scales={"x": x_scale, "y": y_scale},
            fill="bottom",
            fill_opacities=[0.5],
        )

        # Layout only - axes (plural of axis)
        x_axis = bqplot.Axis(scale=x_scale, label="Hour", grid_lines="none")
        y_axis = bqplot.Axis(
            scale=y_scale,
            label="Numer of Users",
            grid_lines="none",
            orientation="vertical",
        )

        def _fix_input_callback(change):
            # ensures we draw integer values 0 or greater and that
            # 00:00 [0] and 24:00 [24] represent the same value.
            with line.hold_sync():

                if change["old"][-1] != change["new"][-1]:
                    line.y[0] = line.y[-1]
                elif change["old"][0] != change["new"][0]:
                    line.y[-1] = line.y[0]

                line.y = np.fmax(0, np.rint(line.y))

        line.observe(_fix_input_callback, names=["y"])

        handdraw_interaction = bqplot.interacts.HandDraw(lines=line)
        self.fig = bqplot.Figure(
            marks=[line],
            axes=[x_axis, y_axis],
            interaction=handdraw_interaction,
            animation_duration=150,
            title=self.figure_title,
        )

        return self.fig

    def get_data(self):
        assert (
            self.fig != None
        ), "Make sure to first present the input form to the user."

        return self.fig.marks[0].y.astype(int)
