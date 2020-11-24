# Landslide EarlyDetection
[![Binder](https://binder.pangeo.io/badge_logo.svg)](https://binder.pangeo.io/v2/gh/Competencia-de-Climate-Change/Landslide_EarlyDetection/master)

Machine Learning Research Project: Landslide Risk based Early Detection

## Data

`products = ReMasFrame.get_products()`

<table>
  <thead>
    <tr>
      <th>Nombre</th>
      <th>Categoría</th>
      <th>ID</th>
      <th>¿Funcionando?</th>
      <th>Link a Notebook</th>
      <th>Resolución</th>
      <th>Por Hacer</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ejemplo</td>
      <td><pre>weather</pre></td>
      <td><pre>codigo</pre></td>
      <td>NO</td>
      <td><a href="examples/remasframe_01.ipynb">Notebook Link</a></td>
      <td>X.XX</td>
      <td>probar xxx </td>
    </tr>
    <tr>
      <td>goes17:fulldisk:v1</td>
      <td><pre>weather</pre></td>
      <td><pre>products['weather']['goes']</pre></td>
      <td>NO</td>
      <td><a href="examples/weather/goes.ipynb">Notebook Link</a></td>
      <td>NA</td>
      <td>NA</td>
    </tr>
    <tr>
      <td>GSOD Daily Interpolation Weather Product</td>
      <td><pre>weather</pre></td>
      <td><pre>products['weather']['gsod']</pre></td>
      <td>SI</td>
      <td><a href="examples/weather/gsod.ipynb">Notebook Link</a></td>
      <td>0.1</td>
      <td>NA</td>
    </tr>
    <tr>
      <td>CHIRPS Daily Precipitation Weather</td>
      <td><pre>weather</pre></td>
      <td><pre>products['weather']['chirps']</pre></td>
      <td>SI</td>
      <td><a href="examples/weather/chirps.ipynb">Notebook Link</a></td>
      <td>0.05</td>
      <td>create stack</td>
    </tr>
    <tr>
      <td>NCEP CFS-v2 Derived Daily Weather Product</td>
      <td><pre>weather</pre></td>
      <td><pre>products['weather']['cfs']</pre></td>
      <td>SI</td>
      <td><a href="examples/weather/cfs.ipynb">Notebook Link</a></td>
      <td>0.20</td>
      <td>TODO</td>
    </tr>
    <tr>
      <td>smap:SMPL3SM_E</td>
      <td><pre>soil_moist</pre></td>
      <td><pre>products['soil_moist']['smap']</pre></td>
      <td>SI</td>
      <td><a href="examples/soil_moist/smap.ipynb">Notebook Link</a></td>
      <td>0.1</td>
      <td>NA</td>
    </tr>
    <tr>
      <td>VisMet Data</td>
      <td><pre>weather</pre></td>
      <td><pre>products['weather']['vismet']</pre></td>
      <td>NO</td>
      <td><a href="examples/weather/vismet.ipynb">Notebook Link</a></td>
      <td>NA</td>
      <td>to product</td>
    </tr>
  </tbody>
</table>

Recordatorios: 

`products = ReMasFrame.get_products()`

`buffer_size = 0.1` <img src="https://render.githubusercontent.com/render/math?math=\iff"> `0.1 deg`
<img src="https://render.githubusercontent.com/render/math?math=\approx"> `10km`
<img src="https://render.githubusercontent.com/render/math?math=\implies">` box de 10kmx10km aprox.`

## Google Compute Engine

### Bucket

url : `gs://data-projectx`

```{Python}
!pip install fsspec
!pip install gcsfs

import fsspec

fs = fsspec.get_mapper('gcs://data-projectx/')

# show files
print(list(fs))

# access files
with fs.open(path, mode='rb', cache_type='readahead') as f:
  use_for_something(f)
```

* Tutorial access see notebook example (TODO)
* [ffsspec docs](https://readthedocs.org/projects/filesystem-spec/downloads/pdf/latest/)



## DescartesLab

Gives access to satellite data and `Workbench` (4vCPUs, 13GB~RAM, optional GPU)

### Credentials

If you need to access DescartesLab ask Step, Tomas or José

