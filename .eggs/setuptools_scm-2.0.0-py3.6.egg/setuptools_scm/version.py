from __future__ import print_function
import datetime
import warnings
import re
from itertools import chain, repeat, islice

from .utils import trace

from pkg_resources import iter_entry_points

from pkg_resources import parse_version

SEMVER_MINOR = 2
SEMVER_PATCH = 3
SEMVER_LEN = 3


def _pad(iterable, size, padding=None):
    padded = chain(iterable, repeat(padding))
    return list(islice(padded, size))


def _get_version_class():
    modern_version = parse_version("1.0")
    if isinstance(modern_version, tuple):
        return None
    else:
        return type(modern_version)


VERSION_CLASS = _get_version_class()


class SetuptoolsOutdatedWarning(Warning):
    pass


# append so integrators can disable the warning
warnings.simplefilter('error', SetuptoolsOutdatedWarning, append=1)


def _warn_if_setuptools_outdated():
    if VERSION_CLASS is None:
        warnings.warn("your setuptools is too old (<12)", SetuptoolsOutdatedWarning)


def callable_or_entrypoint(group, callable_or_name):
    trace('ep', (group, callable_or_name))

    if callable(callable_or_name):
        return callable_or_name

    for ep in iter_entry_points(group, callable_or_name):
        trace("ep found:", ep.name)
        return ep.load()


def tag_to_version(tag):
    trace('tag', tag)
    if '+' in tag:
        warnings.warn("tag %r will be stripped of the local component" % tag)
        tag = tag.split('+')[0]
    # lstrip the v because of py2/py3 differences in setuptools
    # also required for old versions of setuptools

    version = tag.rsplit('-', 1)[-1].lstrip('v')
    if VERSION_CLASS is None:
        return version
    version = parse_version(version)
    trace('version', repr(version))
    if isinstance(version, VERSION_CLASS):
        return version


def tags_to_versions(tags):
    versions = map(tag_to_version, tags)
    return [v for v in versions if v is not None]


class ScmVersion(object):
    def __init__(self, tag_version,
                 distance=None, node=None, dirty=False,
                 preformatted=False,
                 branch=None,
                 **kw):
        if kw:
            trace("unknown args", kw)
        self.tag = tag_version
        if dirty and distance is None:
            distance = 0
        self.distance = distance
        self.node = node
        self.time = datetime.datetime.now()
        self.extra = kw
        self.dirty = dirty
        self.preformatted = preformatted
        self.branch = branch

    @property
    def exact(self):
        return self.distance is None

    def __repr__(self):
        return self.format_with(
            '<ScmVersion {tag} d={distance}'
            ' n={node} d={dirty} b={branch} x={extra}>')

    def format_with(self, fmt, **kw):
        return fmt.format(
            time=self.time,
            tag=self.tag, distance=self.distance,
            node=self.node, dirty=self.dirty, extra=self.extra,
            branch=self.branch, **kw)

    def format_choice(self, clean_format, dirty_format, **kw):
        return self.format_with(
            dirty_format if self.dirty else clean_format, **kw)

    def format_next_version(self, guess_next, fmt="{guessed}.dev{distance}", **kw):
        guessed = guess_next(self.tag, **kw)
        return self.format_with(fmt, guessed=guessed)


def _parse_tag(tag, preformatted):
    if preformatted:
        return tag
    if VERSION_CLASS is None or not isinstance(tag, VERSION_CLASS):
        tag = tag_to_version(tag)
    return tag


def meta(tag, distance=None, dirty=False, node=None, preformatted=False, **kw):
    tag = _parse_tag(tag, preformatted)
    trace('version', tag)
    assert tag is not None, 'cant parse version %s' % tag
    return ScmVersion(tag, distance, node, dirty, preformatted, **kw)


def guess_next_version(tag_version):
    version = _strip_local(str(tag_version))
    return _bump_dev(version) or _bump_regex(version)


def _strip_local(version_string):
    public, sep, local = version_string.partition('+')
    return public


def _bump_dev(version):
    if '.dev' not in version:
        return

    prefix, tail = version.rsplit('.dev', 1)
    assert tail == '0', 'own dev numbers are unsupported'
    return prefix


def _bump_regex(version):
    prefix, tail = re.match(r'(.*?)(\d+)$', version).groups()
    return '%s%d' % (prefix, int(tail) + 1)


def guess_next_dev_version(version):
    if version.exact:
        return version.format_with("{tag}")
    else:
        return version.format_next_version(guess_next_version)


def guess_next_simple_semver(version, retain, increment=True):
    parts = map(int, str(version).split('.'))
    parts = _pad(parts, retain, 0)
    if increment:
        parts[-1] += 1
    parts = _pad(parts, SEMVER_LEN, 0)
    return '.'.join(map(str, parts))


def simplified_semver_version(version):
    if version.exact:
        return guess_next_simple_semver(
            version.tag, retain=SEMVER_LEN, increment=False)
    else:
        if version.branch is not None and 'feature' in version.branch:
            return version.format_next_version(
                guess_next_simple_semver, retain=SEMVER_MINOR)
        else:
            return version.format_next_version(
                guess_next_simple_semver, retain=SEMVER_PATCH)


def _format_local_with_time(version, time_format):

    if version.exact or version.node is None:
        return version.format_choice(
            "", "+d{time:{time_format}}",
            time_format=time_format)
    else:
        return version.format_choice(
            "+{node}", "+{node}.d{time:{time_format}}",
            time_format=time_format)


def get_local_node_and_date(version):
    return _format_local_with_time(version, time_format="%Y%m%d")


def get_local_node_and_timestamp(version, fmt='%Y%m%d%H%M%S'):
    return _format_local_with_time(version, time_format=fmt)


def get_local_dirty_tag(version):
    return version.format_choice('', '+dirty')


def postrelease_version(version):
    if version.exact:
        return version.format_with('{tag}')
    else:
        return version.format_with('{tag}.post{distance}')


def format_version(version, **config):
    trace('scm version', version)
    trace('config', config)
    if version.preformatted:
        return version.tag
    version_scheme = callable_or_entrypoint(
        'setuptools_scm.version_scheme', config['version_scheme'])
    local_scheme = callable_or_entrypoint(
        'setuptools_scm.local_scheme', config['local_scheme'])
    main_version = version_scheme(version)
    trace('version', main_version)
    local_version = local_scheme(version)
    trace('local_version', local_version)
    return version_scheme(version) + local_scheme(version)
