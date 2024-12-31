rm -f python_files.tar python_files.tar.gz
tar cvf python_files.tar package
gzip python_files.tar
gsutil cp python_files.tar.gz $GCS_BUCKET_URI/pgd-at-alexnet-trainer.tar.gz