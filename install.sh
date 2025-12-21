#!/bin/bash
# Install/reinstall json-holygrail tool with latest version

uv cache clean json-holygrail 2>/dev/null || true
uv tool install --force .
