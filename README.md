# Territories
Simulations of territories and nations. Currently it only makes Delaunay triangulations :)

## Dependencies
Needs `poetry` to run. 
Install the dependencies with poetry:

```
poetry install
```

## Running

```
poetry run delauny
```

```
poetry run territories [options]

OPTIONS
	**-s** 
		Saves point generation to 'points' file

	**-l**
		Loads point generation from 'points' file

	**-p** N
		Demand N points	
```
