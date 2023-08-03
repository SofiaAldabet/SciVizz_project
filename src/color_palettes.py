# Define the color ramp for SOC stock change
soc_color_ramp = [
    "#B30200",  # -10
    "#E34A33",  # -7.5
    "#FC8D59",  # -5
    "#FDCC8A",  # -2.5
    "#FFFFCC",  # 0
    "#A1DAB4",  # 2.5
    "#31B3BD",  # 5
    "#1C9099",  # 7.5
    "#066C59",  # 10
]


# Define the color ramp for land cover
sld_ramp = """
<RasterSymbolizer>
  <ColorMap type="ramp" extended="false">
    <ColorMapEntry color="#5b5b18" quantity="10" label="Cropland rainfed" />
    <ColorMapEntry color="#7d7617" quantity="11" label="Cropland rainfed herbaceous" />
    <ColorMapEntry color="#124d00" quantity="12" label="Cropland rainfed tree or shrub" />
    <ColorMapEntry color="#a09113" quantity="20" label="Cropland irrigation or post-flood" />
    <ColorMapEntry color="#c0ab10" quantity="30" label="Mosaic cropland" />
    <ColorMapEntry color="#dfc30c" quantity="40" label="Mosaic natural vegetation" />
    <ColorMapEntry color="#136010" quantity="50" label="Tree broadleaved evergreen closed to open" />
    <ColorMapEntry color="#117221" quantity="60" label="Tree broadleaved decidious closed to open" />
    <ColorMapEntry color="#0b842f" quantity="61" label="Tree broadleaved decidious closed" />
    <ColorMapEntry color="#2a9339" quantity="62" label="Tree broadleaved decidious open" />
    <ColorMapEntry color="#4aa040" quantity="70" label="Tree needle evergreen closed to open" />
    <ColorMapEntry color="#91c357" quantity="80" label="Tree needle decidious closed to open" />
    <ColorMapEntry color="#a5ce5f" quantity="81" label="Tree needle decidious closed" />
    <ColorMapEntry color="#b9d867" quantity="82" label="Tree needle decidious open" />
    <ColorMapEntry color="#cce36f" quantity="90" label="Tree mixed" />
    <ColorMapEntry color="#e0ed78" quantity="100" label="Mosaic tree and shrubland" />
    <ColorMapEntry color="#967216" quantity="110" label="Mosaic herbaceous" />
    <ColorMapEntry color="#a67d1a" quantity="120" label="Shrubland" />
    <ColorMapEntry color="#b6881f" quantity="121" label="Shrubland evergreen" />
    <ColorMapEntry color="#c69323" quantity="122" label="Shrubland decidious" />
    <ColorMapEntry color="#d69e27" quantity="130" label="Grassland" />
    <ColorMapEntry color="#e6a82b" quantity="140" label="Lichens and mosses" />
    <ColorMapEntry color="#f6b148" quantity="150" label="Sparse vegetation" />
    <ColorMapEntry color="#febc7a" quantity="151" label="Sparse tree" />
    <ColorMapEntry color="#ffcaaa" quantity="152" label="Sparse shrub" />
    <ColorMapEntry color="#f8dcd3" quantity="153" label="Sparse herbaceous" />
    <ColorMapEntry color="#016a6d" quantity="160" label="Tree cover flooded fresh or brackish water" />
    <ColorMapEntry color="#42ded5" quantity="170" label="Tree cover flooded saline water" />
    <ColorMapEntry color="#35adad" quantity="180" label="Shrub or herb cover flood" />
    <ColorMapEntry color="#3640b7" quantity="190" label="Urban" />
    <ColorMapEntry color="#df704f" quantity="200" label="Bare areas" />
    <ColorMapEntry color="#c54802" quantity="201" label="Bare areas consolidated" />
    <ColorMapEntry color="#fd9ca7" quantity="202" label="Bare areas unconsolidated" />
    <ColorMapEntry color="#48a7ff" quantity="210" label="Water bodies" />
    <ColorMapEntry color="#b9eeef" quantity="220" label="Snow and ice" />
  </ColorMap>
</RasterSymbolizer>
"""  # noqa: E501


# Dictionary to store land cover class names and colors
landcover_info = {
    "10": {"Landcover": "Cropland rainfed", "Color": "#5b5b18"},
    "11": {"Landcover": "Cropland rainfed herbaceous", "Color": "#7d7617"},
    "12": {"Landcover": "Cropland rainfed tree or shrub", "Color": "#124d00"},
    "20": {"Landcover": "Cropland irrigation or post-flood", "Color": "#a09113"},
    "30": {"Landcover": "Mosaic cropland", "Color": "#c0ab10"},
    "40": {"Landcover": "Mosaic natural vegetation", "Color": "#dfc30c"},
    "50": {"Landcover": "Tree broadleaved evergreen closed to open", "Color": "#136010"},
    "60": {"Landcover": "Tree broadleaved deciduous closed to open", "Color": "#117221"},
    "61": {"Landcover": "Tree broadleaved deciduous closed", "Color": "#0b842f"},
    "62": {"Landcover": "Tree broadleaved deciduous open", "Color": "#2a9339"},
    "70": {"Landcover": "Tree needle evergreen closed to open", "Color": "#4aa040"},
    "80": {"Landcover": "Tree needle deciduous closed to open", "Color": "#91c357"},
    "81": {"Landcover": "Tree needle deciduous closed", "Color": "#a5ce5f"},
    "82": {"Landcover": "Tree needle deciduous open", "Color": "#b9d867"},
    "90": {"Landcover": "Tree mixed", "Color": "#cce36f"},
    "100": {"Landcover": "Mosaic tree and shrubland", "Color": "#e0ed78"},
    "110": {"Landcover": "Mosaic herbaceous", "Color": "#967216"},
    "120": {"Landcover": "Shrubland", "Color": "#a67d1a"},
    "121": {"Landcover": "Shrubland evergreen", "Color": "#b6881f"},
    "122": {"Landcover": "Shrubland deciduous", "Color": "#c69323"},
    "130": {"Landcover": "Grassland", "Color": "#d69e27"},
    "140": {"Landcover": "Lichens and mosses", "Color": "#e6a82b"},
    "150": {"Landcover": "Sparse vegetation", "Color": "#f6b148"},
    "151": {"Landcover": "Sparse tree", "Color": "#febc7a"},
    "152": {"Landcover": "Sparse shrub", "Color": "#ffcaaa"},
    "153": {"Landcover": "Sparse herbaceous", "Color": "#f8dcd3"},
    "160": {"Landcover": "Tree cover flooded fresh or brackish water", "Color": "#016a6d"},
    "170": {"Landcover": "Tree cover flooded saline water", "Color": "#42ded5"},
    "180": {"Landcover": "Shrub or herb cover flood", "Color": "#35adad"},
    "190": {"Landcover": "Urban", "Color": "#3640b7"},
    "200": {"Landcover": "Bare areas", "Color": "#df704f"},
    "201": {"Landcover": "Bare areas consolidated", "Color": "#c54802"},
    "202": {"Landcover": "Bare areas unconsolidated", "Color": "#fd9ca7"},
    "210": {"Landcover": "Water bodies", "Color": "#48a7ff"},
    "220": {"Landcover": "Snow and ice", "Color": "#b9eeef"},
}  # noqa: E501
