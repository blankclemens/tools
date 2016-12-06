#!/usr/bin/env python

import xml.etree.ElementTree as ET
import argparse
import yaml
import requests

#####

parser = argparse.ArgumentParser(description="""
Generate a YAML tool file from a shed_tool_conf.xml file or a Galaxy instance.
""")

parser.add_argument('--input', '-i', help='tool config XML file or Galaxy \
                    instance when using --api, e.g. http://localhost:8080',
                    required=True)
parser.add_argument('--output', '-o', help='output YAML file', required=True)
parser.add_argument('--latest', action='store_true',
                    help='install latest revisions instead of those specified')
parser.add_argument('--api', action='store_true',
                    help='Use the API to recieve tool information. Specify \
                          as input a Galaxy instance. Provide an API key with \
                          --key if necessary.')
parser.add_argument('--key', '-k', help="API key to use with --api")
parser.add_argument('--tool_dep', dest='tool_dep', action='store_true',
                    help='Flag to install tool dependencies.')
parser.add_argument('--no-tool_dep', dest='tool_dep',
                    action='store_false',
                    help='Flag to disable tool dependencies.')
parser.set_defaults(tool_dep=True)
parser.add_argument('--repository_dep', dest='repository_dep',
                    action='store_true',
                    help='Flag to install repository dependencies.')
parser.add_argument('--no-repository_dep', dest='repository_dep',
                    action='store_false',
                    help='Flag to disable repository dependencies.')
parser.set_defaults(repository_dep=True)
parser.add_argument('--resolver_dep', dest='resolver_dep',
                    action='store_true',
                    help='Flag to install resolver dependencies.')
parser.add_argument('--no-resolver_dep', dest='resolver_dep',
                    action='store_false',
                    help='Flag to disable resolver dependencies.')
parser.set_defaults(resolver_dep=False)

args = parser.parse_args()

#####

data = {}

data['api_key'] = 'KEY'
data['galaxy_instance'] = 'GALAXY_INSTANCE'
data['tools'] = []

unique_tools = []


if args.api:
    if args.key:
        r = requests.get(args.input + '/api/tools?key=' + args.key)
    else:
        r = requests.get(args.input + '/api/tools')

    tools = r.json()

    for section in tools:
        if 'elems' not in section:
            continue
        for tool in section['elems']:
            if 'tool_shed_repository' in tool:

                if args.latest:
                    revision = 'latest'
                else:
                    revision = \
                        str(tool['tool_shed_repository']['changeset_revision'])

                if (str(tool['tool_shed_repository']['name']) +
                        str(tool['tool_shed_repository']['changeset_revision'])
                        not in unique_tools):

                    unique_tools.append(
                        str(tool['tool_shed_repository']['name']) +
                        str(tool['tool_shed_repository']['changeset_revision']))

                    data['tools'].append({
                        'name': tool['tool_shed_repository']['name'],
                        'owner': tool['tool_shed_repository']['owner'],
                        'tool_panel_section_id': tool['panel_section_id'],
                        'tool_panel_section_label': tool['panel_section_name'],
                        'tool_shed_url': tool['tool_shed_repository']['tool_shed'],
                        'install_tool_dependencies': args.tool_dep,
                        'install_repository_dependencies': args.repository_dep,
                        'install_resolver_dependencies': args.resolver_dep,
                        'revisions': [revision]})

else:

    tree = ET.parse(args.input)
    root = tree.getroot()

    for section in root.iter('section'):

        for i, tool in enumerate(section):
            if args.latest:
                revision = 'latest'
            else:
                revision = str(tool.find('installed_changeset_revision').text)

            if (tool.find('repository_name').text + str(revision)
                    not in unique_tools):

                unique_tools.append(tool.find('repository_name').text +
                                    str(revision))

                data['tools'].append({
                    'name': tool.find('repository_name').text,
                    'owner': tool.find('repository_owner').text,
                    'tool_panel_section_id':
                        section.get('name').lower().replace(' ', '_'),
                    'tool_panel_section_label': section.get('name'),
                    'tool_shed_url': tool.find('tool_shed').text,
                    'install_tool_dependencies': args.tool_dep,
                    'install_repository_dependencies': args.repository_dep,
                    'install_resolver_dependencies': args.resolver_dep,
                    'revisions': [revision]})

with open(args.output, 'w') as outfile:
    yaml.dump(data, outfile, default_flow_style=False)
