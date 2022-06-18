
serv_clip_transformers:
	uvicorn http_server:app \
		--host=0.0.0.0 \
		--port=51001 \
		--workers=2 \
		--log-level=debug \
		--use-colors \
		--reload \
		&
	python -m clip_server flows/flow-transformers.yml

build_and_push_dependency_image:
	docker login
	docker build -f image/Dockerfile -t dockhardman/ac-clip:${IMAGE_TAGNAME} .
	docker push dockhardman/ac-clip:${IMAGE_TAGNAME}

build_and_push_image:
	docker login
	docker build -f Dockerfile -t dockhardman/ac-clip:${IMAGE_TAGNAME} .
	docker push dockhardman/ac-clip:${IMAGE_TAGNAME}
