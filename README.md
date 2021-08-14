# PlotRock - 3D Graphing Addon for Blender

Plotrock is a [Blender](http://www.blender.org) plugin that allows users to create line graphs,
using data from their tables and spreadsheets.

## Features
* Import files from Excel, LibreOffice, Google Sheets, or other similar spreadsheet programs.
* Ability to edit .csv file within Blender and regenerate plot.
* Handy sidemenu that allows plot customization.
* Utilize all Blender tools such as materials, lighting, and animated cameras.

https://user-images.githubusercontent.com/43371347/129456528-502482cb-86b4-4a55-a419-97ae086831ed.mp4


## Install
1. Find the latest [release](https://github.com/theTaikun/plotrock/releases).
2. Download the `Source Code` zip.
3. In Blender, navigate to `Edit` => `Preferences` => `Add-Ons`.
4. Click `Install` and select the dowloaded .zip.
5. Now that the addon is installed, click its checkbox to enable it.

## Usage
_PlotRock side menu can be accessed by pressing the N key in the 3D Vieport._

1. Attain data, either from exporting spreadsheet data to .csv, or procuring a .csv file from elsewhere.
2. Import data either from `File`=>`Import`=>`Import CSV for plotting` or from the PlotRock side menu.
    1. On the right-hand side of the import menu, double check import settings. By default, imports file with headers, and comma seperated.
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
