#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Создает текстовый файл с указанным содержимым

version_added: "1.0.0"

description: Модуль создает текстовый файл на удаленном хосте по указанному пути с заданным содержимым.

options:
    path:
        description: Путь, по которому должен быть создан файл..
        required: true
        type: str
    content:
        description: Содержимое для записи в файл.
        required: true
        type: str

author:
    - Glubuchik (@GlubuchikAr)
'''

EXAMPLES = r'''
# Создаем файл с именем содержимого
- name: Create a test file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/test.txt
    content: "Hello World!"

# Создайте другой файл с именем
- name: Create configuration file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /etc/myapp/config.conf
    content: |
      setting1=value1
      setting2=value2
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
path:
    description: The path where the file was created.
    type: str
    returned: always
    sample: '/tmp/test.txt'
content:
    description: The content that was written to the file.
    type: str
    returned: always
    sample: 'Hello World!'
file_exists:
    description: Whether the file existed before module execution.
    type: bool
    returned: always
    sample: false
'''

from ansible.module_utils.basic import AnsibleModule
import os


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        path='',
        content='',
        file_exists=False
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        # In check mode, we check if file doesn't exist or content is different
        path = module.params['path']
        if os.path.exists(path):
            result['file_exists'] = True
            with open(path, 'r') as f:
                current_content = f.read()
            if current_content != module.params['content']:
                result['changed'] = True
        else:
            result['changed'] = True
        module.exit_json(**result)

    # manipulate or modify the state as needed
    path = module.params['path']
    content = module.params['content']
    
    result['path'] = path
    result['content'] = content
    
    # Check if file exists and compare content
    file_exists = os.path.exists(path)
    result['file_exists'] = file_exists
    
    if file_exists:
        with open(path, 'r') as f:
            current_content = f.read()
        if current_content == content:
            # File exists and content is the same - no changes
            result['changed'] = False
        else:
            # File exists but content is different - update file
            with open(path, 'w') as f:
                f.write(content)
            result['changed'] = True
    else:
        # File doesn't exist - create it
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True

    # in the event of a successful module execution
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()