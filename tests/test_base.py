import os

from pip_madison.utils import filename_parser_factory
numpy_versions = os.path.join(os.path.dirname(__file__),"numpy_versions.dat")
flask_versions = os.path.join(os.path.dirname(__file__),"flask_versions.dat")
django_versions = os.path.join(os.path.dirname(__file__),"django_versions.dat")
def test_re_match_file_numpy_1():
    parser = filename_parser_factory("numpy",py="cp27",os="win",endswith=".whl")
    result = parser("numpy-3.1.2-cp27_none-win32.whl")
    assert result['list'] == [3,1,2]
    assert result['ver'] == '3.1.2'
    assert result['package_name'] == 'numpy'
    assert result['py'] == 'cp27_none'
    assert result['os'] == 'win32'
    assert result['fname'] == 'numpy-3.1.2-cp27_none-win32.whl'

def test_re_no_match_file_numpy_1():
    parser = filename_parser_factory("numpy", py="cp27", os="win", endswith=".whl")
    result = parser("numpy-3.1.2-cp27_none-manylinux.whl")
    assert not result
    result = parser("numpy-3.1.2-cp27_none-macosx.whl")
    assert not result
    result = parser("numpy-3.1.2-cp36_none-win32.whl")
    assert not result

def test_numpy_dat_1():
    parser = filename_parser_factory("numpy", py="cp27", os="win", endswith=".whl")
    results={'win32':[],'win64':[]}
    for line in open(numpy_versions):
        line = line.strip()
        test = parser(line)
        if test:
            if 'win32' in line:
                results['win32'].append(test)
            else:
                results['win64'].append(test)
            print line
    assert len(results['win32']) == len(results['win64']) == 42
    assert max(results['win32'],key=lambda x:x['list'])['list'] == [1,16,6]
    assert max(results['win64'],key=lambda x:x['list'])['list'] == [1,16,6]
        # print test

def test_flask_dat_1():
    parser = filename_parser_factory("flask", py="cp27", os="win", endswith=".whl")
    print("cwd",os.getcwd())
    results=[]
    for line in open(flask_versions):
        line = line.strip()
        test = parser(line)
        if test:
            results.append(test)
            print(line)
    assert len(results) == 16
    assert results[-1]['list'] == [1,1,2]
    # assert len(results['win32']) == len(results['win64']) == 42
    # assert len(results['win32']) == len(results['win64']) == 42
    # assert max(results['win32'],key=lambda x:x['list'])['list'] == [1,16,6]
    # assert max(results['win64'],key=lambda x:x['list'])['list'] == [1,16,6]
def test_django_dat_1():
    parser = filename_parser_factory("django", py="cp27", os="win", endswith=".whl")
    results=[]
    for line in open(django_versions):
        line = line.strip()
        test = parser(line)
        if test:
            results.append(test)
            print(line)
    assert results[0]['list'] == [1,5,2]
    assert len(results) == 112
