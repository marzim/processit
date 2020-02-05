import pandas as pd
import random
from pandas import ExcelWriter

class MyChart:

    def __init__(self, sheetname=None, col_retrieve=None, chartname=None, chart_position=None):
        self.sheetname = sheetname
        self.col_retrieve =  col_retrieve
        self.chartname = chartname
        self.chart_position = chart_position

    def createchart(self, title, col_retrieve, workbook, sheetname, row_count):
        # Create a chart object.
        chart = workbook.add_chart({'type': 'line'})

        # Configure the series of the chart from the dataframe data.
        for i in range(len(col_retrieve)):
            col = i + 1
            chart.add_series({
                'name':       [sheetname, 0, col_retrieve[i]],
                'categories': [sheetname, 1, 0, row_count, 0],
                'values':     [sheetname, 1, col_retrieve[i], row_count, col_retrieve[i]],        
            })

        # Configure the chart axes.
        chart.set_x_axis({'name': 'Elapsed Time', 'major_gridlines': {'visible': False}})
        chart.set_y_axis({'name': title, 'major_gridlines': {'visible': True}})
        chart.set_legend({'position': 'bottom'})
        chart.set_title({'name': title})
        chart.set_size({'width': 510, 'height': 350})

        return chart
    

    
