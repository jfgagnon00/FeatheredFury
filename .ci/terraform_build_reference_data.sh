echo "Index Dataset"
ffury dataset index

echo "Build Reference"
ffury dataset reference

echo "Upload Reference"
ffury monitoring upload-reference
