tests = [
  ['test-bz89617.c', {'c_args': ['-DSRCDIR="@0@"'.format(meson.current_source_dir())]}],
  ['test-bz131804.c'],
  ['test-bz96676.c'],
  ['test-name-parse.c'],
]

foreach test_data : tests
  fname = test_data[0]
  opts = test_data.length() > 1 ? test_data[1] : {}
  extra_c_args = opts.get('c_args', [])

  test_name = fname.split('.')[0].underscorify()
  exe = executable(test_name, fname,
    c_args: c_args + extra_c_args,
    include_directories: incbase,
    link_with: [libfontconfig],
  )

  test(test_name, exe)
endforeach
