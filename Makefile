default: run


run:
	go run config.go ddnsc.go

dist:
	rm -rf ddnsc
	go build -o ddnsc -ldflags "-s -w" -trimpath config.go ddnsc.go