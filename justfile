version := shell("python3 src/litesort/config.py v")
builddir := "build/"
outdir := builddir + version + "/"
pypi := "https://pypi.org/legacy/"
tpypi := "https://test.pypi.org/legacy/"

build-all:
	echo {{outdir}}
	uv sync --active
	uv build --out-dir {{outdir}}

build-whl:
	echo {{outdir}}
	uv sync --active
	uv build --wheel --out-dir {{outdir}}

publish token: build-all
	uv publish --token {{token}} --publish-url {{pypi}} {{outdir}}/*.[whl,tar.gz]

publish-test token: build-all
	#!/bin/sh
	uv publish --token {{token}} --publish-url {{tpypi}} {{outdir}}/*.whl {{outdir}}/*.tar.gz

clean:
	rm -rf {{builddir}}/*
