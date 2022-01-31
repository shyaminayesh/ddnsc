default: run


run:
	go run ddnsc.go

dist:
	rm -rf ddnsc
	go build -o ddnsc -ldflags "-s -w" -trimpath ddnsc.go