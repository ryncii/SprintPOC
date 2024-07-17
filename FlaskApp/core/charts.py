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

def plotPacingBar(target: float, current:float, pace: float):
    fig = pGraph.Figure(data=[
        pGraph.Bar(name='Month Revenue', y=['Pace'], x=[current], orientation='h', 
                   marker=dict(
                       color = '#154360',
                   )),
        pGraph.Bar(name='', y=['Pace'], x=[max(target-current, 0)], orientation='h',
                   marker=dict(
                       color = '#FFFFFF',
                   )
                   )])

    fig['data'][0].width = 0.2
    fig['data'][1].width = 0.05

    fig.update_layout(barmode='stack',
                  yaxis_type='category')
    
    return fig.to_json()