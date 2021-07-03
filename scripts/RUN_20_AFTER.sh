# Run at :20 after the hour

cd ingestors/madis
python extract_hfmetar.py 0 &

sleep 60
cd ../../plots
./RUN_PLOTS

cd ../isusm
python agg_1minute.py

cd ../isuag
python isusm2rr5.py

cd ../hads
python compute_hads_pday.py

cd ../ingestors
python uscrn_ingest.py

cd ../uscrn
python compute_uscrn_pday.py

cd ../dl
python download_imerg.py $(date -u --date '5 hours ago' +'%Y %m %d %H 00')
python download_imerg.py $(date -u --date '5 hours ago' +'%Y %m %d %H 30') ac
python download_imerg.py $(date -u --date '24 hours ago' +'%Y %m %d %H 00')
python download_imerg.py $(date -u --date '24 hours ago' +'%Y %m %d %H 30')
python download_imerg.py $(date -u --date '32 hours ago' +'%Y %m %d %H 00')
python download_imerg.py $(date -u --date '32 hours ago' +'%Y %m %d %H 30')
python download_imerg.py $(date -u --date '6 months ago' +'%Y %m %d %H 00')
python download_imerg.py $(date -u --date '6 months ago' +'%Y %m %d %H 30')
