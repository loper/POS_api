run:
	docker run -it -d --name pos_api -v /usr/sap/gkretail/sm.server/import/templates/:/templates/:ro -p 5000:5000 pos_version_api:1.1
run_dev:
	docker run -it -d --name pos_api -v /home/msy/POS_ver_api/templates/:/templates/:ro -p 5000:5000 pos_version_api:1.1
build:
	docker build -t pos_version_api:1.1 .
clean:
	find . -type d -name __pycache__ -exec rm -r {} \; || true
	find . -type d -name .ropeproject -exec rm -r {} \; || true
	docker rm -f pos_api || true

