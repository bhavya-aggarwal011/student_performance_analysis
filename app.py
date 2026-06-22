

# ── Imports ────────────────────────────────────────────────────────────────
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ── Load Dataset ───────────────────────────────────────────────────────────
# When running locally: data/student_dataset_10000_rows.csv
# When deployed on Render: same path (Render uses your repo structure)
df = pd.read_csv('data/student_dataset.csv')

# ── Constants ──────────────────────────────────────────────────────────────
COLOR_MAP   = {'Placed': '#4C72B0', 'Not Placed': '#DD8452'}
CHART_BG    = '#f8f9fa'
CARD_BG     = '#ffffff'

NUMERIC_COLS = [
    'study_hours', 'attendance', 'sleep_hours',
    'internet_usage', 'assignments_completed',
    'previous_score', 'exam_score'
]

# ── Styles ─────────────────────────────────────────────────────────────────
CARD_STYLE = {
    'backgroundColor': CARD_BG,
    'borderRadius': '12px',
    'padding': '20px',
    'marginBottom': '20px',
    'boxShadow': '0 1px 6px rgba(0,0,0,0.08)'
}
HEADER_STYLE = {
    'background': 'linear-gradient(135deg,#1a237e,#3949ab)',
    'color': 'white',
    'padding': '28px 36px',
    'marginBottom': '24px'
}
SECTION_STYLE = {
    'fontSize': '17px',
    'fontWeight': '700',
    'color': '#1a237e',
    'borderLeft': '4px solid #3949ab',
    'paddingLeft': '12px',
    'margin': '24px 0 12px'
}
KPI_BOX = {
    'backgroundColor': CARD_BG,
    'borderRadius': '12px',
    'padding': '20px',
    'textAlign': 'center',
    'flex': '1',
    'boxShadow': '0 1px 6px rgba(0,0,0,0.08)',
    'borderTop': '4px solid #3949ab'
}
FILTER_STYLE = {
    'backgroundColor': CARD_BG,
    'borderRadius': '12px',
    'padding': '20px 28px',
    'marginBottom': '20px',
    'boxShadow': '0 1px 6px rgba(0,0,0,0.08)',
    'display': 'flex',
    'gap': '32px',
    'alignItems': 'flex-end',
    'flexWrap': 'wrap'
}
LABEL_STYLE = {
    'fontSize': '13px',
    'fontWeight': '600',
    'color': '#555',
    'marginBottom': '6px',
    'display': 'block'
}

# ── Initialise App ─────────────────────────────────────────────────────────
app  = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server   # ← Render needs this line to deploy!
app.title = 'Student Performance Dashboard'

