import plotly.graph_objs as go
import plotly.offline as py
from plotly.subplots import make_subplots
import plotly.io as pio
from scipy.stats import linregress

def plotScratchWidth(scratchWidth, frames):
    width = []
    std = []
    for i in scratchWidth:
        width.append(i[0])
        std.append(i[-1])
    Rm = cell_migrations(scratchWidth[0][0], scratchWidth[-1][0], len(scratchWidth))

    fig = go.Figure(layout=go.Layout(
        xaxis=dict(title='Frames'),
        yaxis=dict(title='Wound Width (px)'),
        title='The change of wound width over time',
    ))

    fig.add_trace(go.Scatter(
        x=frames,
        y=width,
        mode='lines+markers',
        line_color='rgb(128, 0, 128)',
        name='Wound Width',
        error_y=dict(type='data', array=std),
    ))
    fig.update_layout(
        showlegend=True,
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            tickvals=frames,
            ticks="outside",
            tickson="boundaries",
            ticklen=5
        ),
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
        width=850,
        height=600,
    )
    fig.add_annotation(
        x=1,
        y=1,
        xref="paper",
        yref="paper",
        text='Rate of Cell Migration: {:.2f} px/h'.format(Rm),
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
        ),
        align="center",
        bordercolor="#c7c7c7",
        bgcolor="#ff7f0e",
        opacity=0.8
    )
    return fig


def cell_migrations(Wi, Wf, frame, hour=1):
    """Hucre gocu hizini hesaplar ve geri dondurur.
    Args:
        Wi (int): Deneyin ilk karesindeki ortalama yara alani genisligi.
        Wf (int): Olcumun yapilacagi son ortalama yara alani genisligi.
        frame (str): Kare sayisi.
        hour (str): Karelerin ne siklikla kaydedildigi (geçen süre) saat cinsinden.
    Returns:
        RM (float): Hucre gocu hizi
    """
    t = frame * hour
    return (Wi - Wf) / t


def plotWoundArea(woundArea, frames):
    variation = []
    to_frames = []

    for i in range(len(woundArea) - 1):
        variation.append(woundArea[i] - woundArea[i + 1])

    for j in range(len(frames) - 1):
        to_frames.append(frames[j] + " to -> " + frames[j + 1])

    variation = [(i / woundArea[0]) * 100 for i in variation]

    times = [int(i) for i in frames]
    slope, intercept, r_value, p_value, std_err = linregress(times, woundArea)

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)
    fig.append_trace(go.Bar(
        x=variation,
        y=to_frames,
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        ),
        name='Amount of Reduction of the Wound Area in the Next Frame',
        orientation='h',
    ), 1, 1)

    fig.append_trace(go.Scatter(
        x=frames,
        y=woundArea,
        mode='lines+markers',
        line_color='rgb(128, 0, 128)',
        name='Wound Area',
        orientation='h'
    ), 1, 2)

    fig.update_layout(
        showlegend=True,
        title='Change of the Wound Area over Time',
        yaxis=dict(
            title="Frames",
            showgrid=False,
            showline=False,
            showticklabels=True,
        ),
        yaxis2=dict(
            title="Wound Area by Time (px)",
            showgrid=True,
            showline=True,
            showticklabels=True,
            linecolor='rgba(102, 102, 102, 0.8)',
            linewidth=2,
        ),
        xaxis=dict(
            title="Amount of Reduction of the Wound Area in the Next Frame (%px)",
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
        ),
        xaxis2=dict(
            title="Frames",
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            tickvals=frames,
        ),
        paper_bgcolor='rgb(255, 255, 255)',#rgb(248, 248, 255)
        plot_bgcolor='rgb(255, 255, 255)',
    )
    fig.add_annotation(
        x=1,
        y=0.93,
        xref="paper",
        yref="paper",
        text='R\N{SUPERSCRIPT TWO}: {:.2f}'.format(r_value ** 2),
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
        ),
        align="center",
        bordercolor="#c7c7c7",
        bgcolor="#ff7f0e",
        opacity=0.8
    )

    fig.add_annotation(
        x=1,
        y=1,
        xref="paper",
        yref="paper",
        text='y = {:.2f}x + {:.2f}'.format(slope, intercept),
        showarrow=False,
        font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
        ),
        align="center",
        bordercolor="#c7c7c7",
        bgcolor="#ff7f0e",
        opacity=0.8
    )
    return fig


def plotRWD(woundArea, frames, size):
    RWD = []
    for i in range(len(woundArea)):
        RWD.append(abs(((woundArea[i] - woundArea[0]) / (size - woundArea[i] - woundArea[0])) * 100))

    fig = go.Figure(layout=go.Layout(
        xaxis=dict(title='Frames'),
        yaxis=dict(title='Relative Wound Density %'),
        title='The change of relative wound density over time',
    ))

    fig.add_trace(go.Scatter(
        x=frames,
        y=RWD,
        mode='lines+markers',
        line_color='rgb(128, 0, 128)',
        name='%RWD',
    ))
    fig.update_layout(
        showlegend=True,
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            tickvals=frames,
            ticks="outside",
            tickson="boundaries",
            ticklen=5
        ),
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
        width=650,
        height=600,
    )
    return fig
