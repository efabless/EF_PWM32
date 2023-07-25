class CUPROJ:
    CARAVEL = 0
    CARAVAN = 1
    OPENFRAME = 2
    num_of_pins = [38, 38, 44]

    def __init__(self, name, type=CARAVEL):
        self.name = name
        if type not in range(3):
            raise Exception(f"Invalid chip type: {type}")
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