#!/usr/bin/env bash
# Recompile all com.fribbels.* sources against the bundled backend.jar
# (which carries every third-party dep) and splice the rebuilt classes
# back in. This is the proper fix for stale-binary drift between the
# checked-in jar and the evolving Java source — required when adding new
# enum values (e.g. WarfareSet/PursuitSet) because the old kernel and
# handler classes hardcode the previous set count.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
JAR="$ROOT/data/jar/backend.jar"
SRC_ROOT="$ROOT/backend/src/main/java"
LOMBOK_VER="1.16.4"
LOMBOK="$ROOT/scripts/lombok-$LOMBOK_VER.jar"
WORK="$(mktemp -d)"
trap "rm -rf $WORK" EXIT

command -v javac >/dev/null || { echo "javac missing — install openjdk-8-jdk"; exit 1; }
command -v jar   >/dev/null || { echo "jar missing — install openjdk-8-jdk"; exit 1; }

if [ ! -f "$LOMBOK" ]; then
    echo "Downloading lombok $LOMBOK_VER..."
    curl -fsSL "https://repo1.maven.org/maven2/org/projectlombok/lombok/$LOMBOK_VER/lombok-$LOMBOK_VER.jar" -o "$LOMBOK"
fi

echo "Collecting sources..."
# Stage sources into a no-space path so javac @argfile (which doesn't
# support quoted paths) works regardless of project location.
STAGE_SRC="$WORK/src"
mkdir -p "$STAGE_SRC"
cp -r "$SRC_ROOT/com" "$STAGE_SRC/"
SOURCES_FILE="$WORK/sources.txt"
find "$STAGE_SRC/com/fribbels" -name "*.java" > "$SOURCES_FILE"
echo "  $(wc -l < $SOURCES_FILE) files"

echo "Compiling against $JAR ..."
# Stage the jar too so the -cp arg has no spaces either.
STAGE_JAR="$WORK/backend.jar"
cp "$JAR" "$STAGE_JAR"
mkdir -p "$WORK/classes"
javac -source 1.8 -target 1.8 \
      -g \
      -cp "$STAGE_JAR:$LOMBOK" \
      -d "$WORK/classes" \
      -Xlint:none \
      @"$SOURCES_FILE"
# -g is REQUIRED: aparapi parses kernel bytecode at runtime to emit
# OpenCL, and needs the LocalVariableTable to do it correctly. Without
# debug info, aparapi falls back to a synthetic table ("experimental")
# that produces invalid OpenCL → clBuildProgram fails → JVM segfaults
# in libOpenCL during cleanup. This is why GPU acceleration broke after
# the first jar rebuild.

echo "Splicing rebuilt com/fribbels/** into $JAR ..."
# Use jar -uf with relative paths from the classes dir
( cd "$WORK/classes" && find com/fribbels -name "*.class" -print0 | xargs -0 jar uf "$JAR" )

# Mirror to release tree if present
UNPACKED="$ROOT/release/linux-unpacked/data/jar/backend.jar"
if [ -f "$UNPACKED" ]; then
    cp "$JAR" "$UNPACKED"
    echo "Mirrored to release/linux-unpacked"
fi

echo "Verifying Set enum..."
unzip -p "$JAR" com/fribbels/enums/Set.class | strings | grep -E "WarfareSet|PursuitSet" || {
    echo "Set verification failed!"; exit 1;
}
echo "Done. Relaunch the app."
