""""""
import importlib


class StructGenerator:
    """Struct builder """

    def __init__(self, filename: str, prefix: str):
        """Constructor"""
        self.filename = filename
        self.prefix = prefix
        self.typedefs = {}

        self.load_constant()

    def load_constant(self):
        """"""
        module_name = f"{self.prefix}_typedef"
        module = importlib.import_module(module_name)

        for name in dir(module):
            if "__" not in name:
                self.typedefs[name] = getattr(module, name)

    def run(self):
        """ run generation """
        self.f_cpp = open(self.filename, "r")
        self.f_struct = open(f"{self.prefix}_struct.py", "w")

        for line in self.f_cpp:
            self.process_line(line)

        self.f_cpp.close()
        self.f_struct.close()

        print("Struct generate success ")

    def process_line(self, line: str):
        """ each processing line """
        line = line.replace(";", "")
        line = line.replace("\n", "")

        if line.startswith("struct"):
            self.process_declare(line)
        elif line.startswith("{"):
            self.process_start(line)
        elif line.startswith("}"):
            self.process_end(line)
        elif "\t" in line and "///" not in line:
            self.process_member(line)

    def process_declare(self, line: str):
        """ processing statement """
        words = line.split(" ")
        name = words[1]
        end = "{"

        new_line = f"{name} = {end}\n"
        self.f_struct.write(new_line)

    def process_start(self, line: str):
        """ process begins """
        pass

    def process_end(self, line: str):
        """ processing ends """
        new_line = "}\n\n"
        self.f_struct.write(new_line)

    def process_member(self, line: str):
        """ processing members """
        words = line.split("\t")
        words = [word for word in words if word]

        py_type = self.typedefs[words[0]]
        name = words[1]

        new_line = f"    \"{name}\": \"{py_type}\",\n"
        self.f_struct.write(new_line)


if __name__ == "__main__":
    generator = StructGenerator("../include/xgj/ThostFtdcUserApiStruct.h", "xgj")
    generator.run()
