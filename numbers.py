

class AccurateNumber:
    def __init__(self, values, powers, error):
        if len(values) != len(powers):
            return
        for i in range(len(values)):
            if type(values[i]) is not int: return
            if type(powers[i]) is not int: return
            if abs(values[i]) >= 10**19: return

        self.values = values
        self.powers = powers
        self.error = error

    # 10^19 is max power of 10 for a thing

    def __str__(self):
        final = ""
        addedpt = False

        for i in range(len(self.values)):
            piece = str(self.values[i])
            if self.powers[i]<0 and -self.powers[i]<len(piece):
                splitpt = len(piece)+self.powers[i]
                piece = piece[:splitpt] + "." + piece[splitpt:]
                addedpt = True
            elif self.powers[i]<0 and not addedpt:
                piece = "0."+"0"*(-self.powers[i]-len(piece))+piece
                addedpt = True
            elif self.powers[i]==len(piece) and i+1<len(self.values):
                piece += "."
                addedpt = True

            final += piece

        print(self.values[0] * (10 ** self.powers[0]))

        return final #str(self.values[0] * (10 ** self.powers[0]))

x = AccurateNumber([12345,6789],[5,-4],5)

print(x)