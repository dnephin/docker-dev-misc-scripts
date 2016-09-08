
FROM    golang:1.6-alpine

RUN     apk add -U git bash

RUN     go get golang.org/x/tools/cmd/gomvpkg && \
        go get golang.org/x/tools/cmd/gorename && \
        go get golang.org/x/tools/cmd/eg && \
        go get golang.org/x/tools/cmd/callgraph && \
        go get golang.org/x/tools/cmd/guru && \
        mv /go/bin/* /usr/local/bin && \
        rm -rf /go/src/* /go/pkg/* /go/bin/*

ENV     CGO_ENABLED=0
ENV     GOPATH=/go:/go/src/github.com/docker/docker/vendor
WORKDIR /go/src/github.com/docker/docker/
