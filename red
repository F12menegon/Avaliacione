def updateColor ():
    global red, green, blue
    
    red = 255    # Máximo de Vermelho
    green = 0    # Sem Verde
    blue = 0     # Sem Azul

    fillColor("led", red, green, blue)
    setDeviceProperty(getName(), "red", red)
    setDeviceProperty(getName(), "green", green)
    setDeviceProperty(getName(), "blue", blue)
