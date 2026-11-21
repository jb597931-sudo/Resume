#!/usr/bin/env bash
# Build CV versions into output/.
#   ./build.sh genai                     default version for one profile
#   ./build.sh all                       default version for every profile
#   ./build.sh applications/acme-ml.tex  tailored version for one application
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p output

PROFILES="ml genai nlp cv ds research quant"
personal=personal.tex
[ -f "$personal" ] || { echo "note: personal.tex not found, using placeholder details from personal.example.tex"; personal=personal.example.tex; }
name=$(sed -n 's/^\\def\\cvname{\(.*\)}.*/\1/p' "$personal" | head -1 | tr ' ' '_')

build() { # $1 = output name, $2 = TeX to run
  local out="$1" tex="$2" log="output/$1.log"
  if ! pdflatex -interaction=nonstopmode -halt-on-error -output-directory=output -jobname="$out" "$tex" >/dev/null 2>&1; then
    echo "FAILED: $out"; grep -A3 '^!' "$log" | head -20; exit 1
  fi
  local pages; pages=$(pdfinfo "output/$out.pdf" 2>/dev/null | awk '/^Pages:/{print $2}')
  local status="ok"
  [ "${pages:-1}" -gt 1 ] && status="WARNING: $pages pages, trim bullets to fit one page"
  echo "output/$out.pdf  ($status)"
  last_log="$log"
  rm -f "output/$out.aux" "output/$out.out"
}

case "${1:-}" in
  all)
    for p in $PROFILES; do build "${name}_CV_${p}" "\def\role{$p}\input{cv-master}"; done ;;
  ml|genai|nlp|cv|ds|research|quant)
    build "${name}_CV_$1" "\def\role{$1}\input{cv-master}" ;;
  *.tex)
    [ -f "$1" ] || { echo "No such file: $1"; exit 1; }
    build "${name}_CV_$(basename "$1" .tex)" "\input{$1}" ;;
  *)
    echo "usage: ./build.sh <all | $PROFILES | applications/<file>.tex>"; exit 1 ;;
esac

# One reminder for unfinished personal details
grep -h '^CV-TODO' "$last_log" 2>/dev/null | sed 's/^CV-TODO: /reminder: /' || true
