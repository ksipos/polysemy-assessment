#!/bin/bash
for FILE in ./english/*.pdf; do
  pdfcrop "${FILE}"
done
