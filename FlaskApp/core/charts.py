import plotly.express as px, plotly.utils as pUtils, json, plotly.graph_objects as pGraph

def plotOverallHealth(balance:list, highlight):
    fig = pGraph.Figure()

    fig.add_trace(pGraph.Box(
        x=balance,
        name='OverallHealth',
        marker_color='#154360'
    ))

    fig.add_trace(pGraph.Scatter(
    x=[highlight],
    y=['OverallHealth'],
    mode='markers',
    marker=dict(color="red"),
    showlegend=False
    ))

    fig.update_layout(
        xaxis=dict(title='OverallHealth', zeroline=False),
        boxmode='group'
    )

    fig.update_traces(orientation='h') 
    return fig.to_json()
