import pandas as pd # type: ignore
import numpy as np # type: ignore
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle # type: ignore
from reportlab.lib.styles import getSampleStyleSheet # type: ignore
from reportlab.lib import colors # type: ignore
import matplotlib.pyplot as plt # type: ignore
from reportlab.lib.units import inch # type: ignore
from reportlab.lib.pagesizes import A4 # type: ignore

import seaborn as sns # type: ignore

class insert_in_story:
    def __init__(self):
        self.__story=[]
        self.styles = getSampleStyleSheet()

    def insert_heading(self,text):
        self.__story.append(Paragraph(text,self.styles['Title']))
        self.__story.append(Spacer(1,0.2*inch))

    def insert_subheading(self,text):
        self.__story.append(Paragraph(text,self.styles['h2']))
        self.__story.append(Spacer(1,0.2*inch))

    def insert_text(self,text):
        self.__story.append(Paragraph(text,self.styles['BodyText']))
        self.__story.append(Spacer(1,0.2*inch))

    def insert_linechart(self,x,y,xlabel='',ylabel='',title=''):
        img_buffer = io.BytesIO()
        
        #create a bar chart
        plt.figure(figsize=(16,8))
        plt.plot(x ,y,marker='o')
        plt.xlabel(xlabel) 
        plt.ylabel(ylabel)
        plt.style.use('ggplot')
        plt.title(title)
        plt.xticks(rotation=45)
        plt.grid(True)
        for i,value in enumerate(y):
            plt.text(x[i],value+20000,f"{int(value):,}",ha="center")

        plt.savefig(img_buffer,format='png',dpi=300,bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        graph_img = Image(img_buffer,width=6*inch,height=3*inch)
        self.__story.append(graph_img)

    def insert_barchart(self,x, y, xlabel='', ylabel='', title=''):
        """
        Generates a Matplotlib bar chart and adds it to the global 'story' list for ReportLab.
        
        Args:
            x (list): A list of categories for the x-axis.
            y (list): A list of numerical values for the y-axis.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            title (str): Title of the chart.
        """
        img_buffer = io.BytesIO()

        # Create a bar chart
        plt.figure(figsize=(8, 4))
        plt.bar(x, y, color='skyblue') # Use plt.bar() for a bar chart
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.style.use('ggplot')
        plt.title(title)
        plt.xticks(rotation=45)
        plt.grid(True, axis='y') # Grid on y-axis is common for bar charts

        # Add value labels on top of each bar
        for i, value in enumerate(y):
            plt.text(i, value + (max(y) * 0.01), f"{int(value):,}", ha="center")

        # Save plot to buffer
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()

        # Add image to the ReportLab story
        graph_img = Image(img_buffer, width=6*inch, height=3*inch)
        self.__story.append(graph_img)

    def insert_histogram(self,data, bins='auto', xlabel='', ylabel='Frequency', title=''):
        """
        Generates a Matplotlib histogram and adds it to the global 'story' list for ReportLab.

        Args:
            data (list or array): A list of numerical data to be plotted.
            bins (int or str): The number of bins for the histogram. Defaults to 'auto'.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis. Defaults to 'Frequency'.
            title (str): Title of the chart.
        """
        img_buffer = io.BytesIO()

        # --- Chart Creation ---
        plt.figure(figsize=(8, 4))

        # Use seaborn's hist function to create the histogram
        sns.histplot(data,bins=10,kde=True,color='skyblue')

        # --- Formatting ---
        plt.style.use('ggplot')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)

        # --- Save plot to buffer ---
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()

        # --- Add image to the ReportLab story ---
        graph_img = Image(img_buffer, width=6*inch, height=3*inch)
        self.__story.append(graph_img)

    def insert_piechart(self,labels, sizes, title=''):
        """
        Generates a Matplotlib pie chart and adds it to the global 'story' list for ReportLab.
        
        Args:
            labels (list): A list of string labels for each wedge.
            sizes (list): A list of numerical values representing the size of each wedge.
            title (str): Title of the chart.
        """
    
        img_buffer = io.BytesIO()

        # Create a pie chart
        plt.figure(figsize=(6, 6)) # Pie charts often look best as squares
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title(title)
        plt.style.use('ggplot')


        # Save plot to buffer
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()

        # Add image to the ReportLab story
        graph_img = Image(img_buffer, width=3*inch, height=3*inch)
        self.__story.append(graph_img)

    def insert_heatmap(self,data, row_labels, col_labels, title='', cmap='viridis', annot=True):
        """
        Generates a Seaborn heatmap and adds it to the global 'story' list for ReportLab.

        Args:
            data (2D array-like): The data for the heatmap (e.g., list of lists, numpy array).
            row_labels (list): Labels for the rows (y-axis).
            col_labels (list): Labels for the columns (x-axis).
            title (str): Title of the chart.
            cmap (str): Colormap for the heatmap (e.g., 'viridis', 'coolwarm', 'YlGnBu').
            annot (bool): If True, write the data value in each cell.
        """
        img_buffer = io.BytesIO()

        # --- Chart Creation ---
        # Adjust figsize based on your data shape for better readability
        fig_width = max(8, len(col_labels))
        fig_height = max(6, len(row_labels) * 0.8)
        plt.figure(figsize=(fig_width, fig_height))

        # Use Seaborn's heatmap function for a clean and attractive plot
        sns.heatmap(data,
                    xticklabels=col_labels,
                    yticklabels=row_labels,
                    cmap=cmap,
                    annot=annot,  # Display the numbers in the cells
                    fmt='.2f')      # Format numbers as integers

        # --- Formatting ---
        plt.title(title, fontsize=16)
        plt.xticks(rotation=45, ha='right') # Rotate x-labels for better fit
        plt.yticks(rotation=0)
        
        # --- Save plot to buffer ---
        # Use bbox_inches='tight' to ensure all labels are included in the saved image
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()

        # --- Add image to the ReportLab story ---
        # Adjust width/height as needed for your report layout
        graph_img = Image(img_buffer, width=7*inch, height=5*inch)
        self.__story.append(graph_img)

    def insert_stacked_barchart(self,categories, data, xlabel='', ylabel='', title=''):
        """
        Generates a Matplotlib stacked bar chart and adds it to the global 'story' list.
        
        Args:
            categories (list): A list of category names for the x-axis.
            data (dict): A dictionary where keys are series names (str) 
                        and values are lists of numerical data.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            title (str): Title of the chart.
        """
        
        img_buffer = io.BytesIO()

        # Create a stacked bar chart
        plt.figure(figsize=(8, 4))
        
        series_labels = list(data.keys())
        num_categories = len(categories)
        
        # Initialize a numpy array to keep track of the bottom of each stack
        bottom = np.zeros(num_categories)

        # Plot each data series on top of the previous one
        for label in series_labels:
            values = data[label]
            plt.bar(categories, values, label=label, bottom=bottom)
            bottom += np.array(values) # Add the current values to the bottom for the next series

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.xticks(rotation=45)
        plt.style.use('ggplot')
        plt.legend() # Add a legend to identify the series
        plt.grid(True, axis='y')

        # Save plot to buffer
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()

        # Add image to the ReportLab story
        graph_img = Image(img_buffer, width=6*inch, height=3*inch)
        self.__story.append(graph_img)

    def insert_grouped_barchart(self, grouped_data, xlabel='', ylabel='', title=''):
        """
        Generates a Matplotlib grouped (side-by-side) bar chart and adds it to the global 'story' list.
        
        Args:
            categories (list): A list of category names for the x-axis.
            data (dict): A dictionary where keys are series names (str) 
                        and values are lists of numerical data.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            title (str): Title of the chart.
        """
        
        img_buffer = io.BytesIO()

        # --- Chart Creation ---
        plt.figure(figsize=(10, 5)) # A wider figure often helps with grouped bars
        
        sns.barplot(data=grouped_data,x='Month',y='Revenue',hue='Country')

        # --- Formatting ---
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
    
        
        # Set the x-ticks to be in the middle of each group
        plt.xticks(rotation=45)
        
        plt.legend()

        # --- Save plot to buffer ---
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()

        # --- Add image to the ReportLab story ---
        graph_img = Image(img_buffer, width=7*inch, height=3.5*inch)
        self.__story.append(graph_img)

    def insert_table(self,attr_info):
        table_data = [['Attribute', 'Description']]
        for key, value in attr_info.items():
            table_data.append([Paragraph(key), Paragraph(value)])

        # Create the table
        attr_table = Table(table_data, colWidths=[100, 350])
        attr_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.black),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ]))

        # Add the table to the story
        self.__story.append(attr_table)
        self.__story.append(Spacer(1,0.2*inch))

    def get_story(self):
        return self.__story

class loader():
    @classmethod
    def load_json(self,location):
        df = pd.read_json(location)
        return df
    
    @classmethod
    def insert_to_pdf(self,story):
        # Create a PDF document
        doc = SimpleDocTemplate('report.pdf', pagesize=A4)
        styles = getSampleStyleSheet()
        doc.build(story)

    