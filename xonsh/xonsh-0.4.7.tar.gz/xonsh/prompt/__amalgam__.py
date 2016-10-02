"""Amalgamation of xonsh.prompt package, made up of the following modules, in order:

* cwd
* env
* gitstatus
* job
* vc_branch
* base

"""

from sys import modules as _modules
from types import ModuleType as _ModuleType
from importlib import import_module as _import_module


class _LazyModule(_ModuleType):

    def __init__(self, pkg, mod, asname=None):
        '''Lazy module 'pkg.mod' in package 'pkg'.'''
        self.__dct__ = {
            'loaded': False,
            'pkg': pkg,  # pkg
            'mod': mod,  # pkg.mod
            'asname': asname,  # alias
            }

    @classmethod
    def load(cls, pkg, mod, asname=None):
        if mod in _modules:
            key = pkg if asname is None else mod
            return _modules[key]
        else:
            return cls(pkg, mod, asname)

    def __getattribute__(self, name):
        if name == '__dct__':
            return super(_LazyModule, self).__getattribute__(name)
        dct = self.__dct__
        mod = dct['mod']
        if dct['loaded']:
            m = _modules[mod]
        else:
            m = _import_module(mod)
            glbs = globals()
            pkg = dct['pkg']
            asname = dct['asname']
            if asname is None:
                glbs[pkg] = m = _modules[pkg]
            else:
                glbs[asname] = m
            dct['loaded'] = True
        return getattr(m, name)

#
# cwd
#
# -*- coding: utf-8 -*-
"""CWD related prompt formatter"""

os = _LazyModule.load('os', 'os')
shutil = _LazyModule.load('shutil', 'shutil')
builtins = _LazyModule.load('builtins', 'builtins')
xt = _LazyModule.load('xonsh', 'xonsh.tools', 'xt')
xp = _LazyModule.load('xonsh', 'xonsh.platform', 'xp')
def _replace_home(x):
    if xp.ON_WINDOWS:
        home = (builtins.__xonsh_env__['HOMEDRIVE'] +
                builtins.__xonsh_env__['HOMEPATH'][0])
        if x.startswith(home):
            x = x.replace(home, '~', 1)

        if builtins.__xonsh_env__.get('FORCE_POSIX_PATHS'):
            x = x.replace(os.sep, os.altsep)

        return x
    else:
        home = builtins.__xonsh_env__['HOME']
        if x.startswith(home):
            x = x.replace(home, '~', 1)
        return x


def _replace_home_cwd():
    return _replace_home(builtins.__xonsh_env__['PWD'])


def _collapsed_pwd():
    sep = xt.get_sep()
    pwd = _replace_home_cwd().split(sep)
    l = len(pwd)
    leader = sep if l > 0 and len(pwd[0]) == 0 else ''
    base = [i[0] if ix != l - 1 else i
            for ix, i in enumerate(pwd) if len(i) > 0]
    return leader + sep.join(base)


