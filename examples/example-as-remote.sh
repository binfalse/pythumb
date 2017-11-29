#!/bin/bash


# let's assume that the server is running at localhost:12346
SERVER=localhost:12346
# to learn how to run the server have a look at https://github.com/binfalse/pythumb/


# create thumbnail of the file test/files/pdflike-2.pdf
# and store the thumbnail in /tmp/pythumb-tmp-file.png
curl -s -F target=upload -F filename=main.pdf -F file=@test/files/pdflike-2.pdf $SERVER  > /tmp/pythumb-tmp-file.png
echo "thumbnail of test/files/pdflike-2.pdf stored in /tmp/pythumb-tmp-file.png"


# create a thumbnail of https://binfalse.de/
# and store it in /tmp/pythumb-tmp-web.png
curl -s -F target=https://binfalse.de/ $SERVER  > /tmp/pythumb-tmp-web.png
echo "thumbnail of https://binfalse.de/ stored in /tmp/pythumb-tmp-web.png"

