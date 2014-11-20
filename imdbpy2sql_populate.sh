
#rm imdb.sqlite
#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#command="imdbpy2sql.py -d . -u 'sqlite://$DIR/imdb.sqlite'"
command="imdbpy2sql.py -d . -u 'mysql://imdbpy:XXVTvgceiprPX85WzFy0@localhost/imdbpy'"

mkdir imdbpy2sql-temp
cd imdbpy2sql-temp

wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/actors.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/actresses.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/aka-names.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/aka-titles.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/alternate-versions.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/biographies.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/business.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/certificates.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/cinematographers.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/color-info.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/complete-cast.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/complete-crew.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/composers.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/costume-designers.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/countries.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/crazy-credits.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/directors.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/distributors.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/editors.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/genres.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/german-aka-titles.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/goofs.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/iso-aka-titles.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/italian-aka-titles.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/keywords.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/language.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/laserdisc.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/literature.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/locations.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/miscellaneous-companies.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/miscellaneous.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/movie-links.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/movies.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/mpaa-ratings-reasons.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/plot.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/producers.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/production-companies.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/production-designers.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/quotes.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/ratings.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/release-dates.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/running-times.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/sound-mix.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/soundtracks.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/special-effects-companies.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/taglines.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/technical.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/trivia.list.gz
wget ftp://ftp.fu-berlin.de/pub/misc/movies/database/writers.list.gz

eval $command

#mv imdb.sqlite ..

cd ..
rm -r imdbpy2sql-temp
