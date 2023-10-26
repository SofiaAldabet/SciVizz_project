import ee
import streamlit as st
from streamlit_folium import st_folium
from shapely import Polygon

from src.maps import FoliumMap
from src.data_params import GEEData
from src.processing import LandcoverAnalyzer
from src.verification import selected_bbox_too_large, selected_bbox_in_boundary

MAP_CENTER = [-4.656, -50.94]
MAP_ZOOM = 8
MAX_ALLOWED_AREA_SIZE = 20.0
BTN_LABEL = "Submit"

# Initialize GEE
ee.Initialize()


# Create the Streamlit app and define the main code:
def main():
    st.set_page_config(
        page_title="science_project-demo",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("Science Project Demo")

    # Create the map
    m = FoliumMap(center=MAP_CENTER, zoom=MAP_ZOOM)

    # Add layers
    soc_data = GEEData('SOC-Stock-Change')
    m.add_gee_layer(dataset=soc_data)

    glc_data = GEEData('Global-Land-Cover')
    for year in ['2000', '2018']:
        m.add_gee_layer(dataset=glc_data, year=year)

    m.add_layer_control()

    output = st_folium(m, key="init", width=1200, height=600)

    # Get the GeoJSON data of the selected area
    geojson = None
    if output["all_drawings"] is not None:
        if len(output["all_drawings"]) != 0:
            if output["last_active_drawing"] is not None:
                # get latest modified drawing
                geojson = output["last_active_drawing"]

    # ensure progress bar resides at top of sidebar and is invisible initially
    progress_bar = st.sidebar.progress(0)
    progress_bar.empty()

    # Create an empty container for the plotly figure
    text_container = st.empty()
    plot_container = st.empty()

    # Create the sidebar
    with st.sidebar.container():
        # Getting started
        st.subheader("Getting Started")
        st.markdown(
            f"""
                        1. Click the black square on the map
                        2. Draw a rectangle on the map
                        3. Click on <kbd>{BTN_LABEL}</kbd>
                        4. Wait for the computation to finish
                        """,
            unsafe_allow_html=True,
        )

        # Add the button and its callback
        if st.button(
            BTN_LABEL,
            key="compute_zs",
            disabled=False if geojson is not None else True,
        ):
            # Check if the geometry is valid
            geometry = geojson['geometry']
            if selected_bbox_too_large(geometry, threshold=MAX_ALLOWED_AREA_SIZE):
                st.sidebar.warning(
                    "Selected region is too large, fetching data for this area would consume too many resources. "
                    "Please select a smaller region."
                )
            elif not selected_bbox_in_boundary(geometry):
                st.sidebar.warning(
                    "Selected rectangle is not within the allowed region of the world map. "
                    "Do not scroll too far to the left or right. "
                    "Ensure to use the initial center view of the world for drawing your rectangle."
                )
            else:
                # Instantiate a LandcoverAnalyzer object with the GEEData object as its argument
                lc_analyzer = LandcoverAnalyzer(glc_data)

                # Calculate the frequency histogram for the year 2018
                data = lc_analyzer.calculate_frequency_histogram(geometry=geometry, year='2018')

                # Generate the plot using Plotly
                fig = lc_analyzer.get_pie_chart_plotly(title='')

                # Display the plot using Streamlit
                text_container.subheader("Land Cover (2018)")
                plot_container.plotly_chart(fig)


if __name__ == "__main__":
    main()