#!/bin/bash
# convert binary representation to hex
function b2h {
  printf '%x\n' "$((2#$1))"
}

export -f b2h
echo $1 | sed 's/.\{4\}/& /g' | xargs -n1 -I{} bash -c 'b2h "$@"' _ {} | tr -d \\n | sed 's/.\{4\}/& /g'