# ── Layout ─────────────────────────────────────────────────────────────────
app.layout = html.Div(
    style={'backgroundColor': '#f0f2f5',
           'fontFamily': 'Segoe UI, Arial, sans-serif',
           'minHeight': '100vh'},
    children=[

        # HEADER
        html.Div(style=HEADER_STYLE, children=[
            html.H1('📊 Student Performance Dashboard',
                    style={'margin': '0 0 6px', 'fontSize': '26px'}),
            html.P('Data Analysis',
                   style={'margin': '0', 'opacity': '0.85'}),
            
        ]),

        html.Div(
            style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '0 24px 40px'},
            children=[

                # FILTERS
                html.Div(style=FILTER_STYLE, children=[

                    html.Div(style={'minWidth': '200px'}, children=[
                        html.Label('🎯 Placement Status', style=LABEL_STYLE),
                        dcc.Dropdown(
                            id='filter-placement',
                            options=[
                                {'label': 'All Students',   'value': 'All'},
                                {'label': 'Placed Only',    'value': 'Placed'},
                                {'label': 'Not Placed Only','value': 'Not Placed'},
                            ],
                            value='All',
                            clearable=False,
                            style={'fontSize': '14px'}
                        )
                    ]),

                    html.Div(style={'flex': '1', 'minWidth': '260px'}, children=[
                        html.Label('📚 Study Hours Range', style=LABEL_STYLE),
                        dcc.RangeSlider(
                            id='filter-study',
                            min=1, max=11, step=1,
                            value=[1, 11],
                            marks={i: str(i) for i in range(1, 12)},
                            tooltip={'placement': 'bottom', 'always_visible': False}
                        )
                    ]),

                    html.Div(style={'flex': '1', 'minWidth': '260px'}, children=[
                        html.Label('🏫 Attendance Range (%)', style=LABEL_STYLE),
                        dcc.RangeSlider(
                            id='filter-attendance',
                            min=40, max=100, step=5,
                            value=[40, 100],
                            marks={i: str(i) for i in range(40, 101, 10)},
                            tooltip={'placement': 'bottom', 'always_visible': False}
                        )
                    ]),

                    html.Div(style={'flex': '1', 'minWidth': '260px'}, children=[
                        html.Label('📝 Exam Score Range', style=LABEL_STYLE),
                        dcc.RangeSlider(
                            id='filter-score',
                            min=0, max=100, step=5,
                            value=[0, 100],
                            marks={i: str(i) for i in range(0, 101, 20)},
                            tooltip={'placement': 'bottom', 'always_visible': False}
                        )
                    ]),
                ]),

                # KPI CARDS
                html.P('Key Metrics', style=SECTION_STYLE),
                html.Div(
                    id='kpi-cards',
                    style={'display': 'flex', 'gap': '16px',
                           'marginBottom': '20px', 'flexWrap': 'wrap'}
                ),

                # INSIGHT CARDS
                html.P('Top 5 Insights', style=SECTION_STYLE),
                html.Div(
                    style={'display': 'grid',
                           'gridTemplateColumns': 'repeat(auto-fit,minmax(220px,1fr))',
                           'gap': '16px', 'marginBottom': '24px'},
                    children=[
                        html.Div(style={**CARD_STYLE, 'borderTop': '4px solid #4C72B0',
                                        'padding': '18px', 'marginBottom': '0'}, children=[
                            html.P('💡 Study Hours — Top Predictor',
                                   style={'fontSize': '13px', 'color': '#555', 'marginBottom': '6px'}),
                            html.P('r = +0.563', style={'fontSize': '22px', 'fontWeight': '700',
                                                         'color': '#1a237e', 'margin': '0'}),
                            html.P('+2.6 score per extra study hour',
                                   style={'fontSize': '12px', 'color': '#888', 'marginTop': '6px'})
                        ]),
                        html.Div(style={**CARD_STYLE, 'borderTop': '4px solid #2ecc71',
                                        'padding': '18px', 'marginBottom': '0'}, children=[
                            html.P('💡 Attendance Gap',
                                   style={'fontSize': '13px', 'color': '#555', 'marginBottom': '6px'}),
                            html.P('17% gap', style={'fontSize': '22px', 'fontWeight': '700',
                                                      'color': '#1a237e', 'margin': '0'}),
                            html.P('High vs Low attendance placement rate',
                                   style={'fontSize': '12px', 'color': '#888', 'marginTop': '6px'})
                        ]),
                        html.Div(style={**CARD_STYLE, 'borderTop': '4px solid #e74c3c',
                                        'padding': '18px', 'marginBottom': '0'}, children=[
                            html.P('💡 Internet Hurts Performance',
                                   style={'fontSize': '13px', 'color': '#555', 'marginBottom': '6px'}),
                            html.P('r = -0.152', style={'fontSize': '22px', 'fontWeight': '700',
                                                         'color': '#1a237e', 'margin': '0'}),
                            html.P('Only negative predictor in dataset',
                                   style={'fontSize': '12px', 'color': '#888', 'marginTop': '6px'})
                        ]),
                        html.Div(style={**CARD_STYLE, 'borderTop': '4px solid #e67e22',
                                        'padding': '18px', 'marginBottom': '0'}, children=[
                            html.P('💡 Assignments = Placement',
                                   style={'fontSize': '13px', 'color': '#555', 'marginBottom': '6px'}),
                            html.P('27% gap', style={'fontSize': '22px', 'fontWeight': '700',
                                                      'color': '#1a237e', 'margin': '0'}),
                            html.P('Low vs Very High assignment completion',
                                   style={'fontSize': '12px', 'color': '#888', 'marginTop': '6px'})
                        ]),
                        html.Div(style={**CARD_STYLE, 'borderTop': '4px solid #8e44ad',
                                        'padding': '18px', 'marginBottom': '0'}, children=[
                            html.P('💡 Star Student Profile',
                                   style={'fontSize': '13px', 'color': '#555', 'marginBottom': '6px'}),
                            html.P('100% placed', style={'fontSize': '22px', 'fontWeight': '700',
                                                          'color': '#1a237e', 'margin': '0'}),
                            html.P('Study>=8 + Attend>=80% + Internet<=4hrs',
                                   style={'fontSize': '12px', 'color': '#888', 'marginTop': '6px'})
                        ]),
                    ]
                ),

                # CHARTS
                html.P('Placement Overview', style=SECTION_STYLE),
                html.Div(style=CARD_STYLE, children=[dcc.Graph(id='chart-pie')]),

                html.P('Study Hours vs Exam Score', style=SECTION_STYLE),
                html.Div(style=CARD_STYLE, children=[dcc.Graph(id='chart-scatter')]),

                html.P('Variable Distributions', style=SECTION_STYLE),
                html.Div(style=CARD_STYLE, children=[dcc.Graph(id='chart-hist')]),

                html.P('Box Plots — Placed vs Not Placed', style=SECTION_STYLE),
                html.Div(style=CARD_STYLE, children=[dcc.Graph(id='chart-box')]),

                html.P('All Metrics Comparison', style=SECTION_STYLE),
                html.Div(style=CARD_STYLE, children=[dcc.Graph(id='chart-bar')]),

                html.P('Correlation Heatmap', style=SECTION_STYLE),
                html.Div(style=CARD_STYLE, children=[dcc.Graph(id='chart-heat')]),

                # FOOTER
                html.Div(
                    'Student Performance Dashboard | ReadyNest Corp Week 1 | Python · Pandas · Plotly Dash',
                    style={'textAlign': 'center', 'color': '#aaa', 'fontSize': '13px',
                           'padding': '24px 0', 'borderTop': '1px solid #e0e0e0'}
                )
            ]
        )
    ]
)


