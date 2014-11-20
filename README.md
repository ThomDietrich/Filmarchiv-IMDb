# Filmarchiv-IMDb

Starting from a flat alphabetic collection of movies, this:

```
MyMovies
    - 21 Jump Street (2012)
    - American Pie 1 (1999)
    - Iron Man (2008)
    - Old Men in New Cars (2002)
```

will be converted to this:

```
MyMoviesSorted
    - A-Z
        - 21 Jump Street (2012)
        - American Pie 1 (1999)
        - Iron Man (2008)
        - Old Men in New Cars (2002)
    - Genre
        - Action
            - 21 Jump Street (2012)
            - Iron Man (2008)
            - Old Men in New Cars (2002)
        -Comedy
            - 21 Jump Street (2012)
            - American Pie 1 (1999)
    - IMDb Rating
        - (6.8)  Old Men in New Cars (2002)
        - (7.0)  American Pie 1 (1999)
        - (7.2)  21 Jump Street (2012)
        - (7.9)  Iron Man (2008)
    - Year
        - ...
    - ...
```

The Structure "MyMoviesSorted" is build in parallel to the original "MyMovies" collection. The structue is build by using [hardlinks](http://en.wikipedia.org/wiki/Hard_link), therefor both folders have to be on the same logical partition.

The movie releated data is fetched directly from IMDb, filtering after that is easy and can be easily customized.

Requirements:
  - [Python2.7](http://python.org)
  - [IMDbPY](http://imdbpy.sourceforge.net)
  - [colorama](https://pypi.python.org/pypi/colorama)

