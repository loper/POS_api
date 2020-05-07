
from glob import glob
from re import findall, split
from statistics import mode
from os.path import isdir

from config import TEMPLATES_DIR


def append_zeroes(data):
    result = []
    for ver in data:
        formatted = ['{:03d}'.format(int(a)) for a in ver if a.isdigit()]
        if len(formatted) != 3:
            continue
        result.append(formatted)
    return result


def filter_out_uncommon(data, depth=2):
    for i in range(depth):
        # find most common values
        common_value = mode([d[i] for d in data])
        # filter out other occurences
        filtered = [d for d in data if d[i] == common_value]
        data = filtered
    return data


def filter_out_by_limits(data, lim):
    lower_limit = lim[0]
    upper_limit = lim[1]
    result = data
    if lower_limit:
        result = [ver for ver in result if ver >= lower_limit]
    if upper_limit:
        result = [ver for ver in result if ver <= upper_limit]
    return result


def sort_by_version(data, num=2):
    versions = append_zeroes(data)
    # remove build numer
    versions = [v[:3] for v in versions]
    versions.sort(reverse=True)
    return versions[:num]


def find_version_dir(version, t_dirs):
    for templ_dir in t_dirs:
        if findall(version, templ_dir):
            return templ_dir
    return None


def get_full_version(version, ver_dirs, templ_dir):
    ver_dir = find_version_dir(version, ver_dirs)
    version_desc_file = glob("{}/**/{}/**/version_descriptor.xml".format(
        templ_dir, ver_dir), recursive=True)
    if not version_desc_file:
        return None
    found = None
    with open(version_desc_file[0], 'r') as ver_file:
        raw = ver_file.readlines()
    for line in raw:
        found = findall(r'NAME="(.*?)"', line.strip())
        if found:
            break
    return found[0]


def find_latest_pos(templates_dir, ver_limits, filter_uncommon=False, dry_run=False):
    t_dirs = [f.split('/')[-1] for f in glob("{}/*pos-full*/*".format(templates_dir),
                                             recursive=False) if isdir(f)]

    if not t_dirs:
        return None, None
    t_dirs.sort()

    if dry_run:
        return t_dirs

    versions = [split(r'\.|\-', ver.replace('v', '')) for ver in t_dirs]

    if filter_uncommon:
        versions = filter_out_uncommon(versions)
    if ver_limits:
        versions = filter_out_by_limits(versions, ver_limits)
    latest = sort_by_version(versions)

    # clear out appending zeroes
    result = []
    for ver in latest:
        version = [str(int(v)) for v in ver]
        result.append('.'.join(version))
    ver_full = get_full_version(result[0], t_dirs, templates_dir)
    par_full = get_full_version(result[1], t_dirs, templates_dir)
    return (ver_full or result[0], par_full or result[1])


def experimental_find_latest_pos(templates_dir, dry_run=False):
    t_dirs = [f.split('/')[-1] for f in glob("{}/*pos-full*/*".format(templates_dir),
                                             recursive=False) if isdir(f)]

    if not t_dirs:
        return None, None
    t_dirs.sort()

    if dry_run:
        return t_dirs

    versions = experimental_sorting(t_dirs)

    # clear out appending zeroes
    result = [versions[-1], versions[-2]]
    ver_full = get_full_version(result[0], t_dirs, templates_dir)
    par_full = get_full_version(result[1], t_dirs, templates_dir)
    return (ver_full or result[0], par_full or result[1])


def experimental_sorting(data):
    result = []
    # versions = [ver.replace('v', '') for ver in data]
    versions = [split(r'\.|\-|\_', ver.replace('v', '')) for ver in data]
    versions = ['{}.{}.{}'.format(ver[0], ver[1], ver[2]) for ver in versions]
    for ver in sorted(versions, key=lambda ver:
                      (int(ver.split(".")[0]),
                       int(ver.split(".")[1]),
                       int(ver.split(".")[2]))):
        result.append(ver)
    return result


if __name__ == "__main__":
    LIMITS = [None, ['1', '99', '999']]
    # VERS = find_latest_pos(TEMPLATES_DIR, LIMITS, dry_run=True)
    # print(VERS)
    print(find_latest_pos(TEMPLATES_DIR, LIMITS, dry_run=True))
    VER_LATEST, VER_PARENT = experimental_find_latest_pos(TEMPLATES_DIR)
    print(VER_LATEST)
    print(VER_PARENT)
