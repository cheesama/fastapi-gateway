from jinja2 import Environment, FileSystemLoader

import yaml

with open("config.yml", 'r') as stream:
    try:
        config_data=yaml.safe_load(stream)
        print(config_data)
    except yaml.YAMLError as exc:
        print(exc)

# Load templates file from templtes folder 
env = Environment(loader = FileSystemLoader('./templates'),   trim_blocks=False, lstrip_blocks=True)
template = env.get_template('main_template.py')
print(template.render(config_data))
