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
  ['vprintf'],
  ['FT_Get_BDF_Property'],
  ['FT_Get_PS_Font_Info'],
  ['FT_Has_PS_Glyph_Names'],
  ['FT_Get_X11_Font_Format'],
  ['FT_Done_MM_Var'],
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

check_sizeofs = [
  ['void *', {'conf-name': 'SIZEOF_VOID_P'}],
]

check_alignofs = [
  ['void *', {'conf-name': 'ALIGNOF_VOID_P'}],
  ['double'],
]

freetype_dep = dependency('freetype2', version: '>= 21.0.15', fallback: ['freetype2', 'freetype_dep'])
expat_dep = dependency('expat', fallback: ['expat', 'expat_dep'])

c_args = ['-DHAVE_CONFIG_H']

conf = configuration_data()
deps = [freetype_dep, expat_dep]
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
  found = true

  found = cc.has_function(name, dependencies: deps)

  if found
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

if cc.links(files('meson-cc-tests/intel-atomic-primitives-test.c'), name: 'Intel atomics')
  conf.set('HAVE_INTEL_ATOMIC_PRIMITIVES', 1)
endif

if cc.links(files('meson-cc-tests/solaris-atomic-operations.c'), name: 'Solaris atomic ops')
  conf.set('HAVE_SOLARIS_ATOMIC_OPS', 1)
endif


prefix = get_option('prefix')

if host_machine.system() == 'windows'
  conf.set_quoted('FC_DEFAULT_FONTS', 'WINDOWSFONTDIR')
  fc_cachedir = 'LOCAL_APPDATA_FONTCONFIG_CACHE'
else
  conf.set_quoted('FC_DEFAULT_FONTS', '/usr/share/fonts')
  fc_cachedir = join_paths(prefix, get_option('localstatedir'), 'cache', meson.project_name())
  thread_dep = dependency('threads')
  uuid_dep = dependency('uuid')
  conf.set('HAVE_PTHREAD', 1)
  deps += [thread_dep, uuid_dep]
endif

fc_templatedir = join_paths(prefix, get_option('datadir'), 'fontconfig/conf.avail')
fc_baseconfigdir = join_paths(prefix, get_option('sysconfdir'), 'fonts')
fc_configdir = join_paths(fc_baseconfigdir, 'conf.d')
fc_xmldir = join_paths(prefix, get_option('datadir'), 'xml/fontconfig')

conf.set_quoted('CONFIGDIR', fc_configdir)
conf.set_quoted('FC_CACHEDIR', fc_cachedir)
conf.set_quoted('FC_TEMPLATEDIR', fc_templatedir)
conf.set_quoted('FONTCONFIG_PATH', fc_baseconfigdir)
conf.set_quoted('FC_FONTPATH', '')

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

conf.set('_GNU_SOURCE', true)

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
subdir('fc-cache')
subdir('fc-cat')
subdir('fc-conflist')
subdir('fc-list')
subdir('fc-match')
subdir('fc-pattern')
subdir('fc-query')
subdir('fc-scan')
subdir('fc-validate')
subdir('test')

configure_file(output: 'config.h', configuration: conf)
configure_file(input: 'fonts.conf.in', output: 'fonts.conf', configuration: conf)
