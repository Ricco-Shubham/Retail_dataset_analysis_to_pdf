import json
from standards import standards
from loader import insert_in_story
from utils import *

class Analysis(standards):
    @classmethod
    def run_analysis(self):
        # sequence of insertion of each objects in pdf
        while True:
            try: 
                level = int(input("Enter the report level 1 / 2 / 3 \n"))
            except:
                print("Please enter a number \n")
                continue
            if level in [1,2,3]:
                break
            else:
                print("Please choose from 1/2/3 \n")


        insertObject = insert_in_story()  # create object for story 
        # sequence of insertion of each objects in pdf
        # level 1
        if level in [1,2,3]:
            heading = 'Retail Data Analysis Report level ' + str(level)
            insertObject.insert_heading(heading)
            insertObject.insert_text(data['content'])

            insertObject.insert_subheading('Dataset Information')
            insertObject.insert_table(data['dataset_info'])

            insertObject.insert_subheading('Attribute Information')
            insertObject.insert_table(data['Attribute Information'])

            insertObject.insert_subheading('Source')
            insertObject.insert_text(data['Source'])

            insertObject.insert_subheading('Citation Request')
            insertObject.insert_text(data['Citation Request'])
            
            insertObject.insert_subheading('Revenue vs month')
            insertObject.insert_linechart(monthly_revenue.index,monthly_revenue.values,'Month','Revenue','Revenue vs month')  

        # level 2 charts
        if level in [2,3]:
            insertObject.insert_subheading('Distribution of Quantity')
            insertObject.insert_histogram(df_quantity['Quantity'],xlabel='Quantity',title='Distribution of Quantity')

            insertObject.insert_subheading('Revenue of top 10 Countries')
            insertObject.insert_barchart(country_revenue.index,country_revenue.values,'Country','Revenue','Revenue of top 10 Countries')

            insertObject.insert_subheading('Quantity sold each month')
            insertObject.insert_linechart(monthly_quantity.index,monthly_quantity.values,'Month','Quantity','Quantity sold each month')

        # level 3
        if level == 3 :
            insertObject.insert_subheading('Grouped bar chart')
            insertObject.insert_grouped_barchart(grouped_data=grouped,title='Grouped bar chart',xlabel='Month',ylabel='Revenue') 

            insertObject.insert_subheading('top 10 countries contribution by revenue')
            insertObject.insert_piechart(labels=top_countries_by_revenue.index,sizes=top_countries_by_revenue.values,title='Pie chart') 

            insertObject.insert_subheading('Heat Map ')
            insertObject.insert_heatmap(corr_matrix,col_labels=labels,row_labels=labels)

        loader.insert_to_pdf(insertObject.get_story())
        print("Report is exported successfully")

if __name__ == '__main__':
    Analysis.run_analysis()