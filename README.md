# jflat
Flatten Json objects
See [this](https://gist.github.com/doug-ol/0c018e82c095cd3addcb1275999c966f)

## Usage
```bash
$ echo '{"a": {"b": 3}}' | python jflat.py
{
  "a.b": 3
}

```

Or
```bash
$ python jfpat.py file.json
...
```


## Setup Notes
jflay.py supports both python2.7 and python>3.5.
jflat.py does not rely on 3rd party libraries 
(no installations are required).

## Tests
To run the tests install and run:
```.env
tox
```
(Assumes you have the required python interpreters installed)