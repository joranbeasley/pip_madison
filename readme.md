# pip-madison

inspired by apt-cache madison

this tool will show you the versions available for a given
package on pypi (or other pypi type indexs)

```bash
$ pip-madison numpy
Looking In: https://pypi.org/simple
  List Versions for: numpy
    1.12.0| numpy-1.12.0b1.tar.gz
    1.11.2| numpy-1.11.2rc1.tar.gz
    1.11.2| numpy-1.11.2.tar.gz
    ...
    1.5.0| numpy-1.5.0.tar.gz
    1.4.1| numpy-1.4.1.tar.gz
    1.3.0| numpy-1.3.0.tar.gz
```

## API Useage

```python
from pip_madison.utils import get_available_versions_files_and_urls, get_index_urls
index_url = get_index_urls()[0]
get_available_versions_files_and_urls(index_url+"/numpy/")
```
