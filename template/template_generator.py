import os
import sys

from fusesoc.capi2.generator import Generator
from jinja2 import Environment, FileSystemLoader

class TemplateGenerator(Generator):
    def run(self):

        output_file   = self.config.get('output_file')
        template_name = self.config.get('template')

        # Look for Jinja templates in the "templates" directory beneath this
        # script's location
        script_dir   = os.path.dirname(sys.argv[0])
        template_dir = os.path.join(script_dir, 'templates')

        env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)

        template = env.get_template(template_name)

        template.stream(self.config).dump(output_file['name'])

        self.add_files([{output_file['name'] : {'file_type' : output_file['type']}}])

g = TemplateGenerator()
g.run()
g.write()
