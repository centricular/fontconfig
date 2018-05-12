project('fontconfig', 'c',
  version: '2.13.0',
  meson_version : '>= 0.46',
  default_options: [ 'buildtype=debugoptimized'],
)

cc = meson.get_compiler('c')
python3 = import('python').find_installation()

check_headers = [
  ['fcntl.h'],
  ['stdlib.h'],
  ['string.h'],
  ['unistd.h'],
  ['sys/statvfs.h'],
  ['sys/vfs.h'],
  ['sys/statfs.h'],
  ['sys/param.h'],
  ['sys/mount.h'],
]

# FIXME AX_CREATE_STDINT_H

check_funcs = [
  ['link'],
  ['mkstemp'],
  ['mkostemp'],
  ['_mktemp_s'],
  ['mkdtemp'],
  ['getopt'],
  ['getopt_long'],
  ['getprogname'],
  ['getexecname'],
  ['rand'],
  ['random'],
  ['lrand48'],
  ['random_r'],
  ['rand_r'],
  ['readlink'],
  ['fstatvfs'],
  ['fstatfs'],
  ['lstat'],
  ['mmap'],
  ['vprintf']
]

check_header_symbols = [
  ['posix_fadvise', 'fcntl.h']
]

check_struct_members = [
  ['struct statvfs', 'f_basetype', ['sys/statvfs.h']],
  ['struct statvfs', 'f_fstypename', ['sys/statvfs.']],
  ['struct statfs', 'f_flags', []],
  ['struct statfs', 'f_fstypename', []],
  ['struct dirent', 'd_type', ['dirent.h']],
]

check_deps = [
  ['freetype', {'pkg': 'freetype2', 'version': '>= 21.0.15'}],
  ['expat'],
  ['uuid'],
]

check_sizeofs = [
  ['void *', {'conf-name': 'SIZEOF_VOID_P'}],
]

check_alignofs = [
  ['void *', {'conf-name': 'ALIGNOF_VOID_P'}],
  ['double'],
]

c_args = ['-DHAVE_CONFIG_H']

conf = configuration_data()
deps = []
incbase = include_directories('.')

foreach check : check_headers
  name = check[0]

  if cc.has_header(name)
    conf.set('HAVE_@0@'.format(name.to_upper().underscorify()), 1)
  endif
endforeach

foreach check : check_funcs
  name = check[0]
  opts = check.length() > 1 ? check[1] : {}
  link_withs = opts.get('link_with', [])
  extra_deps = []
  found = true

  # First try without linking

  found = cc.has_function(name)

  if not found and link_withs.length() > 0
    found = true

    foreach link_with : link_withs
      dep = cc.find_library(link_with)
      if dep.found()
	extra_deps += dep
      else
	found = false
      endif
    endforeach

    if found
      found = cc.has_function(name, dependencies: extra_deps)
    endif
  endif

  if found
    deps += extra_deps
    conf.set('HAVE_@0@'.format(name.to_upper()), 1)
  endif
endforeach

foreach check : check_header_symbols
  name = check[0]
  header = check[1]

  if cc.has_header_symbol(header, name)
    conf.set('HAVE_@0@'.format(name.to_upper()), 1)
  endif
endforeach

foreach check : check_struct_members
  struct_name = check[0]
  member_name = check[1]
  headers = check[2]

  prefix = ''

  foreach header : headers
    prefix += '#include <@0@>\n'.format(header)
  endforeach

  if cc.has_member(struct_name, member_name, prefix: prefix)
    conf.set('HAVE_@0@_@1@'.format(struct_name, member_name).to_upper().underscorify(), 1)
  endif
endforeach

foreach check : check_deps
  name = check[0]
  opts = check.length() > 1 ? check[1] : {}
  pkg_name = opts.get('pkg', name)
  required = opts.get('required', true)

  if opts.contains('version')
    dep = dependency(pkg_name, version : opts['version'], required : required)
  else
    dep = dependency(pkg_name, required : required)
  endif

  if dep.found()
    if not required
      conf.set('@0@_@1@'.format(conf_prefix, name).to_upper(), 1)
    endif
    deps += [dep]
  endif
endforeach

