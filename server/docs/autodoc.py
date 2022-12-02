# -*- coding: utf-8 -*-
from typing import List, Any, Dict, NoReturn, Tuple

from jinja2 import Environment, FileSystemLoader, select_autoescape

import re


__all__ = ['generate']


def _string_to_md(text: str) -> str:
    # colorize numbers
    text = re.sub(r'(-?\d+)', r'<span class="text-orange-400">\1</span>', text)
    # code
    # ```lang
    # source code
    # ```
    text = re.sub(r'```([\w_]+)\s+([\s\S]+?)\s+```', r'<pre><code class="language-\1">\2</code></pre>', text)
    # code
    # `example`
    text = re.sub(
        r'`([^`\n]*?)`',
        r'<div class="flex"><div class="flex bg-fore/[0.1] px-4 rounded-lg h-min">\1</div></div>',
        text
    )
    # list
    # - element
    text = re.sub(r'((\n *- +[^\n]+)+)', r'<ul class="flex flex-col gap-1 pl-4 list-disc">\1</ul>', text)
    text = re.sub(r'\n *- +([^\n]+)', r'<li>\1</li>', text)
    # horizontal line
    # ---
    text = re.sub(
        r'---',
        r'<div class="flex h-[0.5px] bg-fore w-2/3 self-center"></div>',
        text
    )
    # links
    # [text](url)
    text = re.sub(
        r'\[([^]]+)]\((https?://[^\s)]+)\)',
        r'<a target="_blank" rel="noopener noreferrer" href="\2" class="text-pink-300">\1</a>',
        text
    )
    # links [text](#anchor)
    text = re.sub(r'\[([^]]+)]\((#[^\s)]+)\)', r'<a href="\2" class="text-pink-300">\1</a>', text)
    # italic text
    # **text**
    text = re.sub(r'\*\*([^\n*]+)\*\*', r'<i>\1</i>', text)
    # bold text
    # *text*
    text = re.sub(r'\*([^\n*]+)\*', r'<b>\1</b>', text)
    return text.strip()


def _add_mount(
        path: str,
        models: List[Dict[str, Any]],
        mount_path: str
) -> List[Dict[str, Any]]:
    with open(path, 'r', encoding='utf-8') as f:
        mount = f.read()
    methods = []
    for i in re.findall(r"@[^.]+\.([^(]+)\(([^)]+)\)\s+([\s\S]+?\):)\s+(\"\"\"([\S\s]+?)\"\"\")?", mount):
        docstring = i[3].split('\n')
        # method name
        name = docstring[0]
        method_id = re.findall(r'def *([\w_]+)\(', i[2])[0]
        if method_id.startswith('_'):
            continue
        if name:
            name = name[3:]
        else:
            name = method_id.replace('_', ' ')
        # method desc
        description = re.findall(r'[^\n]+\s+([\S\s]+?):param', i[3])
        if description:
            description = _string_to_md(description[0])
            if ':param' in description:
                description = None
        else:
            description = None
        # method params
        params = []
        json = []
        params_result = re.findall(r':param (\S+?): +([^\n]+)', i[3])
        types_result = re.findall(r'([\w_]+) *: *([\w_]+\[[^]]+]|[\w_]+)( *= *([^,]+))?', i[2])
        for t in types_result:
            # Add model json params
            if t[1].endswith('Model'):
                for field, value in models[t[1]].items():
                    json.append({
                        'name': field,
                        'type': value['type'],
                        'description': value['doc'],
                        'required': value['default'] is None
                    })
                continue
            # add URL params
            res = list(filter(lambda x: x[0] == t[0], params_result))
            params.append({
                'name': t[0],
                'type': t[1],
                'description': '' if not res else res[0][1],
                'required': t[2] == ''
            })
        # create method
        method = {
            'name': name,
            'description': description,
            'id': method_id,
            'params': params,
            'json': json,
            'http': f'{i[0].upper()} {mount_path}{i[1][1:-1]} HTTP/1.1',
        }
        methods.append(method)
    return methods


