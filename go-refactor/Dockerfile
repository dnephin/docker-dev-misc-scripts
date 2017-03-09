
FROM    golang:1.7-alpine

RUN     apk add -U git \
            bash \
            musl-dev \
            linux-headers \
            gcc \
            btrfs-progs-dev \
            lvm2-dev

RUN     go get golang.org/x/tools/cmd/gomvpkg && \
        go get golang.org/x/tools/cmd/gorename && \
        go get golang.org/x/tools/cmd/eg && \
        go get golang.org/x/tools/cmd/callgraph && \
        go get golang.org/x/tools/cmd/guru && \
        go get golang.org/x/tools/cmd/fiximports && \
        mv /go/bin/* /usr/local/bin && \
        rm -rf /go/src/* /go/pkg/* /go/bin/*

ENV     GOPATH=/go:/go/src/github.com/docker/docker/vendor
WORKDIR /go/src/github.com/docker/docker/
