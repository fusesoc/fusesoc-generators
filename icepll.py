#!/usr/bin/python
from fusesoc.capi2.generator import Generator
import subprocess

class IcepllGenerator(Generator):
    def run(self):
        fin      = self.config.get('freq_in') or 12
        fout     = self.config.get('freq_out') or 60
        filename = self.config.get('filename') or 'pll.v'

        args = ['icepll', '-m', '-f', filename, '-i', str(fin), '-o', str(fout)]
        rc = subprocess.call(args)
        if rc:
            exit(1)
        self.add_files([{filename : {'file_type' : 'verilogSource'}}])

g = IcepllGenerator()
g.run()
g.write()
