# File contains implementation of the secret code generating algorithms
# See main.py or examples.ipynb for example usage

import random

def list_to_str(arr):
    """Converts a list of charaters to a string

    Args:
        arr (list of chrs): List of characters.

    Returns:
        str: Returns string where all elements of list are joined together.
    """

    return "".join(arr)

def read_from_file(file_name):
    """Reads codes from file

    Args:
        file_name (str): Name of file to read from.

    Returns:
        list of strs: Returns list of codes read from specified file.
    """

    codes = []

    file = open(file_name, "r")

    lines = file.readlines()

    for l in lines:

        codes.append(l.strip())

    file.close()

    return codes

class SCSA:
    """Secret-code selection algorithm
    """

    def __init__(self):
        """Constructor for SCSA
        """

        self.name = ""

    def generate_codes(self, length, colors, num_codes = 1):
        """Generate codes based on secret-code selection algorithm

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list of chrs): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Raises:
            NotImplementedError: Function must be implemented by children classes.
        """

        raise NotImplementedError

    def write_to_file(self, codes, length, num_colors):
        """Writes codes to a file

        Args:
            codes (list of strs): List of codes to write to file.
            length (int): The length of the generated codes (same as number of pegs for an instance of Mastermind).
            num_colors (int): Number of colors that could be used to generate a code (i.e. length of list of colors).
        """

        file_name = self.name + "_" + str(length) + "_" + str(num_colors) + ".txt"

        file = open(file_name, "w")

        for code in codes:

            file.write(code + "\n")

        file.close()

        return

    def generate_and_write_to_file(self, length, colors, num_codes = 100):
        """Generates codes and writes them to a file

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list of chrs): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 100.
        """

        codes = self.generate_codes(length, colors, num_codes)

        if num_codes == 1:

            codes = [codes]

        self.write_to_file(codes, length, len(colors))

        return


class InsertColors(SCSA):
    """ SCSA that generates codes containing colors selected at random
    """

    def __init__(self):
        """Constructor for InsertColors
        """

        self.name = "InsertColors"

    def generate_codes(self, length, colors, num_codes = 1):
        """Generate codes based on InsertColors SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list of chrs): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            str or list of strs: Returns code(s) generated from SCSA. Return type is list of strs if num_codes > 1, otherwise it is a str.
        """

        if len(colors) < 1:

            return

        if num_codes == 1:

            codes = list_to_str(random.choices(colors, k = length))

        else:

            codes = []

            for _ in range(num_codes):

                codes.append(list_to_str(random.choices(colors, k = length))) 
        
        return codes


class TwoColor(SCSA):
    """ SCSA that generates codes containing only two randomly chosen colors
    """

    def __init__(self):
        """Constructor for TwoColor
        """

        self.name = "TwoColor"

    def generate_codes(self, length, colors, num_codes = 1):
        """Generate codes based on TwoColor SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list of chrs): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            str or list of strs: Returns code(s) generated from SCSA. Return type is list of strs if num_codes > 1, otherwise it is a str.
        """

        if len(colors) < 2:

            return

        if num_codes == 1:

            usable_colors = random.sample(colors, k=2)

            # Create 'uninitialized' code as list
            codes = [0]*length

            # Randomly pick two spots in string
            indicies = random.sample(range(0,length), k=2)

            # Set those two spots in the string to the two colors
            # This guarantees both colors are used at least once
            codes[indicies[0]] = usable_colors[0]
            codes[indicies[1]] = usable_colors[1]

            # Set rest of spots in code to one of the two colors randomly
            for i in range(length):

                if codes[i] == 0:

                    codes[i] = random.choice(usable_colors)

            codes = list_to_str(codes)

        else:

            codes = []

            for _ in range(num_codes):

                usable_colors = random.sample(colors, k=2)

                # Create 'uninitialized' code as list
                code = [0]*length

                # Randomly pick two spots in string
                indicies = random.sample(range(0,length), k=2)

                # Set those two spots in the string to the two colors
                # This guarantees both colors are used at least once
                code[indicies[0]] = usable_colors[0]
                code[indicies[1]] = usable_colors[1]

                # Set rest of spots in code to one of the two colors randomly
                for i in range(length):

                    if code[i] == 0:

                        code[i] = random.choice(usable_colors)

                codes.append(list_to_str(code))
                
        return codes


