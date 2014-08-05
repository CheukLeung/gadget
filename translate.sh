language=$1
keyword=""
shift 1
for i in "$@"
do
    i=`echo "$i" | sed 's/ /%20/g'`
    i=`echo "$i" | sed 's/\./%2E/g'`
    i=`echo "$i" | sed 's/~/%7E/g'`
    i=`echo "$i" | sed 's/\//%2F/g'`
    keyword=`echo "${keyword}%20$i"`
done

translate=`curl "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20google.translate%20where%20q%3D%22$keyword%22%20and%20target%3D%22$language%22%3B&diagnostics=true&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys" 2> /dev/null`
translate=`echo "$translate" | sed -n 's/.*<trans>\(.*\)<\/trans>.*/\1/p'` 
echo "$translate"

