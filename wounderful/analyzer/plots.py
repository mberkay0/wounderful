import plotly.graph_objs as go
import plotly.offline as py
from plotly.subplots import make_subplots
import plotly.io as pio
from scipy.stats import linregress


def plotScratchWidth(scratchWidth, frames):
    fig = go.Figure(layout=go.Layout(
        xaxis=dict(title='Frames'),
        yaxis=dict(title='Wound Width (px)'),
        title='The change of wound width over time',
    ))

    for sw in scratchWidth:
        width = []
        std = []
        for i in sw:
            width.append(i[0])
            std.append(i[-1])
        Rm = cell_migrations(sw[0][0], sw[-1][0], len(sw))

        fig.add_trace(go.Scatter(
            x=frames,
            y=width,
            mode='lines+markers',
            name='Wound Width-' + str(scratchWidth.index(sw) + 1),
            error_y=dict(type='data', array=std),
        ))

        fig.add_annotation(
            x=1,
            y=1 - scratchWidth.index(sw) * 0.1,
            xref="paper",
            yref="paper",
            text='Rate of Cell Migration-{}: {:.2f} px/h'.format(scratchWidth.index(sw) + 1, Rm),
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="#ffffff"
            ),
            align="center",
            bordercolor="#c7c7c7",
            bgcolor="#ff7f0e",
            opacity=0.8
        )

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


def plotWoundArea(woundArealist, frames):
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    for woundArea in woundArealist:
        variation = []
        to_frames = []

        for i in range(len(woundArea) - 1):
            variation.append(woundArea[i] - woundArea[i + 1])

        for j in range(len(frames) - 1):
            to_frames.append(frames[j] + " to -> " + frames[j + 1])

        variation = [(i / woundArea[0]) * 100 for i in variation]

        times = [int(i) for i in frames]
        slope, intercept, r_value, p_value, std_err = linregress(times, woundArea)

        fig.append_trace(go.Bar(
            x=variation,
            y=to_frames,
            name="Amount of Reduction of the Wound Area in the Next Frame-" + str(woundArealist.index(woundArea) + 1),
            orientation='h',
        ), 1, 1)

        fig.append_trace(go.Scatter(
            x=frames,
            y=woundArea,
            mode='lines+markers',
            name='Wound Area-' + str(woundArealist.index(woundArea) + 1),
            orientation='h'
        ), 1, 2)
        fig.add_annotation(
            x=1,
            y=0.95 - woundArealist.index(woundArea) * 0.1,
            xref="paper",
            yref="paper",
            text='R\N{SUPERSCRIPT TWO}{}: {:.2f}'.format(woundArealist.index(woundArea) + 1, r_value ** 2),
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="#ffffff"
            ),
            align="center",
            bordercolor="#c7c7c7",
            bgcolor="#ff7f0e",
            opacity=0.8
        )

        fig.add_annotation(
            x=1,
            y=1 - woundArealist.index(woundArea) * 0.1,
            xref="paper",
            yref="paper",
            text='y{} = {:.2f}x + {:.2f}'.format(woundArealist.index(woundArea) + 1, slope, intercept),
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=12,
                color="#ffffff"
            ),
            align="center",
            bordercolor="#c7c7c7",
            bgcolor="#ff7f0e",
            opacity=0.8
        )
    fig.update_layout(
        showlegend=True,
        title="Change of the Wound Area over Time",
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
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
    )

    return fig


def plotRWD(woundArealist, frames, size):
    fig = go.Figure(layout=go.Layout(
        xaxis=dict(title='Frames'),
        yaxis=dict(title='Relative Wound Density %'),
        title='The change of relative wound density over time',
    ))

    for woundArea in woundArealist:
        RWD=[]
        for i in range(len(woundArea)):
            RWD.append(abs(((woundArea[i] - woundArea[0]) / (size[woundArealist.index(woundArea)]-woundArea[i] - woundArea[0])) * 100))

        fig.add_trace(go.Scatter(
            x=frames,
            y=RWD,
            mode='lines+markers',
            name='%RWD-' + str(woundArealist.index(woundArea)+1),
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
            tickvals = frames,
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


