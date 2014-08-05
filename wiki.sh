keyword=""
for i in "$@"
do
    keyword=`echo "${keyword}_$i"`
done

wiki=`curl "http://en.wikipedia.org/w/api.php?format=json&action=query&titles=$keyword&redirects=true&prop=extracts&exintro=true&exsectionformat=plain&format=xml" 2> /dev/null`
wiki=`echo "$wiki" | sed 's/<[()/_a-zA-Z0-9\.\w\= "?\:]*>//g'`
wiki=`echo "$wiki" | sed 's/\&lt;[/a-zA-Z0-9]*\&gt;//g'`
wiki=`echo "$wiki" | sed 's/\&quot;/"/g'`
echo "$wiki"
