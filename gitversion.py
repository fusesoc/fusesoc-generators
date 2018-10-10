#!/usr/bin/python
from fusesoc.capi2.generator import Generator
import subprocess

class VersionGenerator(Generator):
    def run(self):
        verlist = subprocess.check_output(['git',
                                           'describe',
                                           '--tags',
                                           '--dirty',
                                           '--abbrev=8',
                                           '--long'],
                                          cwd=self.files_root).decode().rstrip().split('-')
        dirty = verlist[-1] == 'dirty'
        if dirty:
            verlist.pop()
        sha = verlist.pop()[1:9]

        rev = verlist.pop()

        #Sanity checks on version
        if len(verlist) > 1:
            print("'-' is not allowed in version tag")
            exit(1)

        if not verlist[0][0] == 'v':
            print("Version tag must start with 'v'")
            exit(1)
        ver = verlist[0][1:].split('.')
        major = ver.pop(0)
        minor = ver.pop(0)
        patch = ver[0] if ver else 0

        params = {'VERSION_MAJOR' : major,
                  'VERSION_MINOR' : minor,
                  'VERSION_PATCH' : patch,
                  'VERSION_REV'   : rev,
                  }
        for k,v in params.items():
            self.add_parameter(k,
                               {'datatype'  : 'int',
                                'default'   : int(v),
                                'paramtype' : 'vlogdefine',
                                })
        self.add_parameter('VERSION_DIRTY',
                           {'datatype' : 'bool',
                            'default'  : dirty,
                            'paramtype' : 'vlogdefine'})
        self.add_parameter('VERSION_SHA',
                           {'datatype' : 'str',
                            'default'  : sha,
                            'paramtype' : 'vlogdefine'})

vg = VersionGenerator()
vg.run()
vg.write()
