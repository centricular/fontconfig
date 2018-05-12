fccase = executable('fc-case', ['fc-case.c', fcstdint_h, alias_headers, ft_alias_headers],
  include_directories: [incbase, incsrc],
  c_args: c_args,
)

fccase_h = custom_target('fccase.h',
  output: ['fccase.h'],
  input: ['CaseFolding.txt'],
  command: [python3, stdinwrapper, fccase, files('fccase.tmpl.h')[0], '@OUTPUT@', '@INPUT@']
)
