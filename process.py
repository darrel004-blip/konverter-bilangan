hexa_dict = {
    10:"A",
    11:"B",
    12:"C",
    13:"D",
    14:"E",
    15:"F"
}

reversed_hexa_dict = {
    "A":10,
    "B":11,
    "C":12,
    "D":13,
    "E":14,
    "F":15
}

def fill_bit_binary(string):
    return (8-len(string))*"0"+string

def hexa_convert(num):
    if (num>9): return hexa_dict[num]
    else: return str(num)

def hexa_revert(val):
    if (val in reversed_hexa_dict): return reversed_hexa_dict[val]
    else: return int(val)

# decimal_base
class Decimal():
    def __init__(self, raw):
        self.raw = str(raw)
        self.decimal = self.raw.split(".")

    def check_input(self):
        # check if the input is singular or in form of ip address
        if (len(self.decimal)!=1 and len(self.decimal)!=4): return False
        for slice in self.decimal:
            # check if the input only contains digit
            if (not slice.isdecimal()): return False 

            # check if the input is in 8-bit capacity
            if (not (int(slice)>=0)) or (not (int(slice)<=255)): return False

        return True
            
    def to_binary(self,decimal):
        if (decimal<2): return str(decimal)
        else: return self.to_binary(decimal//2)+str(decimal%2)

    def to_octal(self,decimal):
        if (decimal<8): return str(decimal)
        else: return self.to_octal(decimal//8)+str(decimal%8)

    def to_hexadecimal(self,decimal):
        if (decimal<16): return hexa_convert(decimal%16)
        else: return self.to_hexadecimal(decimal//16)+hexa_convert(decimal%16)

    def output(self):
        if (self.check_input()):
            binary = octal = hexadecimal = str()
            for index, octet in enumerate(self.decimal):
                octet = int(octet)
                if (index!=0):
                    binary+="."
                    octal+="."
                    hexadecimal+="."
                binary += fill_bit_binary(self.to_binary(octet))
                octal += self.to_octal(octet)
                hexadecimal += self.to_hexadecimal(octet)
            return [
                {"basis": "Biner", "hasil": binary},
                {"basis": "Oktal", "hasil": octal},
                {"basis": "Heksadesimal", "hasil": hexadecimal}
            ]
        else:
            return []
# binary_base
class Binary():
    def __init__(self, raw):
        self.raw = str(raw)
        self.binary = self.raw.split(".")
    
    def check_input(self):
        # check if the input is singular or in form of ip address
        if (len(self.binary)!=1 and len(self.binary)!=4): return False
        for slice in self.binary:
            # check if the input only contains digit
            if (not slice.isdecimal()): return False 

            # check if the input is in fixed 8-bit capacity
            if (len(slice)!=8): return False

            # check if the input only contains 0 and 1
            for digit in slice:
                if (digit!="0" and digit!="1"): return False

        return True
     
    def to_decimal(self,binary):
        total = 0
        for power, bit in enumerate(reversed(binary)):
            total += int(bit)*(2**power)
        return str(total)

    def to_octal(self,binary):
        result=[0]*3
        for power, bit in enumerate(reversed(binary)):
            result[len(result)-(power//3)-1] += int(bit)*(2**(power%3))
        return str(int("".join(map(str,result))))

    def to_hexadecimal(self,binary):
        result=[0]*2
        for power, bit in enumerate(reversed(binary)):
            result[len(result)-(power//4)-1] += int(bit)*(2**(power%4))
        result = [hexa_convert(val) for val in result]
        return ("".join(result)).lstrip("0") or "0"

    def output(self):
        if (self.check_input()):
            decimal = octal = hexadecimal = str()
            for index, octet in enumerate(self.binary):
                if (index!=0):
                    decimal+="."
                    octal+="."
                    hexadecimal+="."
                decimal += self.to_decimal(octet)
                octal += self.to_octal(octet)
                hexadecimal += self.to_hexadecimal(octet)
            return [
                {"basis": "Desimal", "hasil": decimal},
                {"basis": "Oktal", "hasil": octal},
                {"basis": "Heksadesimal", "hasil": hexadecimal}
            ]
        else:
            return []
# octal_base
class Octal():
    def __init__(self, raw):
        self.raw = str(raw)
        self.octal = self.raw.split(".")
    
    def check_input(self):
        # check if the input is singular or in form of ip address
        if (len(self.octal)!=1 and len(self.octal)!=4): return False
        for slice in self.octal:
            # check if the input only contains digit
            if (not slice.isdecimal()): return False 

            # check if the input is in 8-bit capacity
            if (not (int(slice)>=0)) or (not (int(slice)<=377)): return False

            # check if the input only contains number 0-7
            for digit in slice:
                if (int(digit)>7): return False

        return True
     
    def to_decimal(self,octal):
        total = 0
        for power, bit in enumerate(reversed(octal)):
            total += int(bit)*(8**power)
        return str(total)

    def to_binary(self,octal):
        binary=""
        for split in octal:
            num = int(split)
            temp = ""
            for i in range(3):
                temp += str(num%2)
                num //= 2
            binary+=temp[::-1]
        binary = fill_bit_binary(binary)
        if (len(binary)>8): binary=binary[1:] # we know that it will reach 9 digit in its maximum value and it is also guaranteed that the first digit is 0 if it is 9-digit binary which means we can just remove it.
        self.temp_binary=binary
        return binary

    def to_hexadecimal(self,binary):
        result=[0]*2
        for power, bit in enumerate(reversed(binary)):
            result[len(result)-(power//4)-1] += int(bit)*(2**(power%4))
        result = [hexa_convert(val) for val in result]
        return ("".join(result)).lstrip("0") or "0"

    def output(self):
        if (self.check_input()):
            decimal = binary = hexadecimal = str()
            for index, octet in enumerate(self.octal):
                octet = octet.lstrip("0") or "0"
                if (index!=0):
                    decimal+="."
                    binary+="."
                    hexadecimal+="."
                decimal += self.to_decimal(octet)
                binary += self.to_binary(octet)
                hexadecimal += self.to_hexadecimal(self.temp_binary)
            return [
                {"basis": "Desimal", "hasil": decimal},
                {"basis": "Biner", "hasil": binary},
                {"basis": "Heksadesimal", "hasil": hexadecimal}
            ]
        else:
            return []
# hexadecimal_base
class HexaDecimal():
    def __init__(self, raw):
        self.raw = str(raw).upper()
        self.hexadecimal = self.raw.split(".")
    
    def check_input(self):
        # check if the input is singular or in form of ip address
        if (len(self.hexadecimal)!=1 and len(self.hexadecimal)!=4): return False
        for slice in self.hexadecimal:
            # check if the input is not a blank space
            if not slice: return False

            # remove leading zero from slice
            slice = slice.lstrip("0") or "0"

            # check if the input only contains suitable digit and char 
            for char in slice:
                if (not char.isdigit()):
                    if not (char in hexa_dict.values()): return False

            # check if the input is in 8-bit capacity
            if (len(slice)>2): return False

        return True
     
    def to_decimal(self,hexadecimal):
        total = 0
        for power, bit in enumerate(reversed(hexadecimal)):
            total += int(bit)*(16**power)
        return str(total)

    def to_binary(self,hexadecimal):
        binary=""
        for split in hexadecimal:
            num = int(split)
            temp = ""
            for i in range(4):
                temp += str(num%2)
                num //= 2
            binary+=temp[::-1]
        binary = fill_bit_binary(binary)
        self.temp_binary=binary
        return binary

    def to_octal(self,binary):
        result=[0]*3
        for power, bit in enumerate(reversed(binary)):
            result[len(result)-(power//3)-1] += int(bit)*(2**(power%3))
        result = [hexa_convert(val) for val in result]
        return ("".join(result)).lstrip("0") or "0"

    def output(self):
        if (self.check_input()):
            decimal = binary = octal = str()
            for index, octet in enumerate(self.hexadecimal):
                octet = octet.lstrip("0") or "0"
                self.hexa_reverted = [hexa_revert(i) for i in octet]
                if (index!=0):
                    decimal+="."
                    binary+="."
                    octal+="."
                decimal += self.to_decimal(self.hexa_reverted)
                binary += self.to_binary(self.hexa_reverted)
                octal += self.to_octal(self.temp_binary)
            return [
                {"basis": "Desimal", "hasil": decimal},
                {"basis": "Biner", "hasil": binary},
                {"basis": "Oktal", "hasil": octal}
            ]
        else:
            return []