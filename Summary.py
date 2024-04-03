

import pandas as pd
import numpy as np 
import plotly.graph_objects as go
import statistics
import os
from dash import Dash, html, dcc, callback, Output, Input

#Recieves number of folds in train
def get_folds():
    num_folds = int(input('Number of folds: '))

    return num_folds

#Recieves name of dataset
def get_dataset():
    dataset = input('Name of Dataset: ')

    return dataset

#Loads csv into a dataframe, puts each dataframe into list
def create_df_list(dataset, num_folds):
    df_list = []
    #Works in in yolov5 directory
    file_path = f'./runs/train/{dataset}/'
    for i in range(num_folds):
        fold_path = file_path + f'Fold{i+1}/results.csv'
        fold_df = pd.read_csv(fold_path)
        fold_df.rename(columns=lambda x: x.strip(), inplace=True)
        df_list.append(fold_df)
        
    return df_list

#Creates visual for each catacory vs epochs
def epochVs(df_list, method):

    #Each line for each fold
    trace_list = []

    #Creating line for epoch vs each method for each fold
    for fold in range(len(df_list)):
        trace = go.Scatter(x=df_list[fold]['epoch'], y=df_list[fold][method], mode='lines', name=f'Fold {fold+1}')
        trace_list.append(trace)     

    #creating figure
    fig = go.Figure(trace_list)
    fig.update_layout(title=method, xaxis_title='Epochs', yaxis_title=method)
    return fig

#Methods = Column names
def getMethods(df_list):
    col_names = []
    for col in df_list[0].columns:
        col_names.append(col)
    col_names.remove('epoch')
    return col_names


#Creates summary for each fold seperatly 
def displayBestRuns(dataset, df_list):
    best_runs_list = []
    #file path from yolo
    file_path = f'./runs/train/{dataset}/'
    num_rows = int(input("How many epochs would you like to see in each fold's best runs? "))
    for df in range(len(df_list)):
        #sorting each fold by best to worst mAP_0.5:0.95 then only showing the specified rows
        best_df = df_list[df].sort_values(by='metrics/mAP_0.5:0.95',ascending=False)
        best_df = best_df.head(num_rows)
        summary_file_path = file_path + f'Fold{df+1}/'
        best_df.to_csv(f'{summary_file_path}Fold{df+1}_best_runs.csv', index=False)
        
       
def createSummary(df_list):
    #creating list containing best values from each fold
    precision_list = []
    recall_list = []
    mAP_list = []
    mAP2_list = []

    
    for i in range(len(df_list)):
        #sorting each fold by best to worst mAP_0.5:0.95
        best_df = df_list[i].sort_values(by='metrics/mAP_0.5:0.95',ascending=False)
        row_index = 0
        #columns to extract
        columns_of_interest = ['metrics/precision', 'metrics/recall','metrics/mAP_0.5','metrics/mAP_0.5:0.95']  # Choose the columns you want to extract
        row_values_list = best_df.iloc[row_index][columns_of_interest].tolist()

        #appending best data to lists
        prec = row_values_list[0]
        precision_list.append(prec)
        
        recall = row_values_list[1]
        recall_list.append(recall)
        
        mAP = row_values_list[2]
        mAP_list.append(mAP)
        
        mAP2 = row_values_list[3]
        mAP2_list.append(mAP2)

    #creating list from best values
    best_lists = [precision_list, recall_list, mAP_list, mAP2_list]

    #Calculating mean and std from best runs
    for i in range(len(best_lists)):
        mean = statistics.mean(best_lists[i])
        std_dev = statistics.stdev(best_lists[i])
        best_lists[i].append(mean)
        best_lists[i].append(std_dev)

    #creating a dictionary to form a pandas dataframe
    raw_data = {
        'Precision' : precision_list,
        'Recall' : recall_list,
        'mAP_0.5' : mAP_list,
        'mAP_0.5:0.95': mAP2_list
    }

    #Creating row labels
    row_labels = []
    for i in range(len(df_list)):
        fold = f'Fold {i+1}'
        row_labels.append(fold)

    row_labels.append('mean')
    row_labels.append('std')

    #Creating summary dataframe
    summarydf = pd.DataFrame(raw_data, index=row_labels)

    #Exporting summary df as a csv file
    file_path = f'./runs/train/{dataset}/'
    summarydf.to_csv(f'{file_path}Training_Summary.csv', index=True)

app = Dash(__name__)

@app.callback(
    Output('epoch-vs-graph', 'figure'),
    [Input('method-dropdown', 'value')]
)
def update_graph(selected_method):
    return epochVs(df_list, selected_method)

if __name__ == '__main__':
    num_folds = get_folds()
    dataset = get_dataset()
    df_list = create_df_list(dataset, num_folds)
    displayBestRuns(dataset, df_list)
    col_names = getMethods(df_list)
    createSummary(df_list)

    
    app.layout = html.Div([
        dcc.Dropdown(
            id='method-dropdown',
            options=[{'label': col, 'value': col} for col in col_names],
            value=col_names[0]
        ),
        dcc.Graph(
        id='epoch-vs-graph',
        style={'width': '1200px', 'height': '600px'}  # Adjust width and height as needed
    )
        
    ])
    
    app.run_server(debug=False, port=2525)






