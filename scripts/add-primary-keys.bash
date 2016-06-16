#!/bin/bash

echo `date` "stopping app server"
sudo service uwsgi stop

echo `date` "Adding primary key 'id' to crop_diversity, exports_*, imports_*"
for TABLE in \
  crop_diversity \
  exports_by_country_raw \
  exports_historical_cleaned_annual_totals \
  exports_historical_cleaned_monthly_totals \
  exports_historical_raw \
  imports_by_country_raw \
  imports_historical_cleaned_annual_totals \
  imports_historical_cleaned_monthly_totals \
  imports_historical_raw
do
  psql -c "ALTER TABLE ${TABLE} ADD COLUMN id INTEGER;"
  psql -c "CREATE SEQUENCE ${TABLE}_id_seq;"
  psql -c "UPDATE ${TABLE} SET id = nextval('${TABLE}_id_seq');"
  psql -c "ALTER TABLE ${TABLE} ALTER COLUMN id SET DEFAULT nextval('${TABLE}_id_seq');"
  psql -c "ALTER TABLE ${TABLE} ALTER COLUMN id SET NOT NULL;"
  psql -c "ALTER TABLE ${TABLE} ADD PRIMARY KEY (id);"
done
psql -c '\d+' > ~vagrant/logs/tables-keyed

echo `date` "starting app server"
sudo service uwsgi start
