class Filtrar_ruido:
    
    def __init__(self, mea_e, est_e, q = 0.01): # Constructor se debe de saber el valor de R0       
      # Datos de estimador Kalman
      self._err_measure =mea_e;
      self._err_estimate=est_e;
      self._q = q;
      self._last_estimate = 0
      self._kalman_gain = 0
      self._current_estimate = 0
      
      # Datos Pasabajas
      self.Z = 0
      
      # Datos EMA
      self.alpha = 0.05
      self.S = 0    
          
    # Filtro pasa bajas de Butterworth Fc= 60Hz
    def Pasa_bajas_fc60(self,mea):
        self.Y = mea
        self.Z = 0.963*self.Z + 0.037*self.Y;
        return self.Z
    
    #Filtro Media Movil Exponencial
    def EMA(self,mea):
        self.Y = mea
        self.S = (self.alpha * self.Y) + ((1 - self.alpha) * self.S);   
        return self.S
        
    # Estimador de Kalman, "no es un filtro"
    def Estimador_Kalman(self,mea):
      self._kalman_gain = self._err_estimate/(self._err_estimate + self._err_measure);
      self._current_estimate = self._last_estimate + self._kalman_gain * (mea - self._last_estimate);
      # Estas variables se necesitan guardar
      self._err_estimate = (1.0 - self._kalman_gain) * self._err_estimate + abs(self._last_estimate - self._current_estimate)* self._q;
      self._last_estimate = self._current_estimate;
      return self._current_estimate 
     
    def setMeasurementError(self, mea_e ):  
      self._err_measure=mea_e;

    def setEstimateError(self, est_e ):
      self._err_estimate=est_e

    def setProcessNoise(self, q ):
      self._q=q

    def getKalmanGain(self):
      return _kalman_gain

    def getEstimateError(self):
      return _err_estimate