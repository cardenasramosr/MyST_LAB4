import data, functions, visualizations

def descarga_de_datos(ticker):
    """
    descarga_de_datos: devuelve el libro de órdenes para la criptomoneda ingresada a través de la paquetería de ccxt.
    
    *ticker: símbolo de la criptomoneda.
    
    """
    
    datos, avance = data.criptoactivo(ticker)
    
    return datos, avance

def microestructura_visuales(datos, ticker):
    """
    microestructura_visuales: devuelve series temporales y sus visuales con las características del libro de órdenes.
    
    *datos: libro de órdenes.
    *ticker: símbolo de la criptomoneda
    
    """
    microestructura_datos = functions.microestructura(datos)
    level, ask_v, bid_v, total_v, mid_p, vwap = visualizations.graficos_plotly(microestructura_datos, ticker)
    
    return microestructura_datos, level, ask_v, bid_v, total_v, mid_p, vwap

def microestructura_modelado(avance):
    """
    microestructura_visuales: modelo de Roll.
    
    *avance: libro de órdenes.
    
    """
    
    return functions.modelado(avance)
