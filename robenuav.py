def readlatlong(path):
    with open(path) as f:
        if not next(f).startswith("n,lat,long"):
            return print("File not supported (must be n,lat,long)")
        
        cords = []
        for line in f:
            line = line.split(",")
            cords.append([float(line[0]), float(line[1])])
        
        return cords
