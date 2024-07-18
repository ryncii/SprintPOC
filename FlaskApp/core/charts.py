import plotly.express as px, plotly.utils as pUtils, json, plotly.graph_objects as pGraph

THEME_COLOR = '#154360'
BACKGROUND_COLOR = '#EAF2F8'


def plotOverallHealth(balance:list, highlight):
    fig = pGraph.Figure()

    fig.add_trace(pGraph.Box(
        x=balance,
        boxmean=True,
        boxpoints='outliers',
        name=0,
        marker_color=THEME_COLOR,
        hoverinfo='skip'
    ))


    fig.add_trace(pGraph.Scatter(
        x=[highlight],
        y=[0.3],
        mode='markers+text',
        marker_symbol = 'triangle-down',
        marker_size= 12,
        marker=dict(color='#000000'),
        showlegend=False,
        hoverinfo = 'skip',
        text = ['Last Month Profit: ' + str(x) + ' SGD' for x in [highlight]],
        textposition='top center'
    ))

    fig.update_layout(
        xaxis=dict(zeroline=False),
        boxmode='group',
        width=500,
        height=100,
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=2
        ),
        yaxis_visible = False,
        showlegend = False,
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR
    )

    fig.update_traces(orientation='h') 
    fig.update_xaxes(ticksuffix=" SGD")
    fig.update_yaxes(range= (-0.5, 2.5))

    return fig.to_json()

def plotPacingBar(target: float, current:float, pace: float):
    fig = pGraph.Figure(data=[
        pGraph.Bar(name='Month Revenue', y=['Pace'], x=[current], orientation='h', 
                   marker=dict(
                       color = THEME_COLOR,
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