def _add_model(path: str, model_name: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        module = f.read()

    model = re.findall(
        model_name + r'\s*\(\S+\):\s*(\"{3}[^"]+\"{3}\s*)?(([\w_]+ *: *[\w_]+[^\n]*\s*)+)', module
    )
    if model:
        return {
            i[0]: {
                'type': i[1],
                'default': i[2].strip().lstrip('=').strip() if i[2] else None,
                'doc': i[3].split('#')[1].strip() if '#' in i[3] else ''
            }
            for i in re.findall(r'([\w_]+) *: *([\w_\[\]]+)( *= *[^\n#]+)?([^#]*#[^\n]+)?', model[0][1])
        }
    return None


def _add_error(path: str) -> List[Dict[str, Any]]:
    with open(path, 'r', encoding='utf-8') as f:
        module = f.read()

    errors = re.findall(
        r'([\w_]+) *= *err_response\(\s*(\d+)\s*,\s*("[\S\s]+?")\s*\)', module
    )

    return [
        {
            'name': i[0].replace('_', ' ').title(),
            'code': int(i[1]),
            'value': i[2]
        } for i in errors
    ]


def _tailwind_config_update(config_file: str, colors: dict):
    print(config_file)
    with open(config_file, 'r', encoding='utf-8') as f:
        data = f.read()
    for key, value in colors.items():
        data = re.sub(r'(' + key + r")'\s*:\s*'(#[a-f0-9A-F]+)", r"\1': '" + value, data)
        print(data)
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(data)


def generate(
        root: str = './',
        template_folder: str = 'template',
        template_file: str = 'index.html',
        title: str = 'FastAPI Docs',
        tailwind_config_file: str = 'js/tailwind.config.js',
        models: List[Tuple[str, str]] = None,
        methods: List[Tuple[str, str]] = None,
        exceptions: List[str] = None,
        api_url: str = 'http://localhost:8000',
        tailwind_colors = None,
) -> NoReturn:
    """Generates FastAPI docs via Jinja2

    Supports:
    - Pydantic models
    - Little markdown (lists, code, links)
    - Highlight.js and tailwind css 3 for template files

    :param root: root path
    :param template_folder: folder with jinja2 templates
    :param template_file: jinja2 template file
    :param tailwind_config_file: tailwind css config file
    :param title: docs title
    :param models: pydantic models
    :param methods: methods description
    :param exceptions: exceptions file
    :param api_url: current api
    :param tailwind_colors: tailwind colors JSON
    """
    if models is None:
        models = []
    if exceptions is None:
        exceptions = []
    if tailwind_colors is None:
        tailwind_colors = {
            'back': '#080f11',
            'fore': '#c44b79',
            'code-back': '#acacac',
            'back-light': '#f2cedb',
            'fore-light': '#ee4968',
          }

    if not root.endswith('/'):
        raise ValueError('root param should be ends with "/".')

    env = Environment(
        loader=FileSystemLoader(f'{root}{template_folder}'),
        autoescape=select_autoescape()
    )
    index_template = env.get_template(template_file)
    _tailwind_config_update(root + tailwind_config_file, tailwind_colors)

    models = {i[0]: _add_model(f'{root}{i[1]}', i[0]) for i in models}
    methods_list = []
    for i in methods:
        methods_list.append(i[0])
        methods_list += _add_mount(f'{root}{i[1]}', models, i[0])
    errors_list = []
    for i in exceptions:
        errors_list += _add_error(f'{root}{i}')

    with open(f'{root}{template_file}', 'w', encoding='utf-8') as f:
        f.write(index_template.render(
            title=title,
            methods=methods_list,
            rootpath=root,
            errors=errors_list,
            api_url=api_url
        ))


if __name__ == '__main__':
    generate(
        title='ColNet API Docs',
        models=[
            ('UserModel', '../models/user.py'),
            ('ChatModel', '../models/chat.py'),
            ('WallPostModel', '../models/wall.py'),
        ],
        methods=[
            ('/colnet/user', '../mounts/user.py'),
            ('/colnet/chat', '../mounts/chat.py'),
            ('/colnet/wall', '../mounts/wall.py'),
            ('/colnet/attachments', '../mounts/attachments.py'),
        ],
        exceptions=[
            '../exceptions.py'
        ]
    )
