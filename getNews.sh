#!/bin/bash
svd='python /home/cheuk/gadget/svd.py'

time=`date +"%Y%m%d%I%M%S"`
filename=$HOME/Downloads/news-$time
date > $filename
echo >> $filename
for news in {0..29}
do
	$svd $news >> $filename 
done
