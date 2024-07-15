import plotly.express as px, plotly.utils as pUtils, json, plotly.graph_objects as pGraph

def plotOverallHealth(balance:list, month:list):
    fig = pGraph.Figure()
    fig.add_trace(pGraph.Box(
        x=balance,
        y=month,
        marker_color='#154360'
    ))

    fig.update_traces(orientation='h') 
    return fig.to_json()
