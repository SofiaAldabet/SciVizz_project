import ee
import matplotlib.pyplot as plt
import plotly.graph_objects as go


class LandcoverAnalyzer:
    """
    A class for analyzing land cover data.

    Attributes:
        dataset (GEEData): A GEEData object containing the land cover data.

    Methods:
        calculate_frequency_histogram(geometry, year=None):
            Calculates the frequency histogram of the land cover data for a given geometry and year.

        display_pie_chart_matplotlib(data, title):
            Displays a pie chart of the land cover data using the Matplotlib library.

        display_pie_chart_plotly(data, title):
            Displays a pie chart of the land cover data using the Plotly library.

        class_names:
            A read-only property that returns a dictionary of class names for the land cover data.

        class_colors:
            A read-only property that returns a dictionary of colors for the land cover data.

    Private Methods:
        _prepare_data(data):
            Prepares the data for display in a pie chart
            by calculating the percentages and colors for each class.

    Usage:
        lc_analyzer = LandcoverAnalyzer(dataset)
        data = lc_analyzer.calculate_frequency_histogram(geometry, year)
        lc_analyzer.display_pie_chart_plotly(data, title)
    """

    def __init__(self, dataset):
        self.dataset = dataset

    def calculate_frequency_histogram(self, geometry, year=None):
        """
        Calculates the frequency histogram of the land cover data for a given geometry and year.

        Args:
            geometry (dict): The geometry to calculate the frequency histogram for.
            year (str, optional): The year to calculate the frequency histogram for.
                                  Defaults to None.

        Returns:
            dict: A dictionary containing the frequency histogram data.
        """
        ee_image = self.dataset.ee_image(year=year) if year else self.dataset.ee_image()
        ee_image = ee_image.clip(geometry)

        lc_histogram = ee_image.reduceRegion(
            reducer=ee.Reducer.frequencyHistogram(),
            geometry=geometry,
            scale=250,
        )
        self.data = lc_histogram.getInfo().get("b1")
        return self.data

    def _prepare_data(self):
        """
        Prepares the data for display in a pie chart by calculating the percentages for each class.

        Args:
            data (dict): A dictionary containing the frequency histogram data.

        Returns:
            tuple: A tuple containing the labels, percentages, and colors for each class.
        """
        values = list(self.data.values())
        total = sum(values)
        labels = list(self.data.keys())
        labels = [self.class_names[key] for key in self.data.keys()]
        colors = [self.class_colors[key] for key in self.data.keys()]
        percentages = [100 * value / total for value in values]

        return labels, percentages, colors

    def get_pie_chart_plotly(self, title):
        """
        Returns a pie chart of the land cover data using the Plotly library.

        Args:
            title (str): The title of the pie chart.

        Returns:
            plotly.graph_objects.Figure: A Plotly figure object.
        """
        labels, percentages, colors = self._prepare_data()

        fig = go.Figure(
            data=[go.Pie(labels=labels, values=percentages, marker=dict(colors=colors))]
        )
        fig.update_layout(title=title, width=1200, height=600)
        return fig

    def display_pie_chart_matplotlib(self, title):
        """
        Displays a pie chart of the land cover data using the Matplotlib library.

        Args:
            title (str): The title of the pie chart.
        """
        labels, percentages, colors = self._prepare_data()

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(percentages, labels=labels, colors=colors, autopct="%1.1f%%")
        ax.set_title(title)
        plt.show()

    def display_pie_chart_plotly(self, title):
        """
        Displays a pie chart of the land cover data using the Plotly library.

        Args:
            title (str): The title of the pie chart.
        """
        fig = self.get_pie_chart_plotly(title)
        fig.show()

    @property
    def class_names(self):
        """
        A read-only property that returns a dictionary of class names for the land cover data.
        """
        return self.dataset.class_names

    @property
    def class_colors(self):
        """
        A read-only property that returns a dictionary of colors for the land cover data.
        """
        return self.dataset.class_colors


class LandcoverComparison:
    def __init__(self, data_2000, data_2018, category_colors, class_names):
        self.landcover_2000 = data_2000
        self.landcover_2018 = data_2018
        self.categories = list(data_2000.keys())
        self.category_colors = category_colors
        self.changes = {category: self.calculate_change(category) for category in self.categories}
        self.class_names = class_names  # Include class_names attribute

    def calculate_change(self, category):
        return (
            (self.landcover_2018[category] - self.landcover_2000[category])
            / self.landcover_2000[category]
            * 100
        )

    def generate_comparison_chart(self, title):
        # Filter out categories with 0% change
        non_zero_categories = [
            category for category in self.categories if self.changes[category] != 0
        ]

        # Create a bar chart using Plotly
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=[self.class_names.get(category, category) for category in non_zero_categories],
                y=[self.changes[category] for category in non_zero_categories],
                marker=dict(
                    color=[self.category_colors[category] for category in non_zero_categories]
                ),
                text=[
                    f"{change:.2f}%"
                    for change in [self.changes[category] for category in non_zero_categories]
                ],
                textposition="auto",
            )
        )

        fig.update_layout(
            xaxis=dict(
                tickmode="array",
                tickvals=list(range(len(non_zero_categories))),
                ticktext=[
                    self.class_names.get(category, category) for category in non_zero_categories
                ],
                tickangle=45,
                tickfont=dict(size=12),
            ),
            yaxis=dict(
                title="% Change",
                tickfont=dict(size=12),
            ),
            title=title,
            bargap=0.15,
            showlegend=False,
            width=1200,
            height=600,
        )

        return fig


class CarbonStockAnalyzer:
    def __init__(self, dataset):
        self.dataset = dataset
        self.data = None

    def calculate_frequency_histogram(self, geometry, year=None):
        ee_image = self.dataset.ee_image(year=year) if year else self.dataset.ee_image()
        ee_image = ee_image.clip(geometry)

        lc_histogram = ee_image.reduceRegion(
            reducer=ee.Reducer.frequencyHistogram(),
            geometry=geometry,
            scale=250,
        )
        self.data = lc_histogram.getInfo().get("b1")
        return self.data

    def categorize_counts(self):
        # Convert the category values to numbers
        values = [float(value) for value in self.data.keys()]

        # Categorize based on the sign of the values
        losses = sum(1 for value in values if value < -2.5)
        no_change = sum(1 for value in values if -2.5 <= value <= 2.5)
        gains = sum(1 for value in values if value > 2.5)

        return losses, no_change, gains

    def get_stackbar_chart_plotly(self, title="Carbon Stock Change (2000-2018))"):
        losses, no_change, gains = self.categorize_counts()
        total = losses + no_change + gains

        percentages = [losses / total * 100, no_change / total * 100, gains / total * 100]
        colors = ["#B30200", "#FFFFCC", "#066C59"]  # Red, Yellow, Green

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=["Total"],
                y=[losses],
                name="Losses",
                marker_color=colors[0],
                text=[f"{percentages[0]:.2f}%"],
                textposition="auto",
            )
        )
        fig.add_trace(
            go.Bar(
                x=["Total"],
                y=[no_change],
                name="No Change",
                marker_color=colors[1],
                text=[f"{percentages[1]:.2f}%"],
                textposition="auto",
            )
        )
        fig.add_trace(
            go.Bar(
                x=["Total"],
                y=[gains],
                name="Gains",
                marker_color=colors[2],
                text=[f"{percentages[2]:.2f}%"],
                textposition="auto",
            )
        )

        fig.update_layout(barmode="stack", title=title, width=400, height=600)

        return fig
