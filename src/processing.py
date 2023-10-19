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
            Prepares the data for display in a pie chart by calculating the percentages and colors for each class.

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
            year (str, optional): The year to calculate the frequency histogram for. Defaults to None.

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
        self.data = lc_histogram.getInfo().get('b1')
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

        return  labels, percentages, colors      
    
    def display_pie_chart_matplotlib(self, title):
        """
        Displays a pie chart of the land cover data using the Matplotlib library.

        Args:
            title (str): The title of the pie chart.
        """
        labels, percentages, colors  = self._prepare_data()

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(percentages, labels=labels, colors=colors, autopct='%1.1f%%')
        ax.set_title(title)
        plt.show()

    def display_pie_chart_plotly(self, title):
        """
        Displays a pie chart of the land cover data using the Plotly library.

        Args:
            title (str): The title of the pie chart.
        """
        labels, percentages, colors  = self._prepare_data()

        fig = go.Figure(data=[go.Pie(labels=labels, values=percentages, marker=dict(colors=colors))])
        fig.update_layout(title=title, width=1200, height=600)
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