# Landslide EarlyDetection
[![Binder](https://binder.pangeo.io/badge_logo.svg)](https://binder.pangeo.io/v2/gh/Competencia-de-Climate-Change/Landslide_EarlyDetection/master)

Machine Learning Research Project: Landslide Risk based Early Detection

## Data

| nombre      | categoria | id       | funcionando | notebook_ejemplo | resolucion | TODOs |
|-------------|-----------|----------|-------------|------------------|------------|-------|
|  ejemplo    | `weather` | `codigo` |    NO       | [link][ejemplo]        |    0.9      | probar xxx|
|  'goes17:fulldisk:v1'      | `weather` | `products['weather']['goes']`    |   NO     |     [link][goes]      |  NA |  NA     |
|  GSOD Daily Interpolation Weather Product   |  `weather`   |   `products['weather']['gsod']`      |   NO     |     [link][gsod]      |  TODO |  TODO     |
|  CHIRPS Daily Precipitation Weather         |  `weather`   |   `products['weather']['chirps']`    |   SI     |     [link](chirps)      |  0.9 |  TODO     |

Recordatorios: 

`products = ReMasFrame.get_products()`

`buffer_size = 0.1` <img src="https://render.githubusercontent.com/render/math?math=\iff"> `0.1 deg`
<img src="https://render.githubusercontent.com/render/math?math=\approx"> `10km`
<img src="https://render.githubusercontent.com/render/math?math=\implies">` box de 10kmx10km aprox.`

[ejemplo]: https://github.com/Competencia-de-Climate-Change/Landslide_EarlyDetection/tree/main/notebooks/weather/ejemplo.ipynb
[goes]: https://github.com/Competencia-de-Climate-Change/Landslide_EarlyDetection/blob/main/examples/products/goes.ipynb
[gsod]: https://github.com/Competencia-de-Climate-Change/Landslide_EarlyDetection/blob/main/examples/products/gsod.ipynb
[chirps]: https://github.com/Competencia-de-Climate-Change/Landslide_EarlyDetection/blob/main/examples/weather/chirps.ipynb
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