# ── Callback — all charts + KPIs update when any filter changes ────────────
@app.callback(
    Output('kpi-cards',     'children'),
    Output('chart-pie',     'figure'),
    Output('chart-scatter', 'figure'),
    Output('chart-hist',    'figure'),
    Output('chart-box',     'figure'),
    Output('chart-bar',     'figure'),
    Output('chart-heat',    'figure'),
    Input('filter-placement',  'value'),
    Input('filter-study',      'value'),
    Input('filter-attendance', 'value'),
    Input('filter-score',      'value'),
)
def update_all(placement, study_range, attend_range, score_range):

    # 1. Filter dataset
    filtered = df.copy()
    if placement != 'All':
        filtered = filtered[filtered['placement_status'] == placement]
    filtered = filtered[
        (filtered['study_hours']  >= study_range[0])  &
        (filtered['study_hours']  <= study_range[1])  &
        (filtered['attendance']   >= attend_range[0]) &
        (filtered['attendance']   <= attend_range[1]) &
        (filtered['exam_score']   >= score_range[0])  &
        (filtered['exam_score']   <= score_range[1])
    ]

    n = len(filtered)
    if n == 0:
        empty = go.Figure()
        empty.update_layout(title='No data matches current filters — adjust sliders')
        kpi = [html.P('No data matches filters',
                      style={'color': 'red', 'fontWeight': '600'})]
        return kpi, empty, empty, empty, empty, empty, empty

    placed_pct = (filtered['placement_status'] == 'Placed').mean() * 100
    avg_score  = filtered['exam_score'].mean()
    avg_study  = filtered['study_hours'].mean()

    # 2. KPI Cards
    def kpi_card(title, value, color, suffix=''):
        return html.Div(
            style={**KPI_BOX, 'borderTop': f'4px solid {color}'},
            children=[
                html.P(title, style={'fontSize': '13px', 'color': '#777', 'margin': '0 0 8px'}),
                html.P(f'{value}{suffix}',
                       style={'fontSize': '30px', 'fontWeight': '700',
                              'color': color, 'margin': '0'})
            ]
        )

    kpi_cards = [
        kpi_card('Students Selected', f'{n:,}',            '#3949ab'),
        kpi_card('Placement Rate',    f'{placed_pct:.1f}', '#2ecc71', '%'),
        kpi_card('Avg Exam Score',    f'{avg_score:.1f}',  '#e67e22'),
        kpi_card('Avg Study Hours',   f'{avg_study:.1f}',  '#8e44ad', ' hrs/day'),
    ]

    layout_common = dict(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CHART_BG,
        font=dict(family='Segoe UI, Arial'),
        margin=dict(t=60, b=40, l=40, r=40)
    )

    # 3. Pie Chart
    counts = filtered['placement_status'].value_counts().reset_index()
    counts.columns = ['Status', 'Count']
    fig_pie = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'pie'}, {'type': 'bar'}]],
        subplot_titles=['Placement Ratio', 'Student Count']
    )
    fig_pie.add_trace(go.Pie(
        labels=counts['Status'], values=counts['Count'],
        hole=0.4,
        marker_colors=[COLOR_MAP.get(s, '#aaa') for s in counts['Status']],
        pull=[0.05] * len(counts),
        hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>%{percent}<extra></extra>'
    ), row=1, col=1)
    fig_pie.add_trace(go.Bar(
        x=counts['Status'], y=counts['Count'],
        marker_color=[COLOR_MAP.get(s, '#aaa') for s in counts['Status']],
        text=counts['Count'].apply(lambda x: f'{x:,}'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Count: %{y:,}<extra></extra>'
    ), row=1, col=2)
    fig_pie.update_layout(
        title=f'Placement Breakdown ({n:,} students)',
        title_x=0.5, height=400, showlegend=False, **layout_common
    )

    # 4. Scatter Plot
    fig_scatter = px.scatter(
        filtered, x='study_hours', y='exam_score',
        color='placement_status', color_discrete_map=COLOR_MAP,
        opacity=0.4,
        hover_data=['attendance', 'assignments_completed', 'placement_status'],
        labels={'study_hours': 'Study Hours/Day', 'exam_score': 'Exam Score',
                'placement_status': 'Status'},
        title=f'Study Hours vs Exam Score | r = +0.563 | {n:,} students'
    )
    fig_scatter.update_traces(marker=dict(size=5))
    fig_scatter.update_layout(title_x=0.5, height=480,
                               legend=dict(title='Status'), **layout_common)

    # 5. Histograms
    fig_hist = make_subplots(
        rows=2, cols=4,
        subplot_titles=[c.replace('_', ' ').title() for c in NUMERIC_COLS],
        vertical_spacing=0.18, horizontal_spacing=0.08
    )
    colors_list = ['#4C72B0', '#DD8452', '#55A868', '#C44E52',
                   '#8172B2', '#937860', '#DA8BC3']
    positions = [(1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3)]
    for i, (col, (r, c)) in enumerate(zip(NUMERIC_COLS, positions)):
        fig_hist.add_trace(go.Histogram(
            x=filtered[col], nbinsx=20,
            marker_color=colors_list[i], opacity=0.85,
            showlegend=False, name=col.replace('_', ' ').title(),
            hovertemplate=f'<b>{col}</b><br>Value: %{{x}}<br>Count: %{{y}}<extra></extra>'
        ), row=r, col=c)
    fig_hist.update_layout(
        title=f'Variable Distributions ({n:,} students)',
        title_x=0.5, height=520, **layout_common
    )

    # 6. Box Plots
    fig_box = go.Figure()
    for status, color in COLOR_MAP.items():
        subset = filtered[filtered['placement_status'] == status]
        if len(subset) == 0:
            continue
        for col in NUMERIC_COLS:
            fig_box.add_trace(go.Box(
                y=subset[col], name=status,
                legendgroup=status,
                showlegend=(col == NUMERIC_COLS[0]),
                marker_color=color, boxmean=True,
                x=[col.replace('_', ' ').title()] * len(subset),
                hovertemplate=f'<b>{status}</b><br>%{{x}}: %{{y}}<extra></extra>'
            ))
    fig_box.update_layout(
        title=f'Box Plots — Placed vs Not Placed ({n:,} students)',
        title_x=0.5, boxmode='group', height=500,
        legend=dict(title='Status'), **layout_common
    )

    # 7. Grouped Bar
    group_means = filtered.groupby('placement_status')[NUMERIC_COLS].mean().round(2)
    fig_bar = go.Figure()
    for status, color in COLOR_MAP.items():
        if status not in group_means.index:
            continue
        vals = group_means.loc[status]
        fig_bar.add_trace(go.Bar(
            name=status,
            x=[c.replace('_', ' ').title() for c in NUMERIC_COLS],
            y=vals.values,
            marker_color=color,
            text=[f'{v:.1f}' for v in vals.values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>%{name}: %{y:.2f}<extra></extra>'
        ))
    fig_bar.update_layout(
        title=f'All Metrics — Placed vs Not Placed ({n:,} students)',
        title_x=0.5, barmode='group', height=480,
        legend=dict(title='Status'), **layout_common
    )

    # 8. Heatmap
    corr = filtered[NUMERIC_COLS].corr().round(3)
    clean = [c.replace('_', ' ').title() for c in NUMERIC_COLS]
    fig_heat = go.Figure(data=go.Heatmap(
        z=corr.values, x=clean, y=clean,
        colorscale='RdBu', zmid=0, zmin=-1, zmax=1,
        text=corr.values.round(2),
        texttemplate='%{text}',
        textfont={'size': 11},
        hovertemplate='<b>%{y} vs %{x}</b><br>r = %{z:.3f}<extra></extra>',
        colorbar=dict(title='r')
    ))
    fig_heat.update_layout(
        title=f'Correlation Heatmap ({n:,} students)',
        title_x=0.5, height=520,
        xaxis=dict(tickangle=-30), **layout_common
    )

    return (kpi_cards, fig_pie, fig_scatter,
            fig_hist, fig_box, fig_bar, fig_heat)


# ── Run ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=8050)