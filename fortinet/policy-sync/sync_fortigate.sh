
file1_compare="FortigateA.txt"
file2_compare="FortigateB.txt"

files_compared=$(diff $file1_compare $file2_compare | grep '<' | awk '{ print $2 }' | cut -d ':' -f1)

echo "config firewall policy"

for i in $files_compared; do
	cat CONF.conf | awk "/edit $i/,/next/{ if (!/set uuid/) { print } } "; done
echo "end"

