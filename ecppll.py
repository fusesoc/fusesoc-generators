#!/usr/bin/python
from fusesoc.capi2.generator import Generator
import subprocess
import os

class EcppllGenerator(Generator):
    def run(self):
        name     = self.config.get('name', 'pll')
        fin      = self.config.get('freq_in', 12)
        fout     = self.config.get('freq_out', 60)
        filename = self.config.get('filename', 'pll.v')
        use_container = self.config.get('use_container', False)

        args = []
        if use_container:
            args += ['docker', 'run', '--rm', '-v', os.getcwd() + ':/src', '-w', '/src', 'hdlc/prjtrellis']
        args += ['ecppll', '-f', filename, '-n', name, '-i', str(fin), '-o', str(fout)]

        rc = subprocess.run(args)

        if rc.returncode:
            exit(1)
        self.add_files([{filename : {'file_type' : 'verilogSource'}}])

g = EcppllGenerator()
g.run()
g.write()
