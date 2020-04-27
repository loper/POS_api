#!/bin/bash

DEST="templates"

TD1="ccn-pos-full"
TD2="opos-fat"

VERSIONS1="v1.0.11/ v1.0.14/ v1.0.2_01/ v1.0.4/ v1.0.6/ v1.0.9/ v1.0.10/ v1.0.12/ v1.0.2/ v1.0.3/ v1.0.5/ v1.0.8/"
VERSIONS2="1.0.11-b64/ 1.0.1-b13/ 1.0.5-b45/ 1.2.0-b01-SNAPSHOT/"

TEST_DIR="config"
TEST_FILE="version_descriptor.xml"

# -------------------------

for ver in $VERSIONS1; do
    mkdir -p "$DEST/$TD1/$ver"
    mkdir -p "$DEST/$TD1/$ver/$TEST_DIR"
    cp -f $TEST_FILE "$DEST/$TD1/$ver/$TEST_DIR/$TEST_FILE"
    build_number="$(echo $ver | tr -d '/')"
    echo "$ver" | grep -q '\-b' || {
        build_number="$build_number-b$(( ( RANDOM % 100 )  + 10 ))"
    }
    sed -i "s|VERSION_GOES_HERE|$build_number|g" "$DEST/$TD1/$ver/$TEST_DIR/$TEST_FILE"
done

for ver in $VERSIONS2; do
    mkdir -p "$DEST/$TD2/$ver"
    mkdir -p "$DEST/$TD2/$ver/$TEST_DIR"
    cp -f $TEST_FILE "$DEST/$TD2/$ver/$TEST_DIR/$TEST_FILE"
    # build_number=$(( ( RANDOM % 100 )  + 10 ))
    build_number="v$(echo $ver | tr -d '/')"
        echo "$ver" | grep -q '\-b' || {
        build_number="$build_number-b$(( ( RANDOM % 100 )  + 10 ))"
    }
    sed -i "s|VERSION_GOES_HERE|$build_number|g" "$DEST/$TD2/$ver/$TEST_DIR/$TEST_FILE"
done
