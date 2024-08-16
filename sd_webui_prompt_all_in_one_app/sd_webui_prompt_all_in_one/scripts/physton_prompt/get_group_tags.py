import os
from ruamel.yaml import YAML

current_dir = os.path.dirname(os.path.abspath(__file__))

def _get_tags_filename(name):
    file = os.path.join(current_dir, '../../../../group_tags/', name + '.yaml')
    return file

def get_group_tags(lang):
    tags_file = _get_tags_filename('custom')
    is_exists = os.path.exists(tags_file)
    if is_exists:
        try:
            with open(tags_file, 'r', encoding='utf8') as f:
                data = f.read()
            is_exists = len(data.strip()) > 0
        except:
            is_exists = False

    if not is_exists:
        tags_file = _get_tags_filename(lang)
        if not os.path.exists(tags_file):
            tags_file = _get_tags_filename('default')
    if not os.path.exists(tags_file):
        return ''

    tags = ''

    try:
        prepend_file = _get_tags_filename('prepend')
        with open(prepend_file, 'r', encoding='utf8') as f:
            prepend = f.read()
        tags += prepend + "\n\n"
    except:
        pass

    try:
        with open(tags_file, 'r', encoding='utf8') as f:
            data = f.read()
        tags += data + "\n\n"
    except:
        pass

    try:
        append_file = _get_tags_filename('append')
        with open(append_file, 'r', encoding='utf8') as f:
            append = f.read()
        tags += append + "\n\n"
    except:
        pass

    return tags


def addGroupTag(lang,cn,en,key,groupKey):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # 防止自动换行

    #文件位置
    filePath = os.path.abspath(os.path.join(current_dir, '../../../../group_tags/', lang + '.yaml'))

    # 读取YAML文件
    with open(filePath, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

        # 定位到需要修改的部分
        for group in data:
            if group.get('name') == key:
                for subgroup in group['groups']:
                    if subgroup.get('name') == groupKey:
                        # 新增tag
                        new_tag = en+": "+cn
                        tag_key, tag_value = new_tag.split(': ')
                        subgroup['tags'][tag_key] = tag_value

    # 写回YAML文件
    with open(filePath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)


def editGroupTag(lang,cn,en,key,groupKey):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # 防止自动换行

    #文件位置
    filePath = os.path.abspath(os.path.join(current_dir, '../../../../group_tags/', lang + '.yaml'))

    # 读取YAML文件
    with open(filePath, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

        # 定位到需要修改的部分
        for group in data:
            if group.get('name') == key:
                for subgroup in group['groups']:
                    if subgroup.get('name') == groupKey:
                        if en in subgroup['tags']:
                            subgroup['tags'][en] = cn

    # 写回YAML文件
    with open(filePath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

def deleteGroupTag(lang,cn,en,key,groupKey):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # 防止自动换行

    #文件位置
    filePath = os.path.abspath(os.path.join(current_dir, '../../../../group_tags/', lang + '.yaml'))

    # 读取YAML文件
    with open(filePath, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

        # 定位到需要修改的部分
        for group in data:
            if group.get('name') == key:
                for subgroup in group['groups']:
                    if subgroup.get('name') == groupKey:
                        if en in subgroup['tags']:
                            del subgroup['tags'][en]

    # 写回YAML文件
    with open(filePath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

def addNewNodeGroup(lang,key,groupKe,color):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # 防止自动换行

    #文件位置
    filePath = os.path.abspath(os.path.join(current_dir, '../../../../group_tags/', lang + '.yaml'))

    # 读取YAML文件
    with open(filePath, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

        new_group = {
            'name': key,
            'groups': [
                {
                    'name': groupKe,
                    'color': color,  # 示例颜色
                    'tags': {}
                }
            ]
        }

        # 找到适当的层级添加新的 group
        # 假设我们想要添加到 data 的顶级
        data.append(new_group)

    # 写回YAML文件
    with open(filePath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)


def addNewGroup(lang,key,groupKe,color):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 1000000  # 防止自动换行

    #文件位置
    filePath = os.path.abspath(os.path.join(current_dir, '../../../../group_tags/', lang + '.yaml'))

    # 读取YAML文件
    with open(filePath, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

        # 新增子类到特定的 group
        target_group_name = key  # 目标 group 的名称
        new_subgroup = {
            'name': groupKe,
            'color': color,  # 示例颜色
            'tags': {}
        }
        # 查找目标 group 并在其 groups 列表中添加新的子类
        for group in data:
            if group.get('name') == target_group_name:
                group['groups'].append(new_subgroup)
                break  # 找到并添加后退出循环

    # 写回YAML文件
    with open(filePath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

def editNodeGroup(lang,key,newKey):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # 防止自动换行

    #文件位置
    filePath = os.path.abspath(os.path.join(current_dir, '../../../../group_tags/', lang + '.yaml'))

    # 读取YAML文件
    with open(filePath, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

        # 修改 group 的 name
        for group in data:
            if group.get('name') == key:
                group['name'] = newKey
                break  # 找到并修改后退出循环

    # 写回YAML文件
    with open(filePath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)


def editChildNodeGroup(lang,key,groupA,newKey):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # 防止自动换行

    #文件位置
    filePath = os.path.abspath(os.path.join(current_dir, '../../../../group_tags/', lang + '.yaml'))

    # 读取YAML文件
    with open(filePath, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

        # 修改特定 subgroup 的 name
        for group in data:
            if group.get('name') == key:
                for index, subgroup in enumerate(group['groups']):
                    if subgroup.get('name') == groupA:
                        # 修改 subgroup 的 name
                        group['groups'][index]['name'] = newKey
                        break  # 找到并修改后退出内层循环

    # 写回YAML文件
    with open(filePath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)

def deleteNodeGroup(lang,key):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # 防止自动换行

    #文件位置
    filePath = os.path.abspath(os.path.join(current_dir, '../../../../group_tags/', lang + '.yaml'))

    # 读取YAML文件
    with open(filePath, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

        # 删除具有特定 name 的 group
        data = [group for group in data if group.get('name') != key]

    # 写回YAML文件
    with open(filePath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)


def deleteChildNodeGroup(lang,key,groupKey):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # 防止自动换行

    #文件位置
    filePath = os.path.abspath(os.path.join(current_dir, '../../../../group_tags/', lang + '.yaml'))

    # 读取YAML文件
    with open(filePath, 'r', encoding='utf-8') as file:
        data = yaml.load(file)

        # 定位到需要修改的部分
        for group in data:
            if group.get('name') == key:
                # 反向迭代 groups 列表
                for i in range(len(group['groups']) - 1, -1, -1):
                    subgroup = group['groups'][i]
                    if subgroup.get('name') == groupKey:
                        # 从列表中删除 subgroup
                        del group['groups'][i]
    # 写回YAML文件
    with open(filePath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file)