foreach check : check_sizeofs
  type = check[0]
  opts = check.length() > 1 ? check[1] : {}

  conf_name = opts.get('conf-name', 'SIZEOF_@0@'.format(type.to_upper()))

  conf.set(conf_name, cc.sizeof(type))
endforeach

foreach check : check_alignofs
  type = check[0]
  opts = check.length() > 1 ? check[1] : {}

  conf_name = opts.get('conf-name', 'ALIGNOF_@0@'.format(type.to_upper()))

  conf.set(conf_name, cc.alignment(type))
endforeach

if cc.compiles(files('meson-cc-tests/flexible-array-member-test.c'))
  conf.set('FLEXIBLE_ARRAY_MEMBER', true)
else
  conf.set('FLEXIBLE_ARRAY_MEMBER', 1)
endif

prefix = get_option('prefix')

if host_machine.system() == 'windows'
  conf.set_quoted('FC_DEFAULT_FONTS', 'WINDOWSFONTDIR')
  fc_cachedir = 'LOCAL_APPDATA_FONTCONFIG_CACHE'
else
  conf.set_quoted('FC_DEFAULT_FONTS', '/usr/share/fonts')
  fc_cachedir = join_paths(prefix, get_option('localstatedir'), 'cache', meson.project_name())
endif

fc_templatedir = join_paths(prefix, get_option('datadir'), 'fontconfig/conf.avail')
fc_baseconfigdir = join_paths(prefix, get_option('sysconfdir'), 'fonts')
fc_configdir = join_paths(fc_baseconfigdir, 'conf.d')
fc_xmldir = join_paths(prefix, get_option('datadir'), 'xml/fontconfig')

c_args += [
  '-DFC_CACHEDIR="@0@"'.format(fc_cachedir),
  '-DFC_TEMPLATEDIR="@0@"'.format(fc_templatedir),
  '-DFONTCONFIG_PATH="@0@"'.format(fc_baseconfigdir),
]

message('Using cache dir at @0@'.format(fc_cachedir))
message('Using template dir at @0@'.format(fc_templatedir))
message('Using font config path @0@'.format(fc_baseconfigdir))

# Thank you systemd
# FIXME: upstream in meson

gperf = find_program('gperf')

gperf_test_format = '''
#include <string.h>
const char * in_word_set(const char *, @0@);
@1@
'''
gperf_snippet_format = 'echo foo,bar | @0@ -L ANSI-C'
gperf_snippet = run_command('sh', '-c', gperf_snippet_format.format(gperf.path()))
gperf_test = gperf_test_format.format('size_t', gperf_snippet.stdout())

if cc.compiles(gperf_test)
  gperf_len_type = 'size_t'
else
  gperf_test = gperf_test_format.format('unsigned', gperf_snippet.stdout())
  if cc.compiles(gperf_test)
    gperf_len_type = 'unsigned'
  else
    error('unable to determine gperf len type')
  endif
endif

message('gperf len type is @0@'.format(gperf_len_type))

conf.set('FC_GPERF_SIZE_T', gperf_len_type,
  description : 'The type of gperf "len" parameter')

incsrc = include_directories('src')

fcstdint_h = configure_file(
  input: 'src/fcstdint.h.in',
  output: 'fcstdint.h',
  configuration: configuration_data())

stdinwrapper = files('stdin_wrapper.py')[0]
makealias = files('src/makealias.py')[0]

alias_headers = custom_target('alias_headers',
  output: ['fcalias.h', 'fcaliastail.h'],
  input: ['fontconfig/fontconfig.h', 'src/fcdeprecate.h', 'fontconfig/fcprivate.h'],
  command: [python3, makealias, join_paths(meson.current_source_dir(), 'src'), '@OUTPUT@', '@INPUT@'],
)

ft_alias_headers = custom_target('ft_alias_headers',
  output: ['fcftalias.h', 'fcftaliastail.h'],
  input: ['fontconfig/fcfreetype.h'],
  command: [python3, makealias, join_paths(meson.current_source_dir(), 'src'), '@OUTPUT@', '@INPUT@']
)

# Do not reorder
subdir('fc-case')
subdir('fc-lang')
subdir('src')

configure_file(output: 'config.h', configuration: conf)
