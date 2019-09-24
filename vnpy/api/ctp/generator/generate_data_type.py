""""""

TYPE_CPP2PY = {
    "int": "int",
    "char": "char",
    "double": "double",
    "short": "int",
}


class DataTypeGenerator:
    """DataType builder """

    def __init__(self, filename: str, prefix: str):
        """Constructor"""
        self.filename = filename
        self.prefix = prefix

    def run(self):
        """ the main function """
        self.f_cpp = open(self.filename, "r")
        self.f_define = open(f"{self.prefix}_constant.py", "w")
        self.f_typedef = open(f"{self.prefix}_typedef.py", "w")

        for line in self.f_cpp:
            self.process_line(line)

        self.f_cpp.close()
        self.f_define.close()
        self.f_typedef.close()

        print("DataType completed generating ")

    def process_line(self, line: str):
        """ each processing line """
        line = line.replace("\n", "")
        line = line.replace(";", "")

        if line.startswith("#define"):
            self.process_define(line)
        elif line.startswith("typedef"):
            self.process_typedef(line)

    def process_define(self, line: str):
        """ deal with constant defines """
        words = line.split(" ")
        words = [word for word in words if word]
        if len(words) < 3:
            return

        name = words[1]
        value = words[2]

        new_line = f"{name} = {value}\n"
        self.f_define.write(new_line)

    def process_typedef(self, line: str):
        """ processing type definition """
        words = line.split(" ")
        words = [word for word in words if word != " "]

        name = words[2]
        typedef = TYPE_CPP2PY[words[1]]

        if typedef == "char":
            if "[" in name:
                typedef = "string"
                name = name[:name.index("[")]

        new_line = f"{name} = \"{typedef}\"\n"
        self.f_typedef.write(new_line)


if __name__ == "__main__":
    generator = DataTypeGenerator("../include/ctp/ThostFtdcUserApiDataType.h", "ctp")
    generator.run()
