import ccxt, datetime, numpy as np, pandas as pd, time 

def microestructura(datos):
    
    microestructura_datos = {}
    
    for proveedor in list(datos.keys()):
        dataFrame = pd.DataFrame(index = list(datos[proveedor].keys()), 
                                 columns = ["Level", "Ask Volume", "Bid Volume", "Total Volume",
                                            "Mid Price", "VWAP"])
        dataFrame.index.name = "Timestamp"
        
        for temp in list(datos[proveedor].keys()):
            dataFrame.loc[temp, "Level"] = sum([1 for i in datos[proveedor][temp]["libro_ordenes"]["asks"]])
            dataFrame.loc[temp, "Ask Volume"] = sum(list(map(lambda x : x[1], 
                                                             datos[proveedor][temp]["libro_ordenes"]["asks"])))
            dataFrame.loc[temp, "Bid Volume"] = sum(list(map(lambda x : x[1], 
                                                             datos[proveedor][temp]["libro_ordenes"]["bids"])))
            dataFrame.loc[temp, "Total Volume"] = dataFrame.loc[temp, "Bid Volume"] +  dataFrame.loc[temp, "Ask Volume"]
            dataFrame.loc[temp, "Mid Price"] = 0.5 * (datos[proveedor][temp]["libro_ordenes"]["asks"][0][0] + 
                                                     datos[proveedor][temp]["libro_ordenes"]["bids"][0][0])
            ask_w = np.array(list(map(lambda x : x[0], datos[proveedor][temp]["libro_ordenes"]["asks"]))) * np.array(list(map(lambda x : x[1], datos[proveedor][temp]["libro_ordenes"]["asks"])))
            bid_w = np.array(list(map(lambda x : x[0], datos[proveedor][temp]["libro_ordenes"]["bids"]))) * np.array(list(map(lambda x : x[1], datos[proveedor][temp]["libro_ordenes"]["bids"])))
            dataFrame.loc[temp, "VWAP"] = (sum(ask_w) + sum(bid_w)) / (dataFrame.loc[temp, "Total Volume"])
        
        microestructura_datos[proveedor] = dataFrame
    
    return microestructura_datos

def modelado(avance):
   
    modelado_microestructura = {}

    for proveedor in list(avance.keys()):
        modelo_df = pd.DataFrame(index = list(avance[proveedor].keys()), columns = ["Close", "Spread", "Effective Spread"])
        modelo_df.index.name = "timeStamp"
    
        for i in range(len(modelo_df)):
            modelo_df.loc[modelo_df.index[i], "Close"] = avance[proveedor][modelo_df.index[i]]["Close_Price"]
            modelo_df.loc[modelo_df.index[i], "Spread"] = avance[proveedor][modelo_df.index[i]]["Spread"]
        
        modelo_df.loc[:, "Diferencia"] = [np.nan] + list(np.diff(modelo_df.loc[:, "Close"]))
        modelado_microestructura[proveedor] = modelo_df
        
        for proveedor in list(modelado_microestructura.keys()):
            idx, j = 10, 0
            for i in range(len(modelado_microestructura[proveedor]) - 10):
                covarianza = np.cov(modelado_microestructura[proveedor].iloc[j + 1 : idx + j - 4, 3], 
                        modelado_microestructura[proveedor].iloc[idx + j - 4: idx + j + 1, 3])
                modelado_microestructura[proveedor].iloc[idx + j, 2] = 2 * np.sqrt(abs(covarianza[0, 1]))
                j += 1
                
    return modelado_microestructura

