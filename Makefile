
serv_clip_transformers:
	python -m clip_server flows/flow-transformers.yml

build_and_push_image:
	docker login
	docker build -f image/Dockerfile -t dockhardman/ac-clip:${IMAGE_TAGNAME} .
	docker push dockhardman/ac-clip:${IMAGE_TAGNAME}