def _dynamically_collapsed_pwd():
    """Return the compact current working directory.  It respects the
    environment variable DYNAMIC_CWD_WIDTH.
    """
    originial_path = _replace_home_cwd()
    target_width, units = builtins.__xonsh_env__['DYNAMIC_CWD_WIDTH']
    if target_width == float('inf'):
        return originial_path
    if (units == '%'):
        cols, _ = shutil.get_terminal_size()
        target_width = (cols * target_width) // 100
    sep = xt.get_sep()
    pwd = originial_path.split(sep)
    last = pwd.pop()
    remaining_space = target_width - len(last)
    # Reserve space for separators
    remaining_space_for_text = remaining_space - len(pwd)
    parts = []
    for i in range(len(pwd)):
        part = pwd[i]
        part_len = int(min(len(part),
                           max(1, remaining_space_for_text // (len(pwd) - i))))
        remaining_space_for_text -= part_len
        reduced_part = part[0:part_len]
        parts.append(reduced_part)
    parts.append(last)
    full = sep.join(parts)
    # If even if displaying one letter per dir we are too long
    if (len(full) > target_width):
        # We truncate the left most part
        full = "..." + full[int(-target_width) + 3:]
        # if there is not even a single separator we still
        # want to display at least the beginning of the directory
        if full.find(sep) == -1:
            full = ("..." + sep + last)[0:int(target_width)]
    return full

#
# env
#
# -*- coding: utf-8 -*-
"""Prompt formatter for virtualenv and others"""

# amalgamated os
# amalgamated builtins
# amalgamated xonsh.platform
def env_name(pre_chars='(', post_chars=')'):
    """Extract the current environment name from $VIRTUAL_ENV or
    $CONDA_DEFAULT_ENV if that is set
    """
    env_path = builtins.__xonsh_env__.get('VIRTUAL_ENV', '')
    if len(env_path) == 0 and xp.ON_ANACONDA:
        env_path = builtins.__xonsh_env__.get('CONDA_DEFAULT_ENV', '')
    env_name = os.path.basename(env_path)
    if env_name:
        return pre_chars + env_name + post_chars


def vte_new_tab_cwd():
    """This prints an escape squence that tells VTE terminals the hostname
    and pwd. This should not be needed in most cases, but sometimes is for
    certain Linux terminals that do not read the PWD from the environment
    on startup. Note that this does not return a string, it simply prints
    and flushes the escape sequence to stdout directly.
    """
    env = builtins.__xonsh_env__
    t = '\033]7;file://{}{}\007'
    s = t.format(env.get('HOSTNAME'), env.get('PWD'))
    print(s, end='', flush=True)

#
# gitstatus
#
# -*- coding: utf-8 -*-
"""Informative git status prompt formatter"""

# amalgamated builtins
collections = _LazyModule.load('collections', 'collections')
# amalgamated os
subprocess = _LazyModule.load('subprocess', 'subprocess')
xl = _LazyModule.load('xonsh', 'xonsh.lazyasd', 'xl')
GitStatus = collections.namedtuple('GitStatus',
                                   ['branch', 'num_ahead', 'num_behind',
                                    'untracked', 'changed', 'conflicts',
                                    'staged', 'stashed', 'operations'])

def _check_output(*args, **kwargs):
    kwargs.update(dict(env=builtins.__xonsh_env__.detype(),
                       stderr=subprocess.DEVNULL,
                       timeout=builtins.__xonsh_env__['VC_BRANCH_TIMEOUT'],
                       universal_newlines=True
                       ))
    return subprocess.check_output(*args, **kwargs)


@xl.lazyobject
def _DEFS():
    DEFS = {
        'HASH': ':',
        'BRANCH': '{CYAN}',
        'OPERATION': '{CYAN}',
        'STAGED': '{RED}●',
        'CONFLICTS': '{RED}×',
        'CHANGED': '{BLUE}+',
        'UNTRACKED': '…',
        'STASHED': '⚑',
        'CLEAN': '{BOLD_GREEN}✓',
        'AHEAD': '↑·',
        'BEHIND': '↓·',
    }
    return DEFS


def _get_def(key):
    def_ = builtins.__xonsh_env__.get('XONSH_GITSTATUS_' + key)
    return def_ if def_ is not None else _DEFS[key]


def _get_tag_or_hash():
    tag = _check_output(['git', 'describe', '--exact-match']).strip()
    if tag:
        return tag
    hash_ = _check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
    return _get_def('HASH') + hash_


def _get_stash(gitdir):
    try:
        with open(os.path.join(gitdir, 'logs/refs/stash')) as f:
            return sum(1 for _ in f)
    except IOError:
        return 0


def _gitoperation(gitdir):
    files = (
             ('rebase-merge', 'REBASE'),
             ('rebase-apply', 'AM/REBASE'),
             ('MERGE_HEAD', 'MERGING'),
             ('CHERRY_PICK_HEAD', 'CHERRY-PICKING'),
             ('REVERT_HEAD', 'REVERTING'),
             ('BISECT_LOG', 'BISECTING'),
             )
    return [f[1] for f in files
            if os.path.exists(os.path.join(gitdir, f[0]))]


def gitstatus():
    """Return namedtuple with fields:
    branch name, number of ahead commit, number of behind commit,
    untracked number, changed number, conflicts number,
    staged number, stashed number, operation."""
    status = _check_output(['git', 'status', '--porcelain', '--branch'])
    branch = ''
    num_ahead, num_behind = 0, 0
    untracked, changed, conflicts, staged = 0, 0, 0, 0
    for line in status.splitlines():
        if line.startswith('##'):
            line = line[2:].strip()
            if 'Initial commit on' in line:
                branch = line.split()[-1]
            elif 'no branch' in line:
                branch = _get_tag_or_hash()
            elif '...' not in line:
                branch = line
            else:
                branch, rest = line.split('...')
                if ' ' in rest:
                    divergence = rest.split(' ', 1)[-1]
                    divergence = divergence.strip('[]')
                    for div in divergence.split(', '):
                        if 'ahead' in div:
                            num_ahead = int(div[len('ahead '):].strip())
                        elif 'behind' in div:
                            num_behind = int(div[len('behind '):].strip())
        elif line.startswith('??'):
            untracked += 1
        else:
            if len(line) > 1 and line[1] == 'M':
                changed += 1

            if len(line) > 0 and line[0] == 'U':
                conflicts += 1
            elif len(line) > 0 and line[0] != ' ':
                staged += 1

    gitdir = _check_output(['git', 'rev-parse', '--git-dir']).strip()
    stashed = _get_stash(gitdir)
    operations = _gitoperation(gitdir)

    return GitStatus(branch, num_ahead, num_behind,
            untracked, changed, conflicts, staged, stashed,
            operations)


def gitstatus_prompt():
    """Return str `BRANCH|OPERATOR|numbers`"""
    try:
        s = gitstatus()
    except subprocess.SubprocessError:
        return None

    ret = _get_def('BRANCH') + s.branch
    if s.num_ahead > 0:
        ret += _get_def('AHEAD') + str(s.num_ahead)
    if s.num_behind > 0:
        ret += _get_def('BEHIND') + str(s.num_behind)
    if s.operations:
        ret += _get_def('OPERATION') + '|' + '|'.join(s.operations)
    ret += '|'
    if s.staged > 0:
        ret += _get_def('STAGED') + str(s.staged) + '{NO_COLOR}'
    if s.conflicts > 0:
        ret += _get_def('CONFLICTS') + str(s.conflicts) + '{NO_COLOR}'
    if s.changed > 0:
        ret += _get_def('CHANGED') + str(s.changed) + '{NO_COLOR}'
    if s.untracked > 0:
        ret += _get_def('UNTRACKED') + str(s.untracked) + '{NO_COLOR}'
    if s.stashed > 0:
        ret += _get_def('STASHED') + str(s.stashed) + '{NO_COLOR}'
    if s.staged + s.conflicts + s.changed + s.untracked + s.stashed == 0:
        ret += _get_def('CLEAN') + '{NO_COLOR}'
    ret += '{NO_COLOR}'

    return ret

#
# job
#
# -*- coding: utf-8 -*-
"""Prompt formatter for current jobs"""

xj = _LazyModule.load('xonsh', 'xonsh.jobs', 'xj')
def _current_job():
    j = xj.get_next_task()
    if j is not None:
        if not j['bg']:
            cmd = j['cmds'][-1]
            s = cmd[0]
            if s == 'sudo' and len(cmd) > 1:
                s = cmd[1]
            return s

#
# vc_branch
#
# -*- coding: utf-8 -*-
"""Prompt formatter for simple version control branchs"""

# amalgamated builtins
# amalgamated os
# amalgamated subprocess
sys = _LazyModule.load('sys', 'sys')
threading = _LazyModule.load('threading', 'threading')
queue = _LazyModule.load('queue', 'queue')
time = _LazyModule.load('time', 'time')
warnings = _LazyModule.load('warnings', 'warnings')
# amalgamated xonsh.platform
# amalgamated xonsh.tools
def _get_git_branch(q):
    try:
        status = subprocess.check_output(['git', 'status'],
                                         stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, OSError):
        q.put(None)
    else:
        info = xt.decode_bytes(status)
        branch = info.splitlines()[0].split()[-1]
        q.put(branch)

def get_git_branch():
    """Attempts to find the current git branch. If this could not
    be determined (timeout, not in a git repo, etc.) then this returns None.
    """
    branch = None
    timeout = builtins.__xonsh_env__.get('VC_BRANCH_TIMEOUT')
    q = queue.Queue()

    t = threading.Thread(target=_get_git_branch, args=(q,))
    t.start()
    t.join(timeout=timeout)
    try:
        branch = q.get_nowait()
    except queue.Empty:
        branch = None
    return branch


def _get_parent_dir_for(path, dir_name, timeout):
    # walk up the directory tree to see if we are inside an hg repo
    # the timeout makes sure that we don't thrash the file system
    previous_path = ''
    t0 = time.time()
    while path != previous_path and ((time.time() - t0) < timeout):
        if os.path.isdir(os.path.join(path, dir_name)):
            return path
        previous_path = path
        path, _ = os.path.split(path)
    return (path == previous_path)


def get_hg_branch(cwd=None, root=None):
    env = builtins.__xonsh_env__
    cwd = env['PWD']
    root = _get_parent_dir_for(cwd, '.hg', env['VC_BRANCH_TIMEOUT'])
    if not isinstance(root, str):
        # Bail if we are not in a repo or we timed out
        if root:
            return None
        else:
            return subprocess.TimeoutExpired(['hg'], env['VC_BRANCH_TIMEOUT'])
    # get branch name
    branch_path = os.path.sep.join([root, '.hg', 'branch'])
    if os.path.exists(branch_path):
        with open(branch_path, 'r') as branch_file:
            branch = branch_file.read()
    else:
        branch = 'default'
    # add bookmark, if we can
    bookmark_path = os.path.sep.join([root, '.hg', 'bookmarks.current'])
    if os.path.exists(bookmark_path):
        with open(bookmark_path, 'r') as bookmark_file:
            active_bookmark = bookmark_file.read()
        branch = "{0}, {1}".format(*(b.strip(os.linesep) for b in
                                     (branch, active_bookmark)))
    else:
        branch = branch.strip(os.linesep)
    return branch


_FIRST_BRANCH_TIMEOUT = True


def _first_branch_timeout_message():
    global _FIRST_BRANCH_TIMEOUT
    sbtm = builtins.__xonsh_env__['SUPPRESS_BRANCH_TIMEOUT_MESSAGE']
    if not _FIRST_BRANCH_TIMEOUT or sbtm:
        return
    _FIRST_BRANCH_TIMEOUT = False
    print('xonsh: branch timeout: computing the branch name, color, or both '
          'timed out while formatting the prompt. You may avoid this by '
          'increaing the value of $VC_BRANCH_TIMEOUT or by removing branch '
          'fields, like {curr_branch}, from your $PROMPT. See the FAQ '
          'for more details. This message will be suppressed for the remainder '
          'of this session. To suppress this message permanently, set '
          '$SUPPRESS_BRANCH_TIMEOUT_MESSAGE = True in your xonshrc file.',
          file=sys.stderr)


def current_branch(pad=NotImplemented):
    """Gets the branch for a current working directory. Returns an empty string
    if the cwd is not a repository.  This currently only works for git and hg
    and should be extended in the future.  If a timeout occurred, the string
    '<branch-timeout>' is returned.
    """
    if pad is not NotImplemented:
        warnings.warn("The pad argument of current_branch has no effect now "
                      "and will be removed in the future")
    branch = None
    cmds = builtins.__xonsh_commands_cache__
    if cmds.lazy_locate_binary('git') or cmds.is_empty():
        branch = get_git_branch()
    if (cmds.lazy_locate_binary('hg') or cmds.is_empty()) and not branch:
        branch = get_hg_branch()
    if isinstance(branch, subprocess.TimeoutExpired):
        branch = '<branch-timeout>'
        _first_branch_timeout_message()
    return branch or None


def _git_dirty_working_directory(q, include_untracked):
    status = None
    try:
        cmd = ['git', 'status', '--porcelain']
        if include_untracked:
            cmd.append('--untracked-files=normal')
        else:
            cmd.append('--untracked-files=no')
        status = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, OSError):
        q.put(None)
    if status is not None:
        return q.put(bool(status))


def git_dirty_working_directory(include_untracked=False):
    """Returns whether or not the git directory is dirty. If this could not
    be determined (timeout, file not found, etc.) then this returns None.
    """
    timeout = builtins.__xonsh_env__.get("VC_BRANCH_TIMEOUT")
    q = queue.Queue()
    t = threading.Thread(target=_git_dirty_working_directory,
                         args=(q, include_untracked))
    t.start()
    t.join(timeout=timeout)
    try:
        return q.get_nowait()
    except queue.Empty:
        return None


def hg_dirty_working_directory():
    """Computes whether or not the mercurial working directory is dirty or not.
    If this cannot be deterimined, None is returned.
    """
    env = builtins.__xonsh_env__
    cwd = env['PWD']
    denv = env.detype()
    vcbt = env['VC_BRANCH_TIMEOUT']
    # Override user configurations settings and aliases
    denv['HGRCPATH'] = ''
    try:
        s = subprocess.check_output(['hg', 'identify', '--id'],
                                    stderr=subprocess.PIPE, cwd=cwd, timeout=vcbt,
                                    universal_newlines=True, env=denv)
        return s.strip(os.linesep).endswith('+')
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired,
            FileNotFoundError):
        return None


def dirty_working_directory(cwd=None):
    """Returns a boolean as to whether there are uncommitted files in version
    control repository we are inside. If this cannot be determined, returns
    None. Currently supports git and hg.
    """
    dwd = None
    cmds = builtins.__xonsh_commands_cache__
    if cmds.lazy_locate_binary('git') or cmds.is_empty():
        dwd = git_dirty_working_directory()
    if (cmds.lazy_locate_binary('hg') or cmds.is_empty()) and (dwd is None):
        dwd = hg_dirty_working_directory()
    return dwd


def branch_color():
    """Return red if the current branch is dirty, yellow if the dirtiness can
    not be determined, and green if it clean. These are bold, intense colors
    for the foreground.
    """
    dwd = dirty_working_directory()
    if dwd is None:
        color = '{BOLD_INTENSE_YELLOW}'
    elif dwd:
        color = '{BOLD_INTENSE_RED}'
    else:
        color = '{BOLD_INTENSE_GREEN}'
    return color


def branch_bg_color():
    """Return red if the current branch is dirty, yellow if the dirtiness can
    not be determined, and green if it clean. These are bacground colors.
    """
    dwd = dirty_working_directory()
    if dwd is None:
        color = '{BACKGROUND_YELLOW}'
    elif dwd:
        color = '{BACKGROUND_RED}'
    else:
        color = '{BACKGROUND_GREEN}'
    return color

#
# base
#
# -*- coding: utf-8 -*-
"""Base prompt, provides FORMATTER_DICT and prompt related functions"""

# amalgamated builtins
itertools = _LazyModule.load('itertools', 'itertools')
# amalgamated os
re = _LazyModule.load('re', 're')
socket = _LazyModule.load('socket', 'socket')
string = _LazyModule.load('string', 'string')
# amalgamated sys
# amalgamated xonsh.lazyasd
# amalgamated xonsh.tools
# amalgamated xonsh.platform
# amalgamated xonsh.prompt.cwd
# amalgamated xonsh.prompt.job
# amalgamated xonsh.prompt.env
# amalgamated xonsh.prompt.vc_branch
# amalgamated xonsh.prompt.gitstatus
@xl.lazyobject
def FORMATTER_DICT():
    return dict(
        user=os.environ.get('USERNAME' if xp.ON_WINDOWS else 'USER', '<user>'),
        prompt_end='#' if xt.is_superuser() else '$',
        hostname=socket.gethostname().split('.', 1)[0],
        cwd=_dynamically_collapsed_pwd,
        cwd_dir=lambda: os.path.dirname(_replace_home_cwd()),
        cwd_base=lambda: os.path.basename(_replace_home_cwd()),
        short_cwd=_collapsed_pwd,
        curr_branch=current_branch,
        branch_color=branch_color,
        branch_bg_color=branch_bg_color,
        current_job=_current_job,
        env_name=env_name,
        vte_new_tab_cwd=vte_new_tab_cwd,
        gitstatus=gitstatus_prompt,
    )


@xl.lazyobject
def _FORMATTER():
    return string.Formatter()


def default_prompt():
    """Creates a new instance of the default prompt."""
    if xp.ON_CYGWIN:
        dp = ('{env_name:{} }{BOLD_GREEN}{user}@{hostname}'
              '{BOLD_BLUE} {cwd} {prompt_end}{NO_COLOR} ')
    elif xp.ON_WINDOWS:
        dp = ('{env_name:{} }'
              '{BOLD_INTENSE_GREEN}{user}@{hostname}{BOLD_INTENSE_CYAN} '
              '{cwd}{branch_color}{curr_branch: {}}{NO_COLOR} '
              '{BOLD_INTENSE_CYAN}{prompt_end}{NO_COLOR} ')
    else:
        dp = ('{env_name:{} }'
              '{BOLD_GREEN}{user}@{hostname}{BOLD_BLUE} '
              '{cwd}{branch_color}{curr_branch: {}}{NO_COLOR} '
              '{BOLD_BLUE}{prompt_end}{NO_COLOR} ')
    return dp


@xt.lazyobject
def DEFAULT_PROMPT():
    return default_prompt()


def _get_fmtter(formatter_dict=None):
    if formatter_dict is None:
        fmtter = builtins.__xonsh_env__.get('FORMATTER_DICT', FORMATTER_DICT)
    else:
        fmtter = formatter_dict
    return fmtter


def _failover_template_format(template):
    if callable(template):
        try:
            # Exceptions raises from function of producing $PROMPT
            # in user's xonshrc should not crash xonsh
            return template()
        except Exception:
            xt.print_exception()
            return '$ '
    return template


def partial_format_prompt(template=DEFAULT_PROMPT, formatter_dict=None):
    """Formats a xonsh prompt template string."""
    try:
        return _partial_format_prompt_main(template=template,
                                           formatter_dict=formatter_dict)
    except Exception:
        return _failover_template_format(template)


def _partial_format_prompt_main(template=DEFAULT_PROMPT, formatter_dict=None):
    template = template() if callable(template) else template
    fmtter = _get_fmtter(formatter_dict)
    bopen = '{'
    bclose = '}'
    colon = ':'
    expl = '!'
    toks = []
    for literal, field, spec, conv in _FORMATTER.parse(template):
        toks.append(literal)
        if field is None:
            continue
        elif field.startswith('$'):
            val = builtins.__xonsh_env__[field[1:]]
            val = _format_value(val, spec, conv)
            toks.append(val)
        elif field in fmtter:
            v = fmtter[field]
            try:
                val = v() if callable(v) else v
            except Exception as err:
                print('prompt: error: on field {!r}'
                      ''.format(field), file=sys.stderr)
                xt.print_exception()
                toks.append('(ERROR:{})'.format(field))
                continue
            val = _format_value(val, spec, conv)
            toks.append(val)
        else:
            toks.append(bopen)
            toks.append(field)
            if conv is not None and len(conv) > 0:
                toks.append(expl)
                toks.append(conv)
            if spec is not None and len(spec) > 0:
                toks.append(colon)
                toks.append(spec)
            toks.append(bclose)
    return ''.join(toks)


@xt.lazyobject
def RE_HIDDEN():
    return re.compile('\001.*?\002')


def multiline_prompt(curr=''):
    """Returns the filler text for the prompt in multiline scenarios."""
    line = curr.rsplit('\n', 1)[1] if '\n' in curr else curr
    line = RE_HIDDEN.sub('', line)  # gets rid of colors
    # most prompts end in whitespace, head is the part before that.
    head = line.rstrip()
    headlen = len(head)
    # tail is the trailing whitespace
    tail = line if headlen == 0 else line.rsplit(head[-1], 1)[1]
    # now to constuct the actual string
    dots = builtins.__xonsh_env__.get('MULTILINE_PROMPT')
    dots = dots() if callable(dots) else dots
    if dots is None or len(dots) == 0:
        return ''
    tokstr = xt.format_color(dots, hide=True)
    baselen = 0
    basetoks = []
    for x in tokstr.split('\001'):
        pre, sep, post = x.partition('\002')
        if len(sep) == 0:
            basetoks.append(('', pre))
            baselen += len(pre)
        else:
            basetoks.append(('\001' + pre + '\002', post))
            baselen += len(post)
    if baselen == 0:
        return xt.format_color('{NO_COLOR}' + tail, hide=True)
    toks = basetoks * (headlen // baselen)
    n = headlen % baselen
    count = 0
    for tok in basetoks:
        slen = len(tok[1])
        newcount = slen + count
        if slen == 0:
            continue
        elif newcount <= n:
            toks.append(tok)
        else:
            toks.append((tok[0], tok[1][:n - count]))
        count = newcount
        if n <= count:
            break
    toks.append((xt.format_color('{NO_COLOR}', hide=True), tail))
    rtn = ''.join(itertools.chain.from_iterable(toks))
    return rtn


def is_template_string(template, formatter_dict=None):
    """Returns whether or not the string is a valid template."""
    template = template() if callable(template) else template
    try:
        included_names = set(i[1] for i in _FORMATTER.parse(template))
    except ValueError:
        return False
    included_names.discard(None)
    if formatter_dict is None:
        fmtter = builtins.__xonsh_env__.get('FORMATTER_DICT', FORMATTER_DICT)
    else:
        fmtter = formatter_dict
    known_names = set(fmtter.keys())
    return included_names <= known_names


def _format_value(val, spec, conv):
    """Formats a value from a template string {val!conv:spec}. The spec is
    applied as a format string itself, but if the value is None, the result
    will be empty. The purpose of this is to allow optional parts in a
    prompt string. For example, if the prompt contains '{current_job:{} | }',
    and 'current_job' returns 'sleep', the result is 'sleep | ', and if
    'current_job' returns None, the result is ''.
    """
    if val is None:
        return ''
    val = _FORMATTER.convert_field(val, conv)
    if spec:
        val = _FORMATTER.format(spec, val)
    if not isinstance(val, str):
        val = str(val)
    return val

