# Landslide EarlyDetection
[![Binder](https://binder.pangeo.io/badge_logo.svg)](https://binder.pangeo.io/v2/gh/Competencia-de-Climate-Change/Landslide_EarlyDetection/master)

Machine Learning Research Project: Landslide Risk based Early Detection

## Data

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
      <td>`weather`</td>
      <td>`codigo`</td>
      <td>NO</td>
      <td>[link](ejemplo)</td>
      <td>X.XX</td>
      <td>probar xxx </td>
    </tr>
    <tr>
      <td>'goes17:fulldisk:v1'</td>
      <td>`weather`</td>
      <td>`products['weather']['goes']`</td>
      <td>NO</td>
      <td>[link](goes)</td>
      <td>NA</td>
      <td>NA</td>
    </tr>
    <tr>
      <td>GSOD Daily Interpolation Weather Product</td>
      <td>`weather`</td>
      <td>`products['weather']['gsod']` </td>
      <td>NO</td>
      <td>[link](gsod)</td>
      <td>TODO</td>
      <td>TODO</td>
    </tr>
    <tr>
      <td>CHIRPS Daily Precipitation Weather </td>
      <td>`weather`</td>
      <td>`products['weather']['chirps']` </td>
      <td>SI</td>
      <td>[link](chirps)</td>
      <td>0.05</td>
      <td>create stack</td>
    </tr>
    <tr>
      <td>NCEP CFS-v2 Derived Daily Weather Product </td>
      <td>`weather`</td>
      <td>`products['weather']['cfs']` </td>
      <td>SI</td>
      <td>[link](cfs)</td>
      <td>0.20</td>
      <td>TODO</td>
    </tr>
    <tr>
      <td>VisMet Data </td>
      <td>`weather`</td>
      <td>`products['weather']['vismet']` </td>
      <td>NO</td>
      <td>[link](vismet)</td>
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

[ejemplo]: examples/remasframe_01.ipynb
[goes]: examples/weather/goes.ipynb
[gsod]: examples/weather/gsod.ipynb
[chirps]: examples/weather/chirps.ipynb
[cfs]: examples/weather/cfs.ipynb

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

### Free Access to TPUs

Step se consiguió TPUs gratis. Todavía no las prueba. El que se ofrezca a explorar esto bienvenido.
Solicitar info a Step.


## DescartesLab

Gives access to satellite data and `Workbench` (4vCPUs, 13GB~RAM, optional GPU)

### Credentials

If you need to access DescartesLab ask Step, Tomas or José

### Data Sources

| nombre |   id   | url  | formato | notebook | TODOs    |
|--------|--------|------|---------|----------|----------|
|        |        |      |         |          |          |
|        |        |      |         |          |          |
|        |        |      |         |          |          |
