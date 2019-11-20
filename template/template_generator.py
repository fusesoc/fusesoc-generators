import os
import sys

from fusesoc.capi2.generator import Generator
from jinja2 import Environment, FileSystemLoader

class TemplateGenerator(Generator):
    def run(self):

        output_file   = self.config.get('output_file')
        template_name = self.config.get('template')

        # Allow the user to specify where to look for Jinja templates, but by
        # default look in the core's directory or in the "templates" directory
        # beneath this script's location
        default_template_path = [self.files_root]

        script_dir   = os.path.dirname(__file__)
        template_dir = os.path.join(script_dir, 'templates')

        default_template_path.append(template_dir)

        template_path = self.config.get('template_path', default_template_path)

        env = Environment(loader=FileSystemLoader(template_path), trim_blocks=True, lstrip_blocks=True)

        template = env.get_template(template_name)

        template.stream(self.config).dump(output_file['name'])

        self.add_files([{output_file['name'] : {'file_type' : output_file['type']}}])

if __name__ == '__main__':
    g = TemplateGenerator()
    g.run()
    g.write()
