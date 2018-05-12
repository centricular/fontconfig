fc_sources = [
  'fcatomic.c',
  'fccache.c',
  'fccfg.c',
  'fccharset.c',
  'fccompat.c',
  'fcdbg.c',
  'fcdefault.c',
  'fcdir.c',
  'fcformat.c',
  'fcfreetype.c',
  'fcfs.c',
  'fcptrlist.c',
  'fchash.c',
  'fcinit.c',
  'fclang.c',
  'fclist.c',
  'fcmatch.c',
  'fcmatrix.c',
  'fcname.c',
  'fcobjs.c',
  'fcpat.c',
  'fcrange.c',
  'fcserialize.c',
  'fcstat.c',
  'fcstr.c',
  'fcweight.c',
  'fcxml.c',
  'ftglue.c',
]

# FIXME: obviously fragile, cc.preprocess would be sweet
if cc.get_id() == 'gcc'
  cpp = ['gcc', '-E', '-P']
elif cc.get_id() == 'msvc'
  cpp = ['cl', '/EP']
elif cc.get_id() == 'clang'
  cpp = ['clang', '-E', '-P']
else
  error('FIXME: implement cc.preprocess')
endif

fcobjshash_gperf = custom_target('fcobjshash.gperf',
  input: 'fcobjshash.gperf.h',
  output: 'fcobjshash.gperf',
  command: [python3, files('cutout.py')[0], '@INPUT@', '@OUTPUT@', cpp],
  build_by_default: true,
)

fcobjshash_h = custom_target('fcobjshash.h',
  input: fcobjshash_gperf,
  output: 'fcobjshash.h',
  command: [gperf, '--pic', '-m', '100', '@INPUT@', '--output-file', '@OUTPUT@']
)

libfontconfig = library('fontconfig', [fc_sources, alias_headers, ft_alias_headers, fclang_h, fcobjshash_h],
  c_args: c_args,
  include_directories: incbase,
  dependencies: deps,
)
