# PlotRock - 3D Graphing Addon for Blender

Plotrock is a [Blender](http://www.blender.org) plugin that allows users to create line graphs,
data from their tables and spreadsheets.

## Features
* Import files from Excel, LibreOffice, Google Sheets, or other similar spreadsheet programs.
* Ability to edit .csv file within Blender and regenerate plot.
* Handy sidemenu that allows plot customization.
* Utilize all Blender tools such as materials, lighting, and animated cameras.

## Usage
1. Attain data, either from exporting spreadsheet data to .csv, or procuring a .csv file from elsewhere.
2. Import the data either from `File`=>`Import`=>`Import CSV for plotting` or from the PlotRock side menu.
3. To edit the data:
    1. Open a Text Editor window, and select the imported file.
    2. Edit the plot data as needed
    3. Click `Update Plot` from the PlotRock side menu.
4. To customize the shape of the plot, select it, and adjust the sliders in the RockPlot menu.
5. Finalize by adding camera(s) and lighting, to taste.

## Limitations
RockPlot is still a work in progress,
and as such,
has some limitations.

* Only handles files formatted as CSV.
* ~~CSVs must actually use commas. Other deliminators not yet supported.~~ Can use either comma or semicolon delimiters.
* Data within CSV has some requirements:
    * 2D data, meaning two column. Must be only one Y value for each X value.
    * Both X and Y values must be a number.
* Files must have the extension `.csv` or `.txt`.
* Only one plot per axis.
* Currently only creates line graphs.
