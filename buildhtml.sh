#!/bin/sh

set -e

cp content/_config.yml.in content/_config.yml
cat content/_config.yml | sed "s/%REVISION%/$(git rev-parse --short HEAD)/" > content/_config.yml
cat content/_config.yml | sed "s/%RELEASE_DATE%/$(date +'%Y\/%m\/%d')/"  > content/_config.yml

die()
{
    echo "$1" >&2
    exit 1
}

find_plantuml()
{
    if [ -f "$PLANTUMLPATH" ]; then
        echo "$PLANTUMLPATH"
        return
    fi

    local oIFS="$IFS"; IFS=':'
    for p in $(pwd):$PATH; do
        local candidate="$p/plantuml.jar"
        if [ -f "$candidate" ]; then
            echo "$candidate"
            return
        fi
    done
    IFS="$oIFS"

    die "didn't find plantuml.jar in system path"
}

plantuml="$(find_plantuml)"
PLANTUMLPATH="$plantuml" PLANTUMLFORMAT='svg' jupyter-book build content
