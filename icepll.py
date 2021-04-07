#!/usr/bin/python
from fusesoc.capi2.generator import Generator
import subprocess
import os

class IcepllGenerator(Generator):
    def run(self):
        fin      = self.config.get('freq_in', 12)
        fout     = self.config.get('freq_out', 60)
        module   = self.config.get('module', False)
        filename = self.config.get('filename', 'pll.v' if module else 'pll.vh')
        use_container = self.config.get('use_container', False)

        args = []
        if use_container:
            args += ['docker', 'run', '--rm', '-v', os.getcwd() + ':/src', '-w', '/src', 'hdlc/icestorm']
        args += ['icepll', '-f', filename, '-i', str(fin), '-o', str(fout)]
        if module:
            args += ['-m']

        rc = subprocess.run(args)

        if rc.returncode:
            exit(1)
        self.add_files([{filename : {'file_type' : 'verilogSource',
                                     'is_include_file' : not module}}])

g = IcepllGenerator()
g.run()
g.write()