class ABColor(SCSA):
    """ SCSA that generates codes containing only "A"s and "B"s
    """

    def __init__(self):
        """Constructor for ABColor
        """

        self.name = "ABColor"

    def generate_codes(self, length, colors, num_codes = 1):
        """Generate codes based on ABColor SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list of chrs): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            str or list of strs: Returns code(s) generated from SCSA. Return type is list of strs if num_codes > 1, otherwise it is a str.
        """

        usable_colors = ["A", "B"]

        if num_codes == 1:

            # Create 'uninitialized' code as list
            codes = [0]*length

            # Randomly pick two spots in string
            indicies = random.sample(range(0,length), k=2)

            # Set those two spots in the string to the two colors
            # This guarantees both colors are used at least once
            codes[indicies[0]] = usable_colors[0]
            codes[indicies[1]] = usable_colors[1]

            # Set rest of spots in code to one of the two colors randomly
            for i in range(length):

                if codes[i] == 0:

                    codes[i] = random.choice(usable_colors)

            codes = list_to_str(codes)

        else:

            codes = []

            for _ in range(num_codes):

                # Create 'uninitialized' code as list
                code = [0]*length

                # Randomly pick two spots in string
                indicies = random.sample(range(0,length), k=2)

                # Set those two spots in the string to the two colors
                # This guarantees both colors are used at least once
                code[indicies[0]] = usable_colors[0]
                code[indicies[1]] = usable_colors[1]

                # Set rest of spots in code to one of the two colors randomly
                for i in range(length):

                    if code[i] == 0:

                        code[i] = random.choice(usable_colors)

                codes.append(list_to_str(code))
                
        return codes


class TwoColorAlternating(SCSA):
    """ SCSA that generates codes that alternate between two colors
    """

    def __init__(self):
        """Constructor for TwoColorAlternating
        """

        self.name = "TwoColorAlternating"

    def generate_codes(self, length, colors, num_codes = 1):
        """Generate codes based on TwoColorAlternating SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list of chrs): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            str or list of strs: Returns code(s) generated from SCSA. Return type is list of strs if num_codes > 1, otherwise it is a str.
        """

        if len(colors) < 2:

            return

        if num_codes == 1:

            first_color, second_color = list_to_str(random.sample(colors, k = 2))

            codes = ""

            for i in range(length):

                if i % 2 == 0:

                    codes += first_color

                else:

                    codes += second_color

        else:

            codes = []

            for _ in range(num_codes):

                first_color, second_color = random.sample(colors, k = 2)

                code = ""

                for i in range(length):

                    if i % 2 == 0:

                        code += first_color

                    else:

                        code += second_color

                codes.append(code)
                
        return codes

class OnlyOnce(SCSA):
    """ SCSA that generates codes in which a color appears at most once
    """

    def __init__(self):
        """Constructor for OnlyOnce
        """

        self.name = "OnlyOnce"

    def generate_codes(self, length, colors, num_codes = 1):
        """Generate codes based on OnlyOnce SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list of chrs): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            str or list of strs: Returns code(s) generated from SCSA. Return type is list of strs if num_codes > 1, otherwise it is a str.
        """

        if len(colors) < length:

            return

        if num_codes == 1:

            codes = list_to_str(random.sample(colors, k = length))

        else:

            codes = []

            for _ in range(num_codes):

                codes.append(list_to_str(random.sample(colors, k = length))) 
                    
        return codes


