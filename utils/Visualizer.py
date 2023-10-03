"""
Questions 
How many containers are being unloaded at each berth?

Currently which warehouse is coming close to its maximum capacity?, I want to know the current capacity of each warehouse
Ans: 
Bar graph with Current number + Maximum captacity

Default Reply:
   --> 
"""
import pandas as pd 
# Graphing libraries
import os 
import sys
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.figure_factory as ff
import inspect
path_to_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

warehouse_df = pd.read_csv(os.path.join(path_to_root, 'src/Warehouse_data.csv'))
warehouse_capacity_df = pd.read_csv(os.path.join(path_to_root, 'src/Warehouse_info.csv'))
class Visualizer:
   """"Main wrapper function"""

   @classmethod
   def plot_current_warehouse_capacity(cls) -> go.Figure:

      # Get the current capacity of the warehouses
      number_cotainers_per_warehouse = warehouse_df['warehouse_id'].value_counts()
      number_cotainers_per_warehouse.sort_index(inplace=True)

      # Create a figure
      fig = go.Figure()
      # Plot current warehouse capacity
      fig.add_bar(x=number_cotainers_per_warehouse.index, y=
                  number_cotainers_per_warehouse.values,name="Currrent Capacity")
      # Another seperate bar for total capacity per warehouse, so we can compare
      fig.add_bar(x=warehouse_capacity_df['warehouse_id'], y=warehouse_capacity_df['total_capacity'],
                  name='Total Capacity')
      # Add title and axis labels
      fig.update_layout(
         title='Current Warehouse Capacity',
         xaxis_title='Warehouse ID',
         yaxis_title='Current Capacity'
      )
      # Add legend
      fig.update_layout(showlegend=True,barmode='group')
      # Add legend for total capacity and current capacity
      return fig
   
   @classmethod
   def get_code(cls) -> str:
      """Returns the code for the visualizer"""
      # Get the source code of the Visualizer class
      code = inspect.getsource(cls)
      # Get the source code of the plot_current_warehouse_capacity method
      code += inspect.getsource(cls.plot_current_warehouse_capacity)
      return code
   
   @classmethod
   def getWarehouseData(cls) -> pd.DataFrame:
      return warehouse_df

