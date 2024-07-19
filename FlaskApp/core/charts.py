import plotly.graph_objects as pGraph, pandas as pd, datetime as dt, statistics as stats

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
                       color = '#000000',
                   )
                   )])

    fig['data'][0].width = 0.25
    fig['data'][1].width = 0.04

    fig.add_vline(
        x=pace, 
        line_dash="dash", 
        annotation_text=str(pace) + ' SGD', 
        annotation_position="top right")

    fig.update_layout(
        xaxis=dict(zeroline=False),
        yaxis_type='category',
        barmode='stack',
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

    fig.update_xaxes(ticksuffix=" SGD")
    
    return fig.to_json()

def plotLastTransactions(transactionData: pd.DataFrame):
    fig = pGraph.Figure()
    
    SCALE = 10

    listIn = []
    listOut = []
    listInText = []
    listOutText = []
    heightList = []

    for index, record in transactionData.iterrows():
        if record['Type'] == 'Sales':
            listIn.append(record['Timestamp'].timestamp())
            listInText.append('[' + dt.datetime.strftime(record['Timestamp'], '%H:%M') + '] ' + record['CounterpartyID'] + ', ' + str(record['Amount']) + ' ' + str(record['Currency']))
        else:
            listOut.append(record['Timestamp'].timestamp())
            listOutText.append('[' + dt.datetime.strftime(record['Timestamp'], '%H:%M') + '] ' + record['CounterpartyID'] + ', ' + str(record['Amount']) + ' ' + str(record['Currency']))
        
        heightList.append(record['Timestamp'].timestamp() / 10000)

    if len(heightList) >= 2:
        heightList.sort()
        leadingIndex = 0
        distanceList = []
        while leadingIndex < len(heightList):
            if leadingIndex == 1:
                minDist = heightList[leadingIndex] - heightList[leadingIndex - 1]
                distanceList.append(minDist)
            elif leadingIndex > 1:
                minDist = min(minDist, heightList[leadingIndex] - heightList[leadingIndex - 1])
                distanceList.append(heightList[leadingIndex] - heightList[leadingIndex - 1])
            leadingIndex += 1
        
        print(distanceList)
        print(minDist)
        gheight = sum([x for x in distanceList]) / minDist * SCALE
        print(gheight)

    else:
        gheight = 300
    
    


    listInX = ['Event' for i in range(len(listIn))]
    listOutX = ['Event' for i in range(len(listOut))]

    fig.add_trace(pGraph.Scatter(y=listIn, x=listInX,
                    mode='lines+markers+text',
                    marker_color=THEME_COLOR,
                    hoverinfo = 'skip',
                    text = listInText,
                    textposition='middle right'))
    
    fig.add_trace(pGraph.Scatter(y=listOut, x=listOutX,
                    mode='lines+markers+text',
                    marker_color=THEME_COLOR,
                    hoverinfo = 'skip',
                    text = listOutText,
                    textposition='middle left'
                    ))

    uniqueDay = list({ record['Timestamp'].replace(hour=0, minute=0, second=0, microsecond=0).timestamp() for index, record in transactionData.iterrows() })
    print(uniqueDay)
    
    for day in uniqueDay:
        fig.add_hline(
            y=day,
            line_dash="dash", 
            annotation_text=str(dt.date.fromtimestamp(day)),
            opacity=0.3,
            annotation_position="bottom")
    
    fig.update_layout(
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10,
            pad=0
        ),
        height= gheight,
        showlegend = False,
        yaxis_visible = False,
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR
    )

    return fig.to_json()