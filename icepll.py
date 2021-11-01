#!/usr/bin/python3
from fusesoc.capi2.generator import Generator
import subprocess

class IcepllGenerator(Generator):
    def run(self):
        fin      = self.config.get('freq_in', 12)
        fout     = self.config.get('freq_out', 60)
        module   = self.config.get('module', False)
        filename = self.config.get('filename', 'pll.v' if module else 'pll.vh')

        args = ['icepll', '-f', filename, '-i', str(fin), '-o', str(fout)]
        if module:
            args.append('-m')
        rc = subprocess.call(args)
        if rc:
            exit(1)
        self.add_files([{filename : {'file_type' : 'verilogSource',
                                     'is_include_file' : not module}}])

g = IcepllGenerator()
g.run()
g.write()
