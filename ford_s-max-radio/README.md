# Usage

Make a named pipe:
```
mkfifo stdout
```
Start the decoder command:
```
cat stdout | xxd -b | awk '{print $2$3$4$5$6$7}' | tr -d '\n' | awk '{ while (match($0, /0101010101010101001101/)) { print substr($0, RSTART, 240); $0 = substr($0, RSTART + 1); } }' | perl -lape '$_=unpack"H*",pack"B*",$_'
```

Alternatively, use this command to decode the payload in the file `decoded.bin`
```
xxd -b decoded.bin| awk '{print $2$3$4$5$6$7}' | tr -d '\n' | awk '{ while (match($0, /0101010101010101001101/)) { print substr($0, RSTART, 240); $0 = substr($0, RSTART + 1); } }' | perl -lape '$_=unpack"H*",pack"B*",$_'
```


