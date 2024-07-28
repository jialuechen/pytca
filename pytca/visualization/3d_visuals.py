import plotly.graph_objs as go

def plot_3d_surface(data):
    fig = go.Figure(data=[go.Surface(z=data)])
    fig.update_layout(title='3D Surface Plot', autosize=False,
                      width=800, height=800,
                      margin=dict(l=65, r=50, b=65, t=90))
    fig.show()
