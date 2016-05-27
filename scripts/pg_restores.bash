#!/bin/bash

echo `date` "Restoring secondary data"
curl -Ls https://raw.githubusercontent.com/hackoregon/cropcompass-sql-dumps/master/imports_dump \
  | psql > ~/logs/imports 2>&1
curl -Ls https://raw.githubusercontent.com/hackoregon/cropcompass-sql-dumps/master/exports_dump \
  | psql > ~/logs/exports 2>&1
