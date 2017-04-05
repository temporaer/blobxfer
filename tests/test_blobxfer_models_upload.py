# coding=utf-8
"""Tests for models upload"""

# stdlib imports
try:
    import pathlib2 as pathlib
except ImportError:  # noqa
    import pathlib
# non-stdlib imports
import pytest
# module under test
import blobxfer.models.upload as upload


def test_localsourcepaths_files(tmpdir):
    tmpdir.mkdir('abc')
    tmpdir.join('moo.cow').write('z')
    abcpath = tmpdir.join('abc')
    abcpath.join('hello.txt').write('hello')
    abcpath.join('blah.x').write('x')
    abcpath.join('blah.y').write('x')
    abcpath.join('blah.z').write('x')
    abcpath.mkdir('def')
    defpath = abcpath.join('def')
    defpath.join('world.txt').write('world')
    defpath.join('moo.cow').write('y')

    a = upload.LocalSourcePaths()
    a.add_include('*.txt')
    a.add_includes(['moo.cow', '*blah*'])
    with pytest.raises(ValueError):
        a.add_includes('abc')
    a.add_exclude('**/blah.x')
    a.add_excludes(['world.txt'])
    with pytest.raises(ValueError):
        a.add_excludes('abc')
    a.add_path(str(tmpdir))
    a_set = set()
    for file in a.files():
        sfile = str(file.parent_path / file.relative_path)
        a_set.add(sfile)

    assert len(a.paths) == 1
    assert str(abcpath.join('blah.x')) not in a_set
    assert str(defpath.join('world.txt')) in a_set
    assert str(defpath.join('moo.cow')) not in a_set

    b = upload.LocalSourcePaths()
    b.add_includes(['moo.cow', '*blah*'])
    b.add_include('*.txt')
    b.add_excludes(['world.txt'])
    b.add_exclude('**/blah.x')
    b.add_paths([pathlib.Path(str(tmpdir))])
    for file in a.files():
        sfile = str(file.parent_path / file.relative_path)
        assert sfile in a_set
