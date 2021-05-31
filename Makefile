UID := $(shell id -u)
GID := $(shell id -g)

export UID
export GID

bin: bin/detect bin/build

bin/detect: main.py
	docker-compose up --build

bin/build:
	cd bin && ln -s ./detect build

.PHONY: clean
clean:
	rm -rf bin

