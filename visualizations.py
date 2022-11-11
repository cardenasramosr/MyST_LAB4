import plotly.graph_objects as go
from plotly.subplots import make_subplots

def graficos_plotly(datos, ticker):
    
    level = make_subplots(specs=[[{"secondary_y": False}]])
    ask_v = make_subplots(specs=[[{"secondary_y": False}]])
    bid_v = make_subplots(specs=[[{"secondary_y": False}]])
    total_v = make_subplots(specs=[[{"secondary_y": False}]])
    mid_p = make_subplots(specs=[[{"secondary_y": False}]])
    vwap = make_subplots(specs=[[{"secondary_y": False}]])
    
    for proveedor in list(datos.keys()):
        level.add_trace(go.Scatter(x = datos[proveedor].index, y = datos[proveedor]["Level"], name = proveedor), 
                       secondary_y = False,)
        level.update_layout(title = "Level: " + ticker,  yaxis_title = "Niveles", xaxis_title = "Fecha")
        
        ask_v.add_trace(go.Scatter(x = datos[proveedor].index, y = datos[proveedor]["Ask Volume"], name = proveedor), 
                       secondary_y = False,)
        ask_v.update_layout(title = "Ask Volume: " + ticker,  yaxis_title = "Volumen", xaxis_title = "Fecha")
        
        bid_v.add_trace(go.Scatter(x = datos[proveedor].index, y = datos[proveedor]["Bid Volume"], name = proveedor), 
                       secondary_y = False,)
        bid_v.update_layout(title = "Bid Volume: " + ticker,  yaxis_title = "Volumen", xaxis_title = "Fecha")
        
        total_v.add_trace(go.Scatter(x = datos[proveedor].index, y = datos[proveedor]["Total Volume"], name = proveedor), 
                       secondary_y = False,)
        total_v.update_layout(title = "Total Volume: " + ticker,  yaxis_title = "Volumen", xaxis_title = "Fecha")
        
        mid_p.add_trace(go.Scatter(x = datos[proveedor].index, y = datos[proveedor]["Mid Price"], name = proveedor), 
                       secondary_y = False,)
        mid_p.update_layout(title = "Mid Price: " + ticker,  yaxis_title = "Precio Dólares", xaxis_title = "Fecha")
        
        vwap.add_trace(go.Scatter(x = datos[proveedor].index, y = datos[proveedor]["VWAP"], name = proveedor), 
                       secondary_y = False,)
        vwap.update_layout(title = "VWAP: " + ticker,  yaxis_title = "Precio Dólares", xaxis_title = "Fecha")
        
    
    return level, ask_v, bid_v, total_v, mid_p, vwap
