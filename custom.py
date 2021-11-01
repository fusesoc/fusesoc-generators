#!/usr/bin/env python3
from fusesoc.capi2.generator import Generator
import os
import shutil
import subprocess
import tempfile

class CustomGenerator(Generator):
    def run(self):

        copy_core = self.config.get('copy_core', False)
        if copy_core:
            tmp_dir = os.path.join(tempfile.mkdtemp(), 'core')
            shutil.copytree(self.files_root, tmp_dir)

        cwd = None
        if self.config.get('run_from_core'):
            cwd = tmp_dir if copy_core else self.files_root

        files      = self.config['output'].get('files', [])
        parameters = self.config['output'].get('parameters', {})

        rc = subprocess.call(self.config['command'].split(), cwd=cwd)
        if rc:
            exit(1)
        if cwd:
            filenames = []
            for f in files:
                for k in f:
                    filenames.append(k)

            for f in filenames:
                d = os.path.dirname(f)
                if d and not os.path.exists(d):
                    os.makedirs(d)
                shutil.copy2(os.path.join(cwd, f),f)

        self.add_files(files)

        for k,v in parameters.items():
            self.add_parameter(k, v)

g = CustomGenerator()
g.run()
g.write()
