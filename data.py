import ccxt, datetime, numpy as np, pandas as pd, time 

def criptoactivo(ticker):
    
    def conexion_ccxt(conexion):
        
        if conexion == "kraken":
            proveedor = ccxt.kraken()
        
        elif conexion == "ftx":
            proveedor = ccxt.ftx()
        
        else:
            proveedor = ccxt.cex()
        
        return proveedor
    
    def descarga(ticker, proveedor):
        datos = {i : {} for i in proveedor}
        conexion1, conexion2, conexion3 = conexion_ccxt(proveedor[0]), conexion_ccxt(proveedor[1]), conexion_ccxt(proveedor[2]) 
        
        for i in range(60):
            try:
                temp = pd.to_datetime(datetime.datetime.now())
                try:
                    libro_ordenes_1 = conexion1.fetch_order_book(ticker)
                    precios_1 = conexion1.fetch_ohlcv(ticker, timeframe = "1m", limit = 1)
                except:
                    pass
                try:
                    libro_ordenes_2 = conexion2.fetch_order_book(ticker)
                    precios_2 = conexion2.fetch_ohlcv(ticker, timeframe = "1m", limit = 1)
                except:
                    pass
                try:
                    libro_ordenes_3 = conexion3.fetch_order_book(ticker)
                    precios_3 = conexion3.fetch_ohlcv(ticker, timeframe = "1m", limit = 1)
                except:
                    pass
                
                temp_dict = {"libro_ordenes" : libro_ordenes_1, 
                                 "precios" : precios_1} 
                datos[proveedor[0]][temp] = temp_dict 
                temp_dict = {"libro_ordenes" : libro_ordenes_2, 
                                 "precios" : precios_2} 
                datos[proveedor[1]][temp] = temp_dict 
                temp_dict = {"libro_ordenes" : libro_ordenes_3, 
                                 "precios" : precios_3} 
                datos[proveedor[2]][temp] = temp_dict 
                
            except:
                pass
            
            time.sleep(60)

        return datos
    
    def seccion1(datos):
        
        avance = {}
        for proveedor in list(datos.keys()):
            avance[proveedor] = {}
            for temp in list(datos[proveedor].keys()):
                ask = datos[proveedor][temp]["libro_ordenes"]["asks"][0][0]
                bid = datos[proveedor][temp]["libro_ordenes"]["bids"][0][0]
                ask_volume = datos[proveedor][temp]["libro_ordenes"]["asks"][0][1]
                bid_volume = datos[proveedor][temp]["libro_ordenes"]["bids"][0][1]
                spread = ask - bid
                try:
                    close_price = datos[proveedor][temp]["precios"][0][4]
                except:
                    close_price = 0.5 * (ask + bid)
                temp_dict = {"Ask" : ask, "Bid" : bid, 
                             "Ask_Volume" : ask_volume, "Bid_Volume" : bid_volume, 
                             "Spread" : spread, "Close_Price" : close_price}
                avance[proveedor][temp] = temp_dict
                
        return avance
    
    proveedores = ["kraken", "ftx", "cex"]
    datos = descarga(ticker, proveedores)
    avance = seccion1(datos)
        
    return datos, avance
