class CUPROJ:
    CARAVEL = 0
    CARAVAN = 1
    OPENFRAME = 2
    num_of_pins = [38, 38, 50]

    def __init__(self, name, type=CARAVEL):
        self.name = name
        self.type = type
        self.design = None
        self.pimap = None

    def add_design(self, design, pinmap):
        self.design = design
        self.validate_pinmap(pinmap)
        self.pinmap = pinmap

    def validate_pinmap(self, pinmap):
        for p in pinmap:
            (mod, pin, ios) = p
            found = False
            for pp in self.design.pins:
                (dmod, dpin, ddir, dsz) = pp
                if dmod == mod and dpin == pin:
                    found = True
            if not found:
                raise Exception(f"Pinmap issue: Pin {mod}/{pin} not found")
        return True
        
    def print(self):
        pass