class FirstLast(SCSA):
    """ SCSA that generates codes in which the first and last colors are the same
    """

    def __init__(self):
        """Constructor for FirstLast
        """

        self.name = "FirstLast"

    def generate_codes(self, length, colors, num_codes = 1):
        """Generate codes based on FirstLast SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list of chrs): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            str or list of strs: Returns code(s) generated from SCSA. Return type is list of strs if num_codes > 1, otherwise it is a str.
        """

        if len(colors) < 1:

            return

        if num_codes == 1:

            codes = random.choices(colors, k = length-2)
            color = random.choices(colors, k = 1)

            codes.insert(0, color[0])
            codes.append(color[0])

            codes = list_to_str(codes)

        else:

            codes = []

            for _ in range(num_codes):

                code = random.choices(colors, k = length-2)
                color = random.choices(colors, k = 1)

                code.insert(0, color[0])
                code.append(color[0])

                code = list_to_str(code)

                codes.append(code) 
                
        return codes

class UsuallyFewer(SCSA):
    """ SCSA that generates codes that usually has fewer (2 or 3) colors
    """

    def __init__(self):
        """Constructor for UsuallyFewer
        """

        self.name = "UsuallyFewer"

    def generate_codes(self, length, colors, num_codes = 1):
        """Generate codes based on UsuallyFewer SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list of chrs): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            str or list of strs: Returns code(s) generated from SCSA. Return type is list of strs if num_codes > 1, otherwise it is a str.
        """

        if len(colors) < 3:

            return

        if num_codes == 1:

            probability = random.randint(0,100)

            if probability < 90:

                num = random.randint(2,3)

                picked_colors = random.sample(colors, k = num)

            else:

                picked_colors = colors

            codes = list_to_str(random.choices(picked_colors, k = length))

        else:

            codes = []

            for _ in range(num_codes):

                probability = random.randint(0,100)

                if probability < 90:

                    num = random.randint(2,3)

                    picked_colors = random.sample(colors, k = num)

                else:

                    picked_colors = colors

                code = list_to_str(random.choices(picked_colors, k = length))

                codes.append(code) 
                
        return codes


class PreferFewer(SCSA):
    """ SCSA that generates codes with a preference for fewer colors
    """
    
    def __init__(self):
        """Constructor for PreferFewer
        """

        self.name = "PreferFewer"

    def generate_codes(self, length, colors, num_codes = 1):
        """Generate codes based on PreferFewer SCSA

        Args:
            length (int): The length of the code to be generated (same as number of pegs for an instance of Mastermind).
            colors (list of chrs): All possible colors that can be used to generate a code.
            num_codes (int, optional): Number of codes to generate. Defaults to 1.

        Returns:
            str or list of strs: Returns code(s) generated from SCSA. Return type is list of strs if num_codes > 1, otherwise it is a str.
        """

        if len(colors) < 2:

            return

        if num_codes == 1:

            probability = random.randint(0,100)

            if probability <= 49:

                num = 1

                picked_colors = random.sample(colors, k = num)


            elif probability <= 74:

                num = 2

                picked_colors = random.sample(colors, k = num)


            elif probability <= 87:

                num = min(3, len(colors))

                picked_colors = random.sample(colors, k = num)

            elif probability <= 95:

                num = min(4, len(colors))

                picked_colors = random.sample(colors, k = num)

            elif probability <= 98: 

                num = min(5, len(colors))

                picked_colors = random.sample(colors, k = num)

            else:

                picked_colors = colors

            codes = list_to_str(random.choices(picked_colors, k = length))

        else:

            codes = []

            for _ in range(num_codes):

                probability = random.randint(0,100)

                if probability <= 49:

                    num = 1

                    picked_colors = random.sample(colors, k = num)


                elif probability <= 74:

                    num = 2

                    picked_colors = random.sample(colors, k = num)


                elif probability <= 87:

                    num = min(3, len(colors))

                    picked_colors = random.sample(colors, k = num)

                elif probability <= 95:

                    num = min(4, len(colors))

                    picked_colors = random.sample(colors, k = num)

                elif probability <= 98: 

                    num = min(5, len(colors))

                    picked_colors = random.sample(colors, k = num)

                else:

                    picked_colors = colors

                code = list_to_str(random.choices(picked_colors, k = length))

                codes.append(code) 
                
        return codes