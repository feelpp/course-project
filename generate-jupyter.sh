#! /bin/sh

dir=${1:-.}
for i in $(find $dir -name "*.adoc" | grep pages ); do 
    if grep ":page-jupyter:" $i; then   
        echo "Generating Jupyter Notebook for $i: "
        ipynb=$(echo $i |  sed -E 's/docs\/modules\/(.*)\/pages\/(.*)/\1\/\2/')
        dir=$(dirname $ipynb)
        mkdir -p notebooks/$dir
        echo "generating notebooks/$dir/$(basename $ipynb .adoc).ipynb..."
        pwd
        npx asciidoctor -r asciidoctor-jupyter -b jupyter $i -o notebooks/$dir/$(basename $ipynb .adoc).ipynb
    fi; 
done