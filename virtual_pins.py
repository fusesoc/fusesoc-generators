import sys
import pathlib

from fusesoc.capi2.generator import Generator

# hdlparse was considered but didn't appear to extract VHDL entities. Someone
# else reported a similar problem in
# https://github.com/kevinpt/hdlparse/issues/6
#
# hdlConvertor has a less refined interface, but seemed better than doing
# something custom with pyparsing or similar

import hdlConvertor
from hdlConvertor.language import Language

class VirtualPinGenerator(Generator):

    @staticmethod
    def _get_lang(f):
        ext = f.suffix

        ext_to_lang = {
          '.v'    : Language.VERILOG,
          '.sv'   : Language.SYSTEM_VERILOG,
          '.vhd'  : Language.VHDL,
          '.vhdl' : Language.VHDL
        }

        if ext not in ext_to_lang:
            print("Unable to map extension {} to a language".format(ext))
            exit(1)
        else:
            return ext_to_lang[ext]

    def run(self):

        ignored_ports_default = ['clk', 'clock', 'rst', 'reset']

        input_file    = pathlib.Path(self.config.get('input_file'))
        output_file   = self.config.get('output_file', 'virtual_pins.tcl')
        ignored_ports = self.config.get('ignored_ports', ignored_ports_default)

        convertor = hdlConvertor.HdlConvertor()

        lang = self._get_lang(input_file)

        # Finding the input file can be tricky since the generator runs
        # in a different directory (on Linux
        # ~/.cache/fusesoc/generated) and doesn't know where FuseSoC
        # was originally run. If the file is associated with the core being built self.files_root
        # should give us the parent path. However, if the input file is
        # associated with a lower-level core a full path is likely to be
        # required.

        # If the input file is a relative path look for it in self.files_root
        if input_file.is_absolute():
            parse_file = input_file
        else:
            parse_file = pathlib.Path(self.files_root).joinpath(input_file)

        if not parse_file.exists():
            print("Can't find input file:", parse_file)
            exit(1)

        lang = self._get_lang(parse_file)

        # Currently just search the directory of the input file for Verilog includes
        include_dirs = [ str(parse_file.parent) ]

        # hdlConvertor is currently a bit chatty, outputing text the user
        # probably doesn't want to see about unsupported features, etc. like
        # the following:
        #
        # /path/to/file.vhd:18:0: DesignFileParser.visitContext_item - library_clause Conversion to Python object not implemented
        #    ...libraryieee;...
        #
        # It would perhaps be nice to capture this output, but that's
        # non-trivial since hdlConvertor uses a C++ parser. See
        #
        # https://stackoverflow.com/questions/52219393/how-do-i-capture-stderr-in-python
        #
        # and the linked blog for how to do this if required

        ast = convertor.parse(str(parse_file), lang, include_dirs)

        # Find modules
        hdl_modules = [m for m in ast.objs if isinstance(m, hdlConvertor.hdlAst.HdlModuleDec)]

        if len(hdl_modules) == 0:
            print("Found no module or entity declarations")
            exit(1)
        elif len(hdl_modules) > 1:
            print("Found multiple module declarations but only using the first")

        # Get port names
        all_ports      = [p.name for p in hdl_modules[0].ports]
        filtered_ports = [ p for p in all_ports if p not in ignored_ports]

        f = open(output_file, 'w');

        # The generated TCL code loops over a list of ports:
        #
        #   set ports {port_a port_b port_c port_d}
        #
        #   foreach p $ports {
        #     set_instance_assignment -name VIRTUAL_PIN ON -to $p
        #   }
        #
        # It may be simpler to just do the looping in Python with something like the following:
        #
        # for p in filtered_ports:
        #     f.write('set_instance_assignment -name VIRTUAL_PIN ON -to {}\n'.format(p))

        tcl = """set ports {{{}}}
foreach p $ports {{
  set_instance_assignment -name VIRTUAL_PIN ON -to $p
}}
"""

        f.write(tcl.format(' '.join(filtered_ports)))

        f.close()
        self.add_files([{output_file : {'file_type' : 'tclSource'}}])

if __name__ == "__main__":
    g = VirtualPinGenerator()
    g.run()
    g.write()

